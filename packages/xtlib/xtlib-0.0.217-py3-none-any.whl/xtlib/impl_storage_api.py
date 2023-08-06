#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# impl_storage_api.py: API for commands
'''
This class gives API callers direct access to storage commands (without the command decorator functions in the call stack).
Eventually, all of the actual implementation of the impl_storage.py commands should be moved into here.

Every command implementation outer method is flagged with a "# COMMAND" command preceeding it.  Since most
commands display command output, these methods should include a "show_output" parameter to allow API callers
to supress all console output produced by the command code.
'''
import os
import sys
import time
import json
import psutil
import fnmatch
import datetime
import tempfile
import subprocess

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import capture 
from xtlib import pc_utils
from xtlib import constants
from xtlib import file_utils
from xtlib import store_utils
from xtlib import job_helper
from xtlib import run_helper
from xtlib import plot_builder
from xtlib import box_information

from xtlib.storage.store import Store
from xtlib.client import Client
from xtlib.console import console
from xtlib.cmd_core import CmdCore
from xtlib.impl_base import ImplBase
from xtlib.helpers import file_helper
from xtlib.backends import backend_aml 
from xtlib.cache_client import CacheClient
from xtlib.report_builder import ReportBuilder   
from xtlib.helpers.feedbackProgress import FeedbackProgress

class ImplStorageApi():
    def __init__(self, config, store):
        self.config = config
        self.store = store

    # COMMAND
    def import_workspace(self, input_file, new_workspace, job_prefix, overwrite, show_output=True):

        ext = file_utils.get_ext(input_file)
        if not ext:
            input_file += ".zip"

        with tempfile.TemporaryDirectory(prefix="import-") as temp_dir:
            self.import_workspace_core(temp_dir, input_file, new_workspace, job_prefix, overwrite, show_output=show_output)

        if show_output:
            console.print("  import completed")

    def import_workspace_core(self, temp_dir, input_file, new_workspace, job_prefix, overwrite, show_output):
        # unzip files and use contents.json
        file_helper.unzip_files(input_file, temp_dir)

        fn_contents = os.path.join(temp_dir, "contents.json")
        text = file_utils.read_text_file(fn_contents)
        contents = json.loads(text)

        workspaces = contents["workspaces"]
        if len(workspaces) > 1:
            errors.combo_error("import of archive files with multiple workspaces not yet supported")

        if not new_workspace:
            new_workspace = workspaces[0]

        archive_version = contents["archive_version"]
        if not archive_version in ["1"]:
            errors.general_error("unrecognized archive format: {}".format(archive_version))

        workspace = workspaces[0]
        jobs = contents["jobs"]

        if not new_workspace:
            new_workspace = workspace

        if self.store.does_workspace_exist(new_workspace):
            errors.combo_error("cannot import to an existing workspace name: {}".format(new_workspace))

        if show_output:
            console.print("\nimporting workspace {} ({} jobs) as {} from: {}".format(workspace, len(jobs), new_workspace, input_file))
        
        # create the new workspace
        self.store.create_workspace(new_workspace)

        # now, import each JOB
        max_run_seen = 0
        max_end_seen = 0

        for jc in jobs:
            prev_job_id = jc["job_id"]

            #prev_base = prev_job_id.split("_")[-1]
            #new_job_id = "{}_{}".format(job_prefix, prev_base)

            if store_utils.STORAGE_FORMAT == "1":
                new_job_id = job_prefix + "_" + prev_job_id
            else:
                new_job_id = prev_job_id

            if self.store.does_job_exist(new_workspace, new_job_id):
                if not overwrite:
                    errors.user_error("cannot import to existing job name: {} (use --overwrite to overwrite)".\
                        format(new_job_id))

                # for now, overwrite job "in place"
                # TODO: delete job from MONGO and STORAGE here
                        
            runs = jc["runs"] 

            if show_output:
                console.print("  importing: {} => {} ({} runs)".format(prev_job_id, new_job_id, len(runs)))

            # create MONGO JOB document
            mongo_job_fn = os.path.join(temp_dir, "mongo/jobs/{}/mongo_job.json".format(prev_job_id))
            self.import_job_mongo_document(mongo_job_fn, new_workspace, prev_job_id, new_job_id)

            # create STORAGE JOB blobs
            storage_job_path = os.path.join(temp_dir, "storage/jobs/{}".format(prev_job_id))
            self.import_job_storage_blobs(storage_job_path, new_workspace, prev_job_id, new_job_id)

            # for each run in job
            next_child_num = 0

            for run_name in runs:

                run_number = run_helper.get_parent_run_number(run_name)
                max_run_seen = max(max_run_seen, run_number)

                # copy MONGO RUN document
                mongo_run_fn = os.path.join(temp_dir, "mongo/workspaces/{}/runs/{}/mongo_run.json".format(workspace, run_name))

                # this will return the new run name (if version 1 import)
                new_run_name, end_id, next_child_num = self.import_run_mongo_document(archive_version, mongo_run_fn, workspace, new_workspace, prev_job_id,
                     new_job_id, run_name, next_child_num)

                max_end_seen = max(max_end_seen, end_id)
                
                # copy STORAGE RUN blobs
                storage_run_path = os.path.join(temp_dir, "storage/workspaces/{}/runs/{}".format(workspace, run_name))
                self.import_run_storage_blobs(storage_run_path, workspace, new_workspace, prev_job_id, new_job_id, new_run_name)

        # update MONGO counters for new workspace
        self.store.mongo.set_workspace_counters(new_workspace, 1+max_run_seen, 1+max_end_seen)

    def import_job_mongo_document(self, fn_mongo_job, new_workspace, prev_job_id, new_job_id):
        text = file_utils.read_text_file(fn_mongo_job)
        job = json.loads(text)

        # update job_id
        job["_id"] = new_job_id
        job["job_id"] = new_job_id
        job["job_num"] = job_helper.get_job_number(new_job_id)

        # update workspace
        job["ws_name"] = new_workspace

        # add to mongo
        self.store.mongo.update_job(job)

    def import_job_storage_blobs(self, storage_job_path, new_workspace, prev_job_id, new_job_id):

        # update files
        # for now, let's keep all storage files as they are

        # upload files as blobs
        self.upload(storage_job_path + "/**", ".", share=None, workspace=new_workspace, experiment=None, job=new_job_id, 
            run=None, feedback=False, show_output=False)

    def import_run_mongo_document(self, archive_version, mongo_run_fn, workspace, new_workspace, prev_job_id, new_job_id, run_name, next_child_num):
        text = file_utils.read_text_file(mongo_run_fn)
        run = json.loads(text)
        
        job_num = job_helper.get_job_number(new_job_id)

        # if archive_version == '1':
        #     if utils.safe_value(run, "is_child"):
        #         # CHILD run
        #         new_run_name = "run{}.{}".format(job_num, next_child_num)
        #         next_child_num += 1

        #     elif utils.safe_value(run, "is_parent"):
        #         # PARENT run
        #         node_index = utils.safe_value(run, "node_index", 0)
        #         new_run_name = "run{}_{}".format(job_num, node_index)

        #     else:
        #         # FLAT RUN
        #         new_run_name = "run{}".format(job_num)
        # else:
        #     new_run_name = run_name

        # we can preserve the run_name for both version 1 and version 2
        new_run_name = run_name

        # update run props
        run["job_id"] = new_job_id

        if store_utils.STORAGE_FORMAT == "1":
            run["ws"] = new_workspace
            if "ws_name" in run:
                del run["ws_name"]
        else:
            run["ws_name"] = new_workspace

        if run_name != new_run_name:
            run["run_name"] = new_run_name
            run["run_number"] = run_helper.get_run_number(new_run_name)

        # add to mongo
        self.store.mongo.update_run_info(new_workspace, new_run_name, run)

        end_id = utils.safe_value(run, "end_id")

        return new_run_name, end_id, next_child_num

    def import_run_storage_blobs(self, storage_run_path, workspace, new_workspace, prev_job_id, new_job_id, run_name):
        # update files
        # for now, let's keep all storage files as they are

        # upload files as blobs
        self.upload(storage_run_path + "/**", ".", share=None, workspace=new_workspace, experiment=None, job=new_job_id, 
            run=run_name, feedback=False, show_output=False)

    # COMMAND
    def export_workspace(self, output_file, workspace, tags_all, tags_any, jobs, experiment, show_output=True, 
        response=None):

        export = True

        ext = file_utils.get_ext(output_file)
        if not ext:
            output_file += ".zip"    # xt export file

        if os.path.exists(output_file):
            answer = pc_utils.input_response("'{}' already exists; OK to delete? (y/n): ".format(output_file), response)
            if answer != "y":
                export = False

        if export:
            if os.path.exists(output_file):
                os.remove(output_file)
            
            with tempfile.TemporaryDirectory(prefix="import-") as temp_dir:
                self.export_workspace_core(temp_dir, output_file, workspace, tags_all, tags_any, jobs, experiment, 
                    show_output=show_output)

            if show_output:
                console.print("  export completed")
        else:
            console.print("  export cancelled")

    def export_workspace_core(self, temp_dir, output_file, workspace, tags_all, tags_any, jobs, experiment, show_output):

        # get specified jobs from workspace (by job name, or by workspace name)
        args = {"job_list": jobs, "tags_all": tags_all, "tags_any": tags_any, "workspace": workspace, "all": True,
            "target": None, "available": None, "experiment": experiment, "service_type": None, 
            "username": None, "filter": None, "columns": ["job", "workspace"]}

        job_list, _, _, _, _ = job_helper.get_list_jobs_records(self.store, self.config, args)

        if show_output:
            console.print("\nexporting workspace {} ({} jobs) to: {}".format(workspace, len(job_list), output_file))

        # build a table of contents structure describing this archive
        archive_version = "1"
        build = constants.BUILD
        username = self.config.get("general", "username")
        dt = datetime.datetime.now()
        dt_text = str(dt)
        storage_name = self.store.get_name()
        mongo_name = self.store.mongo.get_service_name()
        
        workspaces = []
        jobs = []
        contents = {"user": username, "export_date": dt_text, "archive_version": archive_version, "xt_build": build, 
            "storage_format": store_utils.STORAGE_FORMAT, "storage": storage_name, "mongo": mongo_name, 
            "workspaces": workspaces, "jobs": jobs }

        first_job = None
        first_ws = None

        # for each job in workspace
        for jr in job_list:
            job_id = jr["job"]
            job_ws = jr["workspace"] 

            mongo_runs = self.store.mongo.get_info_for_runs(job_ws, {"job_id": job_id}, None)
            run_names = [mr["run_name"] for mr in mongo_runs]

            if show_output:
                console.print("  exporting: {} ({} runs)".format(job_id, len(mongo_runs)))

            job_content = {"job_id": job_id, "workspace": job_ws, "runs": run_names}
            jobs.append(job_content)

            if first_job is None:
                first_job = job_id
                first_ws = job_ws

                workspaces.append(job_ws)

            if job_ws != first_ws:
                errors.combo_error("can only export jobs from a single workspace (job {} has ws={}, job {} as ws={})". \
                    format(first_job, first_ws, job_id, job_ws))

            # copy MONGO JOB document
            temp_mongo_path = os.path.join(temp_dir, "mongo/jobs/{}".format(job_id))
            self.export_job_mongo_document(first_ws, job_id, temp_mongo_path)

            # copy STORAGE JOB blobs
            temp_store_path = os.path.join(temp_dir, "storage/jobs/{}".format(job_id))
            self.export_job_storage_blobs(first_ws, job_id, temp_store_path)

            # for each run in job
            for mr in mongo_runs:

                # copy MONGO RUN document
                run_name = mr["run_name"]
                temp_mongo_path = os.path.join(temp_dir, "mongo/workspaces/{}/runs/{}".format(job_ws, run_name))
                self.export_run_mongo_document(mr, temp_mongo_path)

                # copy STORAGE RUN blobs
                temp_store_path = os.path.join(temp_dir, "storage/workspaces/{}/runs/{}".format(job_ws, run_name))
                self.export_run_storage_blobs(job_ws, run_name, temp_store_path)

        # add contents
        text = json.dumps(contents, indent=4)
        fn_contents = os.path.join(temp_dir, "contents.json")
        file_utils.write_text_file(fn_contents, text)

        # create zip file
        filenames, local_path = file_utils.get_local_filenames(temp_dir + "/**")
        prefix_len = 1 + len(temp_dir)
        file_helper.zip_up_filenames(output_file, filenames, compress=True, remove_prefix_len=prefix_len)

    def export_job_mongo_document(self, ws_name, job_id, temp_mongo_path):
        record = job_helper.get_job_record(self.store, ws_name, job_id)
        text = json.dumps(record)

        fn = os.path.join(temp_mongo_path, "mongo_job.json")
        file_utils.write_text_file(fn, text)

    def export_run_mongo_document(self, record, temp_mongo_path):
        text = json.dumps(record)
        fn = os.path.join(temp_mongo_path, "mongo_run.json")
        file_utils.write_text_file(fn, text)

    def export_job_storage_blobs(self, first_ws, job_id, temp_store_path):
        # copy each storage file
        file_utils.ensure_dir_exists(temp_store_path)

        #fs = self.store.job_files(job_id, use_blobs=True)
        self.download("**", temp_store_path, share=None, workspace=first_ws, experiment=None, job=job_id, 
            run=None, feedback=False, snapshot=True, show_output=False)

    def export_run_storage_blobs(self, workspace, run_id, temp_store_path):
        # copy each storage file
        file_utils.ensure_dir_exists(temp_store_path)

        #fs = self.store.job_files(job_id, use_blobs=True)
        self.download("**", temp_store_path, share=None, workspace=workspace, experiment=None, job=None, 
            run=run_id, feedback=False, snapshot=True, show_output=False)

    # COMMAND
    def download(self, store_path, local_path, share, workspace, experiment, job, run, feedback, snapshot, show_output=True):

        use_blobs = True 
        use_multi = True     # default until we test if store_path exists as a file/blob
        download_count = 0

        fs = self.create_file_accessor(use_blobs, share, workspace, experiment, job, run)

        # test for existance of store_path as a blob/file
        if not "*" in store_path and not "?" in store_path:
            if fs.does_file_exist(store_path):
                use_multi = False

        if local_path:
            # exapnd ~/ in front of local path
            local_path = os.path.expanduser(local_path)
        else:
            # path not specified for local 
            if use_multi:
                local_path = "."
            else:
                local_path = "./" + os.path.basename(store_path)

        uri = fs.get_uri(store_path)

        # default store folder to recursive
        if use_multi and not "*" in store_path and not "?" in store_path:
            store_path += "/**"

        use_snapshot = snapshot
        
        feedback_progress = FeedbackProgress(feedback, show_output)
        progress_callback = feedback_progress.progress if feedback else None

        if use_multi:
            # download MULTI blobs/files

            what = "blobs" if use_blobs else "files"
            single_what = what[0:-1]

            if show_output:
                console.print("collecting {} names from: {}...".format(single_what, uri), end="")

            _, blob_names = fs.get_filenames(store_path, full_paths=False)

            if show_output:
                console.print()

            if len(blob_names) == 0:
                console.print("no matching {} found in: {}".format(what, uri))
                return 0
            elif len(blob_names) == 1:
                what = "blob" if use_blobs else "file"

            if show_output:
                console.print("\ndownloading {} {}...:".format(len(blob_names), what))

            file_utils.ensure_dir_exists(local_path)
            max_name_len = max([len(local_path + "/" + name) for name in blob_names])
            name_width =  1 + max_name_len
            #console.print("max_name_len=", max_name_len, ", name_width=", name_width)

            for f, bn in enumerate(blob_names):
                dest_fn = file_utils.fix_slashes(local_path + "/" + bn)

                if show_output:
                    file_msg = "file {}/{}".format(1+f, len(blob_names))
                    console.print("  {2:}: {1:<{0:}} ".format(name_width, dest_fn + ":", file_msg), end="", flush=True)

                feedback_progress.start()
                full_bn = uri + "/" + bn if uri else bn
                fs.download_file(full_bn, dest_fn, progress_callback=progress_callback, use_snapshot=use_snapshot)
                feedback_progress.end()

                download_count += 1
        else:
            # download SINGLE blobs/files
            what = "blob" if use_blobs else "file"

            if not fs.does_file_exist(store_path):
                errors.store_error("{} not found: {}".format(what, uri))

            local_path = file_utils.fix_slashes(local_path)

            if show_output:
                console.print("\nfrom {}, downloading {}:".format(uri, what))
                console.print("  {}:    ".format(local_path), end="", flush=True)
    
            feedback_progress.start()
            fs.download_file(store_path, local_path, progress_callback=progress_callback, use_snapshot=use_snapshot)
            feedback_progress.end()

            download_count += 1

        return download_count

    # COMMAND
    def upload(self, local_path, store_path, share, workspace, experiment, job, run, feedback, show_output=True):

        use_blobs = True
        use_multi = True
        upload_count = 0

        # exapnd ~/ in front of local path
        local_path = os.path.expanduser(local_path)

        if os.path.exists(local_path) and os.path.isfile(local_path):
            use_multi = False

        #console.print("local_path=", local_path)

        # if directory, default to copy nested
        if os.path.isdir(local_path):
            local_path += "/**"
            use_multi = True

        if not store_path or store_path == ".":
            if not use_multi:
                # single file defaults to the base name of the local file
                store_path = os.path.basename(local_path)
            else:
                store_path = "."

        fs = self.create_file_accessor(use_blobs, share, workspace, experiment, job, run)
        uri = fs.get_uri(store_path)
        actual_path, _ = file_utils.split_wc_path(local_path)

        actual_path = file_utils.relative_path(actual_path)
        actual_path = file_utils.fix_slashes(actual_path)

        if not os.path.exists(actual_path):
            errors.env_error("Cannot find the local file/folder: {}".format(actual_path))

        feedback_progress = FeedbackProgress(feedback, show_output)
        progress_callback = feedback_progress.progress if feedback else None

        if use_multi:
            # upload MULTIPLE files/blobs
            file_names, local_path = file_utils.get_local_filenames(local_path)
            what = "blobs" if use_blobs else "files"

            if len(file_names) == 0:
                if show_output:
                    console.print("no matching files found in: {}".format(what, actual_path))
                return
            elif len(file_names) == 1:
                what = "blob" if use_blobs else "file"

            if show_output:
                console.print("\nto {}, uploading {} {}:".format(uri, len(file_names), what))

            #file_utils.ensure_dir_exists(local_path)
            max_name_len = max([len(name) for name in file_names])
            name_width =  1 + max_name_len
            #console.print("max_name_len=", max_name_len, ", name_width=", name_width)

            for f, fn in enumerate(file_names):
                blob_path = self.make_dest_store_path(local_path, fn, store_path)
                actual_fn = file_utils.fix_slashes(fn)

                if show_output:
                    file_msg = "file {}/{}".format(1+f, len(file_names))
                    console.print("  {2:}: {1:<{0:}} ".format(name_width, actual_fn + ":", file_msg), end="", flush=True)

                feedback_progress.start()
                fs.upload_file(blob_path, actual_fn, progress_callback=progress_callback)
                feedback_progress.end()

                upload_count += 1
        else:
            # upload SINGLE file/blob
            what = "blob" if use_blobs else "file"

            if show_output:
                console.print("\nto: {}, uploading {}:".format(uri, what))

            blob_name = os.path.basename(local_path)
            local_path = file_utils.fix_slashes(local_path)

            if show_output:
                #console.print("store_path=", store_path, ", local_path=", local_path)
                console.print("  {}:    ".format(local_path), end="", flush=True)

            feedback_progress.start()
            fs.upload_file(store_path, local_path, progress_callback=progress_callback)
            feedback_progress.end()

            upload_count += 1

        return upload_count

    def create_file_accessor(self, use_blobs, share, ws_name, exper_name, job_name, run_name):
        # use --experiment option only here
        if share:
            ws_name = store_utils.make_share_name(share)
            fs = self.store.root_files(ws_name, use_blobs=use_blobs)
        elif run_name:
            fs = self.store.run_files(ws_name, run_name, use_blobs=use_blobs)
        elif job_name:
            fs = self.store.job_files(ws_name, job_name, use_blobs=use_blobs)
        elif exper_name:
            fs = self.store.experiment_files(ws_name, exper_name, use_blobs=use_blobs)
        else:
            fs = self.store.workspace_files(ws_name, use_blobs=use_blobs)

        return fs

    def make_dest_store_path(self, source_basepath, source_fn, dest_rel):
        ''' combine the relative part of source_path with dest_rel
        '''
        slen = len(source_basepath)
        source_rel = source_fn[1+slen:] 

        if dest_rel == ".":
            dest_fn = source_rel
        else:
            dest_fn = dest_rel + "/" + source_rel

        return dest_fn

    def log_report(self, client, target, records, view_raw, export, event, 
            data_name, data_value):

        console.print("log for {}:\n".format(target))

        if event:
            # filter records by specified event
            records = [record for record in records if "event" in record and record["event"] == event]

        if data_name:
            if data_value:
                # filter records that define data_name == data_value
                records = [record for record in records if "data" in record and data_name in record["data"] \
                    and record["data"][data_name] == data_value ]
            else:
                # filter records that define data_name
                records = [record for record in records if "data" in record and data_name in record["data"] ]
                
        if view_raw:
            for record in records:
                console.print(record)
        else:
            builder = ReportBuilder(self.config, self.store, client)

            args = {}
            args["columns"] = ["time", "event", "data"]
            args["export"] = export
            args["max_width"] = 80

            report_type = "run-reports" if run_helper.is_well_formed_run_name(target) else "job-reports"

            #builder.build_formatted_table(records, [], col_list=col_list)

            lines, row_count, was_exported = builder.build_report(records, report_type, args)

            # remove trailing blank lines
            while lines and not lines[-1]:
                lines = lines[:-1]

            if lines:
                for line in lines:
                    console.print(line)        
            else:
                console.print("no matching records found")

