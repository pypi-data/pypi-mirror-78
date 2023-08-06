#!/usr/bin/env python3
##import dependency libraries
import sys,time,glob,os,pickle
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
gc.enable()


## check for numpy dependency
try:
    import numpy as np
except:
    print('\n\nnumpy is a dependency for this script\nit can be installed from:\nWindows:\nhttp://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy\nMac:\nhttp://sourceforge.net/projects/numpy/files/NumPy/\nLinux:\nhttps://launchpad.net/~scipy/+archive/ppa\n\n\n')
import scipy
import numpy as np
from scipy.stats import mannwhitneyu as mw
from scipy.linalg import eigh
    
from numpy import linalg
import random
from random import sample

random.seed(12345)
np.random.seed(12345)

## check for matplotlib
if '-no_graphs' in sys.argv:
    no_matplot_lib=True
    pass
else:
    print('\n\nmatplotlib is a dependency for graphs produced by this script\nit can be installed from:\nhttp://matplotlib.org/downloads.html\n\n\n')
    from matplotlib import use
    use('Agg')
    no_matplot_lib=False
    import matplotlib.pyplot as plt



######################################################################################
###############
## basic function library
def read_file(tempFile,linesOraw,quiet=False):
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


def read_table(file, sep='\t'):
    return(make_table(read_file(file,'lines'),sep))
    
def write_table(table, out_file, sep = '\t'):
    make_file(flatten_2D_table(table,sep), out_file)

def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))

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

############################################################################################

## read in the necessary arguments
##############################################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-adjacency_list", "-adj","-adj_list",
    help="the adjacency list ")
parser.add_argument("-nodes_of_interest", "-noi","-nodes",
    help="the nodes that you want to subset and get their degrees of separation from")
parser.add_argument("-ID_list", "-id_list","-ids","-IDs",
    help="the list of all IDs that made the network")
parser.add_argument("-out_dir", 
    help="the directory to place the output file(s)")
parser.add_argument("-all_distances", 
    help="if you want to write a file that has all distances as a matrix. (note that the IDs will be in the same order as the input -ID_list)",
    action = 'store_true',
    default = False)
args = parser.parse_args()
##############################################################
if args.adjacency_list == None:
    sys.exit('-adjacency_list </path/to/file> is a required argument')
else:
    adj_list_file = args.adjacency_list

if args.nodes_of_interest != None:
	nodes_of_interest = args.nodes_of_interest
	nodes_of_interest = nodes_of_interest.split(',')
else:
    nodes_of_interest = None

if args.ID_list!=None:
	ID_list = read_file(args.ID_list, "lines")
	ID_hash = {}
	for i in range(0,len(ID_list)):
		ID_hash[ID_list[i]] = i
else:
	sys.exit('-ID_list </path/to/file> is a required argument')

if args.out_dir != None:
	out_dir = args.out_dir
else:
	out_dir = adj_list_file.split('/')
	out_dir = '/'.join(out_dir[:-1])+'//'


#################################################################
## first read in the adjacency list & make an adjacency matrix ##
#################################################################
print('\n\nmaking the adjacency matrix\n\n')
## make an empty adjacency matrix
G_dense = np.zeros((len(ID_list),len(ID_list)),dtype = bool)

## go through the adjacency list and populate the adjacnecy matrix
first_line = True
for line in fileinput.input(adj_list_file):
    #print(first_line)
    if not first_line:
        temp_line = strip_split(line)
        idx1 = ID_hash[temp_line[0]]
        idx2 = ID_hash[temp_line[1]]
        G_dense[idx1,idx2] = 1
        G_dense[idx2,idx1] = 1
    else:
        first_line = False

################################################################
########## get all shortest paths from & to all nodes ##########
################################################################
print('\n\nfinding all of the shortest paths\n\n')
G_sparse = scipy.sparse.csr_matrix(G_dense)
short_path_mat = scipy.sparse.csgraph.shortest_path(G_sparse)

if args.all_distances:
    temp_outfile = out_dir+'/all_shortest_paths_matrix.txt'
    write_table(short_path_mat,temp_outfile)
else:
    pass



## subset the distance matrix to get all distances from the nodes of interest
header = ['genes']
out_array = np.transpose(np.array([ID_list]))

if nodes_of_interest != None:
    for n in nodes_of_interest:
        if n not in ID_hash:
            sys.exit(str('could not find ' + n + ' in the adjacency matrix'))
        else:
            header.append('dist_to_'+str(n))
            ## get the distances
            temp_dist_vect = short_path_mat[:,ID_hash[n]]

            ## make the shortest list for output
            ## [all_nodes, current_node_of_interest, shortest_path]
            #out_list = np.hstack(out_array, np.transpose(np.array([[n]*len(ID_list)])) ) )

            #print(np.shape(out_list))
            #print(np.shape(temp_dist_vect))
            out_array = np.hstack((out_array, np.transpose(np.array([temp_dist_vect]))) )

            #temp_outfile = out_dir+'/'+n+'_shortest_path_list.txt'
            #print('writing output shortest paths to:\n',temp_outfile)

out_array = np.vstack((np.array([header]), out_array))

temp_outfile = out_dir+'/'+'genes_of_interest_shortest_path_list.txt'
write_table(out_array,temp_outfile)
    		
    		
		








#################################################################




















