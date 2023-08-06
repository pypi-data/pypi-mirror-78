#!/usr/bin/env python

def check_error():
	linelist = []

	dagman = open("marginalize_intrinsic_parameters_BasicIterationWorkflow.dag.dagman.out")
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
	error_file = linelist[8].split()[5].strip()

	print(error_file)

def check_effective_samples_error(iteration):
	import glob
	import sys

	filename = glob.glob("iteration_" + str(iteration) + "_cip/logs/cip*.err")[0]
	err = open(filename)
	err_lines = err.readlines()
	err.close()

	for item in err_lines[::-1]:
        	if ("Effective samples = nan" in item):
                	print(True)
                	sys.exit()
	print(False)
