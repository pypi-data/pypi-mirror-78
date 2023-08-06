#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# controller.py - running on the compute box, controls the management of all XT or XTLib initiated jobs for that machine.
import sys
import os
import json
import rpyc
import copy
import time
import shutil 
import random
import psutil
import logging
import datetime
import traceback
import subprocess
from threading import Thread, Lock
from rpyc.utils.server import ThreadedServer
from rpyc.utils.authenticators import SSLAuthenticator

# xtlib 
from xtlib.helpers.bag import Bag
from xtlib.console import console
from xtlib.run_info import RunInfo
from xtlib.helpers import file_helper
from xtlib.storage.store import store_from_context
from xtlib.mirror_worker import MirrorWorker
from xtlib.hparams.hparam_search import HParamSearch
from xtlib.helpers.stream_capture import StreamCapture

from xtlib import utils
from xtlib import errors
from xtlib import capture
from xtlib import pc_utils
from xtlib import scriptor
from xtlib import xt_vault
from xtlib import constants
from xtlib import file_utils
from xtlib import run_helper
from xtlib import process_utils

logger = logging.getLogger(__name__)
MAX_IDLE_CHECK = 1000

'''
Our controller is implemented as a Service so that client apps (XT and XTLib apps) from the same or different machines 
can connect to it.  Services offered include:
    - start a run  
    - get status of a run
    - enumerate runs on the hosting computer
    - kill a run
    - attach/detach to run's streaming console output
    - run a command on the box
    - copy files to/from box
'''

queue_lock = Lock()            
runs_lock = Lock()            
rundir_lock = Lock()

# def wait_for_process_exit(runner, pipe_thread, process, run_info):
#     '''
#     we use a separate thread to monitor for abnormal process exit that is 
#     not triggered in our "read_from_pipe" thread.
#     '''
#     while True:
#         time.sleep(1)
#         if process.poll():
#             break
    
#     # run post-processing

#     # kill pipe_thread, if still running
#     #pipe_thread.kill()
#     print("wait_for_process_exit THREAD EXITING...")
#     runner.exit_handler(run_info, called_from_thread_watcher=True)
    
def read_from_pipe(pipe, run_info, runner, stdout_is_text):

    # expand any "~" in path
    try:
        run_name = run_info.run_name
        first_output = True

        while True:
            if stdout_is_text:
                text_msg = pipe.readline()
            else:
                binary_msg = pipe.readline()
                text_msg = binary_msg.decode("utf-8")

            if len(text_msg) == 0 or run_info.killing:
                log_title("run ENDED: " + run_name)
                break      # EOF / end of process

            if first_output:
                log_title("run OUTPUT: " + run_name)
                first_output = False

            run_info.process_run_output(text_msg)

        # run post-processing
        runner.exit_handler(run_info, called_from_thread_watcher=True)
    except BaseException as ex:

        logger.exception("Error in controller.read_from_pipe, ex={}".format(ex))
        console.print("** Exception during read_from_pipe(): ex={}".format(ex))

        # for debugging print stack track
        traceback.print_exc()

        # log end of controller to JOB
        runner.store.log_job_event(run_info.workspace, runner.job_id, "node_error", 
            {"node_id": runner.node_id, "run": runner.parent_run_name, "exception": str(ex)})

        # give dev a chance to read the error before exiting (if viewing live log)
        console.print("controller sleeping 30 secs before exiting ...")
        time.sleep(30)    

        # shutdown app now
        console.print("controller calling os._exit(1)...")
        os._exit(1)

class XTController(rpyc.Service):

    def __init__(self, concurrent=1, my_ip_addr=None, multi_run_context_fn=None, multi_run_hold_open=False, 
            port=None, is_aml=False, *args, **kwargs):
        
        super(XTController, self).__init__(*args, **kwargs)

        self.concurrent = concurrent
        self.my_ip_addr = my_ip_addr
        self.multi_run_context_fn = multi_run_context_fn
        self.multi_run_hold_open = multi_run_hold_open
        self.port = port
        self.is_aml = is_aml
        self.restarting = False
        self.restart_delay = None
        self.idle_check_count = 0
        self.workspace = None
        self.mri = None

        # if previous controller log file exists, remove it
        fn = os.path.expanduser(constants.FN_CONTROLLER_EVENTS)
        if os.path.exists(fn):
            #console.print("removing previous CONTROLLER LOG file")
            os.remove(fn)

        self.reset_state(start_queue_worker=True)

    def reset_state(self, start_queue_worker=False):
        self.killing_process = False
        self.started = time.time()
        self.rundirs = {}
        self.shutdown_requested = None
        self.queue_check_count = 0
        self.runs = {}       # all runs that we know about (queued, spawing, running, or completed)
        self.queue = []      # runs that are waiting to run (due to concurrent)
        self.mirror_workers = []
        self.restart_is_present = True
        self.running_jobs = {}
        self.next_run_index = 0

        self.box_secret = os.getenv("XT_BOX_SECRET")
        self.node_id = os.getenv("XT_NODE_ID")

        self.node_index = int(self.node_id[4:])
        # self.state_changed = False

        utils.init_logging(constants.FN_CONTROLLER_EVENTS, logger, "XT Controller")

        is_windows = pc_utils.is_windows()
        
        self.cwd = os.path.abspath(os.getenv("XT_CWD"))
        self.rundir_parent = os.path.abspath(os.getenv("XT_HOMEBASE") + "/.xt/rundirs")

        # for backend services (vs. pool jobs)
        self.job_id = 0
        self.mrc_cmds = None
        self.search_style = None

        fn_inner_log = os.path.expanduser(constants.CONTROLLER_INNER_LOG)
        file_utils.ensure_dir_exists(file=fn_inner_log)

        # capture STDOUT
        self.cap_stdout = StreamCapture(sys.stdout, fn_inner_log, True)
        sys.stdout = self.cap_stdout

        # capture STDERR
        self.cap_stderr = StreamCapture(sys.stderr, True, file=self.cap_stdout.log_file)
        sys.stderr = self.cap_stderr

        log_title("XT Controller", double=True)
        log_info("build", constants.BUILD)
        log_info("date", datetime.datetime.now())

        log_title("CONTROLLER environment")

        log_info("concurrent", self.concurrent)
        log_info("my_ip_addr", self.my_ip_addr)
        log_info("multi_run_context_fn", self.multi_run_context_fn)
        log_info("multi_run_hold_open", self.multi_run_hold_open)
        log_info("port", self.port)
        if self.port:
            log_info("xt client msgs", "enabled")
        else:
            log_info("xt client msgs", "disabled")

        log_info("is_aml", self.is_aml)
        
        log_info("PYTHONPATH",  os.getenv("PYTHONPATH"))
        log_info("PYTHON version", sys.version)

        conda = os.getenv("CONDA_DEFAULT_ENV")

        if not conda:
            log_info("CONDA env",  "NOT SET")
        else:
            log_info("current CONDA env",  conda)

        log_info("node_id", self.node_id)
        log_info("cwd", self.cwd)
        log_info("rundirs", self.rundir_parent)

        log_title("PATH setting")
        log_info("PATH",  os.getenv("PATH"))

        file_utils.ensure_dir_exists(self.rundir_parent)

        # NOTE: do NOT add "store" as a class or instance member since it may vary by run/client
        # it should just be created when needed (at beginning and end of a run)

        self.hparam_search = HParamSearch(self.is_aml)

        if self.multi_run_context_fn:
            self.process_multi_run_context(self.multi_run_context_fn)

        log_info("workspace",  self.workspace)

        if start_queue_worker:
            # start a queue manager thread to start jobs as needed
            # NOTE: when running without the rypyc thread, the queue manager thread holds this process open
            queue_worker = Thread(target=self.bg_queue_worker)
            #queue_worker.daemon = True          # don't wait for this thread before exiting
            queue_worker.start()
    
    def process_multi_run_context(self, multi_run_context_fn):
        # read the cmd and context from the file

        with open(multi_run_context_fn, "rt") as tfile:
            text = tfile.read()

        mrc_data = json.loads(text)

        # NEW mrc data = {"search_style": xxx, "cmds": [], "context_by_nodes": {}
        self.search_style = mrc_data["search_style"]
        self.mrc_cmds = mrc_data["cmds"]
        self.runsets = mrc_data["runsets"]
       
        #debug_break()
        
        context_by_nodes = mrc_data["context_by_nodes"]
        dd = context_by_nodes[self.node_id]
        self.job_id = dd["job_id"]

        context_dict = dd["runs"][0]
        context = utils.dict_to_object(context_dict)
        parent_run_name = context.run_name

        #utils.debug_break()

        self.mrc_context = context
        self.workspace = context.ws
        self.job_id = context.job_id

        self.first_run_index = context.first_run_index
        self.last_run_index = context.last_run_index
        self.next_run_index = self.first_run_index

        # cache store for later use (don't want storge/mongo traffic needed for subsequent creations)
        store = store_from_context(context)
        self.store = store
        mongo = store.mongo

        # log NODE_START to job
        store.log_job_event(self.workspace, self.job_id, "node_start", {"node_id": self.node_id, "run": parent_run_name})

        self.use_simple_scheduling = self.mrc_context.use_simple_scheduling

        was_queued = []    # list of runs that were queued before we were restarted

        # queue the single or parent job in context
        context = self.mrc_context
        cmd_parts = context.cmd_parts
        aml_run = False

        # support for scheduling
        self.parent_run_name = parent_run_name
        self.next_child_id = 1
        self.first_run_index = context.first_run_index
        self.last_run_index = context.last_run_index

        self.write_connect_info_to_job(store, self.job_id)
        
        # controls allocation of child runs 
        self.mri = store.mongo.create_child_run_mgr(self.workspace, self.job_id, parent_run_name, self.node_id)

        # queue up first job
        self.queue_job_core(context, cmd_parts, aml_run=aml_run)

    def write_connect_info_to_job(self, store, job_id):

        if os.getenv("PHILLY_CONTAINER_PORT_RANGE_START"):
            # this is a PHILLY job
            ip = os.getenv("PHILLY_CONTAINER_IP")
            connect_info = {"controller_port": self.port, "ip_addr": ip}

            if store.mongo:
                store.mongo.update_connect_info_by_node(self.workspace, job_id, self.node_id, connect_info)

    def bg_queue_worker(self):
        '''
        We want any exception here to be logged then force app to exit.
        '''
        log_info("bg_queue_worker", "background thread started")

        while True:
            # time.sleep(1)
            # self.queue_check(1)

            try:
                # delay between queue checks
                time.sleep(2)

                self.queue_check(1)
            except BaseException as ex:
                logger.exception("Error in controller.thread_manager, ex={}".format(ex))
                console.print("** Exception during queue_check(): ex={}".format(ex))

                # for debugging print stack track
                traceback.print_exc()

                # give dev a chance to read the error before exiting (if viewing live log)
                console.print("sleeping 30 secs before exiting...")
                time.sleep(30)    

                # shutdown app now
                os._exit(1)

               
    def queue_count(self):
        with queue_lock:
            return len(self.queue)

    def on_shutdown(self, context):
        #log_title("controller SHUTDOWN")

        #remove the cert file
        fn_server_cert = os.path.expanduser(constants.FN_SERVER_CERT)
        if os.path.exists(fn_server_cert):
            os.remove(fn_server_cert)

        # stop logging (and free log file for deletion in below code)
        logging.shutdown()        

        if context:
            store = self.store
            node_num = os.getenv("XT_NODE_ID")[4:]

            # write XT event log to job store AFTER
            fn = os.path.expanduser(constants.FN_CONTROLLER_EVENTS)
            log_info("controller events", fn)   
            log_info("exists", os.path.exists(fn))

            if os.path.exists(fn):
                fn_store = "node-{}/after/xt_logs/{}".format(node_num, os.path.basename(fn))

                #console.print("starting to upload CONTROLLER log: {} => {}".format(fn, fn_store))
                store.upload_file_to_job(context.ws, context.job_id, fn_store, fn)
                #console.print("finished upload of CONTROLLER log")

                # bug workaround - the above shutdown doesn't free the file, so we
                # just make sure to delete the file on startup of next controller run

                # remove it, since it is appended to on each job (local, VM)
                #os.remove(fn)

            # # write controller log to job store AFTER
            # fn = os.path.expanduser(constants.CONTROLLER_INNER_LOG)
            # log_info("controller inner", fn)   
            # log_info("exists", os.path.exists(fn))

            # if os.path.exists(fn):
            #     fn_store = "node-{}/after/xt_logs/controller.log".format(node_num)
            #     store.upload_file_to_job(context.ws, context.job_id, fn_store, fn)

        log_title("XT controller: mongo call stats")
        if self.store.mongo:
            self.store.mongo.print_call_stats()

        # log end of controller to JOB
        self.store.log_job_event(self.workspace, self.job_id, "node_end", {"node_id": self.node_id, "run": self.parent_run_name})

        # give other threads time to wrapup the processing of their runs before
        # we exit
        time.sleep(2)    # wait for 2 secs for any bg thread cleanup
        console.print("controller calling os._exit(0)...")

        # os._exit will exit all threads without running 'finally' blocks 
        # sys.exit will exit current thread only, but run 'finally' blocks for a cleaner exit
        os._exit(0)

    def on_idle(self):

        log_title("controller IDLE detected")

        if self.restarting:
            # simulate some time passing
            time.sleep(self.restart_delay)

            # reset controller's state and start processing the MRC file again
            self.reset_state()
            self.restarting = False
        else:
            # prepare to shut down
            if self.runs:
                first_run = list(self.runs.values())[0]
                context = first_run.context
                store = self.store

                for job_id, alive in self.running_jobs.items():
                    if alive:
                        self.running_jobs[job_id] = False

                        # tell mongo this job node is exiting
                        console.diag("calling MONGO job_node_exit: job_id={}".format(job_id))

                        mongo = store.get_mongo()
                        if mongo:
                            mongo.job_node_exit(context.ws, job_id)
            else:
                context = None

            # is it time to shut down the controller?
            #if self.multi_run_context_fn and not self.multi_run_hold_open:
            if self.shutdown_requested or (self.multi_run_context_fn and not self.multi_run_hold_open):
                self.on_shutdown(context)

    def queue_check(self, max_starts=1):
        ''' see if 1 or more jobs at top of queue can be run '''

        # active_count = self.get_active_runs_count()
        # if active_count == 0:
        #     self.on_idle()

        # for responsiveness, limit # of runs can be released in a single check
        for _ in range(max_starts):       
            running_count = len(self.get_running_names())

            if not self.process_top_of_queue(running_count):
                break

        # AFTER potentially starting a run, see if we are idle
        self.idle_check()

    def idle_check(self):
        self.idle_check_count += 1

        alive = self.get_alive_names()
        alive_count = len(alive)
        if alive_count == 0:

            with runs_lock:
                not_wrapped_up = [ri.run_name for ri in self.runs.values() if not ri.is_wrapped_up]
                wrapping_count = len(not_wrapped_up)

            #print("queue_check: running_count={}, names={}".format(running_count, names))
            if self.idle_check_count > MAX_IDLE_CHECK:
                console.print("idle_check: exceeded MAX_IDLE_CHECK={} checks, aborting controller".format(MAX_IDLE_CHECK))
                self.on_idle()
            elif wrapping_count:
                console.print("idle_check: waiting for runs to wrap up: {}".format(not_wrapped_up))
            else:
                console.print("idle_check: ALL RUNS are wrapped up")
                self.on_idle()

    def process_top_of_queue(self, running_count):
        processed_entry = False
        run_info = None

        with queue_lock:
            if len(self.queue):
                if running_count < self.concurrent or self.concurrent == -1:
                    run_info = self.queue.pop(0)

                    # run_info is ready to run!
                    if run_info.run_as_parent and not run_info.parent_prep_needed:
                        run_info.status = "spawning"
                    else:
                        run_info.status = "running"
                        run_info.started = time.time()

        if run_info:
            self.process_queue_entry(run_info)
            processed_entry = True

        return processed_entry

    def process_queue_entry(self, run_info):
        if run_info.parent_prep_needed:

            # run PARENT PREP script 
            self.start_local_run(run_info, cmd_parts=[])

        elif run_info.run_as_parent:
            
            # should parent spawn new child?
            context = run_info.context
            store = self.store

            # get index of next run for our node storage
            entry = None
            #utils.debug_break()

            if self.mri:
                #entry = store.mongo.get_next_run_index(context.ws, run_info.job_id, self.node_index)
                entry = self.mri.get_next_child_run()

            else:
                # TODO: need to get run index from store
                print("self.next_run_index=", self.next_run_index, "self.last_run_index=", self.last_run_index)

                if self.next_run_index <= self.last_run_index:
                    entry = {"status": "unstarted", "run_index": self.next_run_index}
                    self.next_run_index += 1

            log_info("get_next_run_index",  entry)

            # log run index to JOB
            store.log_job_event(self.workspace, self.job_id, "get_index", {"node_id": self.node_id, "entry": entry})

            if entry:
                run_index = entry["run_index"]
                child_restarting = (entry["status"] == constants.WAITING)

                log_info("==> running INDEX", "{}/{}".format(run_index, context.total_run_count-1))

                # yes: CREATE CHILD
                self.run_template(run_info, run_index, entry, child_restarting)

                # insert back into queue
                with queue_lock:
                    self.queue.append(run_info)
                    run_info.status = "queued"
            else:

                # no: parent has completed
                console.print("marking PARENT RUN as completed: ", run_info.run_name)

                with run_info.lock:
                    run_info.status = "completed"

                    # process end of parent run
                    #run_info.run_wrapup()
                    self.exit_handler(run_info, True, called_from_thread_watcher=False)

        else:
            # start NORMAL RUN
            self.start_local_run(run_info, cmd_parts=run_info.cmd_parts)

    def add_to_runs(self, run_info):
        key = run_info.workspace + "/" + run_info.run_name
        with runs_lock:
            self.runs[key] = run_info

    def run_template(self, run_info, run_index, entry, child_restarting):
        run_name = run_info.run_name

        # ensure PARENT has a rundir (so it can log its own output)
        if not run_info.rundir:
            rundir, rundir_index = self.allocate_rundir(run_name)
            run_info.rundir = rundir

            # set up a console output file
            console_fn = rundir + "/output/console.txt"
            run_info.set_console_fn(console_fn)

        # create a parent log event for "spawning"
        context = run_info.context
        store = self.store
        store.log_run_event(context.ws, run_name, "status-change", {"status": "spawning"})   # , is_aml=self.is_aml)

        # spawn child run from template
        child_info = self.spawn_child(run_info, run_index, entry, child_restarting)
        child_name = child_info.run_name

        # add to runs
        self.add_to_runs(child_info)

         # start normal run of CHILD
        self.start_local_run(child_info, cmd_parts=child_info.cmd_parts)

        if run_info.status == "queued":
            # create a parent log event for "spawing"
            store.log_run_event(context.ws, run_name, "status-change", {"status": "queued"})  # , is_aml=self.is_aml)

    def requeue_run(self, run_info):
        with queue_lock:
            self.queue.append(run_info)
            run_info.status = "queued"

        console.print("run requeued: " + run_info.run_name)

    def schedule_controller_exit(self):
        if self.multi_run_hold_open:
            console.print("holding controller open after single run...")
        else:
            console.print("xt controller - scheduling shutdown..")
            self.shutdown_requested = True

    def spawn_child(self, parent, run_index, entry, child_restarting):
        spawn_start = time.time()

        # create a CLONE of template as a child run
        start_child_start = time.time()

        # create a child run_info from the parent template
        context = copy.copy(parent.context)
        context.repeat = None
        context.is_parent = False
        context.restart = child_restarting

        #debug_break()

        # find cmd to use for this child run
        cmd_index = run_index % len(self.mrc_cmds)

        cmd = self.mrc_cmds[cmd_index]
        log_info("run_index: " + str(run_index), "cmd: {}".format(cmd))

        # update context with new cmd
        context.cmd_parts = utils.cmd_split(cmd)    

        store = self.store

        log_info("spawn_child, parent", parent.run_name)

        if parent.aml_run:
            # create AML child run
            child_aml_run = parent.aml_run.child_run()
            # child_name = "{}.run{}".format(context.exper_name, child_aml_run.number)
            # console.print("created AML child:", child_name)
            child_name = None
        else:
            child_aml_run = None
            child_name = self.mri.get_child_name(entry, self.parent_run_name)

        console.print("spawn_child: created", child_name)

        # the logged value of search_type reflects if it was really used
        if context.search_style in ["dynamic", "static"]:
           search_type = context.search_type
        else:
            search_type = None

        store.start_child_run(context.ws, parent.run_name, context.exper_name,
            child_name=child_name, 
            box_name=context.box_name, app_name=context.app_name, path=context.target_file,
            from_ip=context.from_ip, from_host=context.from_host, sku=context.sku,
            job_id=context.job_id, pool=context.pool, node_index=context.node_index, 
            aggregate_dest=context.aggregate_dest,  
            compute=context.compute, service_type=context.service_type, username=context.username, 
            is_aml=False, search_type=search_type, run_index=run_index)

        #debug_break()

        if context.search_style == "dynamic":
            # perform dynamic HPARAM search
            cmd_parts = self.hparam_search.process_child_hparams(child_name, store, context, parent)
        elif self.runsets:
            # select a runset and apply to run
            runset = self.runsets[run_index % len(self.runsets)]
            cmd_parts = list(context.cmd_parts)
            cmd_parts = self.hparam_search.apply_runset(runset, cmd_parts, context, store, child_name)
        else:
            # select the normal command for the run
            cmd_parts = context.cmd_parts

        # must update context info
        context.run_name = child_name

        self.print_elapsed(start_child_start, "START CHILD RUN")
        
        # log run CMD
        store.log_run_event(context.ws, child_name, "cmd", {"cmd": cmd_parts, "xt_cmd": context.xt_cmd})  # , is_aml=self.is_aml)

        # for now, don't log context (contain private credentials and not clear if we really need it)
        # for CHILD runs, record all "context" (from cmd line, user config, default config) in log (for audit/re-run purposes)
        #store.log_run_event(context.ws, child_name, "context", context.__dict__)

        # get_client_context() should have set this correct for this parent/child run
        #prep_script = context.child_prep_script     
        #prep_script = None

        child_info = RunInfo(child_name, context.ws, cmd_parts, context.run_script, 
            None, context, "running", True, parent_name=parent.run_name, mirror_close_func = self.stop_mirror_worker, 
            aml_run=child_aml_run, node_id=self.node_id, run_index=run_index, mri=self.mri, mri_entry=entry, 
            store=self.store)

        self.print_elapsed(spawn_start, "SPAWN CHILD")

        parent.process_run_output("spawned: {}\n".format(child_name))

        return child_info
 
    def print_elapsed(self, started, title):
        elapsed = time.time() - started
        log_info(title, "{:.2f} secs".format(elapsed))
        
    def exit_handler(self, run_info, run_info_is_locked=False, called_from_thread_watcher=False):
        ''' be conservative here - don't assume we have even started the process.
        '''
        console.print("exit_handler: {}".format(run_info.run_name))

        if not run_info.process_was_created:
            # run died during launch (likely due to Azure/MongoDB errors)
            if run_info.status == "running":
                run_info.status = "error"
                run_info.exit_code = -2    # died during launch

        if run_info.parent_prep_needed:
            console.print("parent prep script exited")
            run_info.wrapup_parent_prep_run()
        else:
            if called_from_thread_watcher:
                console.print("controller: app exit detected: " + run_info.run_name)
                pass
            else:
                console.print("controller: parent app completed: " + run_info.run_name)

            run_info.run_wrapup()

            # send "app exited" msg to callbacks
            msg = constants.APP_EXIT_MSG + run_info.status + "\n"
            run_info.process_run_output(msg, run_info_is_locked)

            # log run end to JOB
            dd = {"node_id": self.node_id, "run": run_info.run_name, "status": run_info.status, 
                "is_parent": run_info.is_parent, "exit_code": run_info.exit_code}
            self.store.log_job_event(self.workspace, self.job_id, "end_run", dd)

            console.print("run_end logged to job: {}".format(run_info.run_name))

        run_info.check_for_completed(True)

        # release rundir
        if run_info.rundir:
            self.return_rundir(run_info.rundir)
            run_info.rundir = None

        if run_info.parent_prep_needed:
            run_info.parent_prep_needed = False

            console.print("run={}, status={}".format(run_info.run_name, run_info.status))

            if run_info.status == "completed":
                # now that the parent prep script has successfully run we can 
                # requeue parent run to spawn child runs
                self.requeue_run(run_info)
        else:
            run_info.is_wrapped_up = True

        console.print("end of exit handler")

    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        #console.print("client attach!")
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        #console.print("client detach!")
        pass


    def fix_path(self, path):
        path = os.path.expanduser(path)

        if  pc_utils.is_windows():
            path = path.replace("$HOME", "%USERPROFILE%")
            path = path.replace("/", "\\")

        return path

    def find_file_in_path(self, name):
        path_list = os.getenv('PATH', '')
        #console.print("path_list=", path_list)

        if pc_utils.is_windows():
            paths = path_list.split(";")
        else:
            paths = path_list.split(":")

        full_fn = None

        for path in paths:
            fn = path + "/" + name
            #console.print("testing fn=", fn)

            if os.path.exists(fn):
                full_fn = fn
                #console.print("match found: fn=", full_fn)
                break
        
        return full_fn

    def is_process_running(self, name):
        name = name.lower()
        found = False

        for process in psutil.process_iter():

            # this is the only allowed exception catching in controller process
            try:
                if name in process.name().lower():
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # ignore known OS exceptions while iterating processes
                pass

        return found

    def validate_request(self, request_token):
        #print("token={}, box_secret={}".format(request_token, self.box_secret))
        
        if request_token != self.box_secret:
            print("*** tokens do not match - validation failed ***")
            errors.service_error("Access denied")
        #print("request validated")

    def exposed_queue_user_request(self, token, request):
        self.validate_request(token)
        fn = os.path.expanduser(constants.FN_USER_REQUEST)

        with open(fn, "at") as outfile:
            outfile.write(request + "\n")

    def exposed_get_tensorboard_status(self, token):
        self.validate_request(token)

        running = self.is_process_running("tensorboard")
        status = {"running": running}
        return status

    def exposed_elapsed_time(self, token):
        self.validate_request(token)
        return time.time() - self.started

    def exposed_xt_version(self, token):
        self.validate_request(token)
        return constants.BUILD

    def exposed_controller_log(self, token):
        self.validate_request(token)
        fn = os.path.expanduser(constants.CONTROLLER_INNER_LOG)
        with open(fn, "r") as textfile:
            text = textfile.read()
        return text

    def copy_bag(self, bag):
        new_bag = Bag()
        for key,value in bag.get_dict().items():
            setattr(new_bag, key, value)

        return new_bag

    def copy_dict(self, dict):
        new_dict = {}
        for key,value in dict.items():
            new_dict[key] = value

        return new_dict

    def allocate_rundir(self, run_name, allow_retry=True):
        rundir = None
        base_name = "rundir"

        with rundir_lock:
            for dirname, rn in self.rundirs.items():
                if not rn:
                    # it's available - mark it as in-use
                    self.rundirs[dirname] = run_name
                    rundir = dirname
                    break

            if not rundir:
                # add a new name
                rundir = base_name + str(1 + len(self.rundirs))
                self.rundirs[rundir] = run_name
                log_info("new rundir", rundir)

            log_info("updated rundirs", self.rundirs)

        start = len(base_name)
        rundir_index = int(rundir[start:])
        runpath = self.rundir_parent + "/" + rundir

        # remove and recreate for a clear start for each run
        try:
            file_utils.ensure_dir_clean(runpath)
        except Exception as ex:    #  AccessDenied:
            print("Exception deleting rundir, ex=", ex)
            if allow_retry:
                #time.sleep(10)    # experiment; see if wating 10 secs helps 
                #file_utils.ensure_dir_clean(runpath)

                # try just once more (a different directory)
                self.allocate_rundir(run_name, allow_retry=False)
            else:
                raise ex

        return runpath, rundir_index

    def return_rundir(self, rundir_path):
        rundir = os.path.basename(rundir_path)

        with rundir_lock:
            # we check because "restart controller" will try to return rundirs from before restart
            if rundir in self.rundirs:
                # mark as no longer used
                self.rundirs[rundir] = None

    def exposed_queue_job(self, token, json_context, cmd_parts):
        self.validate_request(token)

        context = json.loads(json_context)
        context = utils.dict_to_object(context)

        # make a copy of cmd_parts
        cmd_parts = list(cmd_parts)
        context.cmd_parts = cmd_parts
        
        run_info = self.queue_job_core(context, cmd_parts)
        return True, run_info.status

    def queue_job_core(self, context, cmd_parts, previously_queue=False, aml_run=None):

        run_name = context.run_name
        exper_name = context.exper_name
        log_title("QUEUING run: {}".format(run_name))

        #working_dir = os.path.expanduser(context.working_dir)
        app_name = context.app_name
        run_script = context.run_script
        log_info("context.run_script", run_script)

        parent_script = context.parent_script
        parent_prep_needed = context.is_parent and parent_script
        if parent_prep_needed:
            log_info("parent_script=", parent_script)
            run_script = parent_script

        # apply concurrent of run when it is queued
        if context.concurrent is not None:
            self.concurrent = context.concurrent
            log_info("set concurrent", self.concurrent)

        #debug_break()

        run_info = RunInfo(run_name, context.ws, cmd_parts, run_script, context.repeat, context, "queued", True, 
            parent_name=None, parent_prep_needed=parent_prep_needed, mirror_close_func = self.stop_mirror_worker, aml_run=aml_run,
            node_id=self.node_id, run_index=None, store=self.store)

        # log run QUEUED event 
        store = self.store
        store.log_run_event(context.ws, run_name, "queued", {})   # , is_aml=self.is_aml)

        # queue job to be run
        with queue_lock:
            self.queue.append(run_info)
            log_info("job queue", "{} entries".format(len(self.queue)))

        self.add_to_runs(run_info)

        log_info("run QUEUED", run_name)
        
        # before returning - see if this run can be started immediately
        #self.queue_check(1)

        return run_info 

    def create_default_run_script(self, cmd_parts, activate_cmd):
        ''' create a default run_script for user that specified a cmd.
        '''
        #log_info("create run script: cmd_parts", cmd_parts)

        flat_cmd = " ".join(cmd_parts)
        run_script = []
        
        if activate_cmd:
            if pc_utils.is_windows():
                activate_cmd = activate_cmd.replace("$call", "@call")
            else:
                activate_cmd = activate_cmd.replace("$call", "")
            run_script.append(activate_cmd)

        run_script.append(flat_cmd)
        return run_script

    def start_local_run(self, run_info, cmd_parts):
        # wrapper to catch exceptions and clean-up
        # we need to support multiple run directories (for concurrent param) - so we cannot run in originating dir

        # uncomment to break in debugger here
        #debug_break()

        run_name = run_info.run_name
        log_title("STARTING: {}".format(run_name))

        rundir, run_dir_index = self.allocate_rundir(run_name)
        run_info.rundir = rundir

        self.start_local_run_core(run_info, cmd_parts, rundir, run_dir_index)

        # try:
        #     self.start_local_run_core(run_info, cmd_parts, rundir, run_index)
        # except BaseException as ex:
        #     logger.exception("Error in controller.start_local_run, ex={}".format(ex))
        #     console.print("** Exception during start_local_run(): ex={}".format(ex))
        #     self.exit_handler(run_info, False, called_from_thread_watcher=False)
        #     # in controller code, always give up machine if we fail 
        #     raise ex   

    def start_local_run_core(self, run_info, cmd_parts, rundir, rundir_index):
        '''
        Note: 
            when user did NOT specify a run script:
                - cmd_parts is the "python/docker/exe" run cmd
                - its args have been updated with HP search args for this run
            --> in this case, "wrap" cmd_parts in a default script and just run script without args

            when user DID specify a run script:
                - run script should contain a "%*" cmd to be HP-search enabled
                - cmd_parts, in this case, looks like: train.sh --epochs=3, lr=.3, etc.
            --> in this case, run "cmd_parts" (which will run the RUN SCRIPT with correct args)
        '''
        log_info("cmd_parts", cmd_parts)

        context = run_info.context  
        run_name = run_info.run_name

        # download files from STORE to rundir
        store = self.store
        job_id = context.job_id 

        if self.is_aml:
            # # copy contents of current dir to rundir (Azure ML copied snapshot to this dir)
            # file_utils.zap_dir(rundir)
            # file_utils.copy_tree(".", rundir)

            # write generated sweep text to a file in rundir
            if context.generated_sweep_text:
                fn = rundir + "/" + os.path.basename(context.hp_config)
                log_info(fn, "{:.120s}".format(context.generated_sweep_text))

                with open(fn, "wt") as outfile:
                    outfile.write(context.generated_sweep_text)

        # its better to copy user's code files from /.xt/cwd because user may have
        # run some setup commands that added to or modified the files
        side_load_files = True

        if side_load_files:
            # instead of copying code from JOB, we copy from the controller working directory so each run gets
            # the benifit on any parent parent script adjustment to the environment
            omit_list = ["rundirs", "mnt", "blobfusetmp*", "__after__", "__multi_run_context__.json", 
                "__run_controller__.py", "__xt_server_cert__.pem", "__aml_shim__.py", 
                "extract_project.success", "azureml-setup", "azureml-logs", "packages-microsoft-prod.deb", 
                "azureml_compute_logs", "__wrapped__.bat", "__current_running_entry__.txt", "__t__", 
                "__batch_helper__.sh", "__wrapped__.sh", "azureml-logs", "azureml-setup"]

            copy_count = capture.make_local_snapshot(".", rundir, ".", omit_list=omit_list) 
            log_info("sideloaded", "{} CODE files from controller working dir".format(copy_count))
        else:
            # code is stored in JOB BEFORE files
            files = capture.download_before_files(store, job_id, context.ws, run_name, dest_dir=rundir, silent=True)
            log_info("downloaded", "{} BEFORE files from JOB STORE".format(len(files)))

        log_title("DIR " + rundir)
        os.system("ls -lt {} | grep -vh '^total' | head -n 30".format(rundir))

        # HP search generated config.txt is stored in RUN BEFORE files
        files = capture.download_before_files(store, None, context.ws, run_name, dest_dir=rundir, silent=True)
        log_info("downloaded", "{} BEFORE files from RUN STORE".format(len(files)))

        run_script = run_info.run_script
        script_args = None

        if run_script:
            # user supplied a RUN SCRIPT and args in cmd_parts
            script_args = cmd_parts
            # must add rundir since our working dir is different
            fn_script = os.path.join(rundir, cmd_parts[0])
        else:
            # use supplied a run command; wrap it in a default script
            run_script = self.create_default_run_script(cmd_parts, context.activate_cmd)
            script_args = None
            fn_script = None

        # log run STARTED event 
        if context.restart:
            log_title("CHILD RESTART detected")

        start_event_name = "restarted" if context.restart else "started"
        store.log_run_event(context.ws, run_name, start_event_name, {})   # , is_aml=self.is_aml)
        #prep_script = run_info.prep_script  

        exper_name = context.exper_name

        # local function
        def safe_env_value(value):
            return "" if value is None else str(value)

        # copy info from parent environment
        child_env = os.environ.copy()

        # pass xt info to the target app (these are access thru Store "running" API's)
        child_env["XT_USERNAME"] = safe_env_value(context.username)
        child_env["XT_CONTROLLER"] = "1"

        child_env["XT_WORKSPACE_NAME"] = safe_env_value(context.ws)
        child_env["XT_EXPERIMENT_NAME"] = safe_env_value(exper_name)
        child_env["XT_RUN_NAME"] = safe_env_value(run_name)
        child_env["XT_JOB_ID"] = safe_env_value(job_id)

        child_env["XT_TARGET_FILE"] = safe_env_value(context.target_file)
        child_env["XT_RESUME_NAME"] = safe_env_value(context.resume_name)
        child_env["XT_STORE_CODE_PATH"] = context.store_code_path

        sc = json.dumps(context.store_creds)
        child_env["XT_STORE_CREDS"] = utils.text_to_base64(sc)

        mc = safe_env_value(context.mongo_conn_str)
        child_env["XT_MONGO_CONN_STR"] = utils.text_to_base64(mc)

        # update XT_OUTPUT_DIR and XT_OUTPUT_MNT for child run path
        mnt_path = os.getenv("XT_OUTPUT_MNT")
        parent_name = run_info.parent_name
        if mnt_path and parent_name:
            child_mnt_path = mnt_path.replace(parent_name, run_name)
            log_info("child XT_OUTPUT_MNT", child_mnt_path)

            child_env["XT_OUTPUT_MNT"] = child_mnt_path
            child_env["XT_OUTPUT_DIR"] = child_mnt_path

        pp = os.getenv("PYTHONPATH")
        log_info("PYTHONPATH", pp)
        
        log_info("run_script", run_script)

        # this expands symbols in the script AND removes CR chars for linux scripts
        run_script = scriptor.fixup_script(run_script, pc_utils.is_windows(), True, run_info=run_info, concurrent=self.concurrent)  

        # write RUN SCRIPT LINES to a run_appXXX script file
        if pc_utils.is_windows():
            if not fn_script:
                fn_script = self.fix_path("{}/run_app{}.bat".format(self.cwd, rundir_index))
            #utils.send_cmd_as_script_to_box(self, "localhost", flat_cmd, fn_script, prep_script, False)
            scriptor.write_script_file(run_script, fn_script, for_windows=True)
            log_info("WINDOWS script", fn_script)
        else:
            if not fn_script:
                fn_script = self.fix_path("{}/run_app{}.sh".format(self.cwd,    rundir_index))
            #utils.send_cmd_as_script_to_box(self, "localhost", flat_cmd, fn_script, prep_script, True)
            scriptor.write_script_file(run_script, fn_script, for_windows=False)
            log_info("LINUX script", fn_script)

        console_fn = rundir + "/output/console.txt"
        run_info.set_console_fn(console_fn)

        log_info("target", child_env["XT_TARGET_FILE"])

        # use False if we want to capture TDQM output correctly (don't convert CR to NEWLINE's)
        stdout_is_text = True
        bufsize = -1 if stdout_is_text else -1     # doesn't seem to affect TDQM's turning off progress logging...

        if not script_args:
            script_args = [fn_script]

        prefix = context.shell_launch_prefix
        if not prefix and not pc_utils.is_windows():
            # probably running a linux docker container on windows
            prefix = "bash"

        parts = process_utils.make_launch_parts(prefix, script_args)

        # set run's current dir
        cwd = os.path.join(rundir, context.working_dir)

        # write run's context file, in case run needs to access additional info
        json_text = json.dumps(context.__dict__)
        fn_context = os.path.join(cwd, constants.FN_RUN_CONTEXT)
        file_utils.write_text_file(fn_context, json_text)
        log_info("context written", fn_context)

        log_title("starting process: " + run_name)

        # log run start to JOB
        dd = {"node_id": self.node_id, "run": run_name, "restart": context.restart}
        store.log_job_event(self.workspace, self.job_id, "start_run", dd)

        if pc_utils.is_windows():
            # target must be a fully qualified name to work reliably
            fq = os.path.join(rundir, parts[0])
            if os.path.exists(fq):
                parts[0] = fq

            # run as dependent process with HIDDEN WINDOW
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            #console.print("startupinfo=", startupinfo)

            log_info("cwd", cwd)
            log_info("parts", parts)
            log_info("script", file_utils.read_text_file(fn_script))

            p = process = subprocess.Popen(parts, cwd=cwd, startupinfo=startupinfo, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=child_env, universal_newlines=stdout_is_text, bufsize=bufsize)
        else:
            log_info("cwd", cwd)
            log_info("parts", parts)
            log_info("script", file_utils.read_text_file(fn_script))

            p = process = subprocess.Popen(parts, cwd=cwd, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=child_env, universal_newlines=stdout_is_text, bufsize=bufsize)

        with run_info.lock:
            run_info.set_process(process)

        # start a thread to consume STDOUT and STDERR from process
        stdout_thread = Thread(target=read_from_pipe, args=(process.stdout, run_info, self, stdout_is_text))
        stdout_thread.start()

        # start a MIRROR thread to copy files to grok server
        if context.mirror_dest and context.mirror_files and (context.grok_server or context.mirror_dest == "storage"):
            log_info("mirror_dest=", context.mirror_dest)
            log_info("mirror_files=", context.mirror_files)

            self.start_mirror_worker(store, run_info, rundir, run_name, context)

        log_info("process created", p)

        # tell mongo JOBS that this job has a new run
        console.diag("calling MONGO job_run_start: job_id={}".format(job_id))
        mongo = store.get_mongo()
        if mongo:
            mongo.job_run_start(context.ws, job_id)

            # tell mongo RUNS that this run has started
            console.diag("calling MONGO run_start: ws={}, run_name={}".format(context.ws, run_name))
            mongo.run_start(context.ws, run_name)

        if not job_id in self.running_jobs:
            # this is the first run of this job on this node
            self.running_jobs[job_id] = True

            if mongo and not context.restart:
                # tell mongo the first time this job node starts running
                console.diag("calling MONGO job_node_start: job_id={}".format(job_id))
                mongo.job_node_start(context.ws, job_id)

        return True

    def start_mirror_worker(self, store, run_info, rundir, run_name, context):
        console.print("starting a MIRROR thread: grok={}, mirror-dest={}, mirror-path={}".format(context.grok_server, 
            context.mirror_dest, context.mirror_files))
        worker = MirrorWorker(store, rundir, context.mirror_dest, context.mirror_files, context.grok_server, context.ws, run_name)
        
        run_info.mirror_worker = worker
        self.mirror_workers.append(worker)

        worker.start()

    def stop_mirror_worker(self, run_info):
        if run_info.mirror_worker:
            worker = run_info.mirror_worker
            worker.stop()

            if worker in self.mirror_workers:
                self.mirror_workers.remove(worker)
            run_info.worker = None

    def diag(self, msg):
        console.print(msg)

    def get_run_info(self, ws_name, run_name, raise_if_missing=True):
        key = ws_name + "/" + run_name
        with runs_lock:
            if key in self.runs:
                return self.runs[key]
            elif raise_if_missing:
                raise Exception("unknown run_name: " + ws_name + "/" + run_name)
        return None

    def exposed_attach(self, token, ws_name, run_name, callback):
        print("==========> ATTACH: #1")
        self.validate_request(token)
        run_info = self.get_run_info(ws_name, run_name)

        # taking lock here hangs this thread (.attach also takes the lock)
        status = run_info.status
        if (status != "running"):
            return False, status

        run_info.attach(callback)
        return True, status

    def exposed_detach(self, token, ws_name, run_name, callback):
        self.validate_request(token)
        run_info = self.get_run_info(ws_name, run_name)
        index = run_info.detach(callback)
        return index

    def exposed_get_status_of_runs(self, token, ws, run_names_str):
        self.validate_request(token)
        status_dict = {}
        run_names = run_names_str.split("^")

        for run_name in run_names:
            run_info = self.get_run_info(ws, run_name, False)
            if run_info:
                status_dict[run_name] = run_info.status

        json_status_dict = json.dumps(status_dict)
        return json_status_dict

    def exposed_get_status_of_workers(self, token, worker_name):
        self.validate_request(token)
        status_list = []

        for worker in self.mirror_workers:
            status = worker.get_status()
            status_list.append(status)

        json_text = json.dumps(status_list)
        return json_text

    def status_matches_stage_flags(self, status, stage_flags):
        match = False

        if status in ["queued"]: 
            match = "queued" in stage_flags
        elif status in ["spawning", "running"]: 
            match = "active" in stage_flags
        else:
            match = "completed" in stage_flags

        return match

    def exposed_get_runs(self, token, stage_flags, ws_name=None, run_name=None):
        self.validate_request(token)
        if run_name:
            console.print("get_status: ws_name=", ws_name, ", run_name=", run_name)

            run_info = self.get_run_info(ws_name, run_name)
            return run_info.get_summary_stats() + "\n"

        result = ""
        with runs_lock:
            for run_info in self.runs.values():
                matches = self.status_matches_stage_flags(run_info.status, stage_flags)
                if matches:
                    result += run_info.get_summary_stats() + "\n"
        return result

    def cancel_core(self, run_info, for_restart=False):
        result = None
        status = None
        
        console.print("---- killing: {}/{} -----".format(run_info.workspace, run_info.run_name))

        with queue_lock:
            if run_info in self.queue:
                self.queue.remove(run_info)

        # log run KILLED event 
        context = run_info.context
        store = self.store

        if not for_restart:
            store.log_run_event(context.ws, run_info.run_name, "cancelled", {})        # , is_aml=self.is_aml)

        with run_info.lock:
            run_info.killed_for_restart = for_restart
            result, status, before_status = run_info.kill()

            # try:
            #     result, status, before_status = run_info.kill()
            # except BaseException as ex:
            #     logger.exception("Error in controller.cancel_core, ex={}".format(ex))
            #     console.print("{}: got exception while trying to kill process; ex={}".format(run_info.run_name, ex))
            #     # in controller code, always give up machine if we fail 
            #     raise ex   

        console.print("run_info.kill returned result=", result, ", status=", status)
        
        # if run_info == self.single_run:
        #     self.schedule_controller_exit()

        return result, status, before_status

    def get_matching_run_infos(self, full_run_names):
        # match all runinfos that have not finished (exact match and matching children)
        matches = []
        full_name_set = set(full_run_names)

        with runs_lock:
            running = [ri for ri in self.runs.values() if ri.status in ["running", "spawning", "queued"]] 

        for ri in running:
            base_name = ri.run_name.split(".")[0]
            if ri.workspace + "/" + base_name in full_name_set:
                # match parent to parent or child to parent
                matches.append(ri)
            elif ri.workspace + "/" + ri.run_name in full_name_set:
                # exact parent/child name match
                matches.append(ri)

        console.print("matches=", matches)
        return matches

    def get_property_matching_run_infos(self, prop_name, prop_value):
        # match all runinfos that have not finished (exact match and matching children)
        matches = []

        with runs_lock:
            running = [ri for ri in self.runs.values() if ri.status in ["running", "spawning", "queued"]] 

        for ri in running:
            if getattr(ri, prop_name) == prop_value:
                matches.append(ri)

        console.print("matches=", matches)
        return matches

    def cancel_all(self, for_restart=False):
        to_kill = []
        results = []

        # loop until we are IDLE
        while True:
            with queue_lock:
                to_kill += self.queue
                self.queue = []

            # grab all running jobs
            with runs_lock:
                running = [ri for ri in self.runs.values() if ri.status in ["running", "spawning"]] 
                to_kill += running

            if not to_kill:
                # all runs cancelled
                break

            # kill jobs 1 at a time
            for run_info in to_kill:
                result, status, before_status = self.cancel_core(run_info, for_restart=for_restart)

                results.append( {"workspace": run_info.workspace, "run_name": run_info.run_name, 
                    "cancelled": result, "status": status, "before_status": before_status} )

        return results

    def exposed_restart_controller(self, token, delay_secs=.01):
        self.validate_request(token)

        # simulate a service restart (for testing both XT and user's ML restart code)
        self.restarting = True
        self.restart_delay = delay_secs

        # cannot do wrapup for these runs (must look like box rebooted)
        self.cancel_all(for_restart=True)

        return True

    def cancel_specified_runs(self, full_run_names):
        to_kill = []
        results = []

        # loop until we are IDLE
        while True:

            to_kill = self.get_matching_run_infos(full_run_names)
            console.print("cancel_specified_runs: to_kill=", to_kill)

            if not to_kill:
                # we are IDLE
                #console.print("----------- SPECIFIED RUNS ARE IDLE ---------------")
                break

            # kill jobs 1 at a time
            while len(to_kill):
                run_info = to_kill.pop(0)
                result, status, before_status = self.cancel_core(run_info)

                results.append( {"workspace": run_info.workspace, "run_name": run_info.run_name, 
                    "cancelled": result, "status": status, "before_status": before_status} )

        return results

    def cancel_runs_by_property_core(self, prop_name, prop_value):
        to_kill = []
        results = []

        # loop until we are IDLE
        while True:

            to_kill = self.get_property_matching_run_infos(prop_name, prop_value)
            console.print("cancel_runs_by_property_core: to_kill=", to_kill)

            if not to_kill:
                # we are IDLE
                #console.print("----------- SPECIFIED RUNS ARE IDLE ---------------")
                break

            # kill jobs 1 at a time
            while len(to_kill):
                run_info = to_kill.pop(0)
                result, status, before_status = self.cancel_core(run_info)

                results.append( {"workspace": run_info.workspace, "run_name": run_info.run_name, 
                    "cancelled": result, "status": status, "before_status": before_status} )

        return results

    def exposed_shutdown(self, token):
        self.validate_request(token)
        print("shutdown request received...")
        self.schedule_controller_exit()

    def exposed_cancel_run(self, token, run_names):
        '''
        run_names is a python list of ws/run-name entities.
        '''
        self.validate_request(token)
        results = []
        console.print("cancel_run: run_names=", run_names)

        if run_names == "all":
            results = self.cancel_all()
        else:
            # kill specific run(s)
            results = self.cancel_specified_runs(run_names)

        # send results as json text so that client is not tied to controller (which may be killed immediately after this call)
        results_json_text = json.dumps(results)
        return results_json_text

    def exposed_cancel_runs_by_property(self, token, prop_name, prop_value):
        self.validate_request(token)
        results = []
        console.print("cancel_runs_by_property: prop_name=", prop_name, ", prop_value=", prop_value)

        if prop_name == "username":
            results = self.cancel_all()
        else:
            # kill specific run(s)
            results = self.cancel_runs_by_property_core(prop_name, prop_value)

        # send results as json text so that client is not tied to controller (which may be killed immediately after this call)
        results_json_text = json.dumps(results)
        return results_json_text      

    def exposed_get_ip_addr(self, token):
        self.validate_request(token)
        addr = self.my_ip_addr
        if not addr:
            addr = pc_utils.get_ip_address()
        return addr

    def exposed_get_concurrent(self, token):
        self.validate_request(token)
        return self.concurrent

    def exposed_set_concurrent(self, token, value):
        self.validate_request(token)
        self.concurrent = value

    def get_running_names(self):
        with runs_lock:
            running_names = [run.run_name for run in self.runs.values() if run.status == "running"]
        return running_names

    def get_alive_names(self):
        with runs_lock:
            running_names = [run.run_name for run in self.runs.values() if run.status in ["running", "queued", "spawning"]]
        return running_names

# flat functions
def log_title(title, double=False):
    if double:
        line = "=========================================="
    else:
        line = "------------------------------------------"

    console.print(line)
    console.print(title)
    console.print(line)

def log_info(title, value):
    title = (title + ":").ljust(15)
    console.print("{} \t{}".format(title, value))

def print_env_vars():
    print("xt_controller - env vars:")
    keys = list(os.environ.keys())
    keys.sort()

    for key in keys:
        value = os.environ[key]
        if len(value) > 100:
            value = value[0:100] + "..."
        print("    {}: {}".format(key, value))

def debug_break():
    import ptvsd

    # 5678 is the default attach port in the VS Code debug configurations
    console.print("Waiting for debugger attach")
    ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    ptvsd.wait_for_attach()
    breakpoint()

def run(concurrent=1, my_ip_addr=None, multi_run_context_fn=constants.FN_MULTI_RUN_CONTEXT, multi_run_hold_open=False, 
        port=constants.CONTROLLER_PORT, is_aml=False):
    '''
    Runs the XT controller app - responsible for launch and control of all user ML apps for a
    local machine, remote machine, Azure VM, or Azure Batch VM.

    'max-runs' is the maximum number of jobs the controller will schedule to run simultaneously.

    'my_ip_addr' is the true IP address of the machine (as determined from the caller).

    'multi_run_context_fn' is used with Azure Batch - when specified, the controller
       should launch a single job, described in the context file (multi_run_context_fn), and when the job
       is finished, the controller should exit.
    '''

    #debug_break()
    #print_env_vars()
    
    box_secret = os.getenv("XT_BOX_SECRET")
    #console.print("XT_BOX_SECRET: ", box_secret)

    # create the controller
    service = XTController(concurrent, my_ip_addr, multi_run_context_fn, multi_run_hold_open, port, is_aml)

    if box_secret:
        # listen for requests from XT client

        philly_port = os.getenv("PHILLY_CONTAINER_PORT_RANGE_START")   # 14250
        if philly_port:
            port = int(philly_port) + 15

        # write server cert file JIT from env var values
        fn_server_cert = os.path.expanduser(constants.FN_SERVER_CERT)
        cert64 = os.getenv("XT_SERVER_CERT")
        server_cert_text = utils.base64_to_text(cert64)
        file_utils.write_text_file(fn_server_cert, server_cert_text)

        #print("create SSLAuthenticator with keyfile={}, certfile={}".format(fn_server_cert, fn_server_cert))
        authenticator = SSLAuthenticator(keyfile=fn_server_cert, certfile=fn_server_cert)  

        # launch the controller as an RYPC server
        t = ThreadedServer(service, port=port, authenticator=authenticator)
        t.start()

if __name__ == "__main__":      
    run()
