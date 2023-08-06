#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# mongo_v2.py: new XT API for talking to mongo about RUN and JOB data
import os
import uuid
import arrow
import json
import time
import numpy as np
import pymongo
from pymongo import MongoClient

from xtlib import utils
from xtlib import errors
from xtlib import console
from xtlib import constants

DEFAULT_DB = "__default__"
MONGO_INFO = "__mongo_info__"
WORKSPACES = "__workspaces__"

class MongoDB2():
    '''
    XT mongoDB format v2:
        - STORAGE hierarchy: storage-service/workspace/job/run/child-run
            - job names are allocated names within a workspace
            - run names share the job name: "run47.0" is first child run of job47)

        - DB hierarchy: mongo-service/database/workspace/collections
            - each workspace can be its own mongoDB database, or part of the DB_DEFAULT database
            
            - each workspace consists of:
                - 5 run collections
                    - run_info          (write once, _id: ws/run_name)
                    - run_stats         (high update, _id: ws/run_name)
                    - hparams           (write once, _id: ws/run_name)
                    - metrics           (high update, _id: ws/run_name)
                    - log_records       (write once, _id: GUID)

                - 5 job collections:
                    - job_info          (write once, _id: ws/job_name)
                    - job_stats         (high update, _id: ws/job_name)
                    - child_runs        (medium update, _id: ws/job_name/run_index, key: ws/job_name/node_index)
                    - connect_info      (write once, _id: ws/job_name/node_index)
                    - service_info_by_node      (write once, _id: ws/job_name)

            - workspace-independent collections (always in DB_DEFAULT database):
                - __mongo_info__   (contains mongo format info and paired storage name, "_id": 1)
                - __workspaces__   (record for each workspace, _id: ws_name)

            - each of the above collections is shared (for Cosmos DB versions):
                - shard key is always the _id (unique to each document of the collection)
                - whenever possible, we use a predictable _id (since updates must specify the shard key)
    '''
    
    def __init__(self, mongo_cs, db_name=None, ws_name=None, run_cache_dir=None, direct_mode=True):

        '''
        direct_mode: means we update data in mongo directly (from XT or the run) (vs. storge tracking)
        '''
        if not db_name:
            db_name = DEFAULT_DB

        self.direct_mode = direct_mode
        self.is_cosmos = not "localhost" in mongo_cs
        self.db_name = db_name
        self.call_stats = {}
        self.retry_errors = 0
        self.mongo_conn_str = mongo_cs
        self.round_trip_count = 0         # stats for last query
        self.name = "mongo_v2"

        # controls for mongo stats and logging
        self.update_job_stats = True
        self.update_run_stats = True
        self.add_log_records = True

        self.mongo_client = MongoClient(mongo_cs)

        self.ws_name = ws_name
        if ws_name:
            db_name = self.create_workspace_if_needed(ws_name, db_name)

        # update database for workspace
        self.mongo_db = self.mongo_client[db_name]    

        self.run_cache_dir = os.path.expanduser(run_cache_dir) if run_cache_dir else None

    #---- UTILS ----

    def get_service_name(self):
        _, rest = self.mongo_conn_str.split("//", 1)
        if ":" in rest:
            name, _ = rest.split(":", 1)
        else:
            name, _ = rest.split("/", 1)
        return name

    def get_db(self, ws_name=None, db_name=None):
        if not db_name:
            assert bool(ws_name)

            if self.ws_name == ws_name:
                db_name = self.db_name
            else:
                # look it up for the ws_name
                records = self.get_workspace_infos({"_id": ws_name})
                if not records:
                    errors.service_error("workspace not found: {}".format(ws_name))

                db_name = utils.safe_cursor_value(records, "db_name")
                if not db_name:
                    db_name = DEFAULT_DB
                    
                self.db_name = db_name
                self.ws_name = ws_name

        return self.mongo_client[db_name]

    def get_mongo_info(self):
        dbx = self.get_db(db_name=DEFAULT_DB)

        records = self.mongo_with_retries("get_mongo_info", lambda: dbx[MONGO_INFO].find({"_id": 1}, None), return_records=True)
        record = records[0] if records and len(records) else None
        return record

    def set_mongo_info(self, info): 
        dbx = self.get_db(db_name=DEFAULT_DB)

        self.mongo_with_retries("set_mongo_info", lambda: dbx[MONGO_INFO].update( {"_id": 1}, info, upsert=True) )

    def delete_workspace_if_needed(self, ws_name):
        '''
        delete:
           1. entries for specified workspace from our 10 run/job collections
           2. __workspaces__ entry for workspace
        '''

        # this line will raise an exception if the ws_name is not known to mongo
        dbx = self.get_db(ws_name)

        # delete RUN collections
        self.delete_from_collection(dbx, ws_name, "run_info", "_id")
        self.delete_from_collection(dbx, ws_name, "hparams", "_id")
        self.delete_from_collection(dbx, ws_name, "metrics", "_id")
        self.delete_from_collection(dbx, ws_name, "log_records", "_id")
        self.delete_from_collection(dbx, ws_name, "run_stats", "_id")

        # delete JOB collections
        self.delete_from_collection(dbx, ws_name, "job_info", "_id")
        self.delete_from_collection(dbx, ws_name, "job_stats", "_id")
        self.delete_from_collection(dbx, ws_name, "connect_info", "_id")
        self.delete_from_collection(dbx, ws_name, "service_info_by_node", "_id")
        self.delete_from_collection(dbx, ws_name, "child_runs", "_id")

        dbx_default = self.get_db(db_name=DEFAULT_DB)
        self.mongo_with_retries("delete_workspace_if_needed", lambda: dbx_default[WORKSPACES].delete_one( {"_id": ws_name} ))

        return True

    def delete_from_collection(self, dbx, ws_name, collection_name, shard_key=None):
        '''
        if the collection is sharded, we need to query to get shard key values before
        we can delete.
        '''
        if shard_key and self.is_cosmos:
            # query to get shard keys for matching records
            records = self.mongo_with_retries("delete_from_collection", lambda: dbx[collection_name].find( 
                {"ws_name": ws_name}, {shard_key: 1} ), return_records=True)
            shard_keys = [r[shard_key] for r in records]

            # now delete using shard_keys
            if shard_keys:

                # Cosmos DB doesn't support delete_many with shard keys, so we work around issue with bluk_delete
                #self.mongo_with_retries("delete_from_collection", lambda: dbx[collection_name].delete_many( {shard_key: {"$in": shard_keys}} ))
                self.limited_bulk_delete(dbx, collection_name, shard_keys)
        else:
            # easy case; just delete by ws_name
            self.mongo_with_retries("delete_from_collection", lambda: dbx[collection_name].delete_many( {"ws_name": ws_name} ))

    def limited_bulk_delete(self, dbx, collection_name, ids):
        max_deletes = 25
        index = 0

        while index < len(ids):
            id_batch = ids[index:index+max_deletes]

            delete_cmds = []
            for id in id_batch:
                cmd = pymongo.operations.DeleteOne( {"_id": id} )
                delete_cmds.append(cmd)

            self.mongo_with_retries("limited_bulk_delete", lambda: dbx[collection_name].bulk_write( delete_cmds ))

            index += len(id_batch)

    def create_workspace_if_needed(self, ws_name, db_name=None):
        fd = {"_id": ws_name}

        # workspace definitions are stored in DEFAULT_DB
        if not db_name:
            db_name = DEFAULT_DB

        dbx = self.get_db(db_name=DEFAULT_DB)
        records = self.mongo_with_retries("create_workspace_if_needed", lambda: dbx[WORKSPACES].find(fd, {"db_name": 1}), return_records=True)

        if records:
            # workspace already exists
            db_name = utils.safe_cursor_value(records, "db_name")
        else:
            # workspace not found

            # add workspace document
            dd = {"_id": ws_name, "db_name": db_name, "next_job_number": 1, "next_end_id": 1}
            self.update_sys_collection(WORKSPACES, ws_name, dd, dbx=dbx)

            if self.is_cosmos:
                self.create_workspace_collections_if_needed(db_name)

        return db_name

    def set_workspace_counters(self, ws_name, next_job_number, next_end_id):

        dbx = self.get_db(db_name=DEFAULT_DB)
        dd = {"_id": ws_name, "next_job_number": next_job_number, "next_end_id": next_end_id}
        self.update_sys_collection(WORKSPACES, ws_name, dd, dbx=dbx)
        
    def get_workspace_infos(self, filter, fields=None):
        dbx = self.mongo_client[DEFAULT_DB]
        records = self.mongo_with_retries("create_workspace_if_needed", lambda: dbx[WORKSPACES].find(filter, fields), return_records=True)
        return records

    def get_workspace_names(self):
        dbx = self.mongo_client[DEFAULT_DB]
        records = self.mongo_with_retries("create_workspace_if_needed", lambda: dbx[WORKSPACES].find({}, {}), return_records=True)

        ws_names = [r["_id"] for r in records]
        return ws_names

    def create_collection_if_needed(self, dbx, name, shard_key, update_freq, index_key=None):

        cd = {"customAction": "CreateCollection", "collection": name}

        if update_freq == "low":
            thruput = 1000
        elif update_freq == "medium":
            thruput = 5000
        else:
            thruput = 10000

        cd["autoScaleSettings"] = {"maxThroughput": thruput}
        if shard_key:
            cd["shardKey"] = shard_key

        try:
            dbx.command(cd)
        except pymongo.errors.OperationFailure as ex:
            # this is the exception raised by "already exists"
            msg = ex.details["errmsg"]
            if not "already exists" in msg:
                # unexpected exception
                raise

        keys = ["_id", "ws_name"]
        if index_key:
            keys.append(index_key)

        for key in keys:
            dbx[name].create_index(key)

    def create_workspace_collections_if_needed(self, db_name):
        '''
        create our 10 collections in the specified database, if needed
        '''
        dbx = self.get_db(db_name=db_name)

        # run data
        self.create_collection_if_needed(dbx, "run_info", "_id", "low")
        self.create_collection_if_needed(dbx, "run_stats", "_id", "medium")
        self.create_collection_if_needed(dbx, "hparams", "_id", "low")
        self.create_collection_if_needed(dbx, "metrics", "_id", "high")
        self.create_collection_if_needed(dbx, "log_records", "_id", "high")

        # job data
        self.create_collection_if_needed(dbx, "job_info", "_id", "low")
        self.create_collection_if_needed(dbx, "job_stats", "_id", "high")
        self.create_collection_if_needed(dbx, "connect_info", "_id", "medium")
        self.create_collection_if_needed(dbx, "service_info_by_node", "_id", "low")
        self.create_collection_if_needed(dbx, "child_runs", "key", "medium", index_key="key")

    def mongo_with_retries(self, name, mongo_cmd, ignore_error=False, return_records=False, return_single_record=False):
        import pymongo.errors

        retry_count = 25
        result = None
        started = time.time()

        for i in range(retry_count):
            try:
                result = mongo_cmd()

                # most of the time, we want to ALSO want to retry building a record set from the cursor
                if return_records:
                    result = list(result) if result else []
                elif return_single_record:
                    if result:
                        result = list(result)
                        if result:
                            result = result[0]
                break
            # watch out for these exceptions: AutoReconnect, OperationFailure (and ???)
            except BaseException as ex:   # pymongo.errors.OperationFailure as ex:
                
                # this is to help us debug situations where we raise the exception without ever printing retry msgs
                print("got exception in mongo, i={}, retry_count={}, caller={}".format(i, retry_count, name), flush=True)

                # since we cannot config logger to supress stderr, don't log this
                #logger.exception("Error in mongo_with_retries, ex={}".format(ex))
                
                # pymongo.errors.OperationFailure: Message: {"Errors":["Request rate is large"]}
                if ignore_error:
                    console.print("ignoring mongo-db error: name={}, ex={}".format(name, ex))
                    break
                
                if i == retry_count-1:
                    # we couldn't recover - signal a hard error/failure
                    raise ex

                # we get hit hard on the "Request rate is large" errors when running 
                # large jobs (500 simultaneous runs), so beef up the backoff times to
                # [1,61] so we don't die with a hard failure here
                if i == 0:
                    backoff = 1 + 10*np.random.random()
                    self.retry_errors += 1
                else:
                    backoff = 1 + 60*np.random.random()

                ex_code = ex.code if hasattr(ex, "code") else ""
                ex_msg = str(ex)[0:60]+"..."

                console.print("retrying mongo-db: name={}, retry={}/{}, backoff={:.2f}, ex.code={}, ex.msg={}".format(name, i+1, retry_count, backoff, 
                    ex_code, ex_msg))
                    
                time.sleep(backoff)
                
        # track all mongo calls stats
        elapsed = time.time() - started

        if not name in self.call_stats:
            self.call_stats[name] = []
        self.call_stats[name].append(elapsed)

        #print("--> mongo call: {} (elapsed: {:.4f} secs)".format(name, elapsed))
        return result

    def disallow_embedded_props(self, dd, exceptions=[]):
        # in early days of v2, ensure we have no unexpected embedded info
        for name, value in dd.items():
            if isinstance(value, dict):
                assert name in exceptions

    def update_job(self, jd):
        ws_name = jd["ws_name"]
        job_id = jd["job_id"]
        total_runs = jd["run_count"]

        # delete low-priority embedded info
        utils.safe_delete(jd, "runs_by_box")

        # delete obsolete embedded info
        utils.safe_delete(jd, "active_runs")
        utils.safe_delete(jd, "dynamic_runs_remaining")

        # extract embedded info
        service_info_by_node = utils.safe_delete(jd, "service_info_by_node")
        runs_by_box = utils.safe_delete(jd, "runs_by_box")
        connect_info_by_node = utils.safe_delete(jd, "connect_info_by_node")
        secrets_by_node = utils.safe_delete(jd, "secrets_by_node")
        child_runs_by_node = utils.safe_delete(jd, "child_runs_by_node")

        # extract job stats
        job_stats = {}
        utils.safe_move(job_stats, jd, "job_status")
        utils.safe_move(job_stats, jd, "completed_runs")
        utils.safe_move(job_stats, jd, "error_runs")
        utils.safe_move(job_stats, jd, "running_nodes")
        utils.safe_move(job_stats, jd, "running_runs")

        # hardcode some stats so that when processing job log, counts are correct
        job_stats["total_runs"] = total_runs
        job_stats["completed_runs"] = 0
        job_stats["error_runs"] = 0
        job_stats["running_nodes"] = 0
        job_stats["running_runs"] = 0

        self.add_id(job_stats, ws_name, job_id)
        self.update_collection("job_stats", ws_name, job_stats)

        # CHILD RUNS
        if child_runs_by_node:
            self.add_docs_by_node("child_runs", ws_name, job_id, child_runs_by_node)

        # add to SERVICE_INFO_BY_NODE
        if service_info_by_node:
            self.add_id(service_info_by_node, ws_name, job_id)
            self.update_collection("service_info_by_node", ws_name, service_info_by_node, is_flat=False)

        # add to CONNECT_INFO
        if connect_info_by_node or secrets_by_node:
            # merge secrets into connect info
            if connect_info_by_node:
                for n1, n2 in zip(connect_info_by_node, secrets_by_node):
                    connect_info_by_node[n1]["secret"] = secrets_by_node[n1]
            else:
                connect_info_by_node = {}
                for node, secret in secrets_by_node.items():
                    connect_info_by_node[node] = {"secret": secret}

            self.add_doc_by_node("connect_info", ws_name, job_id, connect_info_by_node)

        # add to JOB_INFO
        self.add_id(jd, ws_name, job_id)
        self.update_collection("job_info", ws_name, jd, flat_exceptions=["pool_info", "service_job_info"])

    def update_connect_info_by_node(self, ws_name, job_id, node_id, connect_info_dict):
        _id = "{}/{}/{}".format(ws_name, job_id, node_id)
        connect_info_dict["_id"] = _id
        self.update_collection("connect_info", ws_name, connect_info_dict)

    # V2 API
    def add_docs_by_node(self, collection_name, ws_name, job_id, docs_by_node):
        dbx = self.get_db(ws_name)
        inserts = []

        for node_id, docs in docs_by_node.items():
            node_index = utils.node_index(node_id)

            for doc in docs:
                # add _id
                run_index = doc["run_index"]
                _id = "{}/{}/{}".format(ws_name, job_id, run_index)
                doc["_id"] = _id

                # add key (this is how we will filter our operations)
                key = "{}/{}/{}".format(ws_name, job_id, node_index)
                doc["key"] = key

                # all records must specify ws_name
                doc["ws_name"] = ws_name

                inserts.append(doc)

        inserts = self.filter_out_existing_docs(inserts, collection_name, dbx)
        if inserts:
            self.insert_many(dbx, collection_name, inserts)

    # V2 API
    def add_doc_by_node(self, collection_name, ws_name, job_id, doc_by_node):
        dbx = self.get_db(ws_name)

        inserts = []

        for node_id, doc in doc_by_node.items():
            node_index = utils.node_index(node_id)

            _id = "{}/{}/{}".format(ws_name, job_id, node_index)
            doc["_id"] = _id
            doc["ws_name"] = ws_name

        inserts = self.filter_out_existing_docs(inserts, collection_name, dbx)
        if inserts:
            self.insert_many(dbx, collection_name, inserts)

    def insert_many(self, dbx, collection_name, inserts):
        # prevent rate limit errors
        max_inserts = 10
        start = 0
        while start < len(inserts):
            batch = inserts[start:start+max_inserts]
            self.mongo_with_retries("insert_many", lambda: dbx[collection_name].insert_many(batch) )
            start += len(batch)

    def filter_out_existing_docs(self, docs, collection_name, dbx):
        # create a dict for fast access
        id_list = [doc["_id"] for doc in docs]
        filter = {"_id": {"$in": id_list}}

        records = self.mongo_with_retries("filter_out_existing_docs", 
            lambda: dbx[collection_name].find(filter, {"_id": 1}) )

        found_ids = {record["_id"]:1 for record in records}
        new_docs = [doc for doc in docs if not doc["_id"] in found_ids]

        return new_docs

    def get_collection_records(self, collection, ws_name, filter, fields=None):
        dbx = self.get_db(ws_name)

        records = self.mongo_with_retries("get_collection_records", lambda: dbx[collection].find(filter, fields), return_records=True)
        return records
        
    def update_collection(self, collection_name, ws_name, dd, dbx=None, is_flat=True, flat_exceptions=[]):
        '''
        add or update a single record in the specified collection
        '''
        if not dbx:
            dbx = self.get_db(ws_name)

        if is_flat:
            self.disallow_embedded_props(dd, flat_exceptions)

        # ensure we have assigned an id intentionally
        assert "_id" in dd

        # all collections must have ws_name (for deleting all entries in a specified workspace)
        dd["ws_name"] = ws_name

        # use update_one (vs. insert_one) to add or update record (and allow redundant add/updates for storage tracking)
        update = {"$set": dd}
        filter = {"_id": dd["_id"]}

        self.mongo_with_retries("update_collection", lambda: dbx[collection_name].update_one(filter=filter, update=update, upsert=True) )
            
    def update_sys_collection(self, collection_name, ws_name, dd, dbx=None):
        '''
        add or update a single record in the specified system collection (__workspaces__ or __info__)
        '''
        if not dbx:
            dbx = self.get_db(DEFAULT_DB)

        self.disallow_embedded_props(dd)

        # for sys collections, the caller assigns the _id and key, if any
        # assert not "_id" in dd
        # assert not "key" in dd

        dd["ws_name"] = ws_name

        # use update_one (vs. insert_one) for rewriting same run during mongo v2 dev/debug cycle
        update = {"$set": dd}
        filter = {"_id": dd["_id"]}

        self.mongo_with_retries("update_sys_collection", lambda: dbx[collection_name].update_one(filter=filter, update=update, upsert=True) )

    def update_collection_bulk(self, collection_name, ws_name, run_or_job_name, dd_list):
        dbx = self.get_db(ws_name)

        updates = []
        for dd in dd_list:
            self.disallow_embedded_props(dd)

            # dd[ws_name] = ws_name
            # dd[run_name] = run_name

            if not "key" in dd:
                key = ws_name + "/" + run_or_job_name
                dd["key"] = key

            update = {"$set": dd}
            filter = {"key": key}

            update = pymongo.UpdateOne(filter, update, upsert=True)
            updates.append(update)

        self.mongo_with_retries("update_collection_bulk", lambda: dbx[collection_name].bulk_write(updates) )

    def get_next_job_id(self, ws_name, id_name):
        fd = {"_id": ws_name}
        dbx = self.mongo_client[DEFAULT_DB]
        path = id_name

        record = self.mongo_with_retries("get_next_job_id", lambda: \
                dbx[WORKSPACES].find_and_modify( {"_id": ws_name}, update={"$inc": {path: 1} }, new=False))

        next_id = record[path]
        return next_id

    def process_run_event(self, ws_name, run_name, event, dd, record_dict):
        run_stats = {}
        completed = False

        if event == "created":
            #self.create_mongo_run(dd)
            utils.safe_delete(dd, "node")
            utils.safe_delete(dd, "run_index")

            self.add_id(dd, ws_name, run_name)
            self.update_collection("run_info", ws_name, dd)

        elif event == "status-change":
            run_stats.update(dd)

        elif event == "ended":
            dd = dict(dd)    # make local copy that we can update
            del dd["metrics_rollup"]
            run_stats.update(dd)
            completed = True

        elif event in ["queued", "ended"]:
            run_stats["status"] = event

        elif event in ["started"]:
            run_stats["status"] = "running"

        elif event == "hparams":
            self.add_id(dd, ws_name, run_name)
            self.update_collection("hparams", ws_name, dd)

        elif event == "metrics":
            self.add_id(dd, ws_name, run_name)
            self.update_collection("metrics", ws_name, dd)

        if run_stats:
            self.add_id(run_stats, ws_name, run_name)
            self.update_collection("run_stats", ws_name, run_stats)

        # add to LOG_RECORDS
        record = dict(record_dict)    # make local copy that we can update
        
        # assign a GUID to each record's id
        record["_id"] = str(uuid.uuid4())

        key = self.make_key(ws_name, run_name)
        record["key"] = key
        self.update_collection("log_records", ws_name, record, is_flat=False)

        return completed

    def process_job_events(self, ws_name, job_id, event_records):
        completed = False
        runs = []

        for ev in event_records:
            event = ev["event"]
            dd = ev["data"]

            if event == "node_start":
                self.job_node_start(ws_name, job_id)
            elif event == "node_end":
                completed = self.job_node_exit(ws_name, job_id)
                # add parent run to list of runs
                run = dd["run"]
                runs.append(run)
            elif event == "start_run":
                self.job_run_start(ws_name, job_id)
                run = dd["run"]
                runs.append(run)
            elif event == "end_run":
                is_parent = utils.safe_value(dd, "is_parent")
                if not is_parent:
                    exit_code = dd["exit_code"]
                    self.job_run_exit(ws_name, job_id, exit_code)

        return completed, runs

    def get_service_info_by_node(self, ws_name, job_id):
        dbx = self.get_db(ws_name)

        key = ws_name + "/" + job_id
        filter_dict = {"_id": key}
        records = self.mongo_with_retries("get_service_info_by_node", lambda: dbx["service_info_by_node"].find(filter_dict), return_records=True)
        record = records[0] if records else None

        if record:
            # zap the "_id" and ws_name leaving only the node keys
            del record["_id"]
            del record["ws_name"]

        return record

    def reset_child_runs(self, ws_name, job_id, node_index):
        '''
        called at start of node's controller in order to detected restarted runs
        '''
        dbx = self.get_db(ws_name)

        key = "{}/{}/{}".format(ws_name, job_id, node_index)
        fd = {"key": key, "status": constants.STARTED}
        ud = {"$set": {"status": constants.WAITING}}

        records = self.mongo_with_retries("reset_child_runs", lambda: dbx["child_runs"].\
            find_and_modify(fd, update=ud), return_records=True)

    def get_next_child_run(self, ws_name, job_id, node_index):
        '''
        finds next child run that needs to be run for the specified node.
        '''
        dbx = self.get_db(ws_name)

        key = "{}/{}/{}".format(ws_name, job_id, node_index)
        fd = {"key": key, "status": {"$in": [constants.UNSTARTED, constants.WAITING]}}
        ud = {"$set": {"status": constants.STARTED}}
        #console.print("get_next_child_run: key=", key, "fd=", fd, "ud=", ud)

        # this should return a single record
        entry = self.mongo_with_retries("get_next_child_run", lambda: dbx["child_runs"].\
            find_and_modify(fd, update=ud), return_records=False)

        return entry

    def mark_child_run_completed(self, entry):
        '''
        finds next child run that needs to be run for the specified node.
        '''
        key = entry["key"]
        run_index = entry["run_index"]
        ws_name = entry["ws_name"]

        dbx = self.get_db(ws_name)

        fd = {"key": key, "run_index": run_index}
        ud = {"$set": {"status": "completed"}}

        self.mongo_with_retries("mark_child_run_completed", lambda: dbx["child_runs"].\
            update_one(fd, update=ud))

    def make_key(self, ws_name, job_or_run_name):
        return ws_name + "/" + job_or_run_name

    def add_id(self, dd, ws_name, job_or_run_name):
        _id = ws_name + "/" + job_or_run_name
        dd["_id"] = _id

    def job_run_start(self, ws_name, job_id):
        '''
        A job's run has started running.  We need to:
            - increment the job's "running_runs" property 
        '''
        if self.update_job_stats:
            dbx = self.get_db(ws_name)
            _id = self.make_key(ws_name, job_id)

            cmd = lambda: dbx["job_stats"].find_and_modify( {"_id": _id}, update={"$inc": {"running_runs": 1} })
            self.mongo_with_retries("job_run_start", cmd)

    def job_run_exit(self, ws_name, job_id, exit_code):
        '''
        A job's run has finished running.  We need to:
            - decrement the job's "running_runs" property 
            - increment the job's "completed_runs" property
            - if exit_code != 0, increment the job's "error_runs" property
        '''
        if self.update_job_stats:
            dbx = self.get_db(ws_name)
            _id = self.make_key(ws_name, job_id)

            error_inc = 1 if exit_code else 0
            cmd = lambda: dbx["job_stats"].find_and_modify( {"_id": _id}, 
                update={"$inc": {"running_runs": -1, "completed_runs": 1, "error_runs": error_inc} }, new=True)

            result = self.mongo_with_retries("job_run_exit", cmd)

    def run_start(self, ws_name, run_name):
        '''
        A run has started running.  We need to:
            - set the run "start_time" property to NOW
            - set the run "queue_duration" property to NOW - created_time
        '''
        dbx = self.get_db(ws_name)

        if self.update_run_stats:
            now = arrow.now()
            now_str = str(now)

            # get create_time of run
            cmd = lambda: dbx[ws_name].find({"_id": run_name}, {"create_time": 1})
            records = self.mongo_with_retries("run_start", cmd, return_records=True)

            doc = records[0] if records else None
            if doc and "create_time" in doc:
                create_time_str = doc["create_time"]
                create_time = arrow.get(create_time_str)

                # compute time in "queue" 
                queue_duration = utils.time_diff(now, create_time)

                cmd = lambda: dbx[ws_name].find_and_modify( {"_id": run_name}, update={"$set": {"start_time": now_str, "queue_duration": queue_duration} })
                self.mongo_with_retries("run_start", cmd)

    def run_exit(self, ws_name, run_name):
        '''
        A run has finished running.  We need to:
            - set the run "run_duration" property to NOW - start_time
        '''
        dbx = self.get_db(ws_name)

        if self.update_run_stats:
            now = arrow.now()
            now_str = str(now)

            # get start_time of run
            cmd = lambda: dbx[ws_name].find({"_id": run_name}, {"start_time": 1})
            records = self.mongo_with_retries("run_exit #1", cmd, return_records=True)

            doc = records[0] if records else None
            if doc and "start_time" in doc:
                start_time_str = doc["start_time"]
                start_time = arrow.get(start_time_str)

                # compute run_duration 
                run_duration = utils.time_diff(now, start_time)

                cmd = lambda: dbx[ws_name].find_and_modify( {"_id": run_name}, update={"$set": {"run_duration": run_duration} })
                self.mongo_with_retries("run_exit #2", cmd)

    def job_node_start(self, ws_name, job_id):
        '''
        A job's node has started running.  We need to:
            - increment the job's "running_nodes" property
            - set the "job_status" property to "running"
        '''
        dbx = self.get_db(ws_name)

        if self.update_job_stats:
            _id = self.make_key(ws_name, job_id)
            cmd = lambda: dbx["job_stats"].find_and_modify( {"_id": _id}, update={"$inc": {"running_nodes": 1} }, new=True)
            result = self.mongo_with_retries("job_node_start", cmd)

            cmd = lambda: dbx["job_stats"].find_and_modify( {"_id": _id}, update={"$set": {"job_status": "running"} }, new=True)
            result2 = self.mongo_with_retries("job_node_start", cmd)

            console.diag("job_node_start: result={}, result2={}".format(result, result2))

    def job_node_exit(self, ws_name, job_id):
        '''
        A job's node has finished running.  We need to:
            - decrement the job's "running_nodes" property 
            - if running_nodes==0, set the "job_status" property to "completed"
        '''
        dbx = self.get_db(ws_name)
        job_completed = False
        result2 = None

        if self.update_job_stats:
            _id = self.make_key(ws_name, job_id)
            cmd = lambda: dbx["job_stats"].find_and_modify( {"_id": _id}, update={"$inc": {"running_nodes": -1} }, new=True)
            result = self.mongo_with_retries("job_node_exit", cmd)
            job_completed = (result["running_nodes"] == 0)

            if job_completed:
                cmd = lambda: dbx["job_stats"].find_and_modify( {"_id": _id}, update={"$set": {"job_status": "completed"} })
                result2 = self.mongo_with_retries("job_node_exit", cmd)

            console.diag("job_node_exit: result={}, result2={}".format(result, result2))

        return job_completed

    def update_mongo_run_at_end(self, ws_name, run_name, status, exit_code, restarts, end_time, log_records, hparams, metrics):
        # update run document on Mongo DB
        dbx = self.get_db(ws_name)

        if self.update_run_stats:
            # update properties
            updates = {}
            updates["status"] = status
            updates["exit_code"] = exit_code
            updates["restarts"] = restarts
            updates["end_time"] = end_time

            # add the unique end_id (relative to ws_name)
            updates["end_id"] = self.get_next_job_id(ws_name, "next_end_id")

            self.update_run_info(ws_name, run_name, updates, hparams, metrics)

    def update_run_info(self, ws_name, run_name, dd, hparams=None, metrics=None):

        if self.update_run_stats:
            dbx = self.get_db(ws_name)
    
            # normalize nested info, if present
            if not hparams:
                hparams = {}
                utils.safe_move(hparams, dd, "hparams", flatten=True)

            if not metrics:
                metrics = {}
                utils.safe_move(metrics, dd, "metrics", flatten=True)

            #print("dd=", dd)
            self.disallow_embedded_props(dd)
            
            update_dd = dict(dd)
            update_dd["last_time"] = utils.get_time()
            _id = ws_name + "/" + run_name

            # update RUN_STATS
            update_doc = { "$set": update_dd}
            self.mongo_with_retries("update_run_info", lambda: dbx["run_stats"].update_one( {"_id": _id}, update_doc) )

            if hparams:
                # update HPARAMS
                update_doc = { "$set": hparams}
                self.mongo_with_retries("update_run_info", lambda: dbx["hparams"].update_one( {"_id": _id}, update_doc) )

            if metrics:
                # update METRICS
                update_doc = { "$set": metrics}
                self.mongo_with_retries("update_run_info", lambda: dbx["metrics"].update_one( {"_id": _id}, update_doc) )

    def print_call_stats(self):
        total_count = 0
        total_time = 0
        total_calls = 0

        for name, stats in self.call_stats.items():
            mean = np.mean(stats)
            print("  {}x {}: avg={:.4f}".format(len(stats), name, mean))

            total_calls += len(stats)
            total_time += np.sum(stats)
            total_count += 1

        print()
        print("  {}x {}: total={:.4f} secs".format(total_calls, "CALLS", total_time))
        print()

    def get_info_for_collection(self, ws_name, collection_name, filter_dict, fields_dict=None):

        if not ws_name in filter_dict:
            filter_dict["ws_name"] = ws_name

        dbx = self.get_db(ws_name)

        result = self.mongo_with_retries("get_info_for_collection", lambda: \
            dbx[collection_name].find(filter_dict, fields_dict), return_records=True)
        return result

    def get_filtered_sorted_core(self, ws_name, collection_name, filter_dict, fields_dict=None, sort_col=None, sort_dir=1, 
        skip=None, first=None, return_records=True):

        if not ws_name in filter_dict:
            filter_dict["ws_name"] = ws_name

        dbx = self.get_db(ws_name)

        # put our mongo operations together in a RETRYABLE function
        def fetch():

            cursor = dbx[collection_name].find(filter_dict, fields_dict)
            if sort_col:
                cursor = cursor.sort(sort_col, sort_dir)
            if skip:
                cursor = cursor.skip(skip)
            if first:
                cursor = cursor.limit(first)

            return cursor

        result = self.mongo_with_retries("get_filtered_sorted_core", fetch, return_records=return_records)
        return result

    def does_run_exist(self, ws_name, run_name):
        dbx = self.get_db(ws_name)
        _id = self.make_key(ws_name, run_name)
        fd = {"_id": _id}

        records = self.mongo_with_retries("does_run_exist", lambda: dbx["run_info"].find(fd), return_records=True)
        return bool(records)

    def get_info_for_jobs(self, ws_name, filter_dict, fields_dict):
        '''
        does a find on job_info using specified filter columns from job_info only.
        '''

        dbx = self.get_db(ws_name)
        records = self.mongo_with_retries("get_info_for_jobs", lambda: dbx["job_info"].find(filter_dict, fields_dict), return_records=True)
        return records

    def get_ids_for_filter(self, dbx, ws_name, collection_name, filter, fields, total_ids):

        if total_ids:
            filter["_id"] = {"$in": total_ids}
        else:
            # first filtering must specify ws_name
            filter["ws_name"] = ws_name

        result = self.mongo_with_retries("get_ids_for_filter",  lambda: dbx[collection_name].find(filter, fields), return_records=True)
        if result:
            ids = [r["_id"] for r in result]
        else:
            # no matching records
            ids = None

        return ids

    def get_ids_for_sorted_filter(self, dbx, ws_name, collection_name, filter, fields, total_ids, sort_col=None, sort_dir=1, 
        skip=None, first=None):

        if total_ids:
            filter["_id"] = {"$in": total_ids}
        else:
            # first filtering must specify ws_name
            filter["ws_name"] = ws_name

        # put our mongo operations together in a RETRYABLE function
        def fetch():

            cursor = dbx[collection_name].find(filter, fields)
            if sort_col:
                cursor = cursor.sort(sort_col, sort_dir)
            if skip:
                cursor = cursor.skip(skip)
            if first:
                cursor = cursor.limit(first)

            return cursor
            
        result = self.mongo_with_retries("get_ids_for_sorted_filter", fetch, return_records=True)
        
        if result:
            ids = [r["_id"] for r in result]
        else:
            # no matching records
            ids = None

        return ids
        
    def get_filtered_sorted_collection(self, collections, primary_collection, ws_name, filter_dict, fields_dict, 
        sort_col, sort_dir, skip, first, count_records, buffer_size):

        dbx = self.get_db(ws_name)
        id_fields = {"_id": 1}
        total_ids = None

        # remove sort_col temp. from filter_dict
        if sort_col and sort_col in filter_dict:
            entry = filter_dict[sort_col]
            if entry == {"$exists": True}:
                del filter_dict[sort_col]

        # process filters in each collection
        for cd in collections:
            c_name = cd["name"]
            c_props = cd["props"]
            c_sorted = cd["sorted"]
            c_filter = {}

            for name, value in dict(filter_dict).items():
                if c_name == "hparams":
                    if name.startswith("hparams."):
                        prop = name.split(".", 1)[1]
                        c_filter[prop] = value
                        del filter_dict[name]
                elif c_name == "metrics":
                    if name.startswith("metrics."):
                        prop = name.split(".", 1)[1]
                        c_filter[prop] = value
                        del filter_dict[name]
                elif name in c_props:
                    # xxx_info or xxx_stats
                    c_filter[name] = value
                    del filter_dict[name]

            if c_sorted:
                # we have reached the last collection
                if c_name == primary_collection:
                    # sort_col is in primary collection, so we can fall down into final get_filtered_sorted_core() call
                    filter_dict = c_filter

                else:
                    # must apply first/last/skip/sort on this
                    if not sort_col in c_filter:
                        c_filter[sort_col] = {"$exists": True}
                    
                    total_ids = self.get_ids_for_sorted_filter(dbx, ws_name, c_name, c_filter, id_fields, total_ids,
                        sort_col, sort_dir, skip=skip, first=first)
                    self.round_trip_count += 1

                    if not total_ids:
                        return []

                    # clear sort-related props since we have applied them already 
                    sort_col = None
                    skip = None
                    first = None
                    last = None

            elif c_filter:
                # filter total_ids by props specified for collection c_name
                total_ids = self.get_ids_for_filter(dbx, ws_name, c_name, c_filter, id_fields, total_ids)
                self.round_trip_count += 1

                if not total_ids:
                    return []

        # now, get matching RUN INFO records, with needed sort/skip/first/last/fields
        if total_ids:
            if "ws_name" in filter_dict:
                del filter_dict["ws_name"]
            filter_dict["_id"] = {"$in": total_ids}

        if sort_col and not sort_col in filter_dict:
            filter_dict[sort_col] = {"$exists": True}
        
        fd = filter_dict if filter_dict else None
        cursor = self.get_filtered_sorted_core(ws_name, primary_collection, fd, None, sort_col=sort_col, sort_dir=sort_dir, 
            skip=skip, first=first, return_records=False)
        self.round_trip_count += 1

        # cursor to records
        if cursor:
            # warn user if returning a large amount of records
            if count_records:
                count = cursor.count(True)
                console.print("retreiving {:,} records".format(count))
                if count > 500:
                    console.print("  for faster results, use the --first or --last option")

            # this is where we can encounter "max message size" errors if we try to get all
            # records at once
            cursor = cursor.batch_size(buffer_size)
            records = list(cursor)
        else:
            records = []

        if total_ids and records:
            # sort_col was in another collection (not run_info), so sort records now according to total_ids (but may be a subset)
            records_dict = {r["_id"]: r for r in records}
            records = [records_dict[id] for id in total_ids if id in records_dict]

        return records

    def get_filtered_sorted_run_ids(self, ws_name, filter_dict, fields_dict=None, sort_col=None, sort_dir=1, skip=None, first=None, 
        count_runs=False, buffer_size=50):
        '''
        Processing:
            filter and sort runs (supporting filter and sort cols in related collections) and return job_id's.
        '''

        run_info_props = {"_id": 1, "app_name": 1, "box_name": 1, "compute": 1, "create_time": 1, "description": 1, "exper_name": 1,
            "from_ip": 1, "from_computer_name": 1, "is_child": 1, "is_parent": 1, "is_outer": 1, "job_id": 1, 
            "node_index": 1, "path": 1, "repeat": 1, "script": 1, "run_name": 1, "run_num": 1, "run_guid": 1,
            "search_style": 1, "search_type": 1, "service_type": 1, "sku": 1, "username": 1, "xt_build": 1, "xt_version": 1}

        run_stats_props = {"status": 1, "last_time": 1, "exit_code": 1, "restarts": 1, "end_time": 1, "end_id": 1}

        collections = [
            {"name": "run_info", "props": run_info_props, "sorted": 0},
            {"name": "run_stats", "props": run_stats_props, "sorted": 0},
            {"name": "hparams", "props": None, "sorted": 0},
            {"name": "metrics", "props": None, "sorted": 0}
        ]

        # re-order collections so that the one being sorted is on the bottom
        if sort_col:
            if sort_col in run_info_props:
                collections[0]["sorted"] = 1
            elif sort_col in run_stats_props:
                collections[1]["sorted"] = 1
            elif sort_col.startswith("hparams."):
                collections[2]["sorted"] = 1
                sort_col = sort_col.split(".", 1)[1]
            elif sort_col.startswith("metrics."):
                collections[3]["sorted"] = 1
                sort_col = sort_col.split(".", 1)[1]

            collections.sort(key=lambda i: i["sorted"])

        records = self.get_filtered_sorted_collection(collections, "run_info", ws_name, filter_dict, fields_dict, 
            sort_col, sort_dir, skip, first, count_runs, buffer_size)

        return records

    def get_filtered_sorted_job_ids(self, ws_name, filter_dict, fields_dict=None, sort_col=None, sort_dir=1, skip=None, first=None, 
        count_jobs=False, buffer_size=50):
        '''
        Processing:
            filter and sort jobs (supporting filter and sort cols in related collections) and return job_id's.
        '''

        job_info_props = {"_id": 1, "compute": 1, "concurrent": 1, "exper_name": 1, "hold": 1, "job_id": 1, "job_num": 1,
            "job_guid": 1, "job_secret": 1, "node_count": 1, "primary_metric": 1, "run_count": 1, "repeat": 1, 
            "schedule": 1, "search_type": 1, "search_style": 1, "username": 1, "xt_cmd": 1, "started": 1}

        job_stats_props = {"job_status": 1, "completed_runs": 1, "error_runs": 1, "running_nodes": 1, "total_runs": 1}

        collections = [
            {"name": "job_info", "props": job_info_props, "sorted": 0},
            {"name": "job_stats", "props": job_stats_props, "sorted": 0},
        ]

        # re-order collections so that the one being sorted is on the bottom
        if sort_col:
            if sort_col in job_info_props:
                collections[0]["sorted"] = 1
            elif sort_col in job_stats_props:
                collections[1]["sorted"] = 1

            collections.sort(key=lambda i: i["sorted"])

        records = self.get_filtered_sorted_collection(collections, "job_info", ws_name, filter_dict, fields_dict, 
            sort_col, sort_dir, skip, first, count_jobs, buffer_size)

        return records

    def calc_needed_run_collections(self, fields_dict):
        '''
        Processing:
            Collect names of related run collections specified by fields_dict
            and remove those fields from fields_dict.
        '''
        needed = {}
        default = 0 if fields_dict else 1

        needed["run_info"] = default
        needed["run_stats"] = default
        needed["metrics"] = default
        needed["hparams"] = default
        needed["log_records"] = 0

        if fields_dict:
            orig_fd = dict(fields_dict)

            for name, value in orig_fd.items():
                if name.startswith("hparams"):
                    needed["hparams"] = value
                    del fields_dict[name]

                elif name.startswith("metrics"):
                    needed["metrics"] = value
                    del fields_dict[name]

                elif name == "log_records":
                    needed["log_records"] = value
                    del fields_dict[name]

                elif name == "run_stats":
                    needed["run_stats"] = value
                    del fields_dict[name]

                elif name == "run_info":
                    needed["run_info"] = value
                    del fields_dict[name]
                    #fields_dict["_nosuchfield_"] = 0    # for all run_info fields to be returned

                elif name == "all":
                    needed["run_info"] = value
                    needed["run_stats"] = value
                    needed["log_records"] = value
                    needed["metrics"] = value
                    needed["hparams"] = value
                    del fields_dict[name]

        if not fields_dict:
            fields_dict = None

        return needed, fields_dict

    def get_filtered_sorted_run_info(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_runs=False, buffer_size=50):
        '''
        Processing:
            1. get filtered and sorted run_id's, with support for filter and sort cols in related collections
            2. get specified fields for run_id's, with support for fields in related collections
        '''
        needed_collections, fields_dict = self.calc_needed_run_collections(fields_dict)

        records = self.get_filtered_sorted_run_ids(ws_name, filter_dict, fields_dict, sort_col=sort_col, sort_dir=sort_dir,
            skip=skip, first=first, count_runs=count_runs, buffer_size=buffer_size)

        self.join_needed_run_collections(ws_name, records, needed_collections)
        
        return records

    def get_info_for_runs(self, ws_name, filter_dict, fields_dict=None):

        self.round_trip_count = 0
        needed_collections, fields_dict = self.calc_needed_run_collections(fields_dict)

        records = self.get_info_for_collection(ws_name, "run_info", filter_dict, fields_dict)

        self.join_needed_run_collections(ws_name, records, needed_collections)
        return records
    
    def join_needed_run_collections(self, ws_name, records, needed):
        ids = [run["_id"] for run in records]

        # add RUN_STATS
        if needed["run_stats"]:
            stats = self.get_collection_records("run_stats", ws_name, {"_id": {"$in": ids}})
            self.join_data(records, stats)
            self.round_trip_count += 1

        # add HPARAMS
        if needed["hparams"]:
            hparams = self.get_collection_records("hparams", ws_name, {"_id": {"$in": ids}})
            self.join_data(records, hparams, embed_name="hparams")
            self.round_trip_count += 1

        # add METRICS
        if needed["metrics"]:
            metrics = self.get_collection_records("metrics", ws_name, {"_id": {"$in": ids}})
            self.join_data(records, metrics, embed_name="metrics")
            self.round_trip_count += 1

        # add LOG_RECORDS
        if needed["log_records"]:
            log_records = self.get_collection_records("log_records", ws_name, {"key": {"$in": ids}})
            self.join_log_records(records, log_records)
            self.round_trip_count += 1

    def calc_needed_job_collections(self, fields_dict):
        '''
        Processing:
            Collect names of related job collections specified by fields_dict
            and remove those fields from fields_dict.
        '''
        needed = {}
        default = 0 if fields_dict else 1

        needed["job_stats"] = default
        needed["connect_info"] = default
        needed["service_info_by_node"] = default
        needed["job_info"] = default

        if fields_dict:
            orig_fd = dict(fields_dict)

            for name, value in orig_fd.items():
                if name.startswith("job_stats"):
                    needed["job_stats"] = value
                    del fields_dict[name]

                elif name.startswith("connect_info"):
                    needed["connect_info"] = value
                    del fields_dict[name]

                elif name == "service_info_by_node":
                    needed["service_info_by_node"] = value
                    del fields_dict[name]

                elif name == "job_info":
                    needed["job_info"] = value
                    del fields_dict[name]
                    #fields_dict["_nosuchfield_"] = 0    # for all job_info fields to be returned

                elif name == "all":
                    needed["job_stats"] = value
                    needed["connect_info"] = value
                    needed["service_info_by_node"] = value
                    needed["job_info"] = value
                    del fields_dict[name]

        if not fields_dict:
            fields_dict = None

        return needed, fields_dict

    def get_filtered_sorted_job_info(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_jobs=False, buffer_size=50):
        '''
        Processing:
            1. get filtered and sorted job_id's, with support for filter and sort cols in related collections
            2. get specified fields for job_id's, with support for fields in related collections
        '''
        self.round_trip_count = 0

        needed_collections, fields_dict = self.calc_needed_job_collections(fields_dict)

        records = self.get_filtered_sorted_job_ids(ws_name, filter_dict, fields_dict, sort_col=sort_col, sort_dir=sort_dir,
            skip=skip, first=first, count_jobs=count_jobs, buffer_size=buffer_size)

        self.join_needed_job_collections(ws_name, records, needed_collections)

        return records

    def get_info_for_jobs(self, ws_name, filter_dict, fields_dict=None):

        self.round_trip_count = 0

        needed_collections, fields_dict = self.calc_needed_job_collections(fields_dict)

        records = self.get_info_for_collection(ws_name, "job_info", filter_dict, fields_dict)

        self.join_needed_job_collections(ws_name, records, needed_collections)
        
        return records

    def join_needed_job_collections(self, ws_name, records, needed):
        ids = [job["_id"] for job in records]

        if needed["job_stats"]:
            # add JOB_STATS
            stats = self.get_collection_records("job_stats", ws_name, {"_id": {"$in": ids}})
            self.join_data(records, stats)
            self.round_trip_count += 1

        if needed["service_info_by_node"]:
            # add SERVICE_INFO_BY_NODE
            by_node = self.get_collection_records("service_info_by_node", ws_name, {"_id": {"$in": ids}})
            self.join_data(records, by_node, embed_name="service_info_by_node")
            self.round_trip_count += 1

        # add CONNECT_INFO
        if needed["connect_info"]:
            connect_info = self.get_collection_records("connect_info", ws_name, {"_id": {"$in": ids}})
            self.join_data(records, connect_info, embed_name="connect_info")
            self.round_trip_count += 1

    def join_data(self, records, infos, info_key="_id", embed_name=None):
        # build a dict to quickly find records
        rd = {r["_id"]: r for r in records}

        # update records with infs
        for info in infos:
            id = info[info_key]
            if id in rd:
                record = rd[id]

                if "_id" in info:
                    del info["_id"]

                if "ws_name" in info:
                    del info["ws_name"]

                if embed_name:

                    record[embed_name] = info
                else:
                    record.update(info)


    def join_log_records(self, records, log_recs):
        # build a dict to quickly find records
        rd = {r["_id"]: r for r in records}

        # create a list property on each record
        for record in records:
            record["log_records"] = []

        # add each log_rec to associated record
        for log in log_recs:
            id = log["key"]
            if id in rd:
                record = rd[id]

                # fixup log record
                del log["_id"]
                del log["key"]

                if "data" in log:
                    data = log["data"]
                    if "_id" in data:
                        del data["_id"]

                # add to record
                record["log_records"].append(log)

    def create_child_run_mgr(self, ws_name, job_id, parent_run_name, node_id):
        return MongoRunIndex(self, ws_name, job_id, parent_run_name, node_id)

    def build_child_runs_schedule_data(self, total_run_count, node_count):
        by_node = None

        if total_run_count > 1:
            by_node = {}
            ni = 0

            for ri in range(total_run_count):
                entry = {"run_index": ri, "status": constants.UNSTARTED}

                node_id = utils.node_id(ni)
                if not node_id in by_node:
                    by_node[node_id] = []

                by_node[node_id].append(entry)

                ni += 1
                if ni >= node_count:
                    ni = 0

        return by_node, "child_runs_by_node"

    def get_next_run_name(self, ws_name, job_id, is_parent, total_run_count, node_index):
        # v2 run name takes its base from the job_id
        job_num = job_helper.get_job_number(job_id)
        run_name = "run" + str(job_num)

        if total_run_count > 1:
            run_name += constants.NODE_PREFIX + str(node_index)

        return run_name

class MongoRunIndex():
    '''
    used by Controller to manage scheduling of child runs.
    '''
    def __init__(self, mongo, ws_name, job_id, parent_run_name, node_id, new_session=True):
        self.ws_name = ws_name
        self.mongo = mongo
        self.job_id = job_id
        self.parent_run_name = parent_run_name
        self.node_id = node_id
        self.node_index = utils.node_index(node_id)
        
        if new_session:
            self.mongo.reset_child_runs(ws_name, job_id, self.node_index)

    def get_next_child_run(self):
        entry = self.mongo.get_next_child_run(self.ws_name, self.job_id, self.node_index)     
        return entry

    def mark_child_run_completed(self, entry):
        return self.mongo.mark_child_run_completed(entry)

    def get_child_name(self, entry, parent_run_name):
        #child_num = 1 + (entry["run_index"] - self.first_run_index)
        child_num = entry["run_index"]
        parent_num = run_helper.get_parent_run_number(parent_run_name)

        child_name = "run{}.{}".format(parent_num, child_num)
        return child_name
