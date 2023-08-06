# #!/usr/bin/env python3
import sys, os, glob, time
import numpy as np
import random
import scipy
from subprocess import Popen
from time import sleep
from scipy.stats import spearmanr
from time import time
import fileinput,pickle
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import h5py
from copy import deepcopy
try:
    from pyminer.common_functions import *
    from pyminer.pyminer_common_stats_functions import *
    from pyminer.pyminer_common_stats_functions import no_p_spear, get_Z_cutoff
except:
    from common_functions import *
    from pyminer_common_stats_functions import *
    from pyminer_common_stats_functions import no_p_spear, get_Z_cutoff
print(no_p_spear)

##################################################################################

def cutoff_check(r,p):
    global FPR, rho_cutoff, rho_cutoff_bool
    if rho_cutoff_bool:
        return(abs(r)>=rho_cutoff)
    else:
        return(p<=FPR)
    

#########

def get_spearman_h5(var_index):
    
    ## the offset is for a ! denoted header
    ## in general, this should be 1 because of the title line
    global temp, FPR, many_variables, IDlist, verbose, num_vars, infile
    
    output_lines = []
    cur_var_name1 = IDlist[var_index]
    for i in range(var_index+1,num_vars):
        if i%1000==0:
            print('\t',i)
        cur_var_name2 = IDlist[i]
        r,p=spearmanr(infile[var_index], infile[i])
        if cutoff_check(r,p):
            #print('found a relationship',r,p)
            output_lines.append([cur_var_name1, cur_var_name2, r])
            output_lines.append([cur_var_name2, cur_var_name1, r])
            #print(output_lines[-1])

    ## write status to temp log for this processes
    make_file("working on row "+str(var_index+1),log_file)

    
    if output_lines != []:
        return(output_lines)
    else:
        return(None)





##################################################################################
##############################################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-infile_path", '-i',
    help="the input dataset for making the adjacency list")
parser.add_argument("-adj_list_out", '-o',
    help="the ouptut adj list")
parser.add_argument("-id_list", '-ids',
    help="the file containing the IDs in the appropriate order")
parser.add_argument("-col_ids", 
    help="the file containing column IDs")
parser.add_argument("-rho_cutoff", '-rho',
    help="the cutoff to use for rho values",
    type = float)
parser.add_argument("-hdf5",
    action = 'store_true',
    default = False, 
    help="if the input file is in the hdf5 format")
parser.add_argument("-block_size",
    help = 'how many variables will be used at once for correlation analyzis; this helps keep memory requirements down and prevents a segmentation fault memory error',
     type = int,
     default = 5000)
parser.add_argument("-time",
    action = 'store_true',
    default = False, 
    help="if you only want to test the speed of relationship detection")
parser.add_argument("-sc_clust",
    action = 'store_true',
    default = False, 
    help="if scRNAseq clustering is going to be done")
parser.add_argument("-transpose",
    action = 'store_true',
    default = False, 
    help="if we're going to make an adjacency list on the columns rather than the rows")
parser.add_argument(
    "-rand_seed",'-seed',
    help='the random number input for random number seed, default = 12345',
    dest = 'rand_seed',
    type = int,
    default = 12345)

parser.add_argument("-hdf5_out",
    action = 'store_true',
    default = False, 
    help="if we want to make an hdf5 as the output instead of the rho dicts")
parser.add_argument("-euclidean_dist",
    action = 'store_true',
    default = False, 
    help="if we are going to also calculate the euclidean distance of all points against each other and store as an hdf5.")
parser.add_argument("-row_subset",
    help="a file with the row indices to include if we only want to do this on a subset of the rows. Note that this operation is performed before the transpose if need be.")
parser.add_argument(
    "-rho_dict_dir",
    help='the destination directory')

parser.add_argument(
    "-FPR_multiple",'-mult',
    help="the multiple to use for FPR based anti-correlation feature selection. Only use this if you really know what you're doing.",
    type = int,
    default = 15)
parser.add_argument(
    "-num_pos_cor_cutoff",
    help="the The minimum number of positive correlations that a gene must have to be included in the clustering. Default is 10. Only use this if you really know what you're doing.",
    type = int,
    default = 10)


parser.add_argument("-prop","-proportaionality",
    action = 'store_true',
    default = False, 
    help="if you only want to use proportionality instead of Spearman")

args = parser.parse_args()


np.random.seed(args.rand_seed)
random.seed(args.rand_seed)



## constants
FPR = 1000 ## 1 in 1000 false positive rate for negative correlation clustering
FPR_multiple = args.FPR_multiple ## the number of times the expected number of false positives to be included in clustering
pos_FPR = int(1e3)


##############################################################
args.infile_path = os.path.realpath(args.infile_path)

rho_cutoff_bool = True
rho_cutoff = args.rho_cutoff





##############

## run spearman analysis

infile_path=args.infile_path
if args.hdf5:
    h5f = h5py.File(infile_path, 'r')
    infile=h5f["infile"]
else:
	infile = np.array(read_table(infile_path))



if args.id_list is None and not args.hdf5:
    IDlist = list(infile[1:,0])
    col_ids = list(infile[0,1:])
    infile = np.array(infile[1:,1:],dtype = float)
elif args.id_list != None and not args.hdf5:
    infile = np.array(infile[1:,1:],dtype = float)
    ID_list = args.id_list
    IDlist = read_file(ID_list,'lines')
else:
    ID_list = args.id_list
    IDlist = read_file(ID_list,'lines')

## subset for the pertinent rows
if args.row_subset!=None:
    row_indices = read_file(args.row_subset,'lines')
    row_indices = sorted(list(map(int,row_indices)))
    infile = infile[row_indices,:]



## here's where we'll transpose the input
if args.transpose:
    if args.hdf5:
        infile = np.transpose(infile)
        IDlist = read_file(args.col_ids,'lines')[1:]# start at 1 because of the leader column
    else:
        infile = np.transpose(infile)
        IDlist = col_ids


num_vars = len(IDlist)
## sanity check that the ID list length is equal to the row num
if num_vars != np.shape(infile)[0]:
    print('the length of the ID list does not equal the number of rows in the input dataset')
    print("infile:",np.shape(infile)[0], )
    print("IDlist:",num_vars, IDlist[0:5])
    sys.exit()

index=0

temp_dir=str(infile_path).split('/')
temp_dir=('/').join(temp_dir[:-1])

dump_length = 20
bin_size = args.block_size
bin_size = min([bin_size,len(IDlist)])## this prevents the program from hitting index errors for small datasets


count=0


print('finding the spearman correlations for very big file')
print('this may take a while if your dataset has lots of variables...')

################################################
if args.rho_dict_dir==None:
    rho_dict_dir = temp_dir+'/rho_dicts'
else:
    rho_dict_dir = args.rho_dict_dir
cmd('mkdir '+rho_dict_dir)
#########################################################

#output_lines = [["X_var","Y_var","Spearman_p_val","Spearman_rho"]]
output_lines = []


total_vars = len(IDlist)
bins = []
cur_bin = 0
while cur_bin<total_vars:
	bins.append(min(cur_bin, total_vars))
	cur_bin+=bin_size

bins.append(total_vars)
if args.hdf5_out:
    print('making the hdf5 spearman output file')
    ## make the hdf5 output file
    hdf5_spear_out_file = rho_dict_dir+"/spearman.hdf5"
    print(hdf5_spear_out_file)
    #cmd('rm '+hdf5_spear_out_file)
    
    spear_f = h5py.File(hdf5_spear_out_file, "a")
    try:
        spear_out_hdf5 = spear_f.create_dataset("infile", (total_vars,total_vars), dtype=np.float16)
    except:
        spear_out_hdf5 = spear_f["infile"]



print(np.shape(infile))


print(infile)

print(bins)


start = time.time()
print("finding block...")
for i in range(0,(len(bins)-1)):
    for j in range(i,(len(bins)-1)):
        if (i!=j) or (len(bins) == 2):#True:
            out_rho_dict = rho_dict_dir+"/rho_"+str(bins[i])+"_to_"+str(bins[i+1])+"_vs_"+str(bins[j])+"_to_"+str(bins[j+1])+".pkl"

            ## if we're writing to an hdf5 file, check if the values are already entered
            if args.hdf5_out:
                #do_top_left = np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[i]:bins[i+1]]==0)
                #do_top_right = np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0)
                #do_bottom_left = np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0)
                #do_bottom_right = np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]]==0)
                do_top_left = np.all(spear_out_hdf5[bins[i],bins[i]:bins[i+1]]==0)
                do_top_right = np.all(spear_out_hdf5[bins[i],bins[j]:bins[j+1]]==0)
                do_bottom_left = np.all(spear_out_hdf5[bins[j],bins[i]:bins[i+1]]==0)
                do_bottom_right = np.all(spear_out_hdf5[bins[j],bins[j]:bins[j+1]]==0)
                do_one = (do_top_left or do_top_right or do_bottom_left or do_bottom_right)
                print(do_top_left , do_top_right , do_bottom_left , do_bottom_right)
                #print(spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]])
            else:
                do_one = False
            
            #print((not os.path.exists(out_rho_dict) and not args.hdf5_out) , (args.hdf5_out and do_one))
            #sys.exit()
            if (not os.path.exists(out_rho_dict) and not args.hdf5_out) or (args.hdf5_out and do_one):
                ## find the spearman correlations

                print('working on',bins[i],bins[i+1],'vs',bins[j],bins[j+1])
                r=no_p_spear(infile[bins[i]:bins[i+1],],infile[bins[j]:bins[j+1],], axis = 1, prop=args.prop)
                
                ## if we're not making the spearman correlation matrix into an hdf5 file - save the dictionary:
                if not args.hdf5_out:
                    save_dict(r,out_rho_dict)

                ## if we are making the spearman correlation matrix an hdf5 file, we've got some work to do:
                else:
                    print(np.shape(r))
                    if np.shape(r)[0] == 2*bin_size:
                        #print('is symmetric:',r[bin_size:,bin_size:] == r[:bin_size,:bin_size])
                        if len(bins)==2:#False#np.shape(r)[0]<=bin_size:
                            ## there is a special case, where the number of variables is less than the
                            ## bin size. In this case, the returned matrix will be symmetric in all 4
                            ## quadrants, so we'll reduce it down to just the one
                            r = r[bin_size:,bin_size:]
                    print(np.shape(r))


                    ## because h5py's fancy indexing doesn't work very well with slicing in 2D...

                    ## first set the top left corner bins
                    if np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[i]:bins[i+1]]==0):
                        print("setting top left")
                        spear_out_hdf5[bins[i]:bins[i+1],bins[i]:bins[i+1]] = np.array(r[:bin_size,:bin_size],dtype=np.float16)
                    
                    ## top right
                    if len(bins)!=2:
                        try:
                            if np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0):
                                print("setting top right")
                                spear_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]] = np.array(r[:bin_size,bin_size:],dtype=np.float16)
                        except:
                            print(sys.exit('error setting the top right'))
                            pass
                    
                    ## bottom left
                    if len(bins)!=2:
                        try:
                            if np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0):
                                print('setting bottom left')
                                spear_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1],] = np.array(r[bin_size:,:bin_size],dtype=np.float16)
                        except:
                            print(sys.exit('error setting the bottom left'))
                            pass
                    
                    ## bottom right
                    if len(bins)!=2:
                        try:
                            if np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]]==0):
                                print('setting bottom right')
                                spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]] = np.array(r[bin_size:,bin_size:],dtype=np.float16)
                        except:
                            print(sys.exit('error setting the bottom right'))
                            pass
            else:
                print('already finished block',bins[i],bins[i+1],'vs',bins[j],bins[j+1])

end = time.time()



if args.euclidean_dist:
    from sklearn import metrics
    euclidean_distances = metrics.pairwise.euclidean_distances
    print('making the negative euclidean distance matrix')
    ## make the euclidean distance output matrix
    ## make the hdf5 output file
    hdf5_euc_out_file = rho_dict_dir+"/neg_euc_dist.hdf5"
    print(hdf5_euc_out_file)
    euc_f = h5py.File(hdf5_euc_out_file, "a")
    ## set up the data matrix (this assumes float32)
    float_type = np.float16
    try:
        neg_euc_out_hdf5 = euc_f.create_dataset("infile", (total_vars,total_vars), dtype=float_type)
    except:
        neg_euc_out_hdf5 = euc_f["infile"]
    # else:
    #     neg_euc_out_hdf5 = euc_f.create_dataset("infile", (total_vars,total_vars), dtype=np.float32)
    # ## go through and calculate the negative euclidean distances
    ###########################
    spear_min = 99999
    temp_start=int(0)
    temp_end=int(args.block_size)
    print("calculating the minimum non-zero Spearman rho")
    while temp_end < spear_out_hdf5.shape[0]:
        print(round(100*temp_start/spear_out_hdf5.shape[0],2),"% ","done")
        spear_min=min([spear_min,np.nanmin(spear_out_hdf5[temp_start:temp_end,:])/np.log2(total_vars)])
        temp_start+=args.block_size
        temp_end+=args.block_size
    ## catch the last bit
    spear_min=min([spear_min,np.nanmin(spear_out_hdf5[temp_start:,:])])
    #spear_min = np.nanmin(spear_out_hdf5)/np.log2(total_vars)
    print("spear_min",spear_min)
    ###########################
    for i in range(0,(len(bins)-1)):
        for j in range(i,(len(bins)-1)):
            #print(np.all(neg_euc_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0) , np.all(neg_euc_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0))
            if (np.all(neg_euc_out_hdf5[bins[i],bins[j]:bins[j+1]]==0) and np.all(neg_euc_out_hdf5[bins[j],bins[i]:bins[i+1]]==0)):
                print('calculating negative euclidean distance for',bins[i],bins[i+1],'vs',bins[j],bins[j+1])
                #temp_neg_euc = -euclidean_distances(np.array(spear_out_hdf5[bins[i]:bins[i+1],:],dtype=np.float32),np.array(spear_out_hdf5[bins[j]:bins[j+1],:],dtype=np.float32),squared=True)
                #temp_neg_euc = -euclidean_distances(np.array(spear_out_hdf5[bins[i]:bins[i+1],:],dtype=float_type),np.array(spear_out_hdf5[bins[j]:bins[j+1],:],dtype=float_type),squared=True)/np.log2(total_vars)
                temp_subset_mat_1 = np.array(spear_out_hdf5[bins[i]:bins[i+1],:],dtype=float_type)/np.log2(total_vars)
                temp_subset_mat_2 = np.array(spear_out_hdf5[bins[j]:bins[j+1],:],dtype=float_type)/np.log2(total_vars)
                #print('before')
                #print(temp_subset_mat_1[np.where(np.isnan(temp_subset_mat_1))])
                temp_subset_mat_1[np.where(np.isnan(temp_subset_mat_1))]=spear_min
                #print(temp_subset_mat_1[np.where(np.isnan(temp_subset_mat_1))])
                #print('after')
                temp_subset_mat_2[np.where(np.isnan(temp_subset_mat_2))]=spear_min
                #print(temp_subset_mat_1)
                #print(temp_subset_mat_2)
                num_nan_1 = np.sum(np.isnan(temp_subset_mat_1))
                num_inf_1 = np.sum(np.isinf(temp_subset_mat_1))
                num_nan_2 = np.sum(np.isnan(temp_subset_mat_2))
                num_inf_2 = np.sum(np.isinf(temp_subset_mat_2))
                if num_nan_1+num_inf_1+num_nan_2+num_inf_2 >0:
                    print('num_nan_1:',num_nan_1)
                    print('num_inf_1:',num_inf_1)
                    print('num_nan_2:',num_nan_2)
                    print('num_inf_2:',num_inf_2)
                else:
                    pass#print('no nans or infs')
                temp_neg_euc = -euclidean_distances(temp_subset_mat_1,temp_subset_mat_2)*np.log2(total_vars)
                neg_euc_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]] = temp_neg_euc
                neg_euc_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]] = np.transpose(temp_neg_euc)
                #print(temp_neg_euc)
                #print(neg_euc_out_hdf5[:,:])
                #neg_euc_out_hdf5 = np.transpose(temp_neg_euc)
                #print(np.all(neg_euc_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0) , np.all(neg_euc_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0))
            else:
                print('already finished',bins[i],bins[i+1],'vs',bins[j],bins[j+1])
    for i in range(0,np.shape(neg_euc_out_hdf5)[0]):
        neg_euc_out_hdf5[i,i]=-0.0

    euc_f.close()



if args.hdf5_out:
    ## close the hdf5 file
    spear_f.close()


if args.time:
    print((end-start)/60,'minutes spent finding correlations')
    sys.exit()


###############################################################



################################################################################
## read in the ID list
print('logging all the IDs')

ID_hash = {}
for i in range(0,len(IDlist)):
	ID_hash[IDlist[i]] = i
	

################################################################################
## get the rho dictionaries

## parse the name of the file to get the 
def parse_dict_name(dict_path):
	dict_path = dict_path.split('/')
	dict_path = dict_path[-1]
	dict_path = dict_path.strip('rho_')
	dict_path = dict_path.strip('.pkl')
	dict_path = dict_path.split('_vs_')
	dict_path[0] = dict_path[0].split('_to_')
	dict_path[1] = dict_path[1].split('_to_')
	dict_path[0][0]=int(dict_path[0][0])
	dict_path[0][1]=int(dict_path[0][1])
	dict_path[1][0]=int(dict_path[1][0])
	dict_path[1][1]=int(dict_path[1][1])
	temp_id_indices = np.concatenate((np.arange(dict_path[0][0],dict_path[0][1]),np.arange(dict_path[1][0],dict_path[1][1])))
	temp_IDs=[IDlist[i] for i in temp_id_indices]
	return((temp_id_indices,temp_IDs))

rho_properties_dict = {}
rho_files = []
for glob in glob.glob(rho_dict_dir+'/*.pkl'):
	rho_files.append(glob)
	rho_properties_dict[glob]=parse_dict_name(glob)
	#print(glob,'\n',rho_properties_dict[glob])

	
################################################################################
## make the adjacency list
print('making the adjacency list')


#################
## look at the sum of all negative correlations
sum_neg = []
all_vars_adj_dict = {}
neg_vars_adj_dict = {}
total_neg_vars_adj_dict = {}
for i in range(0,len(IDlist)):
    ## [ID, sum_negative_rho, count_below_threshold, total_number_negative, (count_below_threshold+1)/(count_above_threshold +1)]
    sum_neg.append([IDlist[i],0,0,0,0])
    all_vars_adj_dict[IDlist[i]] = np.zeros(len(IDlist,),dtype = bool)
    neg_vars_adj_dict[IDlist[i]] = np.zeros(len(IDlist,),dtype = bool)
    total_neg_vars_adj_dict[IDlist[i]] = np.zeros(len(IDlist,),dtype = bool)
#################

####
def get_density(in_vect):
    in_vect = np.array(in_vect)
    in_vect = in_vect[np.array((np.isnan(in_vect)*-1)+1,dtype=bool)]## remove nans
    in_vect = in_vect[np.array((np.isinf(in_vect)*-1)+1,dtype=bool)]## remove infs
    offset = min(in_vect)
    #print(offset)
    in_vect = in_vect - offset
    #print(in_vect)
    density = gaussian_kde(in_vect)
    #print(in_vect)
    #print(density)
    xs = np.arange(0,max(in_vect),max(in_vect)/150)
    #print(xs)
    #density.covariance_factor = lambda : 2.5
    #density._compute_covariance()
    #print(density(xs))
    y = density(xs)
    y = y/sum(y)
    return(xs+offset,y)

def plot_one_density(neg_cor_density_x, neg_cor_density_y,out_file, label = 'negative correlation Rhos from bootstrap shuffled negative control'):
    global args
    x_min = np.min(neg_cor_density_x)
    y_min = np.min(neg_cor_density_y)
    x_max = np.max(neg_cor_density_x)
    y_max = np.max(neg_cor_density_y)

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = label,
        color = 'blue',
        linewidth = 3)
    plt.legend()
    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')

def plot_one_density_x_cutoff(neg_cor_density_x, neg_cor_density_y,cutoff,out_file,log = False,poisson_mu=None,label = "density"):
    global args
    from scipy.stats import poisson
    x_min = np.min(neg_cor_density_x)
    y_min = np.min(neg_cor_density_y)
    x_max = np.max(neg_cor_density_x)
    y_max = np.max(neg_cor_density_y)

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = label,
        color = 'blue',
        linewidth = 3)
    plt.plot([cutoff,cutoff],[y_min,y_max],
        color = 'k',
        lw = 2,
        label = 'cutoff')

    ## calculate the poisson at the given mu=cutoff
    if poisson_mu != None:
        temp_x = np.arange(x_max-x_min)+x_min
        dist = poisson(poisson_mu)
        plt.plot(np.log2(temp_x+1), np.log2(dist.pmf(temp_x)+1), ls='--', color='red',
                     label='poisson' , linestyle='steps-mid')
    plt.legend()

    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')


def plot_densities(neg_cor_density_x, neg_cor_density_y,series_2_x,series_2_y,out_file):
    global args
    x_min = min([np.min(neg_cor_density_x),np.min(series_2_x)])
    y_min = min([np.min(neg_cor_density_y),np.min(series_2_y)])
    x_max = max([np.max(neg_cor_density_x),np.max(series_2_x)])
    y_max = max([np.max(neg_cor_density_y),np.max(series_2_y)])

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = 'sum of negative correlations per gene',
        color = 'blue',
        linewidth = 3)
    plt.plot(series_2_x, series_2_y, 
        label = 'bootstrap shuffled negative control',
        color = 'red',
        linewidth = 3)
    plt.legend()
    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')

def plot_avg_densities(neg_cor_density_x, neg_cor_density_y,series_2_x,series_2_y,out_file):
    global args
    x_min = min([np.min(neg_cor_density_x),np.min(series_2_x)])
    y_min = min([np.min(neg_cor_density_y),np.min(series_2_y)])
    x_max = max([np.max(neg_cor_density_x),np.max(series_2_x)])
    y_max = max([np.max(neg_cor_density_y),np.max(series_2_y)])

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = 'average Rho of negative correlations per gene',
        color = 'blue',
        linewidth = 3)
    plt.plot(series_2_x, series_2_y, 
        label = 'average Rho of negative correlations per boostrap negative control',
        color = 'red',
        linewidth = 3)
    plt.legend()
    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')

def density_scatter(x,y,out_file,log_density=0,expected_x=[],expected_y=[]):
    ## remove points that are on the origin
    x=np.array(x)
    y=np.array(y)
    non_origin = (np.array(x==0, dtype = int) + np.array(y==0,dtype=int)) < 2
    x = x[non_origin].tolist()
    y = y[non_origin].tolist()
    if len(x)<2:
        return()
    xy = np.vstack([x,y])
    try:
        z = gaussian_kde(xy)(xy)
    except:
        print("error in getting the gaussian KDE")
        return()
    print(z)
    if log_density:
        while log_density:
            log_density-=1
            z = np.log2(z+1)
            z = z-min(z)
            z = z/max(z)
            print(z)
    plt.clf()
    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=5, edgecolor='', cmap=plt.cm.jet)
    if expected_x != [] and expected_y != [] :
        ax.plot(expected_x,expected_y,linestyle='-',c='black')
        plt.xlim((-1,max(x)+1))
        plt.ylim((0,max(y)+1))

    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight'
        )


###################
small_adj_list = []

do_sum_neg = args.sc_clust

def calculate_mad(in_vect, dev_num = 3, mean = False):
    med = np.median(in_vect)
    if mean:
        dev = np.mean(np.abs(in_vect - med))
    else:
        dev = np.median(np.abs(in_vect - med))
    print('median:',med)
    print('median absolute deviation:',dev)
    cutoff = med + (dev_num * dev)
    print('cutoff =',cutoff)
    return(med,dev,cutoff)

# def get_Z_cutoff(vect,z=4.5,positive = False):
#     ## this is for a half distribution, so mult by -1 to make it 'normal'
#     global FPR
#     vect_original = np.array(deepcopy(vect))
#     vect = list(vect)
#     vect += list(np.array(vect)*-1)
#     vect = np.array(vect)
#     ## get the mean, & SD
#     v_mean = np.mean(vect)
#     v_std = np.std(vect)
#     cutoff = v_std * z
#     if not positive:
#         cutoff *= -1
#         cutoff = max([-0.9,cutoff])
#     else:
#         cutoff = min([0.9,cutoff])
#     print('cutoff:',cutoff)
#     if not positive:
#         num_sig = np.sum(np.array(vect_original<cutoff,dtype = bool))
#         total_num = vect_original.shape[0]
#         print(num_sig, "/", total_num, 'significant')
#         FPR = max([1,total_num])/num_sig
#         return(cutoff, FPR)
#     else:
#         return(cutoff)


# def get_FPR_cutoff(negative_control_negative_rho_vect,FPR,positive = False):
#     ####################################################################
#     ## figure out the cutoff to use for a given false positive rate
#     negative_control_negative_rho_vect = negative_control_negative_rho_vect[np.where(abs(negative_control_negative_rho_vect)!=1)[0]]
#     negative_control_negative_rho_vect = np.sort(negative_control_negative_rho_vect, kind = "mergesort")
#     if positive:
#         negative_control_negative_rho_vect = negative_control_negative_rho_vect[::-1]
#     print("sorting list:")
#     print(negative_control_negative_rho_vect[:5],'...',negative_control_negative_rho_vect[-5:])
#     number_of_total_negative_correlations_in_boot = np.shape(negative_control_negative_rho_vect)[0]
#     print("number_of_total_negative_correlations_in_boot")
#     print(number_of_total_negative_correlations_in_boot)
#     print("FPR:",FPR)

#     neg_cutoff_index = int(max([1,number_of_total_negative_correlations_in_boot/FPR])-1)## this is an emperical cutoff of 1/FPR randomly negative rhos
#     print("cutoff_index")
#     print(neg_cutoff_index)

#     neg_cutoff = float(negative_control_negative_rho_vect[neg_cutoff_index])
#     #print(negative_control_negative_rho_vect[:neg_cutoff_index])
#     print('Rho cutoff:',neg_cutoff)
#     return(neg_cutoff)

    ##################################################################



if do_sum_neg or args.rho_cutoff==None:
    ## run the bootstrap negative control for finding sum negative relationships
    ## first get a bin_size random set of variables to do the negative control on
    neg_control_sample_idxs = np.arange(len(IDlist))
    ## remove any genes that are zero in all samples
    non_zero_idxs = np.where(np.sum(infile,axis=1)>0)[0]
    neg_control_sample_idxs = neg_control_sample_idxs[non_zero_idxs]
    np.random.shuffle(neg_control_sample_idxs)
    print(np.shape(neg_control_sample_idxs))
    bin_size = min([bin_size, np.shape(neg_control_sample_idxs)[0]])
    print(bin_size)
    neg_control_sample_idxs = neg_control_sample_idxs[:bin_size]
    neg_control_sample_idxs = neg_control_sample_idxs.tolist()
    neg_control_sample_idxs.sort()
    print(np.shape(neg_control_sample_idxs))

    ## subset these IDs
    neg_control_subset_mat = np.array(infile[neg_control_sample_idxs,:])
    print('making negative control bootstrap shuffled matrix',np.shape(neg_control_subset_mat))

    ## go through each row and shuffle them within variables
    for i in range(0,np.shape(neg_control_subset_mat)[0]):
        temp_row_shuffle_order = np.arange(np.shape(neg_control_subset_mat)[1])
        np.random.shuffle(temp_row_shuffle_order)
        temp_row_shuffle_order = temp_row_shuffle_order.tolist()

        neg_control_subset_mat[i,:] = neg_control_subset_mat[i,temp_row_shuffle_order]

    ## get the spearman_rhos for the shuffled matrix
    r=no_p_spear(neg_control_subset_mat,neg_control_subset_mat, axis = 1, prop=args.prop)
    r = r[:bin_size,:bin_size]
    print("rho shape",np.shape(r))
    ## remove self correlations
    upper_tiangle_indices = np.triu_indices(bin_size,k=1)
    
    
    ## subset the negative ones
    print(r)
    linear_rho = r[upper_tiangle_indices]
    print(linear_rho)
    print(max(linear_rho))
    print(len(np.where(linear_rho == max(linear_rho))[0]))
    ## calculate the median absolute deviation
    #calculate_mad(linear_rho)

    negative_control_negative_rho_vect = linear_rho[np.where(linear_rho<0)[0]]
    negative_control_positive_rho_vect = linear_rho[np.where(linear_rho>0)[0]]
    #calculate_mad(negative_control_negative_rho_vect)

    ## plot the average Rho per negative correlation
    print(negative_control_negative_rho_vect)
    neg_cor_density_x, neg_cor_density_y = get_density(negative_control_negative_rho_vect)
    pos_cor_density_x, pos_cor_density_y = get_density(negative_control_positive_rho_vect)
    
    
    sum_neg_plot = os.path.dirname(args.adj_list_out)+'/boostrap_neg_cor_rhos.png'
    plot_one_density(neg_cor_density_x, neg_cor_density_y, sum_neg_plot, label="density of negative correlation null distribution")
    pos_rho_plot = os.path.dirname(args.adj_list_out)+'/boostrap_pos_cor_rhos.png'
    plot_one_density(pos_cor_density_x, pos_cor_density_y,pos_rho_plot, label="density of positive correlation null distribution")

    ## plot the distribution of all bootstrap negative control Rhos
    neg_cor_density_x, neg_cor_density_y = get_density(linear_rho)
    sum_neg_plot = os.path.dirname(args.adj_list_out)+'/boostrap_cor_rhos.png'
    plot_one_density(neg_cor_density_x, neg_cor_density_y, sum_neg_plot,label="density of all correlation null distribution")

    print("\n\ncalculating negative correlation FPR cutoff from null distribution:")
    #neg_cutoff = get_FPR_cutoff(negative_control_negative_rho_vect,FPR)
    neg_cutoff, FPR = get_Z_cutoff(negative_control_negative_rho_vect)
    print('\nEmpiric FPR:',FPR)
    print("\n\ncalculating positive correlation FPR cutoff from null distribution:")
    #pos_cutoff = get_FPR_cutoff(negative_control_positive_rho_vect,pos_FPR, positive = True)
    pos_cutoff = get_Z_cutoff(negative_control_positive_rho_vect, z=5.5, positive = True)
    rho_cutoff = pos_cutoff
    args.rho_cutoff = pos_cutoff
    #sys.exit()
#################################################################################
    
## make the output file
cmd('rm '+args.adj_list_out)
cmd('rm '+args.adj_list_out[:-4]+"_dedup.tsv")
out_file_name = args.adj_list_out[:-4]+"_dedup.tsv"
out_file = open(out_file_name, "a")

#out_file.write('\t'.join(['var_1', 'var_2', 'NA', 'NA','NA','NA','rho'])+'\n')
if not args.prop:
    out_file.write('\t'.join(['var_1', 'var_2', 'rho'])+'\n')
else:
    out_file.write('\t'.join(['var_1', 'var_2', 'phi_proportionality'])+'\n')


for rho in rho_files:
    num_pos_cor_dict = {str(temp_id):0 for idx, temp_id in enumerate(IDlist)}
    ## go through all the rho dict files
    print('reading in', rho)
    temp_rho_mat = import_dict(rho)
    temp_indices, temp_IDs = rho_properties_dict[rho]
    for i in range(0,np.shape(temp_rho_mat)[0]):
        ## go through each line in the rho matrix and log the pertinent indices
        cur_i_variable = temp_IDs[i]
        sig_indices = np.where(np.absolute(temp_rho_mat[i,:])>=args.rho_cutoff)[0]
        sig_IDs = [temp_IDs[j] for j in sig_indices]
        sig_rhos = temp_rho_mat[i,sig_indices]

        ## go through the significant indicies
        for q in range(0,len(sig_IDs)):
            if sig_IDs[q] != cur_i_variable:
                if ID_hash[cur_i_variable] > ID_hash[sig_IDs[q]]:
                    ## check if variable pair has been done already
                    temp_relationships = all_vars_adj_dict[cur_i_variable]
                    var2_idx = ID_hash[sig_IDs[q]]
                    ## check if it has been done (ie: currently set to zero.)
                    if temp_relationships[var2_idx] == 0:
                        temp_relationships[var2_idx]+=1## this is the indicator that we've doen it already
                        all_vars_adj_dict[cur_i_variable] = temp_relationships
                        #temp_out_line = [str(cur_i_variable), str(sig_IDs[q]), 'NA', 'NA','NA','NA',str(sig_rhos[q])]
                        temp_out_line = [str(cur_i_variable), str(sig_IDs[q]), str(sig_rhos[q])]
                        out_file.write('\t'.join(temp_out_line)+'\n')
                        ## also log the positive correlations
                        num_pos_cor_dict[str(cur_i_variable)] = 1 + num_pos_cor_dict[str(cur_i_variable)] 
                        num_pos_cor_dict[str(sig_IDs[q])] = 1 + num_pos_cor_dict[str(sig_IDs[q])] 
        
        if do_sum_neg:
            ## do the same for all of the negative correlations, regardless of magnitude
            total_negative_indices = np.where(temp_rho_mat[i,:]<0)[0]
            neg_IDs = [temp_IDs[j] for j in total_negative_indices]
            neg_rhos = temp_rho_mat[i,total_negative_indices]
            for q in range(0,len(neg_rhos)):
                if ID_hash[cur_i_variable] > ID_hash[neg_IDs[q]]:

                    ## check if variable pair has been done already
                    temp_relationships = total_neg_vars_adj_dict[cur_i_variable]
                    var2_idx = ID_hash[neg_IDs[q]]
                    if temp_relationships[var2_idx] == 0:
                        ## total number of Rho <0
                        temp_relationships[var2_idx]+=1
                        total_neg_vars_adj_dict[cur_i_variable] = temp_relationships
                        sum_neg[ID_hash[cur_i_variable]][3]+=1
                        sum_neg[ID_hash[neg_IDs[q]]][3]+=1

                        ## then if it's actually less than the simulation determined cutoff, log it for that as well
                        if neg_rhos[q]<neg_cutoff:# and neg_rhos[q]>-1 :
                            sum_neg[ID_hash[cur_i_variable]][1]+=neg_rhos[q]
                            sum_neg[ID_hash[neg_IDs[q]]][1]+=neg_rhos[q]

                            ## total number < auto-determined Rho cutoff from bootstrap shuffled negative correlations
                            sum_neg[ID_hash[cur_i_variable]][2]+=1
                            sum_neg[ID_hash[neg_IDs[q]]][2]+=1


out_file.close()

if do_sum_neg:
    ## sum up the negative correlations for the bootstrap shuffled negative control
    negative_control_sum_neg = []
    negative_control_count_neg = []
    for i in range(0,np.shape(r)[0]):
        neg_indices = np.where(r[i,:]<0)[0]
        count_neg = np.shape(neg_indices)[0]
        negative_control_count_neg.append(count_neg)
        sum_neg_rhos = sum(r[i,neg_indices])
        negative_control_sum_neg.append(sum_neg_rhos)

    ## calculate the average per comparison for each gene, then multiply it by the number of comparisons 
    ## in the full dataset. This extrapolates the subset to the size of the full dataset.
    ## this will then be used to dynamicaly set the cutoff of what counts as a negative correlation 
    ## at the desired FDR (default FDR = 0.05)
    negative_control_avg_neg = np.array(negative_control_sum_neg)/np.array(negative_control_count_neg)
    negative_control_sum_neg = (np.array(negative_control_sum_neg)/bin_size)*len(IDlist)
    #negative_control_avg_neg = 
    max_neg_ctr = max(negative_control_sum_neg)
    print("max of the negative control =",max_neg_ctr)


    ######################################################################################
    ## process the sum negative table into a vector so that we can do interesting things with it
    print(sum_neg[:10])
    sum_neg_vect = np.zeros(len(sum_neg),dtype = float)
    sum_neg_count = np.zeros(len(sum_neg),dtype = float)
    sum_neg_count_total = np.zeros(len(sum_neg),dtype = float)
    non_sig_neg_count = np.zeros(len(sum_neg),dtype = float)
    for i in range(0,len(sum_neg)):
        sum_neg_vect[i]=sum_neg[i][1]
        sum_neg_count[i]=sum_neg[i][2]
        sum_neg_count_total[i]=sum_neg[i][3]
        non_sig_neg_count[i] = sum_neg[i][3] - sum_neg[i][2]

    sum_neg_vect = np.array(sum_neg_vect)
    sum_neg_count = np.array(sum_neg_count)
    sum_neg_count_total = np.array(sum_neg_count_total)
    count_above_threshold = sum_neg_count_total - sum_neg_count
    count_above_below_ratio = (sum_neg_count+1)/(count_above_threshold+1)

    ## log the ratios in the output file
    for i in range(0,len(sum_neg)):
        sum_neg[i][4]=count_above_below_ratio[i]

    avg_neg = sum_neg_vect/sum_neg_count
    print(sum_neg_vect[:10])


    ## neg count
    #print('\n\t\tcalculating median absolute deviation for the total significant negative count')
    # given the total number of observed negative correlations (expected_y)
    print("max of sum_neg_count_total",np.max(sum_neg_count_total))
    expected_y = np.arange(np.max(sum_neg_count_total))
    expected_x = expected_y/(FPR/FPR_multiple)
    expected_x = np.log2(expected_x)
    expected_x = expected_x[1:]
    expected_y = expected_y[1:]
    print(expected_y)
    print(expected_x)
    #sys.exit()
    sum_neg_count = np.log2(sum_neg_count+1)
    #med,med_dev,cutoff = calculate_mad(sum_neg_count,mean=False)

    ## append whether or not they passed the cutoff to the summary matrix
    def pass_cutoff(above, total, num_pos_cor, num_pos_cor_cutoff = 10):
        global FPR,FPR_multiple, expected_x, expected_y
        ## find the nearest for total (which corresponds to expected_y)
        lowest_index = np.argmin(abs(total - expected_y))
        ## the corresponding y index is the cutoff value
        temp_cutoff = expected_x[lowest_index]
        # if above < 10:
        #     return("False")
        # elif above > temp_cutoff:
        #     return("True")
        # else:
        #     return("False")
        if above < 1:#10:
            return("False")
        elif total/above < (FPR/FPR_multiple) and num_pos_cor >= num_pos_cor_cutoff:
            return("True")
        else:
            return("False")

    #[ID, sum_negative_rho, count_below_threshold, total_number_negative, (count_below_threshold+1)/(count_above_threshold +1)]
    included_indices = []
    for i in range(0,len(sum_neg)):
        sum_neg[i].append(pass_cutoff(sum_neg[i][2],sum_neg[i][3], num_pos_cor_dict[sum_neg[i][0]], num_pos_cor_cutoff = args.num_pos_cor_cutoff))
        if eval(sum_neg[i][-1]):
            included_indices.append(i)
        # sum_neg[]
        # temp_pass = "False"
        # if sum_neg_count[i] > np.log2(expected_false_positives+1):
        #     temp_pass = "True"
        # sum_neg[i].append(temp_pass)


    # ## plot the average Rho per negative correlation
    # neg_cor_density_x, neg_cor_density_y = get_density(avg_neg)
    # series_2_x, series_2_y = get_density(negative_control_sum_neg)
    
    # sum_neg_plot = os.path.dirname(args.adj_list_out)+'/avg_neg_cor.png'
    # plot_densities(neg_cor_density_x, neg_cor_density_y, series_2_x, series_2_y, sum_neg_plot) 

    ## plot the ratio of negative correlations below and above the bootstrap shuffled determined cutoff
    print('count_above_below_ratio',count_above_below_ratio)
    neg_cor_density_x, neg_cor_density_y = get_density(count_above_below_ratio)
    
    sum_neg_plot = os.path.dirname(args.adj_list_out)+'/ratio_of_neg_cor_above_below_cutoff.png'
    plot_one_density(neg_cor_density_x, neg_cor_density_y, sum_neg_plot) 

    ## plot the counts of negative correlations against
    neg_cor_density_x, neg_cor_density_y = get_density(count_above_below_ratio)
    
    sum_neg_plot = os.path.dirname(args.adj_list_out)+'/ratio_of_neg_cor_above_below_cutoff.png'
    plot_one_density_x_cutoff(neg_cor_density_x, neg_cor_density_y, 1/1000, sum_neg_plot) 

    ## plot the counts of significant vs non-significant
    count_sig_vs_non_sig = os.path.dirname(args.adj_list_out)+'/sig_neg_count_vs_total_neg_count.png'
    density_scatter(sum_neg_count,sum_neg_count_total,count_sig_vs_non_sig,log_density=4,expected_x=expected_x,expected_y=expected_y)
    count_sig_vs_non_sig = os.path.dirname(args.adj_list_out)+'/sig_neg_count_vs_total_neg_count_included_only.png'
    if len(included_indices)>0:
        density_scatter(sum_neg_count[included_indices],sum_neg_count_total[included_indices],count_sig_vs_non_sig,log_density=4,expected_x=expected_x,expected_y=expected_y)



    ## write the results to file
    sum_neg_out = os.path.dirname(args.adj_list_out)+'/sum_neg_cor.txt'
    write_table(sum_neg,sum_neg_out)




################################################################################

#cmd('remove_dups.py -infile '+args.adj_list_out)












