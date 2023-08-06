#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# eval_hp_search.py: evaluates runs to-date from specified hyperparmeter search (job or experiment name)
# runnable standalone or from XT (xt plot 

import os
import argparse
from os.path import exists
import math
import json
import numpy as np
import yaml

from xtlib import console
from xtlib.hparams import hp_helper
from xtlib.storage.store import Store

from xtlib.helpers.xt_config import get_merged_config
from xtlib.storage.store import Store

plt = None     # JIT import to keep XT from always loading matplotlib (and font cache building)


# TERMINOLOGY
# hp, setting, value - If a hyperparameter is a dial, a setting is one mark on the dial, and each mark has a value.


MIN_COL_WID = 9

def plot(xs, ys, ds, job_name, y_axis_label):
    ''' Displays a plot of the hyperparameter search progress. '''
    title = 'Retrospective evaluation of the best HP combination after each run'
    fig = plt.figure(figsize=(12, 8))
    fig.canvas.set_window_title('scripts\eval_hp_search.py')
    perf_axes = fig.add_axes([0.08, 0.09, 0.88, 0.84])
    perf_axes.set_title(title, fontsize=16)
    ymax = ys + ds
    ymin = ys - ds
    color = 'blue'
    perf_axes.set_xlabel("Completed runs", fontsize=16)
    perf_axes.set_ylabel(y_axis_label, fontsize=16)
    perf_axes.fill_between(xs, ymax, ymin, color=color, alpha=0.2)
    perf_axes.plot(xs, ys, color=color, label=job_name)  # , label=label, color=color, alpha=alpha, linewidth=LINEWIDTH, linestyle=linestyle, marker='o')
    perf_axes.legend(loc='lower right', prop={'size': 16})
    plt.show()


def get_time(run):
    return run.time

def get_neg_run_mean(run):
    return -run.mean

class RunSet():
    ''' Encapsulates a list of runs that share the same HP combination. '''
    def __init__(self, history, hp_id__setting_id__list, config_str):
        # sort to ensure a consistent order
        if hp_id__setting_id__list:
            hp_id__setting_id__list.sort()

        self.history = history
        self.hp_id__setting_id__list = hp_id__setting_id__list
        self.config_str = config_str
        self.runs = []
        self.sample_count = 0
        self.sample_mean = 0.
        self.sample_m2 = 0.
        self.post_mean = None
        self.post_var = None
        # A circular, doubly-linked list of RunSets, continually sorted by posterior mean in ascending order.
        self.sent = False  # The sentinel, for which dn is the best runset, and up is the worst.
        self.up = None  # The next best runset (or the sentinel).
        self.dn = None  # The next worst runset (or the sentinel).
        self.in_list = False  # Whether in_list or not, dn and up are always valid.

    def update_posteriors(self, prior_mean, prior_var):
        '''
        Uses Bayesian inference to estimate posterior mean and variance,
        assuming that each run's metric values are normally distributed.
        '''
        N = self.sample_count
        if N == 0:
            self.post_mean = prior_mean
            self.post_var = prior_var
        else:
            sample_mean = self.sample_mean
            sample_var = (prior_var + (N - 1) * self.get_sample_var()) / N  # Interpolation
            mean_numer = sample_var * prior_mean + N * prior_var * sample_mean
            var_numer = sample_var * prior_var
            denom = sample_var + N * prior_var
            self.post_mean = mean_numer / denom
            self.post_var = var_numer / denom

    def insert(self, dn=None, up=None):
        ''' Inserts the runset into the list at either the current or specified location. '''
        assert not self.in_list
        if dn:
            self.dn = dn
        if up:
            self.up = up
        assert self.dn.up == self.up
        assert self.up.dn == self.dn
        self.dn.up = self
        self.up.dn = self
        self.in_list = True

    def remove(self):
        ''' Removes the runset from the list, keeping pointers to the previous neighbors. '''
        assert self.in_list
        assert self.dn.up == self
        assert self.up.dn == self
        self.dn.up = self.up
        self.up.dn = self.dn
        self.in_list = False

    def reposition(self):
        ''' Move the runset to its sorted position within the list. '''
        if self.should_move_up():
            if self.in_list:
                self.remove()
            while self.should_move_up():
                self.move_up()
        elif self.should_move_down():
            if self.in_list:
                self.remove()
            while self.should_move_down():
                self.move_dn()
        if not self.in_list:
            self.insert()

    def is_better_than(self, other):
        # Higher mean is better.
        if self.post_mean > other.post_mean:
            return True
        elif self.post_mean < other.post_mean:
            return False
        # Lower variance is better.
        if self.post_var < other.post_var:
            return True
        elif self.post_var > other.post_var:
            return False
        # Older is better.
        return self.runs[0].time < other.runs[0].time

    def should_move_up(self):
        # True if the runset above this one belongs below it.
        if self.up.sent:
            return False
        return self.is_better_than(self.up)

    def should_move_down(self):
        # True if the runset below this one belongs above it.
        if self.dn.sent:
            return False
        return self.dn.is_better_than(self)

    def move_up(self):
        # Walks this runset up one step in the list.
        assert not self.in_list
        self.dn = self.up
        self.up = self.up.up

    def move_dn(self):
        # Walks this runset down one step in the list.
        assert not self.in_list
        self.up = self.dn
        self.dn = self.dn.dn

    def report_configuration(self):
        # print("    config={}".format(self.config_str))
        i = 0
        for hp in self.history.hparams:
            if hp.in_hp_section and hp.has_multiple_values:
                assert hp.id == self.hp_id__setting_id__list[i][0]
                console.print("{} = {}".format(hp.name, hp.settings[self.hp_id__setting_id__list[i][1]].value))
                i += 1

    def report_configuration_string(self):
        i = 0
        sz = ''
        for hp in self.history.hparams:
            if hp.in_hp_section and hp.has_multiple_values:
                width = max(MIN_COL_WID, len(hp.name))
                format_string = ' {' + ':{}s'.format(width) + '}'
                sz += format_string.format(str(hp.settings[self.hp_id__setting_id__list[i][1]].value))
                i += 1
        return sz

    def add_run(self, run):
        ''' Welford's online algorithm for single-pass computation of variance. '''
        self.runs.append(run)
        value = run.mean
        self.sample_count += 1
        delta = value - self.sample_mean
        self.sample_mean += delta / self.sample_count
        delta2 = value - self.sample_mean
        self.sample_m2 += delta * delta2

    def get_sample_var(self):
        if self.sample_count < 2:
            sample_var = 0.
        else:
            sample_var = self.sample_m2 / (self.sample_count - 1)  # Sample variance
        return sample_var


class RunSetTrophy():
    def __init__(self, run_i, runset):
        ''' A new trophy is award to every runset that becomes the best so far. '''
        self.run_i = run_i
        self.num_runs = 1
        self.runset = runset


class Run():
    def __init__(self, run_summary, metric_name):
        ''' Maintains the per-run information. '''
        self.hpname_hpvalue_list = []
        self.num_reports = 0
        self.mean = 0.
        self.time = None
        json_line = json.loads(run_summary)
        event_dict_list = json_line['log']
        for event_dict in event_dict_list:
            event_type = event_dict["event"]
            if event_type == "hparams":
                hp_data = event_dict["data"]
                for hpname in hp_data:
                    self.hpname_hpvalue_list.append((hpname, hp_data[hpname]))
            elif event_type == "metrics":
                metric_dict = event_dict["data"]
                if metric_name in metric_dict:
                    metric_value = float(metric_dict[metric_name])
                    self.mean += metric_value
                    self.num_reports += 1
            elif event_type == "created":
                run_data = event_dict["data"]
                self.run_name = run_data["run_name"]
            self.time = event_dict["time"]  # The time of the last event of the run.
        if self.num_reports > 0:
            self.mean /= self.num_reports


class HyperparameterSetting():
    ''' Stores the allowed values for a given hyperparameter. '''
    def __init__(self, id, hparam, value):
        self.id = id
        self.hparam = hparam
        self.value = value


class Hyperparameter():
    ''' Stores the name and settings for a single hyperparameter. '''
    def __init__(self, id, name, value_string, value_list, in_hp_section):
        self.id = id
        self.name = name
        self.in_hp_section = in_hp_section
        self.value_setting_dict = {}
        self.settings = []
        self.single_value = None
        self.has_multiple_values = False
        if value_string:
            value_strs = value_string.split(',')
            values = []
            for value_str in value_strs:
                values.append(self.cast_value(value_str.strip()))
            values.sort()
        elif value_list:
            values = value_list
        else:
            assert False, 'Either value_string or value_list must be provided.'
        for value in values:
            self.add_setting(value)
        self.has_multiple_values = (len(self.settings) > 1)

    def cast_value(self, value_str):
        if value_str == 'None':
            new_value = None
        elif value_str == 'True':
            new_value = True
        elif value_str == 'False':
            new_value = False
        else:
            try:
                new_value = int(value_str)
            except ValueError:
                try:
                    new_value = float(value_str)
                except ValueError:
                    new_value = value_str
        return new_value

    def add_setting(self, value):
        assert value not in self.value_setting_dict.keys()
        setting = HyperparameterSetting(len(self.settings), self, value)
        self.value_setting_dict[value] = setting
        self.settings.append(setting)
        self.single_value = value


class SearchHistory():
    ''' Loads, processes, and evaluates the runs of a single hyperparameter search job. '''
    def __init__(self, args=None, agg_name=None, workspace=None, timeout=None, primary_metric=None, hp_config_file_name=None):

        global plt
        import matplotlib.pyplot as plt

        if not args:
            arg_list = [agg_name]
            args = parse_args(arg_list)

            # set args from XT
            args.metric = primary_metric
            args.hp_def_file = os.path.basename(hp_config_file_name)
            args.num_reports_per_run = None

        self.args = args
        self.timeout = timeout

        self.DIR_PATH = "{}/{}/".format(args.job_dir, args.job)
        self.runs = []
        self.runsets = []
        self.configstr_runset_dict = {}
        self.best_runset_trophies = []
        self.xtstore = None

    def init_xtstore(self):
        if self.xtstore is None:
            xt_config = get_merged_config(create_if_needed=False)
            self.xtstore = Store(config=xt_config)

    def load_hp_definitions(self):
        ''' Get the hyperparameter definitions, downloaded from Azure if necessary. '''
        if self.args.hp_def_file == 'config.txt':
            config_path = self.DIR_PATH + args.hp_def_file
            self.define_hyperparameters_from_config_txt(config_path)
        else:
            hp_config_path = self.DIR_PATH + self.args.hp_def_file
            if not exists(hp_config_path):
                self.init_xtstore()
                self.xtstore.download_file_from_job(self.args.job, 'hp-config-dir/' + self.args.hp_def_file, hp_config_path)
            self.define_hyperparameters_from_config_yaml(hp_config_path)

    def load_runs(self):
        ''' Download the runs from Azure. '''
        runs_file_name = "all_runs.jsonl"
        all_runs_file_path = self.DIR_PATH + runs_file_name

        if not self.args.no_download:
            self.init_xtstore()
            self.xtstore.download_file_from_job(self.args.job, runs_file_name, all_runs_file_path)

        run_summaries = open(all_runs_file_path, 'r')
        self.num_incomplete_runs = 0
        for run_summary in run_summaries:
            run = Run(run_summary, self.args.metric)
            skip_this_run = False

            if run.num_reports == 0:  # Parent runs report no metrics.
                continue

            if self.args.num_reports_per_run and run.num_reports != self.args.num_reports_per_run:
                self.num_incomplete_runs += 1
                continue

            # Try to assemble a configuration string for this run.
            hp_id__setting_id__list = []

            # remove any reported hparams not found in search (allowed in XT)
            hp_list = run.hpname_hpvalue_list
            search_keys = list(self.name_hparam_dict.keys())
            new_list = [(hp_name, hp_value) for hp_name, hp_value in hp_list if hp_name in search_keys]
            run.hpname_hpvalue_list = new_list

            for hp_name, hp_value in run.hpname_hpvalue_list:
                # we no longer require that all run-reported hparams are present in the hp-config file
                # assert is here to ensure above filtering of run.hpname_hpvalue_list worked correctly
                assert hp_name in self.name_hparam_dict.keys()  

                hparam = self.name_hparam_dict[hp_name]
                
                if not hparam.in_hp_section:  # Ignore controls.
                    continue

                if hp_value not in hparam.value_setting_dict:
                    skip_this_run = True
                    break  # Skip this run. Its value must have been removed from config.txt.

                if hparam.has_multiple_values:  # Filter to HPs with multiple values.
                    setting = hparam.value_setting_dict[hp_value]
                    hp_id__setting_id__list.append((hparam.id, setting.id))

            if skip_this_run:
                continue

            # add this as a valid run
            run.hp_id__setting_id__list = hp_id__setting_id__list
            run.config_str = str(hp_id__setting_id__list)
            self.runs.append(run)

        self.runs.sort(key=get_time)

    def define_hyperparameters_from_config_txt(self, config_path):
        ''' To enable reading of ancient jobs. '''
        self.name_hparam_dict = {}
        self.hparams = []
        with open(config_path, 'r') as file:
            hp_config_file_text = file.read()
        line_num = 0
        in_hp_section = False
        lines = hp_config_file_text.split('\n')
        for line in lines:
            line_num += 1
            if len(line) == 0:
                continue
            if line[0] == '#':
                if "CONTROLS" in line:
                    in_hp_section = False
                elif "HYPERPARAMETERS" in line:
                    in_hp_section = True
                continue
            halves = line.split('=')
            name_string, value_string = halves[0].strip(), halves[1].strip()
            if '#' in value_string:
                value_string = value_string[:value_string.index('#')].strip()
            hp = Hyperparameter(len(self.hparams), name_string, value_string, None, in_hp_section)
            self.hparams.append(hp)
            self.name_hparam_dict[name_string] = hp

    def define_hyperparameters_from_config_yaml(self, hp_config):
        '''
            Input:   XT's standard HP definition file.
            Outputs:
                self.name_hparam_dict:
                self.hparams:
        '''
        self.name_hparam_dict = {}
        self.hparams = []
        chosen_hp_value_dict = yaml.load(open(hp_config, 'r'), Loader=yaml.Loader)
        hpname_valuelist_dict = chosen_hp_value_dict['hyperparameter-distributions']
        for hpname in hpname_valuelist_dict:
            valuelist = hpname_valuelist_dict[hpname]

            if not isinstance(valuelist, (tuple, list)):
                # omit single value hparams or unsupported hyperopt functions
                omit_value = True

                if isinstance(valuelist, str):
                    if valuelist.startswith("$"):
                        hd = hp_helper.parse_hp_dist(valuelist)
                        if "args" in hd and hd["args"] is not None:
                            # $choice or $linspace results in a list of values
                            valuelist = list(hd["args"])
                            if len(valuelist) > 0:
                                omit_value = False

                if omit_value:
                    continue

            hp = Hyperparameter(len(self.hparams), hpname, None, valuelist, True)
            self.hparams.append(hp)
            self.name_hparam_dict[hpname] = hp

    def populate_runsets(self, global_runset):
        ''' Groups runs into runsets that share the same HP combination. '''
        prior_mean = global_runset.sample_mean
        prior_var = global_runset.get_sample_var()
        best_runset = global_runset
        num_trophies = 0
        for i, run in enumerate(self.runs):
            config_str = run.config_str
            hp_id__setting_id__list = run.hp_id__setting_id__list
            if config_str not in self.configstr_runset_dict.keys():
                runset = RunSet(self, hp_id__setting_id__list, config_str)
                self.configstr_runset_dict[config_str] = runset
                self.runsets.append(runset)
            runset = self.configstr_runset_dict[config_str]
            runset.add_run(run)
            runset.update_posteriors(prior_mean, prior_var)
            if not runset.in_list:
                runset.insert(global_runset.dn, global_runset)  # Top of the list.
            runset.reposition()
            if global_runset.dn != best_runset:
                best_runset = global_runset.dn
                num_trophies += 1
                self.best_runset_trophies.append(RunSetTrophy(i, best_runset))
            else:
                self.best_runset_trophies[-1].num_runs += 1
        # print("{} trophies".format(num_trophies))

    def evaluate(self):
        # Get the hyperparameters and the runs.
        self.load_hp_definitions()
        self.load_runs()

        # Add the runs to a global runset, which will double as the sentinel of the runset list.
        global_runset = RunSet(None, None, None)
        for run in self.runs:
            global_runset.add_run(run)
        global_runset.sent = True
        global_runset.insert(global_runset, global_runset)

        # If max_runs is set, discard all later runs.
        if self.args.max_runs and (self.args.max_runs < len(self.runs)):
            self.runs = self.runs[0:self.args.max_runs]

        # Populate the runset list.
        self.populate_runsets(global_runset)

        # Analyze the search progress, based on the expected performance
        # obtained by stopping the search after some number of runs.
        num_runs = len(self.runs)
        xs = np.zeros((num_runs))
        ys = np.zeros((num_runs))
        ds = np.zeros((num_runs))
        x = 0
        # Write the header.
        headers = ' '
        for hp in self.hparams:
            if hp.in_hp_section and hp.has_multiple_values:
                width = max(MIN_COL_WID, len(hp.name))
                format_string = ' {' + ':{}s'.format(width) + '}'
                headers += format_string.format(hp.name)
        headers += 'BEST FOR   ' + 'EST HPMAX  ' + 'RUNS  ' + 'BEST'
        print(headers)
        for trophy in self.best_runset_trophies:
            trophy.runset.runs.sort(key=get_neg_run_mean)
            best = '{}'.format(trophy.runset.runs[0].run_name)  # To show only the best run for each runset.
            print(" {}{:3d} runs   {:9.6f}  {:3d}   {}".format(trophy.runset.report_configuration_string(),
                trophy.num_runs, trophy.runset.post_mean, len(trophy.runset.runs), best))
            y = trophy.runset.post_mean
            d = math.sqrt(trophy.runset.post_var)
            for i in range(trophy.num_runs):
                xs[x] = x + 1
                ys[x] = y
                ds[x] = d
                x += 1
        print(headers)
        print("  History of the best hyperparameter combination after each of the {} completed runs.".format(len(self.runs)))

        # Plot the search progress.
        y_axis_label = "Posterior estimate of {}".format(self.args.metric)
        plot(xs, ys, ds, self.args.job, y_axis_label)


def parse_args(args_list=None):
    example_text = '''Example usage:\n  Evaluate the results of a hyperparameter tuning job:\n    (In rl_nexus...) python scripts/eval_hp_search.py job411'''
    parser = argparse.ArgumentParser(description='Evaluate the results of a hyperparameter tuning job.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=example_text)
    parser.add_argument('job', action='store', help='Name of the job.')
    parser.add_argument('--no_download', action='store_true', help='To save time by skipping download of runs for a completed, previously viewed job.')
    parser.add_argument('--job_dir', action='store', help='Path to the parent directory of the given job, where files will be stored. Defaults to dilbert/jobs/', default='../jobs')
    parser.add_argument('--max_runs', action='store', help='Terminate the evaluation after this many runs.', type=int, default=0)
    parser.add_argument('--metric', action='store', help='(For old jobs) Name of the metric maximized by HP tuning. Defaults to hpmax.', default='hpmax')
    parser.add_argument('--num_reports_per_run', action='store', help='(For old jobs) Expected number of metric reports in each run.', type=int, default=1)
    parser.add_argument('--hp_def_file', action='store', help='(For old jobs) Name of the file defining the HPs.', default='uploaded_hp_config.yaml')
    return parser.parse_args(args_list)


if __name__ == '__main__':
    args = parse_args()
    search_history = SearchHistory(args)
    search_history.evaluate()
