#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# store_utils.py: store-related helper functions
'''
NOTE: when we are running with version 1 storage, we dynamically 
REPLACE ALL OF THE BELOW with their version 1 equivalents 
(functions and properties).
'''
from xtlib import constants

def make_share_name(name):
    return "00-share-{}".format(name)

def is_share_name(name):
    return isinstance(name, str) and name.startswith("00-share-")

def get_run_path(job_id, run_name):
    path = "jobs/{}/runs/{}".format(job_id, run_name)
    return path

def get_jobs_container(ws_name):
    return ws_name    

def make_id(ws_name, obj_name):
    if "/" in obj_name:
        id = obj_name
    else:
        id = ws_name + "/" + obj_name

    return id

def simplify_id(record):
    if "_id" in record:
        _id = record["_id"]
        if "/" in _id:
            _id = _id.split("/")[-1]
            record["_id"] = _id

def simplify_records_id(records):
    if records:
        for r in records:
            simplify_id(r)

MODELS_STORE_ROOT = make_share_name("models")
DATA_STORE_ROOT = make_share_name("data")
STORAGE_FORMAT = constants.STORAGE_FORMAT

