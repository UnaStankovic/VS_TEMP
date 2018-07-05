from subprocess import check_output, CalledProcessError, Popen, PIPE
from file_work import coverage_array_creator, file_opener, find_files, write_array_to_file, delete_by_extension
import os
import time

def check_outputs(command, string):
	try:
		check_output(['bash', '-c', command])
		print(string)
	except CalledProcessError:
		print("CalledProcessError")
		exit()

def run_gcov():
	found_files = find_files(".gcda", ".")
	for f in found_files:
		command = 'gcov ' + f
		check_outputs(command,"Successfully generated .c.gcov.")
	return 1
	
	
def run_test(command, input):
	p = Popen(command, shell=False, stdin=PIPE,stdout=PIPE,stderr=PIPE, universal_newlines=True)
	p.stdin.write(input)
	p.stdin.close()
	#print(p.stdout.read())
	p.wait()
	
def run_tests(path):
	test_info_file = os.path.join(path,"test_info.run")
	with open(test_info_file) as f:
		test_info = f.readlines()
	test_info = [x.rstrip() for x in test_info] 
	for test_name,test_command,test_input in zip(test_info[0::3], test_info[1::3], test_info[2::3]):
		delete_by_extension(os.curdir, ".gcda")
		#delete_by_extension(os.curdir, ".gcno")
		delete_by_extension(os.curdir, ".gcov")
		run_test(test_command, test_input)
		run_gcov()
		merge_gcovs(test_name)

	delete_by_extension(os.curdir, ".gcda")
	delete_by_extension(os.curdir, ".gcov")
	delete_by_extension(os.curdir, ".gcno")
	#command = './test'
	#check_outputs(command, "Successfully runned test.")
	#return run_gcov()

def run_gcc(found):
	command = 'gcc -g -Wall -fprofile-arcs -ftest-coverage -O0 -o test ' + ' '.join(found)
	check_outputs(command,"Successfully compiled with gcc.The test sample will be run now." )
	#return run_tests()
	
def merge_gcovs(test_name):
	found_files = find_files(".gcov", ".")
	merged = []
	for f in found_files:
		opened = file_opener(f)
		merged.append(coverage_array_creator(opened))
	merged = [item for sublist in merged for item in sublist]
	print("Merged gcovs for one test:")
	#print(merged)
	
	merged_int = [ int(i) if i!="#####" else 0 for i in merged]
	print(merged_int)
	prefix = "merged_gcov"
	extension = "pathdata"
	full_name = prefix+"."+test_name+"."+extension
	write_array_to_file(merged_int, full_name) #"merged_gcov.0.pathdata"
	