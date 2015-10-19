#!/usr/bin/env python2

import unittest
import os

from simulator import run_simulator
from base.prototype import Job

from fcfs_scheduler import FcfsScheduler

from conservative_scheduler import ConservativeScheduler
from double_conservative_scheduler import DoubleConservativeScheduler

from easy_backfill_scheduler import EasyBackfillScheduler

from double_easy_backfill_scheduler import DoubleEasyBackfillScheduler
from head_double_easy_scheduler import HeadDoubleEasyScheduler
from tail_double_easy_scheduler import TailDoubleEasyScheduler
from shrinking_easy_scheduler import ShrinkingEasyScheduler

from easy_sjbf_scheduler import EasySjbfScheduler
from reverse_easy_scheduler import ReverseEasyScheduler

from maui_scheduler import MauiScheduler, Weights
from greedy_easy_backfill_scheduler import GreedyEasyBackfillScheduler
from lookahead_easy_backfill_scheduler import LookAheadEasyBackFillScheduler

from easy_plus_plus_scheduler import EasyPlusPlusScheduler
from common_dist_easy_plus_plus_scheduler import CommonDistEasyPlusPlusScheduler

from orig_probabilistic_easy_scheduler import OrigProbabilisticEasyScheduler
#from probabilistic_nodes_easy_scheduler import ProbabilisticNodesEasyScheduler
#from probabilistic_alpha_easy_scheduler import ProbabilisticAlphaEasyScheduler
#from probabilistic_linear_scale_easy_scheduler import ProbabilisticLinearScaleEasyScheduler
#from shrinking_alpha_easy_scheduler import ShrinkingAlphaEasyScheduler

from alpha_easy_scheduler import AlphaEasyScheduler
#from alpha_easy_plus_plus_scheduler import AlphaEasyPlusPlusScheduler


from perfect_easy_backfill_scheduler import PerfectEasyBackfillScheduler
from double_perfect_easy_backfill_scheduler import DoublePerfectEasyBackfillScheduler


from easy_prediction_backfill_scheduler import EasyPredictionBackfillScheduler

from base.prototype import _job_inputs_to_jobs
from base.workload_parser import parse_lines

def parse_jobs_test_input(input_file_name):
    """
    Assumption: Job details are 'correct': submit_time,
    num_required_processors and duration are non-negative, job id is
    unique, and the amount of processors requested by the job is never more
    than the total available processors
    """
    input_file = open(input_file_name) # openning of the specified file for reading
    jobs = []

    for line in input_file:
        if len(line.strip()) == 0: # skip empty lines (.strip() removes leading and trailing whitspace)
            continue
        if line.startswith('#'): # skip comments
            continue

        (str_j_submit_time, j_id, str_j_estimated_run_time, str_j_processors, \
         str_j_actual_run_time, str_j_admin_QoS, str_j_user_QoS, j_user_id) = line.split()

        j_submit_time        = int(str_j_submit_time)
        j_estimated_run_time = int(str_j_estimated_run_time)
        j_actual_run_time    = int(str_j_actual_run_time)
        j_processors         = int(str_j_processors)
	

        if j_estimated_run_time >= j_actual_run_time and j_submit_time >= 0 and j_processors > 0 and j_actual_run_time >= 0:
            j_admin_QoS = int(str_j_admin_QoS)
            j_user_QoS  = int(str_j_user_QoS)
            newJob = Job(j_id, j_estimated_run_time, j_actual_run_time, \
                         j_processors, j_submit_time, j_admin_QoS, j_user_QoS, j_user_id)
            jobs.append(newJob)

    input_file.close()

    return jobs

def run_test_simulator(num_processors, test_input_file, scheduler):
    return run_simulator(
           num_processors = num_processors,
           jobs = parse_jobs_test_input(test_input_file),
           scheduler = scheduler,
           output_swf = None,
           input_file = None,
           no_stats = True
       )

INPUT_FILE_DIR = os.path.dirname(__file__) + "/Input_test_files"

NUM_PROCESSORS=100
options = {"num_processors":NUM_PROCESSORS,"scheduler":{"predictor":{"name":"predictor_tsafrir"},"corrector":{"name":"reqtime"}}}

def feasibility_check_of_cpu_snapshot(jobs, cpu_snapshot):
    assert cpu_snapshot.CpuSlicesTestFeasibility()

    #cpu_snapshot._restore_old_slices()
    #cpu_snapshot.printCpuSlices()

    from base.prototype import Job
    j = Job(1, 1, 1, 1, 1)

    for job in jobs:
        j.id = job.id
        j.num_required_processors = job.num_required_processors
        j.start_to_run_at_time = job.start_to_run_at_time
        j.predicted_run_time = job.actual_run_time 
        cpu_snapshot.delJobFromCpuSlices(j)

    assert cpu_snapshot.CpuSlicesTestEmptyFeasibility()


def simulator_finish_time(simul):
	last_slice = simul.scheduler.cpu_snapshot.archive_of_old_slices[-1]
	return last_slice.start_time + last_slice.duration

def get_id_last_job(simul):
	last_slice = simul.scheduler.cpu_snapshot.archive_of_old_slices[-1]
	if(len(last_slice.job_ids) != 1):
		raise Exception("There is more than one job at the end")
	
	return last_slice.job_ids.pop()


def get_jobs_at(simul, time):
	jobs = simul.scheduler.cpu_snapshot.jobs_at(time)
	return jobs


# TODO: test each scheduler so it calls CpuSnapshot.delJobFromCpuSlices when
#       rescheduling a job or checking backfill legality (e.g. Maui)

class test_Simulator(unittest.TestCase):


    def test_basic_easyPredictionBackfill(self):
	    specoptions = {"num_processors":2,"scheduler":{"predictor":{"name":"predictor_from_think_time"},"corrector":{"name":"reqtime"}}}
	    
	    scheduler = EasyPredictionBackfillScheduler(specoptions)
            simulator = run_simulator(
		    no_stats = True,
		    scheduler=scheduler,
		    num_processors=2,
		    jobs = _job_inputs_to_jobs(parse_lines(open(INPUT_FILE_DIR + "/estimation_starvation.swf")),2))
	    
	    if simulator_finish_time(simulator) != 16:
		    raise Exception("Wrong finish time")
	    if get_id_last_job(simulator) != 2:
		    raise Exception("Wrong last job")
	    
	    scheduler = EasyPredictionBackfillScheduler(specoptions)
            simulator = run_simulator(
		    no_stats = True,
		    scheduler=scheduler,
		    num_processors=2,
		    jobs = _job_inputs_to_jobs(parse_lines(open(INPUT_FILE_DIR + "/estimation_tsafrir_exemple.swf")),2))
	    simulator.scheduler.cpu_snapshot._restore_old_slices()
	    if get_jobs_at(simulator, 0) != set([1]) :
		    raise Exception("Wrong scheduling!")
	    
	    scheduler = EasyPredictionBackfillScheduler(specoptions)
            simulator = run_simulator(
		    no_stats = True,
		    scheduler=scheduler,
		    num_processors=2,
		    jobs = _job_inputs_to_jobs(parse_lines(open(INPUT_FILE_DIR + "/overestimation_exemple.swf")),2))
	    
	    if simulator_finish_time(simulator) != 6:
		    raise Exception("Wrong finish time")
	    
	    specoptions["scheduler"]["predictor"]["name"] = "predictor_reqtime"
	    scheduler = EasyPredictionBackfillScheduler(specoptions)
            simulator = run_simulator(
		    no_stats = True,
		    scheduler=scheduler,
		    num_processors=2,
		    jobs = _job_inputs_to_jobs(parse_lines(open(INPUT_FILE_DIR + "/overestimation_exemple.swf")),2))
	    
	    if simulator_finish_time(simulator) != 8:
		    raise Exception("Wrong finish time")
	    
	    
	    
	    
	    
    # testing the easy plus plus scheduler 
    def test_basic_easyPlusPlusBackfill(self):
        for i in range(15):
            scheduler = EasyPlusPlusScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1,2]: # extreme number test 
            simulator = run_test_simulator(scheduler=EasyPlusPlusScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_easyPlusPlusBackfill(self):
        for i in range(16):
            scheduler = EasyPlusPlusScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/plus_plus_easy." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" "+str(job.finish_time))

    # test common dist easy++ 
    #def test_common_dist_easyPlusPlusBackfill(self):
        #for i in range(1):
            #scheduler = CommonDistEasyPlusPlusScheduler(options)
            #simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      #test_input_file = INPUT_FILE_DIR + "/common_dist_plus_plus_easy." + str(i))
            #feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            #for job in simulator.jobs:
                #self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" "+str(job.finish_time))


    def test_basic_probabilistic_easy(self): 
        for i in range(10):  
            scheduler = OrigProbabilisticEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1,2]: # extreme number test 
            simulator = run_test_simulator(scheduler=OrigProbabilisticEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "extreme, i="+str(i)+" "+str(job) + str(job.finish_time))


    def test_easy_probabilistic(self):
        for i in [0,1,2,3,4,5,7,8,9,10,11,12,13,14,15]: # skip 6, 16, 17, 18, 19, 20, 21  
            scheduler = OrigProbabilisticEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/probabilistic_easy." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" vs. "+str(job.finish_time))



    def test_basic_fcfs(self):
        for i in range(29):
            simulator = run_test_simulator(scheduler=FcfsScheduler(options), \
                                           num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                # the input jobs have their expected finish time encoded in their name.
                # to prevent id collisions their names are 'XX.YY' where XX is the expected time
                expected_finish_time = int(job.id.split(".")[0])
                self.assertEqual(expected_finish_time, job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=FcfsScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_fcfs(self):
        for i in range(8):
            simulator = run_test_simulator(scheduler=FcfsScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/fcfs_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))


    def test_basic_conservative(self):
        for i in range(29):
            simulator = run_test_simulator(scheduler=ConservativeScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=ConservativeScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

   
    def test_conservative(self):
        for i in range(9):
            simulator = run_test_simulator(scheduler=ConservativeScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/bf_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(2):
            simulator = run_test_simulator(scheduler=ConservativeScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/cons_bf_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))


    def test_double_conservative(self):
        for i in range(29):
            simulator = run_test_simulator(scheduler=DoubleConservativeScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))                
        for i in range(3):
            simulator = run_test_simulator(scheduler=DoubleConservativeScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/double_bf." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=DoubleConservativeScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

                
    # tesing the easy backfill scheduler 
    def test_basic_easyBackfill(self):
        for i in range(29):
            simulator = run_test_simulator(scheduler=EasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1,2]: # extreme number test 
            simulator = run_test_simulator(scheduler=EasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

   
    def test_easyBackfill(self):
        for i in range(9):
            simulator = run_test_simulator(scheduler=EasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/bf_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(4):
            simulator = run_test_simulator(scheduler=EasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/easy_bf_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_double_easyBackfill(self):
	for i in range(29):
            simulator = run_test_simulator(scheduler=DoubleEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in range(3):
            simulator = run_test_simulator(scheduler=DoubleEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/double_bf." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=DoubleEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
       
    def test_head_double_easy(self):
	for i in range(29):
            simulator = run_test_simulator(scheduler=HeadDoubleEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in range(4):
            simulator = run_test_simulator(scheduler=HeadDoubleEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/head_double_bf." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=HeadDoubleEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_tail_double_easy(self):
	for i in range(29):
            simulator = run_test_simulator(scheduler=TailDoubleEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(3):
            simulator = run_test_simulator(scheduler=TailDoubleEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/tail_double_bf." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=TailDoubleEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_shrinking_easy(self):
        for i in range(29):
            simulator = run_test_simulator(scheduler=ShrinkingEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(4):
            simulator = run_test_simulator(scheduler=ShrinkingEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/shrink_bf." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in [0,1,2]: # extreme number test 
            simulator = run_test_simulator(scheduler=ShrinkingEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_perfect_easy(self): 
	for i in range(29):
            simulator = run_test_simulator(scheduler=PerfectEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(3):
            simulator = run_test_simulator(scheduler=PerfectEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/perfect." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                

    def test_double_perfect_easy(self): 
	for i in range(29):
            simulator = run_test_simulator(scheduler=DoublePerfectEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(3):
            simulator = run_test_simulator(scheduler=DoublePerfectEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/double_perfect." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))


    def test_SJBF_easy(self): 
	for i in range(29):
            simulator = run_test_simulator(scheduler=EasySjbfScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(3):
            simulator = run_test_simulator(scheduler=EasySjbfScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/sjbf." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=EasySjbfScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                

    def test_reverse_easy(self): 
	for i in range(29):
            simulator = run_test_simulator(scheduler=ReverseEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0]:
            simulator = run_test_simulator(scheduler=ReverseEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/reverse." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

                
    # tests for maui             
    def test_basic_maui(self):
        for i in range(29):
            simulator = run_test_simulator(scheduler=MauiScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=MauiScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
    # below we test the weigths of maui: w_wtime, w_sld, w_user, w_bypass, w_admin, w_size
    def test_maui_wtime(self):
        # here we basically test that the maui with the default weights behaves as the easybackfill
        for i in range(9):
            simulator = run_test_simulator(scheduler=MauiScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/bf_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in range(1):
            simulator = run_test_simulator(scheduler=MauiScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/easy_bf_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_maui_wait_and_size(self):
        # testing w_size = number of processors (vs. w_wait):
        # (w_wtime, w_sld, w_user, w_bypass, w_admin, w_size)
        w_l = Weights(1, 0, 0, 0, 0, 0)
        w_b = Weights(0, 0, 0, 0, 0, -1)

        scheduler = MauiScheduler(options, weights_list = w_l, weights_backfill = w_b)
        simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/maui.size")
        feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
        for job in simulator.jobs:
            self.assertEqual(int(float(job.id)), job.finish_time, str(job)+" "+str(job.finish_time))

    def test_maui_admin_vs_userQoS(self):
        # testing the w_admin = admin QoS and w_user = user QoS:
        # (w_wtime, w_sld, w_user, w_bypass, w_admin, w_size)
        w_l = Weights(0, 0, 0, 0, 1, 0)
        w_b = Weights(0, 0, 1, 0, 0, 0)

        scheduler = MauiScheduler(options, weights_list = w_l, weights_backfill = w_b)
        simulator = run_test_simulator(scheduler=scheduler, \
                                  num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/maui.admin_vs_user")
        feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
        for job in simulator.jobs:
            self.assertEqual(int(float(job.id)), job.finish_time, str(job)+" "+str(job.finish_time))

    def test_maui_bypass_vs_slow_down(self):
        # testing the w_admin = admin QoS and w_user = user QoS:
        # (w_wtime, w_sld, w_user, w_bypass, w_admin, w_size)
        w_l = Weights(0, 0, 0, 1, 1, 0)
        w_b = Weights(0, 1.0, 0, 0, 0, 0)

        scheduler = MauiScheduler(options, weights_list = w_l, weights_backfill = w_b)
        simulator = run_test_simulator(scheduler=scheduler, \
                                  num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/maui.bypass_vs_sld")
        feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
        for job in simulator.jobs:
            self.assertEqual(int(float(job.id)), job.finish_time, str(job)+" "+str(job.finish_time))

    # testing the look ahead schedular 
    def test_basic_look_ahead_easyBackfill(self):
        for i in range(15):
            scheduler = LookAheadEasyBackFillScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=LookAheadEasyBackFillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_look_ahead_easyBackfill(self):
        for i in range(14):
            scheduler = LookAheadEasyBackFillScheduler(options, score_function_for_look_ahead)
            simulator = run_test_simulator(scheduler=scheduler, \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/look_ahead." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, \
                                 "i="+str(i)+" "+str(job) + str(job.finish_time))

    # testing the greedy scheduler 
    def test_basic_greedy_easyBackfill(self):
        for i in range(15):
            scheduler = GreedyEasyBackfillScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=GreedyEasyBackfillScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_greedy_easyBackfill(self):
	bf = (
    		lambda job :  job.user_estimated_run_time,
    		lambda job :  job.num_required_processors,
	)
        for i in range(6):
            scheduler = GreedyEasyBackfillScheduler(options, bf, score_function_for_greedy, 0)
            simulator = run_test_simulator(scheduler=scheduler, \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/greedyBF." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" "+str(job.finish_time))



"""
    def test_basic_probabilistic_nodes_easy(self): 
        for i in range(29):  
            scheduler = ProbabilisticNodesEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))


    def test_easy_probabilistic_nodes_easy(self):
        for i in [0,1]:  
            scheduler = ProbabilisticNodesEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/probabilistic_nodes_easy." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" vs. "+str(job.finish_time))

    def test_shrinking_alpha_easy(self):
        for i in []: #(29)
            simulator = run_test_simulator(scheduler=ShrinkingAlphaEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in []: #(5)
            simulator = run_test_simulator(scheduler=ShrinkingAlphaEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/shrink_bf." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))
                
        for i in [0]: # [0,1,3] extreme number test 
            simulator = run_test_simulator(scheduler=ShrinkingAlphaEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_basic_probabilistic_alpha_easy(self): 
        for i in range(29):  
            scheduler = ProbabilisticAlphaEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1]: # extreme number test 
            simulator = run_test_simulator(scheduler=ProbabilisticAlphaEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))


    def test_easy_probabilistic_alpha(self):
        for i in [0,1,2,6,10,11,16,17,19,20]:  
            scheduler = ProbabilisticAlphaEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/probabilistic_easy." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" vs. "+str(job.finish_time))


    def test_basic_alpha_easy(self): 
        for i in range(29):  
            scheduler = AlphaEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1, 3]: # extreme number test 
            simulator = run_test_simulator(scheduler=AlphaEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))



    def test_basic_probabilistic_linear_scale_easy(self): 
        for i in range(29):  
            scheduler = ProbabilisticLinearScaleEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1,3]: # extreme number test 
            simulator = run_test_simulator(scheduler=ProbabilisticEasyScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

    def test_easy_linear_scale_probabilistic(self):
        for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,19,20,21]: # skip 14, 18 , 15
            scheduler = ProbabilisticLinearScaleEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/probabilistic_easy." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" vs. "+str(job.finish_time))


    def test_alpha_easy(self):
        for i in [0,1,2,3]:  
            scheduler = AlphaEasyScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/alpha_easy." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" vs. "+str(job.finish_time))


    def test_basic_alpha_easy_plus_plus(self): 
        for i in range(29):  
            scheduler = AlphaEasyPlusPlusScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/basic_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

        for i in [0,1, 3]: # extreme number test 
            simulator = run_test_simulator(scheduler=AlphaEasyPlusPlusScheduler(options), \
                                      num_processors=NUM_PROCESSORS, test_input_file = INPUT_FILE_DIR + "/extreme_input." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job) + str(job.finish_time))

	
    def test_alpha_easy_plus_plus(self):
        for i in [0,4]:  
            scheduler = AlphaEasyPlusPlusScheduler(options)
            simulator = run_test_simulator(scheduler=scheduler, num_processors=NUM_PROCESSORS, \
                                      test_input_file = INPUT_FILE_DIR + "/alpha_easy." + str(i))
            feasibility_check_of_cpu_snapshot(simulator.jobs, simulator.scheduler.cpu_snapshot)
            for job in simulator.jobs:
                self.assertEqual(int(float(job.id)), job.finish_time, "i="+str(i)+" "+str(job)+" vs. "+str(job.finish_time))


"""

               
###########

def score_function_for_look_ahead(job):
    return job.num_required_processors

def score_function_for_greedy(list_of_jobs):
        return len(list_of_jobs) # returns the length of the list: and thus a list with more jobs is ranked higher


if __name__ == "__main__":
    try:
        import testoob
        testoob.main()
    except ImportError:
        import unittest
        unittest.main()
