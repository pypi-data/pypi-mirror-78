#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# job_helper.py: functions needed for processing job-related information
import json
import time
import fnmatch

from .console import console
from .report_builder import ReportBuilder   

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import file_utils

def is_job_id(name):
    # compatible with version 1 (prefix-jobNNNN) and version 2 (jobNNNN)
    return "job" in name.lower()

def expand_job_list(store, mongo, workspace, name_list, can_mix=True):
    '''
    parse jobs, expand job ranges
    '''
    if name_list:
        first_name = name_list[0]
        if len(name_list)==1 and file_utils.has_wildcards(first_name):
            # match wildcard to all job names in workspace
            filter_dict = {}

            if workspace:
                filter_dict["ws_name"] = workspace

            all_names = mongo.get_job_names(filter_dict)
            job_list = [jn for jn in all_names if fnmatch.fnmatch(jn, first_name)]
        else:            
            job_list, actual_ws = parse_job_list(store, workspace, name_list, can_mix=can_mix)
    else:
        actual_ws = workspace
        job_list = name_list

    return job_list, actual_ws

def set_job_tags(store, mongo, name_list, tag_list, workspace, fd, clear):
    job_list, actual_ws = expand_job_list(store, mongo, workspace, name_list, can_mix=True)

    if job_list:
        for job in job_list:
            mongo.update_job_info(workspace, job, fd, clear=clear, upsert=False)   
    else:
        console.print("no matching jobs found")


def list_job_tags(store, mongo, ws_name, name_list, tag_list):
    job_list, actual_ws = expand_job_list(store, mongo, ws_name, name_list, can_mix=True)

    if job_list:
        filter_dict = {"job_id": {"$in": job_list}}
        fields_dict = {"tags": 1}

        records = mongo.get_info_for_jobs(ws_name, filter_dict, fields_dict)
        for record in records:
            job = record["_id"]
            console.print("{}:".format(job))

            if "tags" in record:
                tags = record["tags"] 
                tag_names = list(tags.keys())
                tag_names.sort()

                for tag in tag_names:
                    if tag_list and not tag in tag_list:
                        continue
                    console.print("  {}: {}".format(tag, tags[tag]))
    else:
        console.print("no matching jobs found")

def build_filter_part(fd, args, arg_name, store_name):
    value = utils.safe_value(args, arg_name)
    if value:
        if isinstance(value, list):
            fd[store_name] = {"$in": value}
        else:
            fd[store_name] = value

def build_job_filter_dict(job_list, user_to_actual, builder, workspace, args):
    fd = {}
    option_filters = ["experiment", "target", "service_type", "username", "status"]   # "application"

    if job_list:
        # filter by specified job names
        fd["_id"] = {"$in": job_list}

    # filter by workspace
    if workspace:
        fd["ws_name"] = workspace
        
    # filter by specified options
    for name in option_filters:
        build_filter_part(fd, args, name, user_to_actual[name])

    # filter by filter_list
    filter_exp_list = args["filter"]
    if filter_exp_list:
        builder.process_filter_list(fd, filter_exp_list, user_to_actual)

    # filter by tags_all
    tags_all = args["tags_all"]
    if tags_all:
        for tag in tags_all:
            fd["tags." + tag] = {"$exists": True}

    # filter by tags_any
    tags_any = args["tags_any"]
    if tags_any:
        fany_list = []
        for tag in tags_any:
            f = {"tags." + tag: {"$exists": True}}
            fany_list.append(f)

        # or all of fany conditions together
        fd["$or"] = fany_list

    return fd

def get_job_property_dicts():
    # user-friendly property names for jobs
    user_to_actual = {"cluster": "pool_info.cluster", "docker": "pool_info.environment", "experiment": "exper_name",
        "hold": "hold", "job": "job_id","job_num": "job_num", "low_pri": "pool_info.low-pri", 
        "nodes": "pool_info.nodes", "primary_metric": "primary_metric", "queue": "pool_info.queue", 
        "repeat": "repeat", "search": "search_type", "service_type": "pool_info.service", 
        "sku": "pool_info.sku", "runs": "run_count", "search_style": "search_style", "started": "started", "target": "compute", "username": "username", 
        "vc": "pool_info.vc", "vm_size": "pool_info.vm-size", "workspace": "ws_name",  
        "tags": "tags",

        # dynamic properties (get updated at various stages of job)
        "status": "job_status", "running_nodes": "running_nodes", 
        "running_runs": "running_runs", "error_runs": "error_runs", "completed_runs": "completed_runs",
        "total_runs": "total_runs"
        }

    std_cols_desc = {
        "cluster": "the Philly Cluster that the job ran on",
        "docker": "the Docker environment specified for this job",
        "experiment": "the experiment associated with the job",
        "hold": "if the Azure Batch pool for this job was requested to be held open after runs were completed",
        "job": "the job name",
        "job_num": "the sort compatible, numeric portion of the job_id",
        "low_pri": "if the nodes requested for this job were specified as preemptable",
        "nodes": "the number of compute nodes requested for this job",
        "primary_metric": "the name of the metric used for hyperparameter searching",
        "queue": "the Philly queue that the job was submitted to",
        "repeat": "the repeat count specified for the job",
        "runs": "the total number of runs for the job",
        "search": "the type of hyperparameter search requested",
        "search_style": "describes how search is being accomplished (one of: static, dynamic, multi, repeat, single)",
        "service_type": "the service type of the target",
        "sku": "the machine type requested for this job",
        "started": "the datetime when the job was started",
        "target": "the name of the compute target the job was submitted to",
        "username": "the login name of the user who submitted the job",
        "vc": "the Philly Virtual Cluster that the job ran on",
        "vm_size": "the Azure Batch machine size requested for this job",
        "workspace": "the workspace associated with the job",

        # dynamic properties (get updated at various stages of job)
        "job_status": "one of: submitted, running, completed",
        "running_nodes": "the number of nodes in the running state",
        "running_runs": "the number of this job's runs that are current running",
        "completed_runs": "the number of runs that have completed (with or without errors)",
        "error_runs": "the number of runs that have terminated with an error",
        "total_runs": "the total number of runs specified for the job",
    }

    return user_to_actual, std_cols_desc

def get_list_jobs_records(store, config, args):
    job_list = args["job_list"]
    pool = args["target"]

    if job_list:
        # only use workspace if it was explictly set  
        workspace = None   
        explict = qfe.get_explicit_options()
        if "workspace" in explict:
            workspace = explict["workspace"]
    else:
        workspace = args["workspace"]

    if workspace:
        store.ensure_workspace_exists(workspace, flag_as_error=True)

    # get info about job properties
    user_to_actual, std_cols_desc = get_job_property_dicts()        
    actual_to_user = {value: key for key, value in user_to_actual.items()}

    builder = ReportBuilder(config, store, client=None)

    # get list of specified jobs
    mongo = store.get_mongo()
    job_list, actual_ws = expand_job_list(store, mongo, workspace, job_list)

    # build a filter dict for all specified filters
    filter_dict = build_job_filter_dict(job_list, user_to_actual, builder, workspace, args)

    # get the mongo records for the matching JOBS
    #console.print("gathering job data...", flush=True)
    records, using_default_last, last = builder.get_mongo_records(mongo, filter_dict, workspace, "jobs", actual_to_user, args=args)
    return records, using_default_last, last, user_to_actual, builder

def list_jobs(store, config, args):
    available = args["available"]

    records, using_default_last, last, user_to_actual, builder \
        = get_list_jobs_records(store, config, args)

    if available:
        std_cols = list(user_to_actual.keys())
        tag_cols = extract_tag_cols(records)
        lines = builder.available_cols_report("job", std_cols, std_cols_desc, tags_list=tag_cols)

        for line in lines:
            console.print(line)
    else:            
        avail_list = list(user_to_actual.keys())
        lines, row_count, was_exported = builder.build_report(records, report_type="job-reports", args=args)

        if was_exported:
            console.print("")

            for line in lines:
                console.print(line)
        else:
            # console.print the report
            if row_count > 0:
                console.print("")

                for line in lines:
                    console.print(line)

                if row_count > 1:
                    if using_default_last:
                        console.print("total jobs listed: {} (defaulted to --last={})".format(row_count, last))
                    else:
                        console.print("total jobs listed: {}".format(row_count))
            else:
                console.print("no matching jobs found")


def extract_tag_cols(records):
    tag_dict = {}

    for record in records:
        if "tags" in record:
            tags = record["tags"]
            for tag in tags.keys():
                tag_dict[tag] = 1

    return list(tag_dict.keys())

def validate_job_name_with_ws(store, ws_name, job_name, validate):
    job_name = job_name.lower()
    if not is_job_id(job_name):
        return errors.syntax_error("Illegal job name: {}".format(job_name))

    exists = store.does_job_exist(ws_name, job_name)
    if validate and not exists:
        errors.store_error("job '{}' does not exist in workspace '{}'".format(job_name, ws_name))

def parse_job_helper(store, job, job_list, actual_ws, validate=True, can_mix=True):

    if not can_mix:
        validate_job_name_with_ws(store, actual_ws, job, validate)

    job_list.append(job)
    return actual_ws

def get_job_number(job):
    if not is_job_id(job):
        errors.syntax_error("illegal job name, must start with 'job'")

    # allow for import prefixes
    part = job.split("_")[-1]  
    if part.startswith("job"):
        part = part[3:] 
    return int(part)

def parse_job_list(store, workspace, jobs, can_mix=False):
    actual_ws = workspace
    job_list = []

    if jobs:
        for job in jobs:
            job = job.strip()

            if "-" in job:
                # range specified
                low, high = job.split("-")
                low = get_job_number(low)
                high = get_job_number(high)

                for jx in range(low, high+1):
                    jxx = "job" + str(jx)
                    actual_ws = parse_job_helper(store, jxx, job_list, actual_ws, False, can_mix=can_mix)
            else:
                actual_ws = parse_job_helper(store, job, job_list, actual_ws, can_mix=can_mix)
        
    #console.print("actual_ws=", actual_ws)
    return job_list, actual_ws

def validate_job_name(job_id):
    if job_id:
        safe_job_id = str(job_id)
        if not is_job_id(safe_job_id):
            errors.syntax_error("job id must start with 'job': " + safe_job_id)

def get_num_from_job_id(job_id):
    # job341
    return job_id[3:]

def get_client_cs(core, ws_name, job_id, node_index):
    '''
    instantiate the backend service that owns the specified job node and 
    request it's client connection string
    '''
    cs = None
    box_secret = None

    filter = {"_id": job_id}
    jobs = core.store.mongo.get_info_for_jobs(ws_name, filter, None)
    if not jobs:
        errors.store_error("unknown job_id: {}".format(job_id))

    job = jobs[0]
    node_id = utils.node_id(node_index)

    compute = utils.safe_value(job, "compute")
    secrets_by_node = utils.safe_value(job, "secrets_by_node")
    if not secrets_by_node:
        errors.store_error("unknown node_index={} for job={}".format(node_index, job_id))

    box_secret = utils.safe_value(secrets_by_node, node_id)

    service_info_by_node = utils.safe_value(job, "service_info_by_node")
    node_info = utils.safe_value(service_info_by_node, node_id)

    if compute and node_info:
        backend = core.create_backend(compute)
        cs = backend.get_client_cs(node_info)

    cs_plus = {"cs": cs, "box_secret": box_secret, "job": job}
    return cs_plus

def get_job_records(store, workspace, job_names, fields_dict=None):
    ''' return job records for specified job names'''

    mongo = store.get_mongo()

    filter_dict = {}
    filter_dict["job_id"] = {"$in": job_names}

    job_records = mongo.get_info_for_jobs(workspace, filter_dict, fields_dict)

    return job_records
    
def get_job_record(store, workspace, job_id, fields_dict = None):
    job_records = get_job_records(store, workspace, [job_id], fields_dict)
    if not job_records:
        errors.store_error("job {} does not exist".format(job_id))
    jr = job_records[0]
    return jr
    
def get_job_info_with_backend(store, core, workspace, job_id, node_index):
    
    # FYI: getting job record from storage: 2.75 secs, from mongo: 2.39 secs (mongo slightly faster)
    job_info = get_job_record(store, workspace, job_id, {"pool_info": 1, "username": 1, "service_info_by_node": 1})

    pool_info = job_info["pool_info"]
    target = pool_info["name"]
    username = job_info["username"]
    backend = core.create_backend(target, compute_def=pool_info, username=username)

    if not "service_info_by_node" in job_info:
        # mongo v2 requires a separate call for this
        service_info_by_node = store.mongo.get_service_info_by_node(workspace, job_id)
        job_info["service_info_by_node"] = service_info_by_node

    return backend, job_info

def get_service_node_info_with_backend(store, core, workspace, job_id, node_index):
    
    backend, job_info = get_job_info_with_backend(store, core, workspace, job_id)
    service_info_by_node = job_info["service_info_by_node"]  

    node_id = utils.node_id(node_index)
    service_node_info = service_info_by_node[node_id]

    return service_node_info, backend

def get_service_job_info(store, core, ws_name, job_id):

    # get JOB_INFO 
    job_info = get_job_record(store, ws_name, job_id, {"pool_info": 1, "service_job_info": 1, "service_info_by_node": 1})
    service_job_info = job_info["service_job_info"]
    service_info_by_node = job_info["service_info_by_node"]

    # # get SERVICE_INFO_BY_NODE
    # service_info_by_node = store.mongo.get_service_info_by_node(ws_name, job_id)
    # job_info["job_info"] = job_info

    target = job_info["pool_info"]["name"]
    backend = core.create_backend(target)

    return service_job_info, service_info_by_node, backend

# helper
def download_logs_from_storage(ws_name: str, store, items: [str], job_id: str, node_index: int, store_path: str,
        dest_dir: str):

    job_path = "node-{}/{}".format(node_index, store_path)
    new_items = store.download_files_from_job(ws_name, job_id, job_path, dest_dir)

    for ni in new_items:
        items.append(ni)

