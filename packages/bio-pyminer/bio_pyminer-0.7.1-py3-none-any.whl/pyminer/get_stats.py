#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
from copy import deepcopy
import ray
try:
    from pyminer.common_functions import *
except:
    from common_functions import *
#import pandas as pd


##############################################################

##########################################################################
parser = argparse.ArgumentParser()

## global arguments
parser.add_argument(
    '-infile','-in','-i','-input',
    dest='infile',
    type=str)

parser.add_argument(
    "-sample_groups",
    help='if you know how which samples belong to which groups, feed in a file that has the samples in the first column, and their group number (index starting at 0), in the second column. The IDs must be in the same order as in the infile too.',
    dest = 'sample_groups',
    type = str)

parser.add_argument(
    "-classes",
    help='if there are classes to compare, put the annotation table in this argument',
    dest = 'class_file',
    type = str)

parser.add_argument(
    "-within_group",
    help='if you know how which samples belong to which groups, feed in a file that has the samples in the first column, and their group number (index starting at 0), in the second column. The IDs must be in the same order as in the infile too.',
    dest = 'within_group',
    type = int)

parser.add_argument(
    "-out_dir","-o","-out",
    help='if you know how which samples belong to which groups, feed in a file that has the samples in the first column, and their group number (index starting at 0), in the second column. The IDs must be in the same order as in the infile too.',
    dest = 'out_dir',
    type = str)

parser.add_argument(
    "-species","-s",
    help = 'what species is this? Must be gProfiler compatible.',
    dest = 'species',
    type = str,
    default = 'hsapiens')

parser.add_argument(
    '-no_gProfile',
    help = 'should we do the automated gprofiler results?',
    default = False,
    action = 'store_true')

parser.add_argument(
    "-FDR","-fdr","-fdr_cutoff",
    help='The desired Benjamini-Hochberg False Discovery Rate (FDR) for multiple comparisons correction (default = 0.05)',
    dest = 'FDR_cutoff',
    type = float,
    default = 0.05)

parser.add_argument(
    "-Zscore","-Z_score_cutoff","-Z","-zscore","-z",
    help='The desired False Discovery Rate (FDR) for multiple comparisons correction (default = 0.05)',
    dest = 'Zscore',
    type = float,
    default = 2.0)

parser.add_argument(
    '-hdf5',
    help = 'The input file is an HDF5 file',
    default = False,
    action = 'store_true')

parser.add_argument(
    "-ID_list","-ids",
    help = 'If we are using an hdf5 file, give the row-wise IDs in this new line delimeted file',
    type = str)

parser.add_argument(
    "-columns","-cols",
    help = 'If we are using an hdf5 file, give the column-wise IDs in this new line delimeted file',
    type = str)

parser.add_argument(
    '-rows',
    help = 'if the samples are in rows, and variables are in columns',
    default = False,
    action = 'store_true')

parser.add_argument(
    "-log",'-log2','-log_transform',
    help='do a log transformation prior to clustering',
    action = 'store_true',
    default = False)

parser.add_argument(
    '-lin_norm',
    help = 'should we normalize the rows before doing the stats?',
    default = False,
    action = 'store_true')

parser.add_argument(
    '-processes', '-p',
    help = 'The number of processes to use. Default will be the number of available threads.',
    default = None,
    type = int)

args = parser.parse_args()
##########################################################################
args.infile = os.path.realpath(args.infile)
if args.out_dir == None:
    args.out_dir = get_file_path(args.infile)+'sample_clustering_and_summary/'
if args.out_dir[-1]!='/':
    args.out_dir+='/'

sample_dir = args.out_dir
temp = args.out_dir
cmd('mkdir '+args.out_dir)

##############################################################################
## read in the dataset and sample groups

if args.within_group==None:
    sample_group_table = read_table(args.sample_groups)

    sample_group_table_np = np.array(sample_group_table)
    sample_group_order = np.transpose(sample_group_table_np[:,0])
    sorted_list_of_ids = list(sample_group_order)

    grouping_vector = list(np.transpose(sample_group_table_np[:,1]))
    #print(grouping_vector)
    #sys.exit()
else:
    if args.class_file==None:
        sys.exit("to run within class analysis, we need the classes annotation file: -classes")
    orig_sample_group_table = read_table(args.sample_groups)
    orig_sample_group_table_np = np.array(orig_sample_group_table)
    orig_sample_group_order = np.transpose(orig_sample_group_table_np[:,0])
    orig_sorted_list_of_ids = list(orig_sample_group_order)
    orig_grouping_vector = list(np.transpose(orig_sample_group_table_np[:,1]))
    ## we're going to switch around the normal sample groups with the 
    ## classes that are read in 
    class_table_np = np.array(read_table(args.class_file))
    class_labels = list(set(class_table_np[:,1].tolist()))
    class_labels = sorted(class_labels)
    class_hash = {key:value for value, key in enumerate(class_labels)}
    alias_dict = {key:value for key, value in enumerate(class_labels)}
    ## make a table to define which class is which group
    class_index_table = []
    for c in class_labels:
        class_index_table.append([c,class_hash[c]])
        #print(class_index_table[-1])
    ## figure out which indices to keep
    subset_col_idxs=[]
    for i in range(0,len(orig_grouping_vector)):
        if str(orig_grouping_vector[i])==str(float(args.within_group)):
            subset_col_idxs.append(i)
        #print(orig_grouping_vector[i])
    #print(subset_col_idxs,float(args.within_group))
    sample_group_table_np = class_table_np[subset_col_idxs]
    ## go through the annotation table and make
    for i in range(len(subset_col_idxs)):
        sample_group_table_np[i,1]=class_hash[sample_group_table_np[i,1]]
    #print(sample_group_table_np)

    sample_group_table = sample_group_table_np.tolist()
    for i in range(len(sample_group_table)):
        sample_group_table[i][1]=float(sample_group_table[i][1])
    sample_group_table_np = np.array(sample_group_table)
    sample_group_order = np.transpose(sample_group_table_np[:,0])
    sorted_list_of_ids = list(sample_group_order)
    grouping_vector = list(np.transpose(sample_group_table_np[:,1]))
    subset_col_idxs=np.array(subset_col_idxs,dtype=int)
    #print(grouping_vector)
    


if len(list(set(grouping_vector))) == 1:
    one_group = True
    sys.exit('only one sample group, nothing to calculate')
else:
    one_group = False




sample_cluster_ids = []
for i in range(0,len(sample_group_table)):
    
    ## THIS IS IMPORTANT
    ## here we assume that the samples are all listed in the same order as in '-infile'
    ## we also assume that the group indexing starts at 0
    sample_cluster_ids.append(sample_group_table[i][1])
sample_cluster_ids = list(map(int,sample_cluster_ids))
sample_k_lists = []
for i in range(0,max(sample_cluster_ids)+1):
    sample_k_lists.append([])
#print(len(sample_k_lists))
## now populate the list of lists
for i in range(0,len(sample_cluster_ids)):
    ## this appends the sample index to 
    #print(sample_cluster_ids[i])
    sample_k_lists[sample_cluster_ids[i]].append(i)

#print(sample_k_lists)




## check for formatting
if not args.hdf5:
    full_expression_str = read_table(args.infile)
    title = full_expression_str[0]
    full_expression_np = np.array(full_expression_str)
    row_names = full_expression_np[1:,0]
    full_expression = np.array(full_expression_np[1:,1:],dtype = float)
else:
    row_names = read_file(args.ID_list,'lines')
    title = read_file(args.columns,'lines')
    print('making a maliable hdf5 file to preserve the original data')
    cmd('cp '+args.infile+' '+args.infile+'_copy')
    import h5py
    print('reading in hdf5 file')
    infile_path = args.infile+'_copy'
    h5f = h5py.File(infile_path, 'r+')
    full_expression=h5f["infile"]

##########################################################
## if we're doing the subset analysis, subset which columns to include
if args.within_group!=None:
    full_expression = full_expression[:,subset_col_idxs]
    temp_title = np.array(title[1:])
    title = [title[0]] + temp_title[subset_col_idxs].tolist()
    print(row_names)

##########################################################
if args.rows:
    full_expression = np.transpose(full_expression)
    temp_col = ["variables"] + row_names.tolist()
    title = temp_col[:]


if title[1:] != sorted_list_of_ids:
    print('length of columns',len(title[1:]))
    print('length of sample_groups',sorted_list_of_ids)
    for i in range(1,len(title)):
        if title[i] != sorted_list_of_ids[i-1]:
            print('on line',i,'ID_list',title[i],'',sorted_list_of_ids[i-1])
    sys.exit("the sample group ids have to be in the same order as in the input matrix")



def lin_norm_rows(in_mat,min_range=0,max_range=1):
    in_mat = np.transpose(np.array(in_mat))
    in_mat = in_mat - np.min(in_mat, axis = 0)
    in_mat = in_mat / np.max(in_mat, axis = 0)
    in_mat[np.isnan(in_mat)]=0
    return(np.transpose(in_mat))


## make all of the nans equal to zero
full_expression[np.isnan(full_expression)] = 0.0
if args.log:
    full_expression = np.log2(full_expression-np.min(full_expression)+1)
if args.lin_norm:
    full_expression = lin_norm_rows(full_expression)

IDlist = list(row_names)

##############################################################################
## calculate the sample level Z-scores


## first normalize the expression matrix linearly between 1 and 2
#sample_var_enrichment = lin_norm_rows(full_expression) + 1
if not args.hdf5:
    sample_var_enrichment = full_expression

    ## then calculate the mean for each variable
    norm_row_means = np.transpose(np.array([np.mean(sample_var_enrichment, axis = 1)]))
    #print(norm_row_means)
    ## then calculate the sd for each variable
    norm_row_sd = np.transpose(np.array([np.std(sample_var_enrichment, axis = 1)]))
    #print(norm_row_sd)
    ## then calculate the delta for each variable
    norm_row_delta = sample_var_enrichment - norm_row_means

    ## calculate the z-score (ie: how many standard deviations away from the mean is each sample)
    sample_var_enrichment_numeric = norm_row_delta/norm_row_sd
    #print(sample_var_enrichment_numeric)
    #sys.exit()



    ## add the titles

    sample_var_enrichment = np.array([title[1:]] + sample_var_enrichment_numeric.tolist()).tolist()

    temp_ids = ['variables']+IDlist
    for i in range(0,len(sample_var_enrichment)):
        sample_var_enrichment[i]=[temp_ids[i]]+sample_var_enrichment[i]

    #sample_var_enrichment = np.hstack((row_titles,sample_var_enrichment))

    write_table(sample_var_enrichment, sample_dir+'sample_var_enrichment_Zscores.txt')




##############################################################################
## go through each group and generate mean and sd summaries, then write to file

################################
## ray functions
def get_indices(threads, num_genes):
    indices_list = []
    for t in range(threads):
        indices_list.append([])
    temp_idx = 0
    while temp_idx < num_genes:
        for t in range(threads):
            if temp_idx < num_genes:
                indices_list[t].append(temp_idx)
                temp_idx += 1
    return(indices_list)


def get_num_rows_from_dict_lists(dict_list):
    ## goes through all of the indices & returns the number of dims
    row_dims = 0
    for temp_dict in dict_list:
        for temp_key in list(temp_dict.keys()):
            #print(temp_key)
            if temp_key > row_dims:
                row_dims = temp_key
    return(row_dims+1)


def get_num_cols_from_dict_lists(dict_list):
    ## first get the dimentions
    first_key = list(dict_list[0].keys())[0]
    first = dict_list[0][first_key]
    if type(first) == list:
        col_dims = len(first)
    else:
        col_dims = 1
    return(col_dims)


def ray_dicts_to_array(dict_list):
    row_dims = get_num_rows_from_dict_lists(dict_list)
    col_dims = get_num_cols_from_dict_lists(dict_list)
    out_array = np.zeros((row_dims, col_dims))
    print(out_array)
    for temp_dict in dict_list:
        for idx, value in temp_dict.items():
            #print(idx)
            #print(value)
            out_array[idx] = value
    return(out_array)


@ray.remote
def ray_get_global_express_stats(indices, 
                                 ray_full_expression,
                                 hdf5_file = None):
    ## load the ray_full_express if it's hdf5
    if hdf5_file is not None:
        h5f = h5py.File(hdf5_file, 'r')
        ray_full_expression=h5f["infile"]

    global_percent_express_dict = {index:None for index in indices}
    global_non_zero_mean_dict = {index:None for index in indices}

    ray_count = 0

    for index in indices:
        if ray_count % 250 == 0:
            print("worker is:",ray_count/len(indices)*100," percent done")
        temp_binary = np.array(ray_full_expression[index,:] > 0,dtype=bool)
        temp_binary_int = np.array(deepcopy(temp_binary),dtype=int)
        temp_num_express = np.sum(temp_binary_int)
        global_percent_express = temp_num_express/temp_binary_int.shape[0]
        global_non_zero_mean = np.sum(ray_full_expression[index,:])/temp_num_express
        global_percent_express_dict[index] = global_percent_express
        global_non_zero_mean_dict[index] = global_non_zero_mean

        ray_count+=1

    if hdf5_file is not None:
        h5f.close()

    return(global_percent_express_dict, global_non_zero_mean_dict)


@ray.remote
def ray_get_cell_type_express_stats(indices,
                                    ray_full_expression,
                                    ray_list_of_k_sample_indices,
                                    hdf5_file = None):
    ## load the ray_full_express if it's hdf5
    if hdf5_file is not None:
        h5f = h5py.File(hdf5_file, 'r')
        ray_full_expression=h5f["infile"]

    group_percent_express_dict = {index:None for index in indices}
    group_non_zero_mean_dict = {index:None for index in indices}
    
    ray_count = 0
    
    for index in indices:
        if ray_count % 250 == 0:
            print("worker is:",ray_count/len(indices)*100," percent done")

        group_percent_express = []
        group_non_zero_mean = []
        for i in range(len(list_of_k_sample_indices)):
            temp_binary = np.array(ray_full_expression[index,list_of_k_sample_indices[i]] > 0,dtype=bool)
            temp_binary_int = np.array(deepcopy(temp_binary),dtype=int)
            temp_num_express = np.sum(temp_binary_int)
            temp_percent_express = temp_num_express/len(list_of_k_sample_indices[i])
            temp_non_zero_mean = np.sum(ray_full_expression[index,list_of_k_sample_indices[i]])/temp_num_express
            group_percent_express.append(temp_percent_express)
            group_non_zero_mean.append(temp_non_zero_mean)

        group_percent_express_dict[index] = group_percent_express
        group_non_zero_mean_dict[index] = group_non_zero_mean
        
        ray_count += 1
    
    if hdf5_file is not None:
        h5f.close()
    return(group_percent_express_dict, group_non_zero_mean_dict)

#####
## anova functions

@ray.remote
def ray_get_anova(indices,
                  ray_full_expression,
                  ray_list_of_k_sample_indices,
                  hdf5_file = None):
    ## load the ray_full_express if it's hdf5
    if hdf5_file is not None:
        h5f = h5py.File(hdf5_file, 'r')
        ray_full_expression=h5f["infile"]

    aov_dict = {index:None for index in indices}

    ray_count = 0
    for index in indices:
        if ray_count % 250 == 0:
            print("worker is:",ray_count/len(indices)*100," percent done")
        if np.sum(ray_full_expression[index,:]) == 0:
            aov_dict[index] = [np.nan,np.nan]
        list_of_group_values=[]
        for group in range(0,len(ray_list_of_k_sample_indices)):
            #print(len(list_of_k_sample_indices[group]))
            list_of_group_values.append(ray_full_expression[index,ray_list_of_k_sample_indices[group]])
            #print(np.shape(list_of_group_values[-1]))
            #print(list_of_group_values[-1])
            
        return_val = list(aov(*list_of_group_values))
        aov_dict[index] = return_val

        ray_count += 1

    if hdf5_file is not None:
        h5f.close()

    return(aov_dict)











## /ray functions
################################


list_of_k_sample_indices = sample_k_lists
#print(list_of_k_sample_indices)

if not one_group:
    
    sample_names = list(title)[1:]
    #print(sample_names)
    # list_of_k_sample_indices=[]
    
    # for k in sample_k_lists:
    #     print(k)
    #     temp_indices_list=[]
    #     for i in range(0,len(k)):
    #         temp_indices_list.append(sample_names.index(k[i]))
    #     list_of_k_sample_indices.append(temp_indices_list)


    #print(list_of_k_sample_indices)
    list_of_k_sample_indices = np.array(list_of_k_sample_indices)

    ## initialize mean and sd output tables
    #print(list_of_k_sample_indices[0])
    #test=full_expression[:,list_of_k_sample_indices[0]]
    #print(np.mean(test.astype('float32'), axis = 1))
    #print(full_expression[:,list_of_k_sample_indices[0]].shape)



    ## calculate the means accross rows
    all_sample_mean = np.transpose(np.array([np.mean(full_expression, axis=1)]))
    all_sample_sd = np.transpose(np.array([np.std(full_expression, axis=1)]))
    k_group_means = np.transpose(np.array([np.mean(full_expression[:,list_of_k_sample_indices[0]], axis=1)]))
    k_group_sd = np.transpose(np.array([np.std(full_expression[:,list_of_k_sample_indices[0]], axis=1)]))

    for k in range(1,len(list_of_k_sample_indices)):## start from 1 because we already initiated it on the first col
        ## calc row means
        new_mean_col = np.transpose(np.array([np.mean(full_expression[:,list_of_k_sample_indices[k]], axis=1)]))
        k_group_means = np.hstack((k_group_means, new_mean_col))
    
        ## calc sd
        new_sd_col = np.transpose(np.array([np.std(full_expression[:,list_of_k_sample_indices[k]], axis=1)]))
        k_group_sd = np.hstack((k_group_sd, new_sd_col))

    ###########################################################
    ## TODO
    ## calculate the percent non-zero for each cell type
    print("calculating global percent expressed and mean non-zero expression")
    k_group_percent_express = np.zeros((full_expression.shape[0], len(list_of_k_sample_indices))) ## the percentage 
    ratio_percent_express = np.zeros((full_expression.shape[0], len(list_of_k_sample_indices))) ## ratio of within cell type percent expression to global percent expression
    non_zero_mean_expression = np.zeros((full_expression.shape[0], len(list_of_k_sample_indices))) ## ratio of within cell type percent expression to global percent expression
    ratio_non_zero_mean_expression = np.zeros((full_expression.shape[0], len(list_of_k_sample_indices))) ## ratio of within cell type percent expression to global percent expression
    
    # #######################################################################################
    # ################## OLD ##############################
    # #####################################################
    # ## first do the global expression calculations
    if args.processes == 1:
        def get_global_express_stats(index):
            global full_expression
            temp_binary = np.array(full_expression[index,:] > 0,dtype=bool)
            temp_binary_int = np.array(deepcopy(temp_binary),dtype=int)
            temp_num_express = np.sum(temp_binary_int)
            global_percent_express = temp_num_express/temp_binary_int.shape[0]
            global_non_zero_mean = np.sum(full_expression[index,:])/temp_num_express
            return(global_percent_express, global_non_zero_mean)
        
        ## set up multi-threaded global stats
        ## global_percent_express, global_non_zero_mean
        threads = multiprocessing.cpu_count()
        pool = ThreadPool(threads)
        global_results = pool.map(get_global_express_stats,range(full_expression.shape[0]))
        pool.close()
        pool.join()

        ## separate results
        global_percent_express = []
        global_non_zero_mean = []
        for i in range(len(global_results)):
            global_percent_express.append(global_results[i][0])
            global_non_zero_mean.append(global_results[i][1])

        del global_results
        global_percent_express = np.array(global_percent_express)
        global_non_zero_mean = np.array(global_non_zero_mean)

        # ######################## OLD #####################################
        ## get cell type level results
        def get_cell_type_express_stats(index):
            global full_expression, list_of_k_sample_indices
            group_percent_express = []
            group_non_zero_mean = []
            for i in range(len(list_of_k_sample_indices)):
                temp_binary = np.array(full_expression[index,list_of_k_sample_indices[i]] > 0,dtype=bool)
                temp_binary_int = np.array(deepcopy(temp_binary),dtype=int)
                temp_num_express = np.sum(temp_binary_int)
                temp_percent_express = temp_num_express/len(list_of_k_sample_indices[i])
                temp_non_zero_mean = np.sum(full_expression[index,list_of_k_sample_indices[i]])/temp_num_express
                group_percent_express.append(temp_percent_express)
                group_non_zero_mean.append(temp_non_zero_mean)
            return(group_percent_express, group_non_zero_mean)


        ###########################################################
        ## set up multi-threaded global stats
        ## global_percent_express, global_non_zero_mean
        threads = multiprocessing.cpu_count()
        pool = ThreadPool(threads)
        group_results = pool.map(get_cell_type_express_stats,range(full_expression.shape[0]))
        pool.close()
        pool.join()
        
        for i in range(len(group_results)):
            k_group_percent_express[i,:] = group_results[i][0]
            non_zero_mean_expression[i,:] = group_results[i][1]
        del group_results

        print(k_group_percent_express)
        print(non_zero_mean_expression)
        

        ######################## /OLD #####################################

    #################### /OLD ###########################
    #################### NEW ############################
    else:
        if args.processes == None:
            args.processes = multiprocessing.cpu_count()
        threads = args.processes
        indices_list = get_indices(threads, full_expression.shape[0])
        
        ray.init()

        ###########
        if not args.hdf5:
            ray_full_expression = ray.put(full_expression)
        else:
            ## make copies of the input hdf5 file
            hdf5_file_list = []
            for t in range(threads):
                hdf5_file_list.append(args.infile+"_"+str(t))
                cmd('cp '+args.infile+" "+hdf5_file_list[-1])
        ###########

        r_jobs = []
        for t in range(threads):
            if not args.hdf5:
                r_jobs.append(ray_get_global_express_stats.remote(indices_list[t], 
                                                                  ray_full_expression))
            else:
                r_jobs.append(ray_get_global_express_stats.remote(indices_list[t], 
                                                                  None,
                                                                  hdf5_file = hdf5_file_list[t]))
        temp_r_results = ray.get(r_jobs)
        ray.shutdown()
    
        global_percent_express_dict_list = []
        global_non_zero_mean_dict_list = []

        for t in range(len(temp_r_results)):
            global_percent_express_dict_list.append(temp_r_results[t][0])
            global_non_zero_mean_dict_list.append(temp_r_results[t][1])

        global_percent_express = ray_dicts_to_array(global_percent_express_dict_list)
        global_non_zero_mean = ray_dicts_to_array(global_non_zero_mean_dict_list)

        global_percent_express = global_percent_express[:,0]
        global_non_zero_mean = global_non_zero_mean[:,0]

        print(global_percent_express)
        print(global_non_zero_mean)
        #################### /NEW ############################    
        #######################################################################################

        print("calculating percent expressed in cell types and mean non-zero expression")

        
        ######################## NEW #####################################
        ray.init()
        if not args.hdf5:
            ray_full_expression = ray.put(full_expression)

        ###########
        # indices,
        # ray_full_expression,
        # ray_list_of_k_sample_indices,
        # hdf5_file = None)

        r_jobs = []

        if args.processes == None:
            args.processes = multiprocessing.cpu_count()
        threads = args.processes
        for t in range(threads):
            if not args.hdf5:
                r_jobs.append(ray_get_cell_type_express_stats.remote(indices_list[t], 
                                                                     ray_full_expression,
                                                                     list_of_k_sample_indices))
            else:
                r_jobs.append(ray_get_cell_type_express_stats.remote(indices_list[t], 
                                                                     None,
                                                                     list_of_k_sample_indices,
                                                                     hdf5_file = hdf5_file_list[t]))
        temp_r_results = ray.get(r_jobs)
        ray.shutdown()
        
        k_group_percent_express_dict_list = []
        non_zero_mean_expression_dict_list = []

        for t in range(len(temp_r_results)):
            k_group_percent_express_dict_list.append(temp_r_results[t][0])
            non_zero_mean_expression_dict_list.append(temp_r_results[t][1])

        k_group_percent_express = ray_dicts_to_array(k_group_percent_express_dict_list)
        non_zero_mean_expression = ray_dicts_to_array(non_zero_mean_expression_dict_list)

        print(k_group_percent_express)
        print(non_zero_mean_expression)

        ######################## /NEW #####################################

    ## calculate ratios
    print("global_percent_express",global_percent_express.shape)
    print("global_non_zero_mean",global_non_zero_mean.shape)
    print("k_group_percent_express", k_group_percent_express.shape)
    print("non_zero_mean_expression", non_zero_mean_expression.shape)
    print("ratio_percent_express",ratio_percent_express.shape)
    print("ratio_non_zero_mean_expression",ratio_non_zero_mean_expression.shape)
    for i in range(k_group_percent_express.shape[1]):
        ratio_percent_express[:,i] = k_group_percent_express[:,i]/global_percent_express
        ratio_non_zero_mean_expression[:,i] = non_zero_mean_expression[:,i]/global_non_zero_mean

    
##############################################################################
########### use the means of the k-means groups to calculate the enrichment



    ## calculate the sample group z-scores ((Xbar-Mu)/sigma) * sqrt(n), or (Xbar-Mu)/(sigma/sqrt(n))
    print("calculating the sample group vs all sample means")
    row_delta = np.array(k_group_means.transpose() - all_sample_mean.transpose()).transpose()
    print(np.shape(row_delta))
    for k in range(0,len(list_of_k_sample_indices)):
        #print(k)
        row_delta[:,k] = np.array(row_delta[:,k].transpose() / all_sample_sd[:,0].transpose()).transpose()
        row_delta[:,k] = row_delta[:,k] * np.sqrt(len(list_of_k_sample_indices[k]))

    sample_k_group_enrichment = row_delta
    sample_k_group_enrichment_numeric = sample_k_group_enrichment

    #######################################################

    sample_groups = []
    for k in range(0,len(list_of_k_sample_indices)):
        #print(k)
        if 'alias_dict' in globals():
            #print(list(alias_dict.keys()))
            temp_sample_group_name = alias_dict[k]
        else:
            temp_sample_group_name = 'sample_group_'+str(k)
        sample_groups.append(temp_sample_group_name)
        #print(sample_groups)
    sample_groups = np.array(sample_groups)


    ## get ready to write it to file
    k_group_means = np.vstack((sample_groups,k_group_means))
    k_group_sd = np.vstack((sample_groups,k_group_sd))
    sample_k_group_enrichment = np.vstack((sample_groups, sample_k_group_enrichment))

    global_percent_express = np.array(["global_percent_express"]+global_percent_express.tolist())
    global_non_zero_mean = np.array(["global_non_zero_mean"]+global_non_zero_mean.tolist())

    k_group_percent_express = np.vstack((sample_groups, k_group_percent_express))
    non_zero_mean_expression = np.vstack((sample_groups, non_zero_mean_expression))
    ratio_percent_express = np.vstack((sample_groups, ratio_percent_express))

    ratio_non_zero_mean_expression = np.vstack((sample_groups, ratio_non_zero_mean_expression))

    ##############################################################################
    ##### prepare the k-means enrichment for writing to file, then write it
    
    ## these are the names of the variables, making the row labels for the output table
    row_names = np.transpose(np.array([['var_names']+IDlist]))
    
    
    k_group_means = np.hstack((row_names, k_group_means))
    k_group_sd = np.hstack((row_names, k_group_sd))
    sample_k_group_enrichment = np.hstack((row_names, sample_k_group_enrichment))

    k_group_percent_express = np.hstack((row_names, k_group_percent_express))
    non_zero_mean_expression = np.hstack((row_names, non_zero_mean_expression))
    ratio_percent_express = np.hstack((row_names, ratio_percent_express))
    ratio_non_zero_mean_expression = np.hstack((row_names, ratio_non_zero_mean_expression))

    global_percent_express = list(map(list,zip(['var_names']+IDlist, global_percent_express.tolist())))
    global_non_zero_mean = list(map(list,zip(['var_names']+IDlist, global_non_zero_mean.tolist())))


    write_table(k_group_means,sample_dir+'k_group_means.txt')
    write_table(k_group_sd,sample_dir+'k_group_sd.txt')
    write_table(sample_k_group_enrichment, sample_dir+'k_group_enrichment.txt')

    express_metrics_dir = process_dir(os.path.join(sample_dir,'expression_metrics'))
    write_table(global_percent_express,os.path.join(express_metrics_dir,"global_percent_express.tsv"))
    write_table(global_non_zero_mean,os.path.join(express_metrics_dir,"global_non_zero_mean.tsv"))
    write_table(k_group_percent_express,os.path.join(express_metrics_dir,"k_group_percent_express.tsv"))
    write_table(non_zero_mean_expression,os.path.join(express_metrics_dir,"non_zero_mean_expression.tsv"))
    write_table(ratio_percent_express,os.path.join(express_metrics_dir,"ratio_percent_express.tsv"))
    write_table(ratio_non_zero_mean_expression,os.path.join(express_metrics_dir,"ratio_non_zero_mean_expression.tsv"))


##################################################################################################################
##### do a one way anova between groups to test for variables that are significantly different between them ######

from scipy.stats.mstats import f_oneway as aov
from scipy.stats import ttest_ind as ttest

def get_ttests(index, aov_p):
    ## for use in the context of a Friedman's Protected LSD post-hoc to significant anovas
    global args, full_expression, list_of_k_sample_indices
    p_vals = np.ones((len(list_of_k_sample_indices),len(list_of_k_sample_indices)))
    if aov_p > args.FDR_cutoff:
        return(p_vals)
    list_of_group_values=[]
    for group in range(0,len(list_of_k_sample_indices)):
        list_of_group_values.append(full_expression[index,list_of_k_sample_indices[group]])
    for i in range(0,len(list_of_group_values)-1):
        for j in range(i+1, len(list_of_group_values)):
            stat, p = ttest(list_of_group_values[i],list_of_group_values[j])
            p_vals[i,j]=p
            p_vals[j,i]=p
    return(p_vals)

def get_anova(index):
    #print('\n'*10)
    global full_expression, list_of_k_sample_indices
    if np.sum(full_expression[index,:]) == 0:
        return([np.nan,np.nan])
    list_of_group_values=[]
    for group in range(0,len(list_of_k_sample_indices)):
        #print(len(list_of_k_sample_indices[group]))
        list_of_group_values.append(full_expression[index,list_of_k_sample_indices[group]])
        #print(np.shape(list_of_group_values[-1]))
        #print(list_of_group_values[-1])
        
    return_val = list(aov(*list_of_group_values))
    return(return_val)

# if not very_big_file:
#     if len(list_of_k_sample_indices) > 1:
#         enough_k_samples = True
#     else:
#         enough_k_samples = False
# else:
#     enough_k_samples = False

all_sig_enriched_files=[]
all_sig_enriched_gprof_files = []
FDR_cutoff = args.FDR_cutoff
zscore_cutoff = args.Zscore
if not one_group:
    anova_output = [['Variable', 'F', 'uncorrected_p-val', 'BH_corrected_p-val','-log10(BH_cor_p-val)']]
    aov_uncorrected_p_val_list=[]

    if args.processes==1:
        ######### OLD ######################
        # go through each variable and get the uncorrected anova stats
        threads = multiprocessing.cpu_count()
        print('doing the 1-way ANOVAs:',threads,"threads")
        pool = ThreadPool(threads)
        all_aov_results = pool.map(get_anova,range(full_expression.shape[0]))
        pool.close()
        pool.join()
        print('done')

        print(all_aov_results[:5])
        ########## /OLD ######################
    else:
        ######### NEW ##################
        ray.init()
        if not args.hdf5:
            ray_full_expression = ray.put(full_expression)
        ###########
        # indices,
        # ray_full_expression,
        # ray_list_of_k_sample_indices,
        # hdf5_file = None)

        r_jobs = []

        for t in range(threads):
            if not args.hdf5:
                r_jobs.append(ray_get_anova.remote(indices_list[t],
                                                   ray_full_expression,
                                                   list_of_k_sample_indices))
            else:
                r_jobs.append(ray_get_anova.remote(indices_list[t], 
                                                   None,
                                                   list_of_k_sample_indices,
                                                   hdf5_file = hdf5_file_list[t]))


        temp_aov_results = ray.get(r_jobs)
        ray.shutdown()
            
        all_aov_results = ray_dicts_to_array(temp_aov_results).tolist()
        
        ## clean up the copied files
        if args.hdf5:
            for file in hdf5_file_list:
                cmd('rm '+file)

        ######### /NEW ##################
    #################################


    ## now do do the BH correction
    for i in range(0,len(IDlist)):
        anova_output.append([IDlist[i]]+all_aov_results[i])
        aov_uncorrected_p_val_list.append(anova_output[-1][-1])

    ## replace nans with 1s
    aov_uncorrected_p_val_list=np.array(aov_uncorrected_p_val_list)
    aov_uncorrected_p_val_list[np.isnan(aov_uncorrected_p_val_list)] = 1

    #print(aov_uncorrected_p_val_list[:10])
    #print(correct_pvalues_for_multiple_testing(aov_uncorrected_p_val_list[:10]))
    #for line in anova_output:
    #    print(line)
    ## correct the p-values with Benjamini-Hochberg 
    BH_corrected_aov = correct_pvalues_for_multiple_testing(aov_uncorrected_p_val_list)
    #print(BH_corrected_aov[:10])

    indices_less_than_FDR_cutoff=[]
    for i in range(0,len(IDlist)):
        anova_output[i+1]+=[BH_corrected_aov[i], -1*np.log10(BH_corrected_aov[i])]
        if BH_corrected_aov[i] <= FDR_cutoff:
            indices_less_than_FDR_cutoff.append(i)


    #cmd('mkdir "'+args.out_dir+'significance"')
    process_dir(os.path.join(args.out_dir,'significance'))
    write_table(anova_output , args.out_dir+'significance/groups_1way_anova_results.txt')

    ################################################################################################
    ############# Find the significantly different & enriched variables for each group #############
    ################################################################################################

    ## we start off with the variables that are significantly different between groups
    
    ## this is a list of lists for each 
    group_sig_enriched_bool=[]


    for i in range(0,len(IDlist)):
        ## check to see if this variable was significant in the BH corrected 1-way anova
        if i in indices_less_than_FDR_cutoff:
            var_significant = True
        else:
            var_significant = False
        
        ## if it's significant, we want to go in and check which, if any sample groups 
        ## show an elevated z-score enrichment (greater than the zscore_cutoff variable)
        if var_significant:
            #print(sample_k_group_enrichment_numeric[i,])
            temp_sig_enriched_bool_list = list(sample_k_group_enrichment_numeric[i,] >= zscore_cutoff)
        else: 
            temp_sig_enriched_bool_list = [False]*len(list_of_k_sample_indices)
        
        group_sig_enriched_bool.append(temp_sig_enriched_bool_list)
    
    bool_sample_groups = []
    for s in sample_groups:
        bool_sample_groups.append('bool_'+s)
    bool_sample_groups = np.array(bool_sample_groups)
    
    group_sig_enriched_bool = np.array(group_sig_enriched_bool)
    group_sig_enriched = np.vstack((bool_sample_groups,group_sig_enriched_bool))
    group_sig_enriched = np.hstack((row_names,group_sig_enriched))
    
    write_table(group_sig_enriched, args.out_dir+'significance/significant_and_enriched_boolean_table.txt')
    
    ## go through each group, and make a list of the variables that are significant and enriched
    num_sig_enriched = []
    for group in range(0,len(list_of_k_sample_indices)):
        sig_and_enriched_for_this_group = []
        for var in range(0,len(IDlist)):
            if group_sig_enriched_bool[var,group]:
                sig_and_enriched_for_this_group.append(IDlist[var])
        num_sig_enriched.append(len(sig_and_enriched_for_this_group))
        temp_file = args.out_dir+'significance/'+sample_groups[group]+'_significant_enriched.txt'
        all_sig_enriched_files.append(temp_file)
        all_sig_enriched_gprof_files.append(args.out_dir+'significance/gprofiler/'+sample_groups[group]+'_significant_enriched_gprofiler.txt')
        make_file('\n'.join(sig_and_enriched_for_this_group), temp_file)
    
#    print(np.shape(sample_groups))
#    print(np.shape(np.array(num_sig_enriched)))
#    print(num_sig_enriched)
    num_sig_enriched = np.transpose(np.vstack((np.array([sample_groups]),np.array([num_sig_enriched]))))
    
    num_sig_enriched = np.vstack((np.array([['sample_group', 'number_of_significant_and_enriched_vars']]), num_sig_enriched))
    
    write_table(num_sig_enriched, args.out_dir+'significance/number_of_variables_significant_and_enriched_for_each_group.txt')


enriched_in_one_bool = np.sum(group_sig_enriched_bool, axis = 1) != 0
temp_IDs = np.array(IDlist)
IDs_enriched_in_one = temp_IDs[enriched_in_one_bool].tolist()
background = args.out_dir+'significance/background_ids.txt'
make_file('\n'.join(IDlist),background)

if not args.no_gProfile:
    cmd('mkdir '+args.out_dir+'significance/gprofiler/')

    for f in range(0,len(all_sig_enriched_files)):
        temp_gprofile = 'pyminer_gprofile.py -i '+all_sig_enriched_files[f]+' -s '+args.species+' -o '+all_sig_enriched_gprof_files[f]
        temp_gprofile += ' -b '+background
        cmd(temp_gprofile)












