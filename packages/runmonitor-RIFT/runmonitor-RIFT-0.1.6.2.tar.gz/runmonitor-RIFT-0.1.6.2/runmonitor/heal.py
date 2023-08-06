#!/usr/bin/env python

import os

def check_error(ile,rd=None):
	linelist = []

	if rd == None:
		rd = os.getcwd()

	dagman = open(os.path.join(rd,"marginalize_intrinsic_parameters_BasicIterationWorkflow.dag.dagman.out"))
	dag_list = dagman.readlines()[::-1]
	dagman.close()

	for line in dag_list:
        	linelist.append(line)
       		if ("ERROR: the following job(s) failed" in line):
                	break
        	else:
                	if (len(linelist) > 12):
                        	linelist.pop(0)

	linelist = linelist[::-1]

	if (ile):
		job_id = linelist[7].split()[5].split(".")[0].strip("(").strip()
		print(job_id)
		return job_id
	else:
		error_file = linelist[8].split()[5].strip()
		print(error_file)
		return error_file

def check_effective_samples_error(iteration,rd=None):
	import glob
	import sys

	if rd == None:
		rd = os.getcwd()

	filename = glob.glob(rd+"/iteration_" + str(iteration) + "_cip/logs/cip*.err")[0]
	err = open(filename)
	err_lines = err.readlines()
	err.close()

	for item in err_lines[::-1]:
        	if ("Effective samples = nan" in item):
                	print(True)
                	return True
	print(False)
	return False

def get_ile_job(rd=None):
	check_error(True,rd)

def check_encodings_error(iteration, job_id,rd=None):
	import glob
	import sys
	
	if rd == None:
		rd = os.getcwd()
             

	filename = glob.glob(rd+"/iteration_" + str(iteration) + "_ile/logs/ILE*" + str(job_id) + "*.err")[0]

	err = open(filename)
	err_lines = err.readlines()
	err.close()

	for item in err_lines[::-1]:
		if ("No module named 'encodings'" in item):
			print(True)
			return True
	print(False)
	return False
