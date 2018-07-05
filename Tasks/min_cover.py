from file_work import read_array_from_file
import numpy as np


	
# Compares two arrays of ints and checks if one is a subset of the other
# returns (Bool, Bool) 
# first Bool value says if the array1 is a subset of array2
# second Bool value says if the array2 is a subset of array1
# if array1 and array2 are equal (True,True) is returned
def compare_arrays(size, array1, array2):
    equal = True
    i = 0
    while equal and i<size:
        if array1[i] != array2[i]:
            equal = False
        i = i+1
    if equal:
        return (True, True)
    #print("Not equal")
    #print(i-1, array1[i-1], array2[i-1])
    if array1[i-1] < array2[i-1]:
        subset = True
        while subset and i<size:
            if array1[i] > array2[i]:
                return (False, False)
            i = i+1
        return (True, False)
    else:
        subset = True
        while subset and i<size:
            if array2[i] > array1[i]:
                return (False, False)
            i = i+1
        return (False, True)
		
		
# Find minimal set coverage from given array of sets
# Returns array of zeros and ones where ones represent indexes of sets which
# should be included in optimal set coverage
def min_set_coverage_optimal(all_data):
    num_of_arrays, size_of_array = all_data.shape
    added_sets = np.ones(num_of_arrays, dtype=int)
    for i in range(num_of_arrays):
        if added_sets[i]==1:
            for j in range(i+1, num_of_arrays):
                f_in_s, s_in_f = compare_arrays(size_of_array, all_data[i], all_data[j])
                if s_in_f:
                    added_sets[j] = 0 #if second is contained in first or equal to first ignore it from optimal set
                    #print(j, " is equal to ", i) if f_in_s else print(j, " is contained in ", i)
                else:
                    if f_in_s:
                        added_sets[i] = 0 #if first is in contained in second ignore first and end current iteration
                        #print(i, " is contained in ", j)
                        break
    return added_sets
    
		
# Find minimal set coverage from given array of sets
# Returns array of zeros and ones where ones represent indexes of sets which
# should be included in a set coverage	
# Uses greedy implementation so the result is NOT optimal
def min_set_coverage_greedy(all_data):
    num_of_arrays, size_of_array = all_data.shape
    covered_elements = np.zeros(size_of_array, dtype=int)
    num_of_arrays, size_of_array = all_data.shape
    #added_sets = np.full(num_of_arrays, False)
    added_sets = np.zeros(num_of_arrays, dtype=int)
    
    end = False
    while not end:
        sum_array = np.zeros(num_of_arrays, dtype=int)
        for i in range(num_of_arrays):
            if added_sets[i]==0:
                res = covered_elements<all_data[i]
                #print("array no. ", i)
                #print(res.astype(np.int))
                #print(np.sum(res.astype(np.int)))
                sum_array[i] = np.sum(res.astype(np.int))
        #print(sum_array)
        max_index = np.argmax(sum_array)
        if (sum_array[max_index] == 0):
            end = True
        else:
            #print("adding array ", max_index)
            covered_elements = covered_elements + res.astype(np.int)
            added_sets[max_index] = 1
    return added_sets
		
		
def make_test_data():
	all_data = []

	#data1 = np.array(read_array_from_file("..\Examples\01-pathdata\merged_gcov.1234.pathdata"))
	#data2 = np.array(read_array_from_file("..\Examples\01-pathdata\merged_gcov.1235.pathdata"))
	#data3 = np.array(read_array_from_file("..\Examples\01-pathdata\merged_gcov.4321.pathdata"))
	data1 = np.array(read_array_from_file("../Examples/01-pathdata/merged_gcov.1234.pathdata"))
	data2 = np.array(read_array_from_file("../Examples/01-pathdata/merged_gcov.1235.pathdata"))
	data3 = np.array(read_array_from_file("../Examples/01-pathdata/merged_gcov.4321.pathdata"))
	data4 = np.array(data1)
	data4[0] = 0

	#1 and 2 are equal
	#4 is containd in 1

	all_data = np.array([data1, data2, data3, data4])
	size = all_data[0].size
	#for i in range(1, all_data.shape[0]):
	#	assert size == all_data[i].size
	
	return all_data

	
def test_algorithms():
	all_data = make_test_data()
	
	print("Optimal algorithm")
	print(min_set_coverage_optimal(all_data))
	print("Greedy algorithm")
	print(min_set_coverage_greedy(all_data))
	
	