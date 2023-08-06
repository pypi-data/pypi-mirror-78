#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
#import pandas as pd
##############################################################
## basic function library
def read_file(tempFile,linesOraw='lines',quiet=False):
    if not quiet:
        print('reading',tempFile)
    f=open(tempFile,'r')
    if linesOraw=='lines':
        lines=f.readlines()
        for i in range(0,len(lines)):
            lines[i]=lines[i].strip('\n')
    elif linesOraw=='raw':
        lines=f.read()
    f.close()
    return(lines)

def make_file(contents,path):
    f=open(path,'w')
    if isinstance(contents,list):
        f.writelines(contents)
    elif isinstance(contents,str):
        f.write(contents)
    f.close()

    
def flatten_2D_table(table,delim):
    #print(type(table))
    if str(type(table))=="<class 'numpy.ndarray'>":
        out=[]
        for i in range(0,len(table)):
            out.append([])
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    out[i].append(str(table[i][j]))
            out[i]=delim.join(out[i])+'\n'
        return(out)
    else:
        for i in range(0,len(table)):
            for j in range(0,len(table[i])):
                try:
                    str(table[i][j])
                except:
                    print(table[i][j])
                else:
                    table[i][j]=str(table[i][j])
            table[i]=delim.join(table[i])+'\n'
    #print(table[0])
        return(table)

def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))

def make_table(lines,delim):
    for i in range(0,len(lines)):
        lines[i]=lines[i].strip()
        lines[i]=lines[i].split(delim)
        for j in range(0,len(lines[i])):
            try:
                float(lines[i][j])
            except:
                lines[i][j]=lines[i][j].replace('"','')
            else:
                lines[i][j]=float(lines[i][j])
    return(lines)


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return(in_path+'/')


def read_table(file, sep='\t'):
    return(make_table(read_file(file,'lines'),sep))
    
def write_table(table, out_file, sep = '\t'):
    make_file(flatten_2D_table(table,sep), out_file)
    

def import_dict(f):
    f=open(f,'rb')
    d=pickle.load(f)
    f.close()
    return(d)

def save_dict(d,path):
    f=open(path,'wb')
    pickle.dump(d,f)
    f.close()

def cmd(in_message, com=True):
    print(in_message)
    time.sleep(.25)
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)



##############################################################



parser = argparse.ArgumentParser()

## global arguments
parser.add_argument(
	'-means','-m','-mean',
	dest='means',
	type=str)

parser.add_argument(
	'-significance','-sig','-anovas','-anova', '-aov',
	dest='sig',
	type=str)

parser.add_argument(
	'-out','-o',
    help = "output directory",
	dest='out',
	type=str)

parser.add_argument(
	'-annotation_dict','-ad',
	dest='symbol_def_dict',
	type=str)


args = parser.parse_args()
##################################################################

## import the annotation dict
symbol_dict, def_dict = import_dict(args.symbol_def_dict)

## hyperparameters
sig_cutoff = 0.05
q_cutoff = 0.5
## the percent of the largest distance to second to consider for marker genes
## this gives you highly expressed differentially expressed genes
percentile = 0.9


k_group_means_file = np.array(read_table(args.means))
id_list = k_group_means_file[1:,0].tolist()
group_names = k_group_means_file[0,1:].tolist()

if len(group_names)<3:
	sys.exit('need at least 3 groups')

###########################
## get the means array
k_group_means = np.array(k_group_means_file[1:,1:],dtype=float)
k_group_min = np.min(k_group_means,axis=1)
k_group_max = np.max(k_group_means,axis=1)
k_group_range = k_group_max - k_group_min
## get the distance from max to second max
dist_max_to_second = np.zeros((len(id_list)))
q_value_vect = np.zeros((len(id_list)))
for i in range(0,len(id_list)):
	temp_sorted = np.sort(k_group_means[i,:])[::-1]
	dist_max_to_second[i]=temp_sorted[0]-temp_sorted[1]
	q_value_vect[i] = dist_max_to_second[i]/k_group_range[i]

sorted_dist_to_max = np.sort(dist_max_to_second[:],kind="mergesort")
index_for_cutoff = int(len(id_list)*percentile)
dist_max_to_second_cutoff = sorted_dist_to_max[index_for_cutoff]

##########################
## 
BH_corrected_aov_file = np.array(read_table(args.sig))
BH_corrected_aov = np.array(BH_corrected_aov_file[1:,3],dtype=float)

##
## only consider significant genes
sig_bool = BH_corrected_aov<sig_cutoff
q_bool = q_value_vect>q_cutoff
dist_to_second_max_bool = dist_max_to_second>dist_max_to_second_cutoff
print('\n\n\nsig_bool',sig_bool,sum(sig_bool))
print('q_bool',q_bool,sum(q_bool))
print('dist_to_second_max_bool',dist_to_second_max_bool,sum(dist_to_second_max_bool))
sig_q_and_dist = (np.array(sig_bool,dtype=int) + np.array(q_bool,dtype=int) + np.array(dist_to_second_max_bool,dtype=int))==3
print('\ncombined\n',sig_q_and_dist)


print('found',sum(sig_q_and_dist),'highly expressed, somewhat "exclusive" marker genes')

print('making the output table...')

out_file = [['gene','gene_symbol','gene_def', 'aov_BH_p', 'range', 'dist_from_max_to_second_max', 'q_value', 'group']]


def get_group(i):
	global sig_q_and_dist, group_names, k_group_max, k_group_means
	if not sig_q_and_dist[i]:
		return("None")
	else:
		index = int(np.where(k_group_means[i] == k_group_max[i])[0])
		return(group_names[index])

def process_symbol(in_symbol_list,ensg):
	if len(in_symbol_list)==0:
		return(ensg)
	else:
		return('_'.join(in_symbol_list))

def process_def(in_def):
	if len(in_def)==0:
		return("NA")
	else:
		return(in_def[0])

for i in range(0,len(id_list)):
    ## in the case of entrez IDs
    try:
        int(float(id_list[i]))
    except:
        temp_id = id_list[i]
    else:
        temp_id = str(int(float(id_list[i])))
    temp_line = []
    temp_line.append(temp_id)
    temp_line.append(process_symbol(symbol_dict[temp_id],temp_id))
    temp_line.append(process_def(def_dict[temp_id]))
    temp_line.append(BH_corrected_aov[i])
    temp_line.append(k_group_range[i])
    temp_line.append(dist_max_to_second[i])
    temp_line.append(q_value_vect[i])
    temp_line.append(get_group(i))
    out_file.append(temp_line)

## get the input for plot_subset...
plot_subset_input = []
for i in range(0,len(out_file)):
	if out_file[i][-1]!="None":
		plot_subset_input.append([out_file[i][0],out_file[i][1]])

subset_input_file = args.out+"/subset_input.txt"
write_table(plot_subset_input,subset_input_file)
write_table(out_file,args.out+'/marker_gene_annotations.tsv')

#cmd("plot_subset.py -i ""-plot_subset "+subset_input_file)



