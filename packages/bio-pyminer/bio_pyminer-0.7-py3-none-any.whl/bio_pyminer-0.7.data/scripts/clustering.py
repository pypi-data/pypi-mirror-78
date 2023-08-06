#!/home/scott/anaconda3.7/bin/python3
# from __future__ import division, print_function, absolute_import
# import warnings
# import math
# from collections import namedtuple
# # Scipy imports.
# from scipy._lib.six import callable, string_types, xrange
# from scipy._lib._version import NumpyVersion
# from numpy import array, asarray, ma, zeros
from sklearn.cluster import AffinityPropagation as ap
import scipy.special as special
import scipy.linalg as linalg
import numpy as np
from scipy.stats import rankdata
import networkx as nx
import community
import h5py
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
import random
from random import sample
from scipy.stats import gaussian_kde
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from copy import deepcopy

try:
    from pyminer.common_functions import *
    #from pyminer.pyminer_feature_selection import *
    #from pyminer.pyminer_common_stats_functions import *
    from pyminer.pyminer_common_stats_functions import no_p_spear
except:
    from common_functions import *
    #from pyminer_feature_selection import *
    #from pyminer_common_stats_functions import *
    from pyminer_common_stats_functions import no_p_spear

try:
    import umap
except:
    has_umap=False
else:
    has_umap=True

# ########## requirements for no-p spear
# __all__ = ['find_repeats', 'gmean', 'hmean', 'mode', 'tmean', 'tvar',
#            'tmin', 'tmax', 'tstd', 'tsem', 'moment', 'variation',
#            'skew', 'kurtosis', 'describe', 'skewtest', 'kurtosistest',
#            'normaltest', 'jarque_bera', 'itemfreq',
#            'scoreatpercentile', 'percentileofscore', 'histogram',
#            'histogram2', 'cumfreq', 'relfreq', 'obrientransform',
#            'signaltonoise', 'sem', 'zmap', 'zscore', 'iqr', 'threshold',
#            'sigmaclip', 'trimboth', 'trim1', 'trim_mean', 'f_oneway',
#            'pearsonr', 'fisher_exact', 'spearmanr', 'pointbiserialr',
#            'kendalltau', 'linregress', 'theilslopes', 'ttest_1samp',
#            'ttest_ind', 'ttest_ind_from_stats', 'ttest_rel', 'kstest',
#            'chisquare', 'power_divergence', 'ks_2samp', 'mannwhitneyu',
#            'tiecorrect', 'ranksums', 'kruskal', 'friedmanchisquare',
#            'chisqprob', 'betai',
#            'f_value_wilks_lambda', 'f_value', 'f_value_multivariate',
#            'ss', 'square_of_sums', 'fastsort', 'rankdata',
#            'combine_pvalues', ]


# def _chk_asarray(a, axis):
#     if axis is None:
#         a = np.ravel(a)
#         outaxis = 0
#     else:
#         a = np.asarray(a)
#         outaxis = axis
#     if a.ndim == 0:
#         a = np.atleast_1d(a)
#     return a, outaxis


# def _chk2_asarray(a, b, axis):
#     if axis is None:
#         a = np.ravel(a)
#         b = np.ravel(b)
#         outaxis = 0
#     else:
#         a = np.asarray(a)
#         b = np.asarray(b)
#         outaxis = axis
#     if a.ndim == 0:
#         a = np.atleast_1d(a)
#     if b.ndim == 0:
#         b = np.atleast_1d(b)
#     return a, b, outaxis


# def _contains_nan(a, nan_policy='propagate'):
#     policies = ['propagate', 'raise', 'omit']
#     if nan_policy not in policies:
#         raise ValueError("nan_policy must be one of {%s}" %
#                          ', '.join("'%s'" % s for s in policies))
#     try:
#         # Calling np.sum to avoid creating a huge array into memory
#         # e.g. np.isnan(a).any()
#         with np.errstate(invalid='ignore'):
#             contains_nan = np.isnan(np.sum(a))
#     except TypeError:
#         # If the check cannot be properly performed we fallback to omiting
#         # nan values and raising a warning. This can happen when attempting to
#         # sum things that are not numbers (e.g. as in the function `mode`).
#         contains_nan = False
#         nan_policy = 'omit'
#         warnings.warn("The input array could not be properly checked for nan "
#                       "values. nan values will be ignored.", RuntimeWarning)
#     if contains_nan and nan_policy == 'raise':
#         raise ValueError("The input contains nan values")
#     return (contains_nan, nan_policy)


# def no_p_spear(a, b=None, axis=0, nan_policy='propagate'):
#     a, axisout = _chk_asarray(a, axis)
    
#     contains_nan, nan_policy = _contains_nan(a, nan_policy)
    
#     if contains_nan and nan_policy == 'omit':
#         a = ma.masked_invalid(a)
#         b = ma.masked_invalid(b)
#         return mstats_basic.spearmanr(a, b, axis)
    
#     if a.size <= 1:
#         return SpearmanrResult(np.nan, np.nan)
#     ar = np.apply_along_axis(rankdata, axisout, a)
    
#     br = None
#     if b is not None:
#         b, axisout = _chk_asarray(b, axis)
        
#         contains_nan, nan_policy = _contains_nan(b, nan_policy)
        
#         if contains_nan and nan_policy == 'omit':
#             b = ma.masked_invalid(b)
#             return mstats_basic.spearmanr(a, b, axis)
        
#         br = np.apply_along_axis(rankdata, axisout, b)
#     n = a.shape[axisout]
#     rs = np.corrcoef(ar, br, rowvar=axisout)
#     rs = np.nan_to_num(rs)
    
#     olderr = np.seterr(divide='ignore')  # rs can have elements equal to 1
#     try:
#         # clip the small negative values possibly caused by rounding
#         # errors before taking the square root
#         t = rs * np.sqrt(((n-2)/((rs+1.0)*(1.0-rs))).clip(0))
#     finally:
#         np.seterr(**olderr)
    
#     if rs.shape == (2, 2):
#         return rs[1, 0]
#     else:
#         return rs

########################################################
########################################################
########################################################
##############################################################
# ## basic function library
# def read_file(tempFile,linesOraw='lines',quiet=False):
#     if not quiet:
#         print('reading',tempFile)
#     f=open(tempFile,'r')
#     if linesOraw=='lines':
#         lines=f.readlines()
#         for i in range(0,len(lines)):
#             lines[i]=lines[i].strip('\n')
#     elif linesOraw=='raw':
#         lines=f.read()
#     f.close()
#     return(lines)

# def make_file(contents,path):
#     f=open(path,'w')
#     if isinstance(contents,list):
#         f.writelines(contents)
#     elif isinstance(contents,str):
#         f.write(contents)
#     f.close()

    
# def flatten_2D_table(table,delim):
#     #print(type(table))
#     if str(type(table))=="<class 'numpy.ndarray'>":
#         out=[]
#         for i in range(0,len(table)):
#             out.append([])
#             for j in range(0,len(table[i])):
#                 try:
#                     str(table[i][j])
#                 except:
#                     print(table[i][j])
#                 else:
#                     out[i].append(str(table[i][j]))
#             out[i]=delim.join(out[i])+'\n'
#         return(out)
#     else:
#         for i in range(0,len(table)):
#             for j in range(0,len(table[i])):
#                 try:
#                     str(table[i][j])
#                 except:
#                     print(table[i][j])
#                 else:
#                     table[i][j]=str(table[i][j])
#             table[i]=delim.join(table[i])+'\n'
#     #print(table[0])
#         return(table)

# def strip_split(line, delim = '\t'):
#     return(line.strip('\n').split(delim))

# def make_table(lines,delim):
#     for i in range(0,len(lines)):
#         lines[i]=lines[i].strip()
#         lines[i]=lines[i].split(delim)
#         for j in range(0,len(lines[i])):
#             try:
#                 float(lines[i][j])
#             except:
#                 lines[i][j]=lines[i][j].replace('"','')
#             else:
#                 lines[i][j]=float(lines[i][j])
#     return(lines)


# def get_file_path(in_path):
#     in_path = in_path.split('/')
#     in_path = in_path[:-1]
#     in_path = '/'.join(in_path)
#     return(in_path+'/')


# def read_table(file, sep='\t'):
#     return(make_table(read_file(file,'lines'),sep))
    
# def write_table(table, out_file, sep = '\t'):
#     make_file(flatten_2D_table(table,sep), out_file)
    

# def import_dict(f):
#     f=open(f,'rb')
#     d=pickle.load(f)
#     f.close()
#     return(d)

# def save_dict(d,path):
#     f=open(path,'wb')
#     pickle.dump(d,f)
#     f.close()

# def cmd(in_message, com=True):
#     print(in_message)
#     time.sleep(.25)
#     if com:
#         Popen(in_message,shell=True).communicate()
#     else:
#         Popen(in_message,shell=True)



##############################################################

##########################################################################
parser = argparse.ArgumentParser()

## global arguments
parser.add_argument(
	'-infile','-in','-i','-input',
	dest='infile',
	type=str)

parser.add_argument(
    '-out','-o','-out_dir',
    dest='out_dir',
    type=str)

parser.add_argument(
	"-sample_k_known",
    help='If you know how many groups there should be, give an int with this argument',
 	dest = 'sample_k_known',
 	type = int,
    default = 0)

parser.add_argument(
    "-sample_cluster_iter",
    help='the number of iterations for clustering. Default = 10, but going higher will cost more time and yeild better results.',
    dest = 'sample_cluster_iter',
    type = int,
    default = 10)

parser.add_argument(
    "-rand_seed",'-seed',
    help='the random number input for random number seed, default = 12345',
    dest = 'rand_seed',
    type = int,
    default = 12345)

parser.add_argument(
	"-rows",
    help='if you want to cluster the rows instead of columns (default is to cluster columns).',
 	dest = 'do_rows',
 	action = 'store_true',
    default = False)

parser.add_argument(
    "-hdf5", '-do_hdf5',
    help='if we are dealing with an hdf5 file format. This also requires the -columns argument',
    dest = 'do_hdf5',
    action = 'store_true',
    default = False)

parser.add_argument(
    '-columns','-c','-col','-cols','-column_ids','-column_IDs',
    dest='columns',
    type=str)

parser.add_argument(
    '-ID_list','-ids','-IDs','-ID',
    type=str)

parser.add_argument(
    "-var_norm",
    help='if you want to normalize the rows prior to clustering',
    dest = 'var_norm',
    action = 'store_true',
    default = False)

parser.add_argument(
    "-log",'-log2','-log_transform',
    help='do a log transformation prior to clustering',
    action = 'store_true',
    default = False)

parser.add_argument(
    "-rank",
    help='do a rank transformation on the features prior to clustering',
    action = 'store_true',
    default = False)

parser.add_argument(
    "-no_var_norm",
    help='do not normalize the variables for sample clustering',
    dest='var_norm',
    action='store_false',
    default = True)

parser.add_argument(
    "-ap_clust",'-ap',
    help='do affinity propagation clustering',
    action = 'store_true',
    default = False)

parser.add_argument(
    "-louvain_clust",'-louv',
    help='do Louvain modularity for clustering',
    action = 'store_true',
    default = False)

parser.add_argument(
    '-clust_on_genes',
    help = "cluster on the genes listed in the input text file with this argument.",
    type=str)

parser.add_argument(
    '-neg_cor_clust',
    help = "if you want to do clustering based off of only negatively correlated variables, feed in the table which summarizes the positive and negative relationships",
    type=str)

parser.add_argument(
    '-neg_cor_count_clust',
    help = "if you want to do clustering based off of the number of significantly negative correlations, as determined by bootstrap shuffled negative control",
    type=str)

parser.add_argument(
    "-no_spearman_clust",
    help='will not perform clustering on the sample-wise spearman correlation matrix',
    dest='spearman_dist',
    action = 'store_false',
    default = True)

parser.add_argument(
    "-neg_cor_cutoff",
    help='the cutoff for number of relationships to include for a negative correlation based clustering run (default = 15)',
    type = int,
    default = 15)

parser.add_argument(
    "-first_neg_neighbor",'-neg_neighbor',
    help='For negative correlation clusters only. Get the first neighbors (co-regulated) of the negative correlated genes',
    action = 'store_true',
    default = False)

parser.add_argument(
    "-leave_mito_ribo",
    help = "don't remove the mitochondrial and ribosomal genes for clustering.",
    action = "store_true",
    default = False)


parser.add_argument(
    "-sc_clust",
    help='set parameters for single cell RNAseq cell-type identification',
    action = 'store_true',
    default = False)


parser.add_argument(
    '-pos_adj_list',
    help = "for smoothing out the negative correlation clustering, add the first neighbors of these genes",
    type=str)

parser.add_argument(
    '-merge',
    help = "for mergering groups based on similarity. Particularly useful for reconstructing lineage trees.",
    dest = 'do_merger',
    action = 'store_true',
    default = False)

parser.add_argument(
    '-ap_merge',
    help = "This changes the ap clustering to an agglomerative ap clustering which merges clusters of sufficient similarity. Note that this *can* result in non-spaerical clusters, but might not necessarily.",
    dest = 'ap_merge',
    action = 'store_true',
    default = False)

parser.add_argument(
    '-point_size', '-pt_size', '-ps',
    help = 'For plotting the points, how big should they be? (default = 6)',
    type=float,
    default = 6)

parser.add_argument(
    "-perplexity",
    help='Perplexity value to use for tSNE',
    type=int)

parser.add_argument(
    "-tsne_iter",
    help='iterations for tSNE. Default = 1e6',
    type=str,
    default = '1e6')

parser.add_argument(
    "-dpi",
    help='dots per inch',
    default = 600,
    type=int)

parser.add_argument(
    "-manual_sample_groups",
    help='if you already know the sample groups, but just want some plots',
    type=str)

parser.add_argument("-species", '-s',
    help="a gProfiler accepted species code. Dafault = 'hsapiens'",
    type = str,
    default = 'hsapiens')

parser.add_argument(
    '-block_size',
    help = 'In case this dataset is too big for memory, we need the block size (default = 5000)',
    type=int,
    default = 5000)

args = parser.parse_args()
##########################################################################
##########################################################################
if args.sc_clust:
    args.do_merger = True
    args.spearman_dist = True
    args.ap_clust = True
    args.ap_merge = True
    if args.neg_cor_count_clust == None:
        sys.exit('-sc_clust requires an input for the -neg_cor_count_clust option')
    
##########################################################################
##########################################################################
args.infile = os.path.realpath(args.infile)
infile_original_dir = get_file_path(args.infile)

np.random.seed(args.rand_seed)
random.seed(args.rand_seed)

## make a good heatmap color scheme
global_cmap = sns.color_palette("coolwarm", 256)



if args.sample_cluster_iter < 1:
    sys.exit('-sample_cluser_iter must be greater than zero, or else we have nothing to do')

if args.out_dir == None:
	args.out_dir = get_file_path(args.infile)+'sample_clustering_and_summary/'

sample_cluster_iter = args.sample_cluster_iter
sample_dir = args.out_dir
temp = args.out_dir
cmd('mkdir '+args.out_dir)

sample_k_known = args.sample_k_known
if sample_k_known<0:
    sys.exit('sample_k_known must be a positive integer, or zero')

if sample_k_known >0:
    pre_determined_sample_k = sample_k_known
    sample_k_known = True
else:
    pre_determined_sample_k = None
    sample_k_known = False

#######
if args.neg_cor_clust!=None and args.clust_on_genes != None:
    sys.exit("-neg_cor_clust and -clust_on_genes are mututually exclusive arguments")


##########################################################################

def lin_norm_rows(in_mat,min_range=0,max_range=1):
    in_mat = np.transpose(np.array(in_mat))
    in_mat = in_mat - np.min(in_mat, axis = 0)
    in_mat = in_mat / np.max(in_mat, axis = 0)
    in_mat[np.isnan(in_mat)]=0
    return(np.transpose(in_mat))

def lin_norm_rows_hdf5():
    global full_expression
    mins = np.transpose(np.array([np.min(full_expression, axis = 1)]))
    full_expression -= mins
    maxs = np.transpose(np.array([np.max(full_expression, axis = 1)]))
    full_expression /= maxs
    #sys.exit()
    return()

##########################################################################


###### START COPIED TO PYMINER_FEATURE_SELECTION.PY ######
##########################################################################
## if we are doing a negative correlation based run, subset the input matrix
## neg_cor plotting
def get_density(in_vect):
    density = gaussian_kde(in_vect)
    xs = np.arange(0,max(in_vect),.1)
    density.covariance_factor = lambda : 2.5
    density._compute_covariance()
    return(xs,density(xs))

def plot_densities(neg_cor_density_x, neg_cor_density_y, pos_cor_density_x, pos_cor_density_y,out_file):
    global args
    x_min = min([np.min(neg_cor_density_x),np.min(pos_cor_density_x)])
    y_min = min([np.min(neg_cor_density_y),np.min(pos_cor_density_y)])
    x_min = max([np.max(neg_cor_density_x),np.max(pos_cor_density_x)])
    y_min = max([np.max(neg_cor_density_y),np.max(pos_cor_density_y)])

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = 'negative correlation degree density',
        color = 'blue',
        linewidth = 3)
    plt.plot(pos_cor_density_x, pos_cor_density_y, 
        label = 'positive correlation degree density',
        color = 'red',
        linewidth = 3)
    plt.legend()
    plt.savefig(out_file,
        dpi=args.dpi,
        bbox_inches='tight')

def remove_zeros(in_vect):
    in_vect = np.array(in_vect).tolist()
    out_vect = []
    for i in range(0,len(in_vect)):
        if in_vect[i]!=0:
            out_vect.append(in_vect[i])
    return(out_vect)

def get_first_neighbors(passing_ids):
    global args
    first_neighbors = []
    for line in fileinput.input(args.pos_adj_list):
        temp_line = strip_split(line)
        if temp_line[0] in passing_ids or temp_line[1] in passing_ids:
            if temp_line[0] not in first_neighbors:
                first_neighbors.append(temp_line[0])
            if temp_line[1] not in first_neighbors:
                first_neighbors.append(temp_line[1])
    fileinput.close()
    return(first_neighbors)
## /neg_cor plotting
###### END COPIED TO PYMINER_FEATURE_SELECTION.PY ######
##########################################################################
##########################################################################
##########################################################################

if not args.do_hdf5:
    full_expression_str = read_table(args.infile)
else:
    row_names = read_file(args.ID_list,'lines')
    title = read_file(args.columns,'lines')
    print('making a maliable hdf5 file to preserve the original data')
    cmd('cp '+args.infile+' '+args.infile+'_copy')
    print('reading in hdf5 file')
    infile_path = args.infile+'_copy'
    h5f = h5py.File(infile_path, 'r+')
    full_expression=h5f["infile"]

##########################################################################
##########################################################################
## SECTION 1
###### START COPIED TO PYMINER_FEATURE_SELECTION.PY ######
if args.neg_cor_clust != None:
    print('getting the negatively correlated variables')
    ## first we get the variables that pass muster (ie: have enough negative correlations)
    cor_stat_table = read_table(args.neg_cor_clust)
    num_genes_total = len(cor_stat_table)-1
    percentile_cutoff = 0.975
    top_num = int(num_genes_total * percentile_cutoff)

    ## make the plots
    cor_stat_array = np.array(cor_stat_table[:])

    ## get the vectors for the correlation counts
    neg_cor_vect = np.array(cor_stat_array[1:,2], dtype = float)
    pos_cor_vect = np.array(cor_stat_array[1:,1], dtype = float)
    neg_cor_density_x, neg_cor_density_y = get_density(neg_cor_vect)
    pos_cor_density_x, pos_cor_density_y = get_density(pos_cor_vect)

    ## plot them
    plot_densities(neg_cor_density_x, neg_cor_density_y, pos_cor_density_x, pos_cor_density_y,args.out_dir+'negative_positive_correlation_degree_density.png')
    neg_cor_list = sorted(neg_cor_vect[:].tolist())
    print(neg_cor_list[top_num])
    args.neg_cor_cutoff = neg_cor_list[top_num]

    ## do the same but after removing the zeros


    ## remove the zeros from these vectors
    neg_cor_vect_noZero = neg_cor_vect[:]
    pos_cor_vect_noZero = pos_cor_vect[:]
    neg_cor_vect_noZero = remove_zeros(neg_cor_vect_noZero)
    pos_cor_vect_noZero = remove_zeros(pos_cor_vect_noZero)

    ## get their densities and plot them
    nonZero_neg_cor_density_x, nonZero_neg_cor_density_y = get_density(neg_cor_vect_noZero)
    nonZero_pos_cor_density_x, nonZero_pos_cor_density_y = get_density(pos_cor_vect_noZero)
    plot_densities(nonZero_neg_cor_density_x, nonZero_neg_cor_density_y, nonZero_pos_cor_density_x, nonZero_pos_cor_density_y,args.out_dir+'non_zero_negative_positive_correlation_degree_density.png')

    ## come up with the dynamically determined cutoff
    neg_cor_vect_noZero = sorted(neg_cor_vect_noZero)
    percentile_cutoff = 0.85
    top_num = int(len(neg_cor_vect_noZero)*percentile_cutoff)
    print(neg_cor_vect_noZero[top_num])
    args.neg_cor_cutoff = neg_cor_vect_noZero[top_num]

if args.neg_cor_clust!=None:
    passing_ids = []
    for i in range(1,len(cor_stat_table)):
        # start at 1 because of the title line
        if cor_stat_table[i][2] >= args.neg_cor_cutoff:
            # format is: id, # pos cor, # neg cor
            passing_ids.append(cor_stat_table[i][0])

    if len(passing_ids) == 0:
        ## if there aren't any anti-correlated genes, 
        ## then you probably only have one one cell type/state
        print('we only found one cell type/state')



if args.neg_cor_count_clust!=None:
    neg_cor_clust_table = read_table(args.neg_cor_count_clust)
    passing_ids = []
    for i in range(0,len(neg_cor_clust_table)):
        #print(neg_cor_clust_table[i][-1])
        if neg_cor_clust_table[i][-1] == "True":
            passing_ids.append(neg_cor_clust_table[i][0])



if args.neg_cor_clust!=None or args.neg_cor_count_clust!=None:
    ## to prevent giving too much weight to a single gene's expression, we can get the 
    ## first neighbor genes of the co-regulatory network, and add them to the genes 
    ## which got into the first pass negative correlation subset
    if args.first_neg_neighbor and False:
        print('getting the first neighbors of the highly negatively correlated genes')
        first_neighbors = get_first_neighbors(passing_ids)
        passing_ids = sorted(list(set(passing_ids+first_neighbors)))
        #print(passing_ids)

    if not args.do_hdf5:
        temp_full_expression_str = [full_expression_str[0]]
        #print(temp_full_expression_str)
        print(len(passing_ids),'of the variables had enough negative correlations to make the cut')
        ## collect the IDs that 
        usable_indices = []
        for i in range(1,len(full_expression_str)):
            ## start at 1 because of the title line
            if full_expression_str[i][0] in passing_ids:
                usable_indices.append(i-1)#-1 because of the title line
                #temp_full_expression_str.append(full_expression_str[i])
        #full_expression_str = temp_full_expression_str[:]
        #del temp_full_expression_str
        print('found',len(usable_indices),'usable indicies')
        #write_table(full_expression_str[:],args.out_dir+'neg_cor_mat_used_for_clustering.txt')
    else:
        usable_indices = []
        new_row_names = []
        for i in range(0,len(row_names)):
            if row_names[i] in passing_ids:
                usable_indices.append(i)
                new_row_names.append(row_names[i])
        print(len(usable_indices),'of the variables had enough negative correlations to make the cut')
## /SECTION 1
###### END COPIED TO PYMINER_FEATURE_SELECTION.PY ######



##########################################################################


if not args.do_hdf5:
    full_expression_np = np.array(full_expression_str)


if args.do_rows:
    if not args.do_hdf5:
        full_expression_np = np.transpose(full_expression_np)
    else:
        full_expression = np.transpose(full_expression)



## remove nans
if not args.do_hdf5:
    full_expression_num = np.array(full_expression_np[1:,1:], dtype = float)
    full_expression_num[np.isnan(full_expression_num)] = 0.0
    full_expression_np[1:,1:] = full_expression_num
else:
    for i in range(0,np.shape(full_expression)[0]):
        temp_row = full_expression[i]
        temp_row[np.isnan(temp_row)] = 0.0
        full_expression[i] = temp_row


if args.log:
    if not args.do_hdf5:
        full_expression_num = np.array(full_expression_np[1:,1:], dtype = float)
        #print(np.sum(full_expression_num))
        #print("min",np.min(full_expression_num))

        full_expression_np[1:,1:]=np.log2(  full_expression_num - np.min(full_expression_num) +1 )
    else:
        for i in range(0,np.shape(full_expression)[0]):
            temp_row = full_expression[i,:]
            temp_row = np.log2(temp_row+1)
            full_expression[i,:] = temp_row




if args.rank:
    ## this will rank transform the features being clustered
    if not args.do_hdf5:
        full_expression_num = np.array(full_expression_np[1:,1:], dtype = float)
        #print(np.sum(full_expression_num))
        #print("min",np.min(full_expression_num))
        for i in range(0,np.shape(full_expression_num)[0]):
            full_expression_num[i,:] = rankdata(full_expression_num[i,:],method='min')
        full_expression_np[1:,1:]=full_expression_num
    else:
        for i in range(0,np.shape(full_expression)[0]):
            full_expression[i,:] = rankdata(full_expression[i,:],method='min')
        




#print(full_expression)
if args.var_norm or args.ap_clust:
    print('normalizing the rows')
    if not args.do_hdf5:
        full_expression_np[1:,1:]=lin_norm_rows(np.array(full_expression_np[1:,1:],dtype=float))
    else:
        lin_norm_rows_hdf5()


if not args.do_hdf5:
    if not args.do_rows:
        title = list(full_expression_np[0])
        #print(title)
        row_names = full_expression_np[1:,0]
        full_expression = np.array(full_expression_np[1:,1:],dtype = float)
    else:
        row_names = list(full_expression_np[0])
        #print(title)
        title = full_expression_np[:,0]
        full_expression = np.array(full_expression_np[1:,1:],dtype = float)
else:
    if not args.do_rows:
        title = read_file(args.columns)
        row_names = read_file(args.ID_list)
    else:
        row_names = read_file(args.columns)[1:]
        title = ['variables'] + read_file(args.ID_list)

#print(np.sum(full_expression))

#print(row_names)
IDlist = list(row_names)
ID_list = IDlist
id_hash = {key:idx for idx, key in enumerate(IDlist)}
print(len(ID_list))
print(ID_list[:5])
temp_dir=str(args.infile).split('/')
temp_dir=('/').join(temp_dir[:-1])
##########################################################


###### START COPIED TO PYMINER_FEATURE_SELECTION.PY ######
if args.clust_on_genes != None:
    print('picking out the specified genes')
    ## this can either be a table with the genes in the left most column or a new-line delimited list of only the gene ids
    ## if the last column is "False" it means this gene will not be included
    clust_on_genes = read_table(args.clust_on_genes)
    clust_gene_ids = []
    clust_gene_idxs = []
    if clust_on_genes == []:
        pass
    else:
        if type(clust_on_genes[0])==list:
            for i in range(0,len(clust_on_genes)):
                #print(clust_on_genes[i])
                try:
                    id_hash[str(clust_on_genes[i][0])]
                except:
                    print("couldn't find",clust_on_genes[i][0])
                else:
                    if clust_on_genes[i][-1] != "False":
                        clust_gene_ids.append(clust_on_genes[i][0])
        else:
            clust_gene_ids = clust_on_genes
        clust_gene_idxs = [id_hash[str(x)] for x in clust_gene_ids]
        if len(clust_gene_idxs)==0:
            print("couldn't find any of the genes in your input -clust_on_genes")
    usable_indices = clust_gene_idxs[:]
    print('\n\nwe found',len(clust_gene_idxs), 'genes in -clust_on_genes input')
else:
    ## if we've already filtered for negative correlations or something like that
    if 'usable_indices' in globals():
        clust_gene_idxs = usable_indices[:]
        #print(usable_indices)
        clust_gene_ids = np.array(ID_list)[usable_indices]
    ## If there weren't any other filters prior to this step
    else:
        clust_gene_ids = ID_list[:]
        clust_gene_idxs = np.arange(len(ID_list)).tolist()

#####################
def process_dict(in_file, ensg_idx):
    out_dict = {}
    for i in range(0,len(in_file)):
        out_dict[in_file[i][ensg_idx]]=True
    return(out_dict)

def quick_search(in_dict,key):
    try:
        in_dict[key]
    except:
        return(False)
    else:
        return(True)
##############################
######### remove the ribosomal and mitochondrial genes if we need to
if args.leave_mito_ribo:
    remove_ribo_mito = False
else:
    remove_ribo_mito = True
#####
## set up a quick-search dictionary
print(len(usable_indices))
print(len(clust_gene_ids))
usable_id_hash = {key:value for value, key in enumerate(clust_gene_ids)}
##
#####

## remove the mito and ribo genes
if remove_ribo_mito:
    print("finding all of the ribosomal and mitchondrial genes to remove")
    ## if we'll remove the mitochondrial and ribsomal related genes first
    mitochondrial = ["GO:0044429","GO:0006390","GO:0005739","GO:0005743",
                     "GO:0070125","GO:0070126","GO:0005759","GO:0032543",
                     "GO:0044455","GO:0005761"]
    ribosome = ["GO:0005840","GO:0003735","GO:0022626","GO:0044391","GO:0006614",
                "GO:0006613","GO:0045047","GO:0000184","GO:0043043","GO:0006413",
                "GO:0022613","GO:0043604","GO:0015934","GO:0006415","GO:0015935",
                "GO:0072599","GO:0071826","GO:0042254","GO:0042273","GO:0042274",
                "GO:0006364","GO:0022618","GO:0005730","GO:0005791","GO:0098554",
                "GO:0019843"]
    ribo_mito_go = mitochondrial + ribosome
    from gprofiler import GProfiler
    gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)
    results = gp.gconvert(ribo_mito_go,organism="hsapiens", target="ENSG")
    #results = gp.gconvert(ribo_mito_go,organism=args.species, target="ENSG")
    ## first go to the annotation file, and read that in.
    if args.species == 'hsapiens':
        if os.path.isfile(infile_original_dir+'annotations.tsv'):
            annotations = read_table(infile_original_dir+'annotations.tsv')
            ensg_idx = 3
    else:
        if os.path.isfile(infile_original_dir+'human_orthologues.tsv'):
            annotations = read_table(infile_original_dir+'human_orthologues.tsv')
            ensg_idx = 4
    ## catelogue the results
    ensg_mito_ribo_dict=process_dict(results,3)
    # if args.species!="hsapiens":
    #     ensg_mito_ribo_dict = convert_dict_to_dict(all_mito_ribo_genes,)
    all_mito_ribo_genes = list(ensg_mito_ribo_dict.keys())
    print('\tfound',len(all_mito_ribo_genes),'mito or ribo genes')
    print('\t\t',all_mito_ribo_genes[:3])
    final_clust_gene_ids = []
    final_clust_gene_idxs = []
    for i in range(1,len(annotations)):
        temp_gene = annotations[i][ensg_idx]
        #temp_idx = clust_gene_idxs[i]
        if quick_search(ensg_mito_ribo_dict,temp_gene):
            print('\texcluding:',annotations[i][1])
            ## here we don't include the mito and ribo genes in the final list
        else:
            # temp_original_id = str(annotations[i][1]).replace("ENTREZGENE_ACC:","")
            # print(temp_original_id)
            # if args.species != "hsapiens":
            #     pass
            # if quick_search(usable_id_hash,temp_original_id):
            #     final_clust_gene_ids.append(temp_original_id)
            #     final_clust_gene_idxs.append(id_hash[temp_original_id])
            # else:
            if int(annotations[i][0])-1 in usable_indices:
                #print("\tproblem mapping",temp_original_id,"but we'll include it")
                final_clust_gene_ids.append(ID_list[int(annotations[i][0])-1])
                final_clust_gene_idxs.append(int(annotations[i][0])-1)
    clust_gene_ids = list(set(final_clust_gene_ids))
    clust_gene_idxs = list(set(final_clust_gene_idxs))
    usable_indices = clust_gene_idxs
#print("\t",len(clust_gene_ids),"genes included for clustering")
print(len(usable_indices),"currenlty usable indices")
## see which of these passing ids
# if "usable_indices" in globals():
#     temp_usable_indices = list(set(usable_indices).intersection(clust_gene_idxs))
temp_usable_indices = list(set(usable_indices))
#print(temp_usable_indices)
##########################################################
## remove genes that are only expressed in a very small number of cells
remove_sparse=True
if remove_sparse and args.clust_on_genes == None:
    print('removing genes that are only observed in 5 percent or less of cells, or 100 cells')
    cutoff = min([100,np.shape(full_expression)[1]*.05])#1% cutuff for expression
    usable_indices = []
    for i in temp_usable_indices:
        num_seen = np.sum(np.array(full_expression[i,:]>0,dtype=int))
        if num_seen >= cutoff:
            usable_indices.append(i)
    print(len(temp_usable_indices)-len(usable_indices),'genes removed because of sparse expression')
    print(len(usable_indices),'used for clustering')
    clust_gene_idxs = usable_indices[:]
    clust_gene_ids = [IDlist[idx] for idx in usable_indices]
    #clust_gene_ids = final_clust_gene_ids
    #clust_gene_idxs = list(set(final_clust_gene_idxs))
    #print("\t",len(clust_gene_ids),"genes included for clustering")
##########################################################
##########################################################
################# end feature selection ##################
##########################################################
##########################################################
##########################################################

###### END COPIED TO PYMINER_FEATURE_SELECTION.PY ######


usable_id_hash = {key:value for value, key in enumerate(clust_gene_ids)}
usable_indices = clust_gene_idxs
usable_indices_hash = {key:value for value, key in enumerate(usable_indices)}
print(len(clust_gene_idxs))
print(len(usable_indices))


if "usable_indices" in globals():
    full_expression = full_expression[usable_indices,:]

## write the indexes used for the clustering to file
used_indices_out = []
for i in range(0,len(usable_indices)):
    used_indices_out.append([ID_list[usable_indices[i]],usable_indices[i]])
write_table(used_indices_out,temp_dir+'/sample_clustering_and_summary/genes_used_for_clustering.txt')

## if there are no usable indices, it means there aren't any distinct cell types
if len(usable_indices)<=1 or (args.neg_cor_count_clust != None and len(usable_indices)<=10):
    print('not enogh usable indicies for clustering! Probably only one group')
    out_table = []
    for i in range(1,len(title)):
        out_table.append([title[i],0])
    out_sample_file = temp_dir+"/sample_clustering_and_summary/sample_k_means_groups.txt"
    write_table(out_table,out_sample_file)
    args.manual_sample_groups = out_sample_file

##########################################################
##########################################################
##########################################################
##########################################################
##########################################################




################# do the clustering ######################


##########################################################
##########################################################
##########################################################
##########################################################

def get_known_centers(sample_k_lists):
    global full_expression_np, ID_list#, sample_k_lists
    ## get the point that is closest to the median for each group
    best_centers = []
    for i in range(0, len(sample_k_lists)):
        temp_idxs = sample_k_lists[i]
        temp_medoid = np.median(full_expression[:,temp_idxs], axis =0)
        # print(np.shape(temp_medoid))
        temp_dist = np.sqrt(np.sum((full_expression[:,temp_idxs]-temp_medoid)**2,axis=0))
        #temp_dist = np.sqrt(np.sum((full_expression[:,temp_idxs]-temp_medoid)**2,axis=1))
        if len(temp_idxs)!=np.shape(temp_dist)[0]:
            print('wrong dimention')
        # print(temp_dist)
        best_idx = np.argmin(temp_dist)
        print(best_idx)
        best_idx = temp_idxs[best_idx]
        best_centers.append(best_idx)
        # print(best_idx)
        # sys.exit()
    return(best_centers)


if args.manual_sample_groups != None:
    print('\n\n\nManual sample groups!\n\n')
    sample_group_table = read_table(args.manual_sample_groups)
    sample_group_table_np = np.array(sample_group_table)
    sample_group_order = np.transpose(sample_group_table_np[:,0])
    sorted_list_of_ids = list(sample_group_order)

    grouping_vector = list(np.transpose(sample_group_table_np[:,1]))
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


    ## get the 'optimal_centroid_indices' for manual sample_groups
    optimal_centroid_indices = get_known_centers(sample_k_lists)


####################################################################

#rho_dir_dict = temp_dir+'/rho_dicts/'
neg_euc_hdf5_file = temp_dir+"/sample_clustering_and_summary/rho_dicts/neg_euc_dist.hdf5"
spear_hdf5_file = temp_dir+"/sample_clustering_and_summary/rho_dicts/spearman.hdf5"
def get_big_spearman():
    global neg_euc_hdf5_file,temp_dir, args
    block_size = args.block_size
    print(args.infile)
    print(args.ID_list)
    euc_call = "mat_to_adj_list.py -time -transpose -hdf5_out -i '"+args.infile+"'"
    if args.do_hdf5: 
        euc_call += " -hdf5 -ids "+args.ID_list
        euc_call += ' -col_ids '+args.columns
    euc_call += ' -block_size '+str(int(block_size))
    euc_call += ' -rho_dict_dir '+temp_dir+'/sample_clustering_and_summary/rho_dicts/'
    if "usable_indices" in globals():
        euc_call += ' -row_subset '+temp_dir+'/used_indices.txt'
        usable_indices_str = usable_indices[:]
        make_file('\n'.join(list(map(str,usable_indices_str))),temp_dir+'/used_indices.txt')
    if True:#args.ap_clust:
        euc_call += " -euclidean_dist "
    if True:
        cmd(euc_call)
    return()


#################################################

from sklearn import metrics
euclidean_distances = metrics.pairwise.euclidean_distances
def try_neg_spear_euc():
    global full_expression,euclidean_distances
    full_expression = no_p_spear(full_expression)
    total_vars = np.shape(full_expression)[1]
    full_expression = -euclidean_distance(full_expression,squared=True)/np.log2(total_vars)
    print('-euclidean dist:\n',full_expression[:5,:5])
    return()

if args.spearman_dist:
    plt.clf()
    all_nans = np.isnan(full_expression)
    if np.sum(all_nans)>0:
        full_expression[all_nans] = np.nanmin(full_expression)
    if False:#try:
        sns.clustermap(full_expression,cmap=global_cmap)
        plt.savefig(temp+'/genes_used_for_clustering_heatmap.png',
            dpi=args.dpi,
            bbox_inches='tight')
    else:#except:
        print("couldn't get the full heatmap going")
        row_dim = np.shape(full_expression)[0]
        col_dim = np.shape(full_expression)[1]
        sample_rows = np.array(list(sorted(np.random.choice(np.shape(full_expression)[0],size=(min([1000,row_dim]),),replace=False))),dtype=int)
        sample_cols = np.array(list(sorted(np.random.choice(np.shape(full_expression)[1],size=(min([500,col_dim]),) ,replace=False))),dtype=int)
        full_expression_r = full_expression[sample_rows,:]
        full_expression_r = full_expression_r[:,sample_cols]
        for i in range(full_expression_r.shape[0]):
            full_expression_r[i,:]=rankdata(full_expression_r[i,:], method="min")
        if full_expression_r.shape[0]>2:
            sns.clustermap(full_expression_r,cmap=cm.get_cmap(name="hot"))
            plt.savefig(temp+'/sample_genes_used_for_clustering_heatmap.png',
                dpi=args.dpi,
                bbox_inches='tight')
            # full_expression_r = full_expression_r - np.mean(full_expression_r,axis=1)
            # sns.clustermap(full_expression_r,cmap=global_cmap)
            # plt.savefig(temp+'/sample_genes_used_for_clustering_heatmap_mean_centered.png',
            #     dpi=args.dpi,
            #     bbox_inches='tight')


    print("calculating sample-wise spearman correlations")
    from scipy.stats import spearmanr
    #gene_full_expression_copy = full_expression[:]
    if args.louvain_clust:
        ## if we're doing louvain clustering, just do it out of memory
        mem_err = True
    else:
        ## otherwise, we'll try to do it in memory first
        mem_err = False
    if not mem_err: 
        try:
            full_expression = no_p_spear(full_expression)
        except Exception as e:
            if isinstance(e, MemoryError):
                mem_err = True
            else:
                mem_err = False
        else:
            print("spear cor:\n",full_expression[:5,:5])
            total_vars = np.shape(full_expression)[1]
            num_nan = np.sum(np.array(np.isnan(full_expression),dtype=int))
            num_inf = np.sum(np.array(np.isinf(full_expression),dtype=int))
            if num_nan+num_inf>0:
                print(num_nan,"nans found!")
                print(num_inf,"inf found!")
                if num_nan>0:
                    full_expression[np.isnan(full_expression)]=0
            full_expression = -euclidean_distances(full_expression,squared=True)/np.log2(total_vars)
            print('-euclidean dist:\n',full_expression[:5,:5])
    elif mem_err:
        print("couldn't do the full spearman in one go, we'll have to break it up into chuncks and do it peice meal")
        get_big_spearman()
    else:
        sys.exit("something went wrong")
        

#sample_k_known,temp,  page_ranks, IDlist, c_PR_list, control_name, d_PR_list, disease, pre_determined_sample_k, 
first_prob = True
cluster_prob=False

############################################################################

from numpy import linalg










##############################################################################
####################### find k means for all samples #########################

##############################################################################
#########      functions for performing k-means clustering    ################

def linear_normalization(in_matrix,axis=1):
    in_matrix = in_matrix - np.transpose( np.array( [np.min(in_matrix, axis=axis)] ) )
    in_matrix = in_matrix / np.transpose( np.array( [np.max(in_matrix, axis=axis)] ) )
    print(np.min(in_matrix, axis=axis))
    print(np.max(in_matrix, axis=axis))
    return(in_matrix)

##################
def convert_to_prob(vect):
    ## calculate probabilities based on standard deviation 
    probabilities = vect - min(vect)
    probabilities = probabilities / max(probabilities)
    probabilities = probabilities / sum(probabilities)
    if np.sum(np.isnan(probabilities)) > 0:
        probabilities = np.ones(np.shape(probabilities))
        probabilities = probabilities / np.sum(probabilities)
    return(probabilities)



########################
start_length=35
stopping_length=5
def unknown_k_means_sample(sample_names, expression_matrix, prob = False):
    global sample_k_known,temp, first_prob, IDlist
    ## expressoin matrix format:
    ##        sample1, sample2, sample3 ...
    ## var1[[  1.0   ,   1.5  ,   2.0  ],
    ## var2 [  0.2   ,   1.5  ,   2.0  ],
    ## var3 [  1.0   ,   1.5  ,   2.0  ]]

    ## because the kmeans2 function from scipy clusters based on rows, 
    ## the expression matrix will be transposed

    ## samples are now in rows, and expression values are now in columns

    #### constant ####
    # go_past_for_local_min is the variable which is used for seeing how far in 
    # k selection we should go past a local minimum

    # expression_matrix = np.transpose(expression_matrix)
    # expression_matrix = expression_matrix.astype('float32')
    
    ## this variable is for testing passed a local minimum of the f(k) function
    stopping_length = 10
    
    if expression_matrix.shape[0] <= stopping_length:
        print('expression_matrix is too small to subdivide')
        
        output_cluster_annotations = list(zip(sample_names, [0]*len(sample_names)))
        for i in range(0,len(output_cluster_annotations)):
            output_cluster_annotations[i]=list(output_cluster_annotations[i])
        #output_cluster_annotations, out_var_group_list_of_lists, f_list, optimal_centroid_indices
        return(output_cluster_annotations, [sample_names], [1],[0])
    
    
    ## find the variable with the greatest number of interactions (or total expression)
    row_std = np.std(expression_matrix, axis = 1)
    print(expression_matrix)
    print(row_std)
    max_row_std = np.max(row_std)
    if prob or first_prob:
        probabilities = convert_to_prob(row_std)
        print(row_std)
        print(np.sum(row_std))
        print(len(sample_names))
        print(len(probabilities))
        centroid_initialization_index = np.random.choice ( list( range(0,len(sample_names)) ) , size = 1, replace = False, p = probabilities ) 
    else:
        centroid_initialization_index = sample(list(np.where(row_std == max_row_std)[0]), 1)
    print('first centroid index:',centroid_initialization_index)
    centroid_indices = list(centroid_initialization_index[:])
    
    temp_centroids, variable_labels = kmeans2(expression_matrix, expression_matrix[centroid_indices,:], minit='matrix', iter=10)
    
    print('\ncentroid_indices for k =',len(centroid_indices))
    print(centroid_indices)
    print('\n\n')
    
    ## initialize with k = 1
    Sk = None
    Ak = None
    temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, [list(variable_labels)], expression_matrix)
    f_list = [temp_f]
    centroid_distances_matrix = np.array(get_all_distances_from_a_centroid(expression_matrix[centroid_indices[-1]], expression_matrix))
    
    print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)


    
    while k_stopping_function(f_list, num_vars = len(sample_names)):
        ## len(f_list) must be at least the length of the stopping_length +1 for k=1
        ## then the first time that min(f(k)) is not within the stopping length, 
        ## then stop and return the optimal k

        ## first thing to do is find out all the current distances from all centroids
        if len(centroid_indices)>1:
            centroid_distances_matrix = np.hstack((centroid_distances_matrix, np.array(get_all_distances_from_a_centroid(expression_matrix[centroid_indices[-1]], expression_matrix))))
        
        ## find the index of the next centroid based on the current distance matrix
        if prob:
            next_centroid = get_next_centroid_index(centroid_distances_matrix, existing_centroids = centroid_indices, prob = True)
        else:
            next_centroid = get_next_centroid_index(centroid_distances_matrix, existing_centroids = centroid_indices)
        if next_centroid in centroid_indices:
            ## this means that the newly of the remaining points, there are now ties
            ## with already existing centroids for farthest away from other centroids
            print('already established centroid was picked again')
            break
        print(centroid_indices)
        centroid_indices.append(next_centroid)
        print('\ncentroid_indices for k =',len(centroid_indices))
        print(centroid_indices)
        print('\n\n')
        
        temp_centroids, variable_labels = kmeans2(expression_matrix, expression_matrix[centroid_indices,:], minit='matrix', iter=10)
        
        ## this function will take variable labels of format [0,1,1,0,0,2]
        ## and change it to: 
        ## [[0,3,4], ## centroid 0
        ##    [1,2],   ## centroid 1
        ##     [5]]     ## centroid 2
        variable_labels = rearrange_variable_labels(variable_labels)
       # print('variable_labels\n',variable_labels)
        if len(variable_labels) < len(centroid_indices):
            ## this means that two centroids have converged during the k-means clustering, indicating
            ## that the number of centroids is already oversaturated
            print("centroids converged, stopping due to overfit")
            break
        
        
        temp_f, Sk, Ak  = f_of_k(Sk, Ak, temp_centroids, variable_labels, expression_matrix)
        f_list.append(temp_f)
        print('k =',len(f_list),'\nf(k) =',temp_f,'\tSk =',Sk,'\tAk =',Ak)
        
    print(k_stopping_function(f_list, num_vars = len(sample_names)))
    if not k_stopping_function(f_list, num_vars = len(sample_names)):
        
        print(f_list)
    if not sample_k_known:
        optimal_k_index = get_estimated_k_from_f_list(f_list)
        print('optimal k =',optimal_k_index+1)
    elif sample_k_known:
        print('sample k known')
        optimal_k_index = int(pre_determined_sample_k-1)
    print('optimal k index:',optimal_k_index)
#    if not no_graphs:
#        plt.clf()
#        plt.plot(np.arrange(1,len(flist)),f_list,'o-')
#        plt.savefig(output, dpi=dpi_in, facecolor='w', edgecolor='w',orientation='portrait', papertype=None, format=None,transparent=False, bbox_inches='tight', pad_inches=0.1)
    optimal_centroid_indices = centroid_indices[:optimal_k_index+1]
    #print(optimal_centroid_indices)
    
    final_centroids, final_variable_labels = kmeans2(expression_matrix, expression_matrix[optimal_centroid_indices,:], minit='matrix', iter=10)
    
    ## convert the final variable labels into a list of lists containing the variable names
    rearranged_var_labels = rearrange_variable_labels(final_variable_labels)
    out_var_group_list_of_lists = []
    for r in rearranged_var_labels:
        out_var_group_list_of_lists.append(list(sample_names[var] for var in r))
    
    
        
    output_cluster_annotations = list(map(list,zip(sample_names, final_variable_labels)))
    
    
    if sample_k_known:
        copy_centroids=optimal_centroid_indices[:]
        print(list(map(str,copy_centroids)))
        #cmd('mkdir '+temp+'/sample_clustering_and_summary/')
        #make_file('\n'.join(list(map(str,copy_centroids))),temp+'/sample_clustering_and_summary/centroid_indices.txt')
    
    return(output_cluster_annotations, out_var_group_list_of_lists, f_list, optimal_centroid_indices)

########################################################################

#####################

def get_all_distances_from_a_centroid(centroid, in_mat):
    euclidean_distances = []
    for i in range(0, in_mat.shape[0]):
        ## get the euclidean distance of each variable from given centroid
        temp_dist=linalg.norm(in_mat[i] - centroid)
        euclidean_distances.append(temp_dist**2)
#        euclidean_distances.append(temp_dist)
    return(np.transpose(np.array([np.array(euclidean_distances)])))

######################

multiply_by_min = True
def get_next_centroid_index(distance_list, existing_centroids = [], prob = False):
    ## this function calculates the sum of the squares of the euclidean distances from
    ## the all of the current centroids for all variables, then returns the index of the
    ## variable with the maximum sum of the square euclidean distances from all centroids
    global multiply_by_min
    
    #print('distance_list')
    #print(distance_list)
    
    temp_dist_mat=np.array(distance_list)
    #row_sum=np.sum(temp_dist_mat * temp_dist_mat, axis=1)
    row_sum=np.sum(temp_dist_mat, axis=1)
    #print(temp_dist_mat)
    if multiply_by_min:
        row_max=np.amax(temp_dist_mat,axis=1)
        row_min=np.amin(temp_dist_mat,axis=1)
        #print(row_min)
        row_range_plus1=(row_max-row_min)+1
        #print(row_range_plus1)
    
        
        all_distances=row_sum*row_min
    else:
        all_distances=row_sum

    
    #print(all_distances)
    #sys.exit()

    ## add all subsequent squared distances

    if prob:
        ## calculate probabilities based on standard deviation 
        probabilities = convert_to_prob(all_distances)
        max_indices = np.random.choice ( list( range(0, np.shape(distance_list)[0] ) ) , size = 1, replace = False, p = probabilities ) 
        
        num_max_indices = 1
    else:
        max_indices = np.where(all_distances == np.max(all_distances))[0]
        num_max_indices = np.shape(max_indices)[0]
        print('\n\tnumber equal to max',num_max_indices)
    
    
    final_candidate_next_centroids = []
    if num_max_indices > 1:
        max_indices = list(max_indices)
        final_candidate_next_centroids = []
        for i in range(0,num_max_indices):
            if max_indices[i] not in existing_centroids:
                final_candidate_next_centroids.append(max_indices[i])
        if final_candidate_next_centroids == []:
            return(sample(max_indices,1)[0])
        else:
            return(sample(final_candidate_next_centroids,1)[0])
        
    else:
        return(sample(list(max_indices),1)[0])


##################

from scipy.cluster.vq import kmeans2
def do_k_means(centroids, in_matrix, name, temp_IDs, iters = 10):
    global temp, IDlist
    
    final_centroids, variable_labels = kmeans2(in_matrix, centroids, minit='matrix', iter=iters)
    
    print(final_centroids)
    print(variable_labels)
    make_file(flatten_2D_table([['variable','group']]+list(map(list,list(zip(temp_IDs, variable_labels)))), '\t'), temp+'/'+name+'_k_groups.txt')
    #sys.exit()
    
    return

#################

def euclidean_distance(row1,row2):
    global linalg
    temp_eucl_dist = linalg.norm(row1-row2)
    return(temp_eucl_dist)


#################
from sklearn import metrics

def get_half_distance_matrix(in_array):
    ## this function returns the symetric matrix of euclidean distance between
    ## all genes based on the input array that are passed into this 
    ## function
    try:
        return(metrics.pairwise.euclidean_distances(in_array,in_array))
    except:
        distance_matrix = np.zeros((in_array.shape[0],in_array.shape[0]))
        for i in range(0,in_array.shape[0]):
            for j in range(i,in_array.shape[0]):
                if i==j:
                    pass
                else:
                    temp_dist = euclidean_distance(in_array[i,:], in_array[j,:])
                    distance_matrix[i,j] = temp_dist
                    #distance_matrix[j,i] = temp_dist
        return(distance_matrix)


#######################

def global_impact_of_k_clusters(centroids, members, interaction_matrix):
    ## centroids is a list of the centroids
    ## members is a list of the indices of each member belonging to the ith centroid
    ## the interaction matrix is given for subsetting the members out
    #print('centroids')
    #print(type(centroids))
    
    if len(members) != centroids.shape[0]:
        print('incorrect dimentions\tmembers:',len(members), '\tcentroids:', centroids.shape[0])
        sys.exit('incorrect dimentions')
    Sk=0
    Sk_vector=[]
    for i in range(0,len(members)):
        ## dummy is set because this function returns the erroneous IDs for the subset matrix
        ## this function does this because it thinks it's getting the full interaction matrix,
        ## even though in reality it is getting a subsetted matrix
        #dummy, member_subset = subset_interaction_matrix(members[i], interaction_matrix)
        member_subset = interaction_matrix[members[i],:]
        
        ## trim the centroid to only include the indices of the subset matrix
        
        #temp_centroid = centroids[i,members[i]]
        temp_centroid = centroids[i,]
        
        #print(members[i])
        distance_vector = get_all_distances_from_a_centroid(temp_centroid, member_subset)
        temp_sk = np.sum(distance_vector)
        
        Sk_vector.append(temp_sk)
        Sk += temp_sk

    return(Sk)

####################

def f_of_k(prior_Sk, prior_Ak, centroids, members, interaction_matrix):
    ## * note that if k == 1, or k == 2, the 'prior_Ak' argument is not actually used
    ## so any dumby value can be fed into the function without ill effect
    print('prior_Sk',prior_Sk)
    print('prior_Ak',prior_Ak)
    #print('centroids')
    #print(centroids)
    #print('members')
    #print(members)
    #print('interaction_matrix')
    #print(interaction_matrix)
    k = len(members)
    Nd = interaction_matrix.shape[0]
    if k == 1:
        cur_Ak = None


    ## this function should only be run on 'clusters' with at least two possible members
    if Nd == 1:
        return (None, None, None)

    ## calculate Sk 
    else:
        cur_Sk = global_impact_of_k_clusters(centroids, members, interaction_matrix)
    
    ## calculate the current Ak
    if k == 2 and Nd > 1:
        cur_Ak = 1 - ( 3 / ( 4 * Nd ) )
    elif k > 2 and Nd > 1:
        cur_Ak = prior_Ak + ( (1 - prior_Ak) / 6 )

    
    ## calculate the k evaluation function
    if k == 1 or (prior_Sk == 0 and k > 1):
        f = 1
    else:
#        print('original f(k)',cur_Sk / (cur_Ak * prior_Sk))
        f = cur_Sk / (cur_Ak * prior_Sk)

#        print('new f(k)',f)

    return(f, cur_Sk, cur_Ak)

###################

def k_stopping_function(f_list, num_vars = None, starting_length=None, stopping_length=5, delta_cutoff=10):
    ## returning True allows the k search to continue, while returning False makes it stop
    if starting_length==None:
        starting_length = int(min([np.sqrt(num_vars)+1,50])) ## this is a guess for the max number of groups to test at the beginning, barring any run-offs of local minimas
    global sample_k_known, pre_determined_sample_k
    if sample_k_known:
        if len(f_list) < pre_determined_sample_k:
            return(True)
        if len(f_list) == pre_determined_sample_k:
            return(False)
    else:
        if len(f_list)==1:
            return(True)
        if (f_list[-1] - f_list[-2]>10):
            return(False)
        if (len(f_list) < starting_length+1):
            return(True)
        if (min(f_list) in f_list[-stopping_length:]):
            return(True)

def get_estimated_k_from_f_list(f_list):
    global sample_k_known, pre_determined_sample_k
    if sample_k_known:
        return(pre_determined_sample_k-1)
    else:
        f_deltas=[]
        f_delta_delta=[]
        for f in range(1,len(f_list)):
            f_deltas.append(f_list[f]-f_list[f-1])
            f_delta_delta.append(f_list[f]-f_deltas[-1])
        
        #optimal_k=f_delta_delta.index(min(f_delta_delta))
#        print('f_delta_delta')
#        print(f_delta_delta)
        min_f=min(f_list)
        optimal_k_index=f_list.index(min_f)
        #next_best=min(f_list[optimal_k_index+1:])
        #if next_best < min_f*1:
        #    optimal_k_index=f_list.index(next_best)
        return(optimal_k_index)


##################

def rearrange_variable_labels(variable_labels):
    ## this function will take variable labels of format [0,1,1,0,0,2]
    ## and change it to: 
    ## [[0,3,4], ## centroid 0
    ##    [1,2],   ## centroid 1
    ##     [5]]     ## centroid 2
    max_label = max(variable_labels)
    variable_labels = np.array(variable_labels)
    new_var_labels=[]
    for i in range(0,max_label+1):## plus1 because the range function is exclusive in python, not inclusive
        new_var_labels.append(list(np.where(variable_labels == i)[0]))
    return(new_var_labels)











#########################################################
upper_nine_k = True
def do_unknown_k_means_clustering_iter(title, full_expression, cluster_iter = 10, performed_on_samples = False):
    global sample_k_known, pre_determined_sample_k, cluster_prob, upper_nine_k
    print("sample_k_known",sample_k_known)
    sample_k_table_list_list=[]
    sample_k_lists_list=[]
    f_list_list=[]
    optimal_centroid_indices_list=[]
    min_f=[]
    k_estimate_list = []

    ## transposed dataset to feed into k-means
    full_expression_t = np.array(np.transpose(full_expression),dtype=np.float32)

    print(cluster_iter)
    for i in range(0,cluster_iter):
        print(i)
        if i == 0:
            print(title[:5],'...',title[-5:])
            print(full_expression)
            print(np.shape(full_expression))
            # a = unknown_k_means_sample(title, full_expression_t, prob=False)
            # print(len(a))
            # for i in a:
            #     print(i)
            temp_sample_k_table, temp_sample_k_lists, temp_f_list, temp_optimal_centroid_indices = unknown_k_means_sample(title, full_expression_t, prob=False)
        else:
            temp_sample_k_table, temp_sample_k_lists, temp_f_list, temp_optimal_centroid_indices = unknown_k_means_sample(title, full_expression_t, prob=cluster_prob)
        
        sample_k_table_list_list.append(temp_sample_k_table)
        sample_k_lists_list.append(temp_sample_k_lists)
        f_list_list.append(temp_f_list)
        if bool(sample_k_known):
            min_f.append(temp_f_list[pre_determined_sample_k-1])
        else:
            min_f.append(min(temp_f_list))
        k_estimate_list.append(temp_f_list.index(min_f[-1])+1)
        
        optimal_centroid_indices_list.append(temp_optimal_centroid_indices)

    
    if performed_on_samples:
        if bool(sample_k_known):
            write_table(f_list_list,temp+'/f_lists_k_known.txt')
        else:
            write_table(f_list_list,temp+'/f_lists_k_not_known.txt')

    if upper_nine_k and not bool(sample_k_known):
        sample_k_known = True
        
        temp_k_list = k_estimate_list[:]
        temp_k_list = sorted(temp_k_list)
        pre_determined_sample_k = temp_k_list[ int(round(cluster_iter*.9, 0)) - 1 ]
        
        return( do_unknown_k_means_clustering_iter(title, full_expression, cluster_iter = cluster_iter, performed_on_samples = performed_on_samples) )
        
    ############
    print('k estimate list',k_estimate_list)
    for f in range(0,len(f_list_list)):
        print('iter',f,'k estimate',k_estimate_list[f],'f',min_f[f],f_list_list[f])

        
    
    ############
    if True:#sample_k_known:
        global_min_f = min(min_f)
        print('global_min_f',global_min_f)
        global_min_f_indices = min_f.index(global_min_f)
        print('global_min_f_indices',global_min_f_indices)
        if type(global_min_f_indices) == int:
            optimal_k_iter=global_min_f_indices
        else:
            optimal_k_iter = sample(list(global_min_f_indices),1)[0]
        f_list = f_list_list[optimal_k_iter]
        optimal_centroid_indices=optimal_centroid_indices_list[optimal_k_iter]
    
        print(optimal_centroid_indices)
        
        sample_k_table_list = sample_k_table_list_list[optimal_k_iter]
        sample_k_lists = sample_k_lists_list[optimal_k_iter]
    ############
    
    #print(full_expression[:,optimal_centroid_indices])
    

    return(sample_k_table_list, sample_k_lists, f_list, optimal_centroid_indices)
        
#########################################################

def group_list_to_sample_k_table(labels):
    global title
    sample_names = title[1:]
    num_clust = len(list(set(labels)))
    print(labels)
    #print(len(labels))
    #sys.exit()
    f_list = None
    #print(dir(af))
    sample_k_table = []
    for i in range(0,len(sample_names)):
        sample_k_table.append([sample_names[i],labels[i]])
    sample_k_lists = []
    for i in range(num_clust):
        sample_k_lists.append([])
    #print(sample_k_lists)
    for i in range(0,len(sample_names)):
        sample_k_lists[labels[i]].append(sample_names[i])
    return(sample_k_table, sample_k_lists)

#################################################################################
#################################################################################
#################################################################################
#################################################################################
#################################################################################






from sklearn.cluster import AffinityPropagation as ap

def new_affinity_propagation(S, preference=None, convergence_iter=15, max_iter=200,
                         damping=0.5, copy=True, verbose=False,
                         return_n_iter=False, temp_ap_hdf5 = None):
    """Perform Affinity Propagation Clustering of data

    Read more in the :ref:`User Guide <affinity_propagation>`.

    Parameters
    ----------

    S : array-like, shape (n_samples, n_samples)
        Matrix of similarities between points

    preference : array-like, shape (n_samples,) or float, optional
        Preferences for each point - points with larger values of
        preferences are more likely to be chosen as exemplars. The number of
        exemplars, i.e. of clusters, is influenced by the input preferences
        value. If the preferences are not passed as arguments, they will be
        set to the median of the input similarities (resulting in a moderate
        number of clusters). For a smaller amount of clusters, this can be set
        to the minimum value of the similarities.

    convergence_iter : int, optional, default: 15
        Number of iterations with no change in the number
        of estimated clusters that stops the convergence.

    max_iter : int, optional, default: 200
        Maximum number of iterations

    damping : float, optional, default: 0.5
        Damping factor between 0.5 and 1.

    copy : boolean, optional, default: True
        If copy is False, the affinity matrix is modified inplace by the
        algorithm, for memory efficiency

    verbose : boolean, optional, default: False
        The verbosity level

    return_n_iter : bool, default False
        Whether or not to return the number of iterations.

    Returns
    -------

    cluster_centers_indices : array, shape (n_clusters,)
        index of clusters centers

    labels : array, shape (n_samples,)
        cluster labels for each point

    n_iter : int
        number of iterations run. Returned only if `return_n_iter` is
        set to True.

    Notes
    -----
    See examples/cluster/plot_affinity_propagation.py for an example.

    References
    ----------
    Brendan J. Frey and Delbert Dueck, "Clustering by Passing Messages
    Between Data Points", Science Feb. 2007
    """
    #S = as_float_array(S, copy=copy)
    global args

    n_samples = S.shape[0]
    ind = np.arange(n_samples)

    print("S:")
    print(S[:5,:5])

    bins = []
    cur_bin = 0
    bin_size = args.block_size
    while cur_bin<n_samples:
        bins.append(min(cur_bin, n_samples))
        cur_bin+=bin_size

    bins.append(n_samples)
    print(bins)

    if S.shape[0] != S.shape[1]:
        raise ValueError("S must be a square array (shape=%s)" % repr(S.shape))

    if preference is None:
        try:
            preference = np.min(S,axis=1)
        except:
            # print('matrix too large to calculate the median')
            # print('we have to take the average of the medians from a few samples instead')
            # sample_size = int(1e6)
            # preference_vect = []
            # temp_sample_indices_x = sorted(np.random.choice(ind, size = sample_size, replace= True))
            # temp_sample_indices_y = sorted(np.random.choice(ind, size = sample_size, replace= True))
            # for j in range(0,sample_size-1):
            #     temp_rand_x=temp_sample_indices_x[j]
            #     temp_rand_y=temp_sample_indices_y[j]
            #     temp_affinity = S[temp_rand_x,temp_rand_y]
            #     if temp_affinity != 0:
            #         preference_vect.append(S[temp_rand_x,temp_rand_y])
            # print('\t',preference_vect[:10],'...')
            preference = np.zeros((np.shape(S)[0],))
            for i in range(0,np.shape(S)[0]):
                preference[i] = np.min(S[i,:])


    if damping < 0.5 or damping >= 1:
        raise ValueError('damping must be >= 0.5 and < 1')

    random_state = np.random.RandomState(0)

    # Place preference on the diagonal of S
    print("setting preference to",preference)
    for d in range(0,np.shape(S)[0]):
        S[d,d] = preference


    if 'A' in temp_ap_hdf5:
        del temp_ap_hdf5['A']

    if 'S2' in temp_ap_hdf5:
        del temp_ap_hdf5['S2']

    if 'R' in temp_ap_hdf5:
        del temp_ap_hdf5['R']
    
    if 'tmp' in temp_ap_hdf5:
        del temp_ap_hdf5['tmp']

    if 'rand_mat' in temp_ap_hdf5:
        del temp_ap_hdf5['rand_mat']
    
    A = temp_ap_hdf5.create_dataset('A',(n_samples, n_samples),dtype = np.float16)
    R = temp_ap_hdf5.create_dataset('R',(n_samples, n_samples),dtype = np.float16)
    #A = np.zeros((n_samples, n_samples),dtype = 'f0')
    #R = np.zeros((n_samples, n_samples),dtype = 'f0')  # Initialize messages
    
    # Intermediate results
    tmp = temp_ap_hdf5.create_dataset('tmp',(n_samples, n_samples),dtype = np.float16)
    #tmp = np.zeros((n_samples, n_samples))
    # rand_mat = temp_ap_hdf5.create_dataset('rand_mat',(n_samples, n_samples),dtype = np.float16)

    # for i in range(0,n_samples):
    #     rand_mat[i,:] = random_state.randn(n_samples,)

    # Remove degeneracies
    # rand_mat = np.array(random_state.randn(n_samples, n_samples),dtype=np.float16)
    # S += ((np.finfo(np.double).eps * S + np.finfo(np.double).tiny * 100) *
    #       rand_mat)
    print('removing degeneracies')
    for i in range(0,len(bins)-1):
        nrow = np.shape(S[bins[i]:bins[i+1],:])[0]
        temp_rand = S[bins[i]:bins[i+1],:]*np.finfo(np.float16).eps
        temp_rand = temp_rand+(np.finfo(np.float16).tiny * 100)
        temp_rand = temp_rand*random_state.randn(nrow,n_samples)
        S[bins[i]:bins[i+1],:] = S[bins[i]:bins[i+1],:] + temp_rand
        #S[bins[i]:bins[i+1],:] = S[bins[i]:bins[i+1],:]*np.finfo(np.float16).eps
    # for i in range(0,len(bins)-1):
    #     S[bins[i]:bins[i+1],:] = S[bins[i]:bins[i+1],:]+(np.finfo(np.float16).tiny * 100)
    # for i in range(0,len(bins)-1):
    #     S[bins[i]:bins[i+1],:] = S[bins[i]:bins[i+1],:]*random_state.randn(nrow,n_samples)

    # S2 = temp_ap_hdf5.create_dataset('S2',(n_samples, n_samples),dtype = np.float16)
    # S2 = S
    # S2 *= np.finfo(np.float16).eps
    # S2 += (np.finfo(np.float16).tiny * 100)
    # S += (S2 * rand_mat)
    # del temp_ap_hdf5['S2']
          

    # Execute parallel affinity propagation updates
    e = np.zeros((n_samples, convergence_iter))





    test=True
    if test:
        print('S\n',S[:5,:5])
        print('A\n',A[:5,:5])
        print('R\n',R[:5,:5])
        print('tmp\n',tmp[:5,:5])
        print('e\n',e[:5,:5])
        #sys.exit()

    for it in range(max_iter):

        for i in range(0,len(bins)-1):
            tmp[bins[i]:bins[i+1],:] = A[bins[i]:bins[i+1],:] + S[bins[i]:bins[i+1],:]# + tmp#; compute responsibilities
        # np.add(A, S, tmp)

        I = np.zeros((n_samples,))
        for i in range(0,len(bins)-1):
            I[bins[i]:bins[i+1]] = np.argmax(tmp[bins[i]:bins[i+1],:], axis=1)

        for i in range(0,n_samples):
            I[i] = np.argmax(tmp[i,:])
        ##################################
        Y = np.zeros((n_samples,))
        for i in range(0,n_samples):
            Y[i] = tmp[i, I[i]]  # np.max(A + S, axis=1)
        
        for i in range(0,n_samples):
            tmp[i, I[i]] = -np.inf

        Y2 = np.zeros((n_samples,))
        for i in range(0,len(bins)-1):
            Y2[bins[i]:bins[i+1]] = np.max(tmp[bins[i]:bins[i+1],:], axis=1)

        # tmp = Rnew
        for i in range(0,len(bins)-1):
            tmp[bins[i]:bins[i+1],:] = S[bins[i]:bins[i+1],:] - Y[bins[i]:bins[i+1], None]
        for i in range(0,n_samples):
            tmp[i, I[i]] = S[i, I[i]] - Y2[i]
        

        # Damping
        for i in range(0,len(bins)-1):
            tmp[bins[i]:bins[i+1],:] = tmp[bins[i]:bins[i+1],:]*(1 - damping)
        #print(damping)
        for i in range(0,len(bins)-1):
            R[bins[i]:bins[i+1],:] = R[bins[i]:bins[i+1],:] * damping
            R[bins[i]:bins[i+1],:] = R[bins[i]:bins[i+1],:] + tmp[bins[i]:bins[i+1],:]

        
        if test:
            print('after dampening')
            print(it,'S\n',S[:5,:5])
            print(it,'A\n',A[:5,:5])
            print(it,'R\n',R[:5,:5])
            print(it,'tmp\n',tmp[:5,:5])
            print(it,'e\n',e[:5,:5])
            print(it,'Y\n',Y[:5,])
            print(it,'Y2\n',Y2[:5,])
            #sys.exit()



        # tmp = Rp; compute availabilities
        #print('R\n',R[:5,:5])
        for i in range(0,len(bins)-1):
            tmp[bins[i]:bins[i+1],:] = np.maximum(R[bins[i]:bins[i+1],:], 0)#, tmp)
        #print('R\n',R[:5,:5])
        #tmp.flat[::n_samples + 1] = R.flat[::n_samples + 1]
        for d in range(0,n_samples):
            tmp[d,d] = R[d,d]


        
        if test:
            print('after computing availabilities')
            print(it,'S\n',S[:5,:5])
            print(it,'A\n',A[:5,:5])
            print(it,'R\n',R[:5,:5])
            print(it,'tmp\n',tmp[:5,:5])
            print(it,'e\n',e[:5,:5])
            print(it,'Y\n',Y[:5,])
            print(it,'Y2\n',Y2[:5,])
            #sys.exit()




        # tmp = -Anew
        for i in range(0,len(bins)-1):
            tmp[:,bins[i]:bins[i+1]] -= np.sum(tmp[:,bins[i]:bins[i+1]], axis=0)

        dA=np.zeros((n_samples,))
        for d in range(0,n_samples):
            dA[d]=tmp[d,d]
        #dA = np.diag(tmp[:,:]).copy()
        for i in range(0,len(bins)-1):
            tmp[bins[i]:bins[i+1],:] = np.clip(tmp[bins[i]:bins[i+1],:], 0, np.inf)
        for d in range(0,n_samples):
            tmp[d,d] = dA[d]

        
        if test:
            print('after -Anew')
            print(it,'S\n',S[:5,:5])
            print(it,'A\n',A[:5,:5])
            print(it,'R\n',R[:5,:5])
            print(it,'tmp\n',tmp[:5,:5])
            print(it,'e\n',e[:5,:5])
            print(it,'Y\n',Y[:5,])
            print(it,'Y2\n',Y2[:5,])
            #sys.exit()


        # Damping
        for i in range(0,len(bins)-1):
            tmp[bins[i]:bins[i+1],:] = tmp[bins[i]:bins[i+1],:]*(1 - damping)
            A[bins[i]:bins[i+1],:] = A[bins[i]:bins[i+1],:] * damping
            A[bins[i]:bins[i+1],:] = A[bins[i]:bins[i+1],:] - tmp[bins[i]:bins[i+1],:]
        # for i in range(0,np.shape(R)[0]):
        #     A[i,:] = A[i,:] * damping
        #     A[i,:] = A[i,:] - tmp[i,:]



        # Check for convergence
        E = np.array(np.zeros(n_samples,),dtype=bool)
        for d in range(0,n_samples):
            E[d] = (A[d,d]+R[d,d]) > 0
        #E = (np.diag(A) + np.diag(R)) > 0
        e[:, it % convergence_iter] = E
        K = np.sum(E, axis=0)

        if it >= convergence_iter:
            se = np.sum(e, axis=1)
            unconverged = (np.sum((se == convergence_iter) + (se == 0))
                           != n_samples)
            if (not unconverged and (K > 0)) or (it == max_iter):
                if verbose:
                    print("Converged after %d iterations." % it)
                break
    else:
        if verbose:
            print("Did not converge")


    dA = np.zeros((n_samples,))
    dR = np.zeros((n_samples,))
    for d in range(0,n_samples):
        dA[d] = A[d,d]
        dR[d] = R[d,d]
    I = np.where((dA + dR) > 0)[0]
    K = I.size  # Identify exemplars


    print(it,'dAR\n',dA+dR)
    print(it,'I\n',I)
    print(it,'K\n',K)

    if K > 0:
        c = np.argmax(S[:, I], axis=1)
        c[I] = np.arange(K)  # Identify clusters
        # Refine the final set of exemplars and clusters and return results
        for k in range(K):
            ii = np.where(c == k)[0]
            #j = np.argmax(np.sum(S[ii[:, np.newaxis], ii], axis=0))
            temp_j_calc_mat = np.zeros((np.shape(ii)[0],np.shape(ii)[0]))
            for exemp in range(0,np.shape(ii)[0]):
                exemp_ind = ii[exemp]
                temp_S = S[exemp_ind,:]
                temp_j_calc_mat[exemp,:] = temp_S[ii]
            j = np.argmax(np.sum(temp_j_calc_mat, axis=0))
            I[k] = ii[j]

        c = np.argmax(S[:, I], axis=1)
        c[I] = np.arange(K)
        labels = I[c]
        # Reduce labels to a sorted, gapless, list
        cluster_centers_indices = np.unique(labels)
        labels = np.searchsorted(cluster_centers_indices, labels)
    else:
        labels = np.empty((n_samples, 1))
        cluster_centers_indices = None
        labels.fill(np.nan)

    if return_n_iter:
        return cluster_centers_indices, labels, it + 1
    else:
        temp_ap_hdf5.close()
        return cluster_centers_indices, labels


class hdf5_affinity_propagation(ap):

    def __init__(self, damping=.5, max_iter=200, convergence_iter=15,
                 copy=True, preference=None, affinity='euclidean',
                 temp_ap_hdf5 = None, verbose=False):

        self.damping = damping
        self.max_iter = max_iter
        self.convergence_iter = convergence_iter
        self.copy = copy
        self.verbose = verbose
        self.preference = preference
        self.affinity = affinity
        self.temp_ap_hdf5 = temp_ap_hdf5


    def fit(self, X, y=None):
        """ Create affinity matrix from negative euclidean distances, then
        apply affinity propagation clustering.

        Parameters
        ----------

        X : array-like, shape (n_samples, n_features) or (n_samples, n_samples)
            Data matrix or, if affinity is ``precomputed``, matrix of
            similarities / affinities.
        """
        #X = check_array(X, accept_sparse='csr')
        if self.affinity == "precomputed":
            self.affinity_matrix_ = X
        elif self.affinity == "euclidean":
            self.affinity_matrix_ = -euclidean_distances(X, squared=True)
        else:
            raise ValueError("Affinity must be 'precomputed' or "
                             "'euclidean'. Got %s instead"
                             % str(self.affinity))

        self.cluster_centers_indices_, self.labels_, self.n_iter_ = \
            new_affinity_propagation(
                self.affinity_matrix_, self.preference, max_iter=self.max_iter,
                convergence_iter=self.convergence_iter, damping=self.damping,
                copy=False, verbose=self.verbose, return_n_iter=True,
                temp_ap_hdf5 = self.temp_ap_hdf5)

        if self.affinity != "precomputed":
            self.cluster_centers_ = X[self.cluster_centers_indices_].copy()

        return self

##########################################################################

def check_symmetric(a, tol=1e-8):
    return np.allclose(a, np.transpose(a), atol=tol)


##################################################################################
######################### original ap ############################################
##################################################################################












##################################################################################

def do_big_ap():
    global neg_euc_hdf5_file, args
    if not os.path.isfile(neg_euc_hdf5_file):
        get_big_spearman()

    #f_ap = h5py.File(neg_euc_hdf5_file, "r")
    cmd('cp '+neg_euc_hdf5_file+' '+neg_euc_hdf5_file+'_copy')
    neg_euc_hdf5_file = neg_euc_hdf5_file+'_copy'
    f_ap = h5py.File(neg_euc_hdf5_file, "a")
    neg_euc_dist = f_ap["infile"]
    print('top of neg euc dist mat')
    print(neg_euc_dist[:5,:5])

    print('making the hdf5 file for ap clustering')
    temp_ap_hdf5 = os.path.splitext(args.out_dir)[0]+'/temp_ap_clust.hdf5'
    temp_ap = h5py.File(temp_ap_hdf5, "w")
    print('\t',temp_ap_hdf5)
    #sys.exit()

    #af = AffinityPropagation(preference = None, affinity = "precomputed", copy = False).fit(neg_euc_dist)
    ## note that the default preference in this function is min, axis=1
    print("\n\n\nstarting Louvain from do_big_ap()")
    af = do_louvain_primary_clustering(neg_euc_dist, out_dir = args.out_dir)
    #af = hdf5_affinity_propagation(preference = None, affinity = "precomputed", copy = False, temp_ap_hdf5 = f_ap).fit(neg_euc_dist)
    #sys.exit()
    return(af)

#################################################################################
#################################################################################
#################################################################################
def do_ap_clust(sample_names, clust_array, pref_multiplier = 1, do_louvain = False):
    global args, mem_err
    if (clust_array.shape[0]!=clust_array.shape[1]):
        clust_array = np.transpose(clust_array)
    print('cluster array shape:',np.shape(clust_array))
    print('number of samples:',len(sample_names))

    print("starting the clustering:")
    if not do_louvain:
        ################################################
        ## If we're just doing normal AP clustering
        print('\tAP clustering')
        if mem_err:
            af = do_big_ap()
        else:
            if not args.spearman_dist:
                ## calculate the affinity matrix
                try:
                    am = -euclidean_distances(clust_array, squared=True)/np.log2(np.shape(clust_array)[1])
                except:
                    if _debug and isinstance(e, MemoryError):
                        print('hit a memory error, going to try it again with an HDF5 format affinity matrix intermediate')
                        af = do_big_ap()
                else:## if the affinity matrix calcualtion was successful
                    try:
                        af = ap(preference = np.min(am,axis=1),affinity="precomputted").fit(am)
                        #print(af.affinity_matrix_[:5,:5])
                    except Exception as e:
                        if _debug and isinstance(e, MemoryError):
                            print('hit a memory error, going to try it again with an HDF5 format affinity matrix intermediate')
                            af = do_big_ap()
                    else:
                        pass
            else:
                #pref = np.min(clust_array)*.5
                pref = np.min(clust_array,axis=1)*pref_multiplier
                print(np.shape(clust_array))
                print("preference:",pref)
                #sys.exit()
                try:
                    af = ap(preference = pref, affinity="precomputed").fit(clust_array)
                    #print(af.affinity_matrix_[:5,:5])
                except Exception as e:
                    if _debug and isinstance(e, MemoryError):
                        print('hit a memory error, going to try it again with an HDF5 format affinity matrix intermediate')
                        af = do_big_ap()
                else:
                    pass
        print("ap auto pref:",af.preference)
    else:
        ################################################
        ## we're doing the full louvain clustering
        print("\tLouvain modularity based clustering")
        if not args.spearman_dist:
            print("\n\n\nstarting Louvain from do_ap_clust() without Spearman dist")
            ## mildly different am matrix calc for non-spear dist. just the actual euclidean distance of the array, and scaled back to be 
            try:
                am = -euclidean_distances(clust_array, squared=True)
            except:
                if _debug and isinstance(e, MemoryError):
                    print('hit a memory error, going to try it again with an HDF5 format affinity matrix intermediate')
                    sys.exit()
                    ## TODO:
                    ## write the bit to do pass this to the mat_to_adj
            else:
                af = do_louvain_primary_clustering(am, out_dir = args.out_dir)
        else:
            print("\n\n\nstarting Louvain from do_ap_clust() with Spearman dist")
            ## if spearman_dist is true, then we've already converted it to an affinity matrix
            print(type(clust_array))
            af = do_louvain_primary_clustering(clust_array, out_dir = args.out_dir)



    optimal_centroid_indices = af.cluster_centers_indices_
    #print(type(optimal_centroid_indices))
    if str(type(optimal_centroid_indices)) == "<class 'NoneType'>":
        optimal_centroid_indices = [0]
        labels = [0]*len(sample_names)
        #return()
    else:
        labels = af.labels_

    print(labels)
    num_clust = len(optimal_centroid_indices)
    print(labels)
    print(optimal_centroid_indices)
    # print('AP clustering found',num_clust,'clusters')
    
    #print(labels)
    #print(len(labels))
    #sys.exit()
    f_list = None
    #print(dir(af))
    sample_k_table, sample_k_lists = group_list_to_sample_k_table(labels)
    sample_k_table = []
    for i in range(0,len(sample_names)):
        sample_k_table.append([sample_names[i],labels[i]])
    sample_k_lists = []
    for i in range(num_clust):
        sample_k_lists.append([])
    print(sample_k_lists)
    for i in range(0,len(sample_names)):
        sample_k_lists[labels[i]].append(sample_names[i])
    return(sample_k_table, sample_k_lists, f_list, optimal_centroid_indices, af)
#########################################################
#########################################################
#########################################################
#########################################################
## some functions for merging clusters based on 
## transition probability
################################################
################################################
## find cluster mergers

sample_id_hash = {key:value for  value, key in enumerate(title[1:])}


def zero_to_na(in_mat):
    in_mat[in_mat == 0] = np.nan
    return(in_mat)

def sample_k_lists_to_cluster_indices(sample_k_lists):
    global sample_id_hash
    cluster_indices = []
    for i in range(0,len(sample_k_lists)):
        cluster_indices.append([sample_id_hash[k] for k in sample_k_lists[i]])
        #print(i,len(cluster_indices[-1]))
    return(cluster_indices)

def euc_dist_across_class(cluster1,cluster2, in_mat):
    d = np.zeros((len(cluster1),len(cluster2)))
    for i in range(0,len(cluster1)):
        for j in range(len(cluster2)):
            d[i,j] = euclidean_distance(in_mat[:,cluster1[i]],in_mat[:,cluster2[j]])
    return(d)


def calc_dist_sd(cluster1,in_mat):
    if len(cluster1)==0:
        return(0)
    ## first find the average minimum distance within each cluster
    # Euclidean distance
    cluster1 = sorted(cluster1)
    ## if it's not already a distance matrix, then calculate it
    if in_mat.shape[0]!=in_mat.shape[1] and not in_mat[:10,:]==np.transpose(in_mat[:,:10]):
        clust1_euc_dist = get_half_distance_matrix(in_mat[:,cluster1])
        clust1_euc_dist += np.transpose(clust1_euc_dist)
        clust1_euc_dist = zero_to_na(clust1_euc_dist)
        ## return the standard deviation of those distances
        clust1_dist_sd = np.nanstd(clust1_euc_dist)
        return(clust1_dist_sd)
    ## otherwise, we can skip right ahead to the std 
    else:
        temp_subset = in_mat[cluster1,:]
        temp_subset = temp_subset[:,cluster1]
        clust1_dist_sd = zero_to_na(np.tril(temp_subset,k=-1)).flatten()
        clust1_dist_sd = np.abs(clust1_dist_sd[~np.isnan(clust1_dist_sd)])
        #print(clust1_dist_sd)
        temp_sd = np.std(clust1_dist_sd.tolist())
        print("\tStDev:",temp_sd)
        return(temp_sd)


def get_sample_means(sample_k_lists,cluster_indices):
    global full_expression
    sample_means = np.zeros((np.shape(full_expression)[0],len(sample_k_lists)))
    for i in range(0,len(cluster_indices)):
        temp_samples = cluster_indices[i]
        sample_means[:,i] = np.mean(full_expression[:,temp_samples], axis=1)
    return(sample_means)


from sklearn.metrics.pairwise import euclidean_distances
def get_exemplar_distances_mat(exemplar_indices):
    global full_expression
    ## make the output matrix
    if full_expression.shape[0]!=full_expression.shape[1] and full_expression[:10,:]==np.transpose(full_expression[:,:10]):
        edist_mat = np.zeros((full_expression.shape[0],len(exemplar_indices)))
        for i in range(len(exemplar_indices)):
            edist_mat[:,i]=full_expression[:,exemplar_indices[i]]
        print("\n\nexemplar matrix:")
        print(edist_mat)
        print('\n\n')
        return(euclidean_distances(np.transpose(edist_mat)))
    else:
        dist_mat = np.zeros((len(exemplar_indices),len(exemplar_indices)))
        for i in range(len(exemplar_indices)):
            for j in range(i,len(exemplar_indices)):
                if i != j:
                    e_1_idx = exemplar_indices[i]
                    e_2_idx = exemplar_indices[j]
                    dist_mat[i,j] = np.abs(full_expression[i,j])
                    dist_mat[j,i] = np.abs(full_expression[j,i])
        return(dist_mat)


def ids_to_idxs(in_ids):
    global sample_id_hash
    temp_index_list = [sample_id_hash[i] for i in in_ids]
    return(temp_index_list)


def do_cluster_merger(sample_k_lists,optimal_centroid_indices,name_leader='',colors=None, dont_save=False):
    global out_plot_dict, full_expression, temp
    ###########################################################
    ## first calculate the within cluster spread
    do_max_min_spread = False
    do_sd_spread = True

    #exemplar_adj_mat = get_exemplar_distances(optimal_centroid_indices,k=10)

    if do_sd_spread:
        print('finding the spread within each cluster')
        within_clust_dist_sd =[]
        indices = list(range(0,len(sample_k_lists)))
        for i in indices:
            print('\tworking on cluster',i)
            ## get the indices for this group
            cluster1 = ids_to_idxs(sample_k_lists[i])
            ## sd of Euclidean distances of all points in cluster from each other
            temp_sd = calc_dist_sd(cluster1, full_expression)
            print("\t\t",temp_sd)
            within_clust_dist_sd.append(temp_sd)

        ## get the Euclidean distance of all exemplars from each other
        exemplar_distance_mat = get_exemplar_distances_mat(optimal_centroid_indices)
        print("exemplar_distance_mat")
        print(exemplar_distance_mat)

        ## make the matrix showing the SD1 + SD2 standard deviation for each cluster pair
        sum_sds = np.zeros((len(sample_k_lists),len(sample_k_lists)))## matrix for each cluster by each cluster adding their internal SDs
        for i in range(0,len(within_clust_dist_sd)):
            for j in range(i,len(within_clust_dist_sd)):
                sum_sds[i,j]=within_clust_dist_sd[i]+within_clust_dist_sd[j]
        sum_sds += np.transpose(sum_sds)
        
        ## calculate the Z-score distance of clusters from each other
        cluster_z_distance_mat = exemplar_distance_mat/sum_sds
        cluster_z_distance_mat = np.nan_to_num(cluster_z_distance_mat)
        print("sum_sds")
        print(sum_sds)
        print("cluster_z_distance_mat")
        print(cluster_z_distance_mat)
        ## calculate the probabilty of clusters merging based on this
        from scipy.stats import norm
        ## use 2-tailed Z probabilities
        transition_probability_matrix = norm.sf(abs(cluster_z_distance_mat))
        print("transition_probability_matrix")
        print(transition_probability_matrix)
        ## cell fraction transitioning at current state
        one_cell_per_x_at_current_state = 1/transition_probability_matrix

        if True:#type(colors) == np.array and not dont_save:
            ## plot a heatmap of the transition probability matrix
            reorder_cluster_map = sns.clustermap(transition_probability_matrix,
                col_colors = colors,
                row_colors = colors,
                cmap=global_cmap)
            plt.savefig(temp+'/'+name_leader+'cell_type_transition_probabilities.png',
                    dpi=args.dpi,
                    bbox_inches='tight')
            # avg_transitional_cells_per_thousand = 1000/(1/transition_probability_matrix)

            # sns.clustermap(np.log2(avg_transitional_cells_per_thousand+1),
            #             col_colors = colors,
            #             row_colors = colors)
            # plt.savefig(temp+'/log2_avg_transitional_cells_per_thousand.png',
            #         dpi=args.dpi,
            #         bbox_inches='tight')

            # sns.clustermap(np.log10(transition_probability_matrix+1e-100),
            #             col_colors = colors,
            #             row_colors = colors)
            # plt.savefig(temp+'/log10_cell_type_transition_probabilities.png',
            #         dpi=args.dpi,
            #         bbox_inches='tight')
            reorder_cluster_map_copy = reorder_cluster_map
            ## put the transition probability into the output dictionary
            out_plot_dict["transition_probability"]=reorder_cluster_map
            save_dict(out_plot_dict,temp+'/clustering_plots.pkl')


        ## write transition probabilities
        transition_probability_matrix_copy = transition_probability_matrix[:]
        transition_probability_matrix_copy=transition_probability_matrix_copy.tolist()
        col_titles = ["cell_types"]
        for i in range(0,len(transition_probability_matrix_copy)):
            temp_cell_type = "sample_group_"+str(i)
            transition_probability_matrix_copy[i] = [temp_cell_type] + transition_probability_matrix_copy[i]
            col_titles.append(temp_cell_type)
        transition_probability_matrix_copy = [col_titles]+transition_probability_matrix_copy
        if not dont_save:
            write_table(transition_probability_matrix, temp+"/"+name_leader+"cell_type_transition_probabilities.txt")

        return(transition_probability_matrix)


############################################################################################################################
class louvain_clust_object():
    def __init__(self, affinity, labels):
        self.affinity_matrix_ = affinity
        self.labels_ = labels
        self.sample_k_table, self.sample_k_lists = group_list_to_sample_k_table(labels)
        self.cluster_indices = sample_k_lists_to_cluster_indices(self.sample_k_lists)
        self.cluster_centers_indices_= []
        self.cluster_centers_ =  []
        self.get_cluster_center_indices()

    def get_cluster_center_indices(self):
        print(self.cluster_indices)
        for i in range(len(self.cluster_indices)):
            temp_indices = np.array(self.cluster_indices[i])
            temp_subset = self.affinity_matrix_[temp_indices,:]
            temp_subset = temp_subset[:,temp_indices]
            temp_sum = np.sum(self.affinity_matrix_[temp_indices,:],axis = 1)
            print(temp_sum)
            temp_center_index = np.argmax(temp_sum)
            print(temp_center_index)
            temp_center = temp_indices[temp_center_index]
            self.cluster_centers_indices_.append(temp_center)
            print("\t\tnew cluster center:",self.cluster_centers_indices_[-1])
        self.cluster_centers_ = np.zeros((len(self.cluster_centers_indices_),self.affinity_matrix_.shape[1]))
        for i in range(len(self.cluster_centers_)):
            print(self.cluster_centers_indices_[i])
            self.cluster_centers_[i,:]=self.affinity_matrix_[self.cluster_centers_indices_[i],:]
        #self.cluster_centers_ = np.array(self.affinity_matrix_[self.cluster_centers_indices_])

############################################################################################################################
def normalize_subset_of_am(am_subset,temp_global_nan_min,percentile,offset=0,epsilon=1e-10):
    if np.nanmin(am_subset[:,:])<0:
        am_subset[:,:] = -1/((am_subset[:,:]-temp_global_nan_min)+1)
    else:
        am_subset[:,:] = 1/((am_subset[:,:]-temp_global_nan_min)+1)
    cutoff = np.nanpercentile(am_subset[:,:], (percentile)*100, axis = 1)
    #print("\tusing cutoff of:",cutoff)
    ## func3
    for i in range(am_subset.shape[0]):
        am_subset[i,:]-=(cutoff[i]-epsilon)
    am_subset[am_subset[:,:]<0] = 0
    temp_max = np.nanmax(am_subset[:,:],axis=1)
    for i in range(am_subset.shape[0]):
        am_subset[i,:] /= temp_max[i]
    ## set the 'diagonal' to zero
    for i in range(am_subset.shape[0]):
        am_subset[i,i+offset]=0
    return(am_subset)


def normalize_am(am, percentile, min_neighbors = 5, global_percentile = False):
    ## First convert the eye to nans
    temp_global_nan_min = 99999999999999
    print('input matrix shape:',am.shape)
    print("\tfinding global min")
    for i in range(am.shape[0]):
        if i%10000==0 and i!=0:
            print('\t\t',round(100*i/am.shape[0],2),"%")
        am[i,i]=np.nan
        if np.nanmin(am[i,:])>0:
            temp_local_min = np.nanmin(am[i,:])
        else:
            temp_local_min = np.nanmin(am[i,:]*-1)
        temp_global_nan_min = min([temp_local_min,temp_global_nan_min])
    print("temp_global_nan_min:",temp_global_nan_min)
    #print("normalizing to min")
    print("\tnormalizing affinity matrix")
    counter=0
    interval = 10000
    while counter+interval< am.shape[0]:
        print("\t\t",round((counter+interval)/am.shape[0]*100,2),"%")
        #########
        ## func2
        am[counter:(counter+interval),:] = normalize_subset_of_am(np.array(am[counter:(counter+interval),:]),temp_global_nan_min,percentile,offset=counter)
        counter+=interval
    am[counter:,:] = normalize_subset_of_am(np.array(am[counter:,:]),temp_global_nan_min,percentile,offset=counter)
    ##
    # print("number of connections:")
    # print(np.sum(am>0,axis=1))
    # print(np.max(am,axis=1))
    # for i in range(am.shape[0]):
    #     temp_vect = am[i,am[i,:]>0]
    #     print(i,np.min(temp_vect),np.max(temp_vect),temp_vect.shape)


    # # counter = 0
    # # interval = 10000
    # # while counter+interval< am.shape[0]:
    # #     print("\t",round((counter+interval)/am.shape[0]*100,2),"%")
    # #     #########
    # #     ## func2
    # #     am[counter:(counter+interval),:] = 1/((am[counter:(counter+interval),:]-temp_global_nan_min)+1)
    # #     #am[counter:(counter+interval),:] = am[counter:(counter+interval),:]-temp_global_nan_min
    # #     #am[counter:(counter+interval),:] = 1/(am[counter:(counter+interval),:]+1)
    # #     counter+=interval
    # # ########
    # # ## func2
    # # am[counter:,:] = 1/((am[counter:,:]-temp_global_nan_min)+1)
    # #am[counter:,:] = 1/(am[counter:,:]+1)

    # # for i in range(am.shape[0]):
    # #     if i%2500 == 0:
    # #         print('\t',i)
    # # print(am)

    # if global_percentile:
    #     ## calculate the percentile cutoff
    #     cutoff = np.nanpercentile(am, (percentile)*100)
    #     #cutoff = np.min(np.max(am[:,:],axis=1))+1e-15
    #     row_cutoff = np.nanmax(am[:,:],axis=1)-1e-15

    #     ## mask everything less than the cutoff
    #     for i in range(am.shape[0]):
    #         am[i,:]=am[i,:]-min([cutoff,row_cutoff[i]])
    # else:
    #     # ## calculate the percentile cutoff
        
    #     ## original
    #     print('calculating row-wise percentile')
    #     #cutoff = np.nanpercentile(am, (percentile)*100, axis = 1)
    #     cutoff = np.zeros((am.shape[0]))
    #     counter = 0
    #     interval = 10000
    #     while counter+interval< am.shape[0]:
    #         cutoff[counter:(counter+interval)] = np.nanpercentile(am[counter:(counter+interval),:], (percentile)*100, axis = 1)
    #         counter+=interval
    #     cutoff[counter:] = np.nanpercentile(am[counter:,:], (percentile)*100, axis = 1)
        

    #     ## new
    #     # global_cutoff = np.nanpercentile(am, (percentile)*100)
    #     # cutoff = np.nanmax(am, (percentile)*100, axis = 1)
    #     # cutoff[cutoff>global_cutoff] = global_cutoff

    #     # #cutoff = np.min(np.max(am[:,:],axis=1))+1e-15
    #     # row_cutoff = np.nanmax(am[:,:],axis=1)-1e-15

    #     ## mask everything less than the cutoff and make the 
    #     counter = 0
    #     interval = 10000
    #     print("normalizing to max")
    #     while counter+interval< am.shape[0]:
    #         print("\t",round((counter+interval)/am.shape[0]*100,2),"%")
    #         # am[counter:(counter+interval),:] = am[counter:(counter+interval),:]-temp_global_nan_min
    #         # am[counter:(counter+interval),:] = 1/(am[counter:(counter+interval),:]+1)
    #         am[counter:(counter+interval),:]=am[counter:(counter+interval),:]-cutoff[counter:(counter+interval)]#min([cutoff,row_cutoff[i]])
    #         am[counter:(counter+interval),am[counter:(counter+interval),:]<0] = 0
    #         am[counter:(counter+interval),:] /= np.nanmax(am[counter:(counter+interval),:],axis=1)
    #         counter+=interval
    #     am[counter:(counter+interval),:]=am[counter:(counter+interval),:]-cutoff[counter:(counter+interval)]#min([cutoff,row_cutoff[i]])
    #     am[counter:,am[counter:,:]<0] = 0
    #     am[counter:,:] /= np.nanmax(am[counter:,:])
    #     # for i in range(am.shape[0]):
    #     #     am[i,:]=am[i,:]-cutoff[i]#min([cutoff,row_cutoff[i]])
    #     #     am[i,am[i,:]<0] = 0
    #     #     am[i,:] /= np.nanmax(am[i,:])
    #     #     if i%2500 == 0:
    #     #         print('\t',i)

    # #am[am<0]=0
    # print("\tusing cutoff of:",cutoff)

    # ## change the eye to zero
    # for i in range(am.shape[0]):
    #     am[i,i]=0

    print("\tfinal network matrix:")
    print(am)
    return(am)


def get_current_edges(cur_row, cur_index):
    cur_row = np.array(cur_row)
    indices = np.where(cur_row != 0)[0]
    all_edges = []
    for index in indices:
        #if index > cur_index:
        all_edges.append((cur_index,index,{"weight":cur_row[index]}))
    return(all_edges)


def do_louvain_primary_clustering(am, percentile = 0.95, flexible_percentile = True, flexible_cap = 200, comp_length_cutoff = 4, out_dir = None):
    """
    Takes in the full affinity matrix and performs louvain modularity on it.
    Percentile is the the X percentile of affinities to 
    """
    cur_vars=set(vars().keys()).union(set(globals().keys()))
    print("\n\nmemory check:")
    for element in cur_vars:
        temp_type=eval('type('+element+')')
        if temp_type==np.ndarray:
            temp_shape=eval(element+'.shape')
            print("\t",temp_shape,element,temp_type)
    print("\n\nDoing Louvain clustering:")
    print("\tconverting affinity matrix into local weighted network")
    print("\tinitial matrix:")
    print(type(am))
    print(am)
    # counter = 0
    # interval = 10000
    # print("re-creating regular Euc Dist")
    # while counter+interval< am.shape[0]:
    #     print("\t",round((counter+interval)/am.shape[0]*100,2),"%")
    #     am[counter:(counter+interval),:] = am[counter:(counter+interval),:]*-1
    #     counter+=interval
    # am[counter:,:] = am[counter:,:] *-1
    # print("min last:",np.min(am[counter:,:]))
    # print("max last:",np.max(am[counter:,:]))
    # for i in range(am.shape[0]):
    #     if i % 15000==0 and i != 0:
    #         print("\t",i)
    #     am[i,:] = am[i,:]*-1

    if flexible_percentile:
        ## this dynamically changes the percentile such that it will do the percentile, unless there are sufficiently large number of cells
        ## at which point, it'll cap the number of edges to the flexible cap number of edges
        equivalent_percentile_for_flexible = 1-(flexible_cap/am.shape[0])
        print("1-(",flexible_cap,'/',am.shape[0],"):",equivalent_percentile_for_flexible)
        if flexible_cap<am.shape[0]:
            percentile = max([percentile,equivalent_percentile_for_flexible])
    print("\nlocally weighted affinity matrix percentile cutoff:",percentile,'% (',int(am.shape[0]-percentile*am.shape[0]),'cells)','\n')
    ## normalize the affinity matrix (and reconvert it to positive range if needed)
    am = normalize_am(am, percentile = percentile)

    print("\tconverting into network")
    ## convert to a network graph
    G = nx.Graph()
    G.add_nodes_from(list(range(am.shape[0])))
    for i in range(am.shape[0]):
        if i%5000==0 and i != 0:
            print("\t\t",round(i/am.shape[0]*100,2),"%")
        G.add_edges_from(get_current_edges(am[i,:],i))
    print("\tdoing the modularity now")
    partition = community.best_partition(G)

    labels = []
    for i in range(len(partition.keys())):
        labels.append(partition[i])

    if out_dir is not None:
        pos = nx.spring_layout(G)
        node_size = 2.5
        edge_width = 2.5/np.sqrt(nx.number_of_edges(G))

        print("\n"*10,"saving cell ebmedding graph","\n\n\n")
        save_dict(G,os.path.join(out_dir,"cell_embedding.graphpkl"))

    af = louvain_clust_object(affinity = am, labels = labels)

    return(af)


def do_louvain(transition_probability_matrix, components_list, comp_length_cutoff = 4):
    """
    The transition probability matrix is the full matrix from the original clustering
    results. The components list is the list of components whose transition probability 
    was greater than or equal to the cutoff. The component length cutoff is the number
    of components that must be in a sub-component graph to determine if they should be 
    subjected to louvain re-cutting. 
    """
    out_comps = []
    for i in range(len(components_list)):
        temp_comp_ids = components_list[i]
        if len(temp_comp_ids)>=comp_length_cutoff:
            sub_trans_mat = transition_probability_matrix[np.array(temp_comp_ids),:]
            sub_trans_mat = sub_trans_mat[:,np.array(temp_comp_ids)]
            #print(sub_trans_mat)
            #print(nx.from_numpy_matrix(sub_trans_mat))
            #print(sub_trans_mat)
            G = nx.from_numpy_matrix(sub_trans_mat)
            partition = community.best_partition(G)
            #print(partition)
            partition_list = []
            for i in range(len(temp_comp_ids)):
                partition_list.append(partition[i])
            ## create a list of new comps
            new_temp_comps = []
            for new_lists in list(set(partition_list)):
                new_temp_comps.append([])
            print('\tsplitting a comp into',len(new_temp_comps))
            ## append the original group ids to their new comps
            for i in range(0,len(temp_comp_ids)):
                new_temp_comps[partition_list[i]].append(temp_comp_ids[i])
            ## append the new comps to the final comp list
            for comp in new_temp_comps:
                out_comps.append(comp)
        else:
            ## if we don't need to re-cut, just append the original
            out_comps.append(temp_comp_ids)
    ## start out with the assumption that there aren't any mergers left
    ## then check if there still are
    any_merged = False
    for comp in out_comps:
        if len(comp)>1:
            any_merged = True
    return(any_merged, out_comps)


def should_clusters_be_merged(transition_probability_matrix, prob_cutoff=0.30):
    ## takes in trantransition_probability_matrix
    ## returns a graph network based on  the transition probability cutoff
    transition_probability_matrix=np.array(transition_probability_matrix)
    np.fill_diagonal(transition_probability_matrix,0)
    max_prob = np.max(transition_probability_matrix)
    any_merged = max_prob >= prob_cutoff
    adj_mat = transition_probability_matrix>=prob_cutoff
    ## turn it into a graph
    temp_graph = nx.Graph(adj_mat)
    ## get the connected components and convert it to lists
    comp_list = list(nx.connected_components(temp_graph))
    for i in range(0,len(comp_list)):
        comp_list[i]=list(comp_list[i])
        print(comp_list[i])
    ## now do louvain modularity to cut this component into more sensical groups
    any_merged, comp_list = do_louvain(transition_probability_matrix, comp_list)
    return(any_merged, comp_list)


def get_updated_sample_group_lists(sample_k_lists, comp_list):
    ## get new lists
    new_sample_k_lists = []
    for i in range(0,len(comp_list)):
        print('working on comp',i)
        temp_comp_groups = comp_list[i]
        temp_list = []
        for j in range(0,len(temp_comp_groups)):
            print('adding group',temp_comp_groups[j])
            temp_list+=sample_k_lists[temp_comp_groups[j]]
        new_sample_k_lists.append(temp_list)
    ## now sort them again
    for i in range(0,len(new_sample_k_lists)):
        #print(i,len(new_sample_k_lists[i]))
        new_sample_k_lists[i]=sorted(new_sample_k_lists[i])
    return(new_sample_k_lists)


def search_for_group(index, sample_k_array):
    ## go through each sample group and look for the current sample index 
    for i in range(len(sample_k_array)):
        if index in sample_k_array[i]:
            return(i)
    sys.exit("couldn't find "+str(index)+" in any of the sample_k_arrays - this is a bug")


def get_sample_k_table_from_sample_k_list(sample_k_lists):
    ## take in the sample k lists (list of list of sample indices by their cluster)
    global title, sample_id_hash
    sample_names = title[1:]
    sample_group_vect = np.zeros((len(sample_names)))
    ## convert the linked list to an array for faster search
    if len(sample_k_lists)>0:
        for i in range(0,len(sample_k_lists)):
            temp_sample_list = sample_k_lists[i]
            for j in range(0,len(temp_sample_list)):
                temp_sample_idx = sample_id_hash[temp_sample_list[j]]
                sample_group_vect[temp_sample_idx]=i
    else:
        sample_group_vect=[0]*len(sample_names)
    ## go through the samples and catelogue their group
    sample_k_table = []
    for i in range(0,len(sample_names)):
        sample_k_table.append([sample_names[i],sample_group_vect[i]])
    return(sample_k_table)


def get_ap_merge_new_clusters(sample_k_table,sample_k_lists,optimal_centroid_indices):
    any_merged = True
    merge_count = 0
    dont_save = False
    original_transition_prob = do_cluster_merger(sample_k_lists,optimal_centroid_indices, name_leader = "original_ap_"+str(merge_count)+"_", dont_save = dont_save)
    any_merged, comp_list = should_clusters_be_merged(original_transition_prob)
    print("do we keep merging?:",any_merged)
    if not any_merged:
        return(sample_k_table,sample_k_lists,optimal_centroid_indices)
    sample_k_lists = get_updated_sample_group_lists(sample_k_lists, comp_list)
    cluster_indices = sample_k_lists_to_cluster_indices(sample_k_lists)
    sample_k_table = get_sample_k_table_from_sample_k_list(sample_k_lists)
    optimal_centroid_indices = get_known_centers(cluster_indices)
    return(sample_k_table,sample_k_lists,optimal_centroid_indices)

#########################################################
#########################################################

## and make the output for plotting later
out_plot_dict = {"transition_probability":None,"plots":{},"exemplar_indices":None,'color_vect':None}

#########################################################
#########################################################
if (args.spearman_dist) and (os.path.isfile(neg_euc_hdf5_file)):
    ## read in the spearman hdf5 file and make full_expression that
    print('reading in the negative Euclidean distance matrix from the hdf5 file')
    cmd('cp '+neg_euc_hdf5_file+' '+neg_euc_hdf5_file+'_copy')
    neg_euc_hdf5_file_copy = neg_euc_hdf5_file+'_copy'
    spear_h5f = h5py.File(neg_euc_hdf5_file_copy, 'r+')
    full_expression = spear_h5f["infile"]


if args.manual_sample_groups == None:
    print('starting clustering on:')
    print(full_expression)
    if not args.ap_clust and not args.louvain_clust:
        sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = do_unknown_k_means_clustering_iter(title[1:], full_expression, cluster_iter = sample_cluster_iter, performed_on_samples = True)
        # if not args.do_rows:
        #     sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = do_unknown_k_means_clustering_iter(title[1:], full_expression, cluster_iter = sample_cluster_iter, performed_on_samples = True)
        # else:
        #     sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = do_unknown_k_means_clustering_iter(title[1:], full_expression, cluster_iter = sample_cluster_iter, performed_on_samples = False)
    else:
        sample_k_table, sample_k_lists, f_list, optimal_centroid_indices, ap_results = do_ap_clust(title[1:], full_expression, do_louvain = args.louvain_clust)
        original_sample_k_table=sample_k_table[:]
        original_sample_k_lists=sample_k_lists[:]
        original_optimal_centroid_indices=optimal_centroid_indices[:]
        ## if ap clustering split it into too many, the preference was likely too low (beyond the point of stability)
        ## so we'll increase it a bit
        print("len(optimal_centroid_indices)>.05*len(title[1:]) or len(optimal_centroid_indices)==1")
        print(len(optimal_centroid_indices),.05*len(title[1:]))
        print(len(optimal_centroid_indices)>.05*len(title[1:]))
        if len(optimal_centroid_indices)>.05*len(title[1:]) or len(optimal_centroid_indices)==1:
            print("affinity propogation failed likely because there were too few real clusters: trying again with Louvain")
            sample_k_table, sample_k_lists, f_list, optimal_centroid_indices, ap_results = do_ap_clust(title[1:], full_expression, do_louvain = args.louvain_clust)
            #sample_k_table, sample_k_lists, f_list, optimal_centroid_indices, ap_results = do_ap_clust(title[1:], full_expression,pref_multiplier=0.5)
            #sample_k_table, sample_k_lists, f_list, optimal_centroid_indices = do_unknown_k_means_clustering_iter(title[1:], full_expression, cluster_iter = sample_cluster_iter, performed_on_samples = True)
        if (args.ap_clust and args.ap_merge) and not args.louvain_clust:
            print('\ndoing ap_merge')
            ## if we're doing the ap_merge protocol for agglomerative ap_clusering
            cluster_indices = sample_k_lists_to_cluster_indices(sample_k_lists)
            sample_means = get_sample_means(sample_k_lists,cluster_indices) 
            sample_k_table,sample_k_lists,optimal_centroid_indices=get_ap_merge_new_clusters(sample_k_table,sample_k_lists,optimal_centroid_indices)
            #print(optimal_centroid_indices)
            #for i in range(0,len(sample_k_lists)):
            #    print(len(sample_k_lists[i]),sample_k_lists[i][:5])
            #sys.exit()
        else:
            print('\nskipping ap_merge')

else:
    labels = list(map(int,list(map(float,grouping_vector))))
    sample_k_table = sample_group_table
    sample_k_table, sample_k_lists = group_list_to_sample_k_table(labels)


# print(sample_k_table)
# print('\n\n\n\n\n\n')
# print(sample_k_lists)
# sys.exit()
########################################################
###### now we need to write it all down ################
########################################################

## here we create the vector of sample ids
sample_ids = title[1:]

sample_id_hash = {key:value for  value, key in enumerate(title[1:])}



if len(sample_ids)!=len(sample_k_table):
    sys.exit('number of input known sample groups does not equal the number of samples in the input file')
sample_cluster_ids = np.zeros(len(sample_ids),dtype = int)-1 ## first start out with -1 as default groups
## then we go through the sample_k_table finding the index of that sample
## then plug in the sample cluster id in the right spot
for i in range(0,len(sample_ids)):
    #temp_index = sample_ids.where(sample_k_table[i][0])
    temp_index = np.where(sample_ids == sample_k_table[i][0])
    sample_cluster_ids[temp_index]=sample_k_table[i][1]
    temp_clust_idx = sample_k_table[i][1]



print("we found",len(sample_k_lists),"clusters")
cluster_indices = sample_k_lists_to_cluster_indices(sample_k_lists)

## write the results of the cell clustering 

print("writing groups")
write_table(sample_k_table,sample_dir+'sample_k_means_groups.txt')
if args.manual_sample_groups == None:
    #print('optimal k =',len(optimal_centroid_indices))
    copy_centroids=optimal_centroid_indices[:]
    #print(list(map(str,copy_centroids)))
    make_file('\n'.join(list(map(str,copy_centroids))),temp+'/centroid_indices.txt')
    #print(f_list)



###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
####################################################
################ plot some results #################
####################################################


print("writing exemplar indices")
colors = cm.nipy_spectral(np.arange(len(sample_k_lists))/len(sample_k_lists))

out_plot_dict['color_vect']=colors
out_plot_dict["exemplar_indices"]=np.array(list(map(int,optimal_centroid_indices[:])),dtype=int)
save_dict(out_plot_dict,temp+'/clustering_plots.pkl')

cluster_indices = sample_k_lists_to_cluster_indices(sample_k_lists)




## TODO: incorporate sample_indices_for_plotting into all plotting functions & log it in the 
plotting_sample_size = 15000
if full_expression.shape[1]>plotting_sample_size:
    sample_indices_for_plotting = sorted(np.random.choice(np.shape(full_expression)[1],size=(plotting_sample_size,),replace=False).tolist())
    sample_indices_for_plotting += deepcopy(optimal_centroid_indices)
    sample_indices_for_plotting = sorted(list(set(sample_indices_for_plotting)))
else:
    sample_indices_for_plotting = list(range(np.shape(full_expression)[1]))
out_plot_dict['sample_indices_for_plotting']=sample_indices_for_plotting
save_dict(out_plot_dict,temp+'/clustering_plots.pkl')


###########################################
## subset the matrix just for plotting
plotting_mat = full_expression[:,sample_indices_for_plotting]
if full_expression.shape[0]==full_expression.shape[1] and np.all(full_expression[:10,:] == np.transpose(full_expression[:,:10])):
    plotting_mat = plotting_mat[sample_indices_for_plotting,:]
###########################################

try:
    # temp_express = full_expression[:,sample_indices_for_plotting]
    # if full_expression.shape[0]==full_expression.shape[1]:
    #     temp_express = temp_express[sample_indices_for_plotting,:]
    sns.clustermap(plotting_mat,cmap=global_cmap)
    plt.savefig(temp+'/sample_used_for_clustering_heatmap.png',
        dpi=args.dpi,
        bbox_inches='tight')
except:
    print("That didn't work either...")




#####################################################################
if os.path.isfile(neg_euc_hdf5_file) and args.louvain_clust:
    ## if we've done the clustering out of memory, we'll have to load back the full negative euclidean distance matrix
    ## to calculate full distances and spread - otherwise lineage would be inaccruate because it's just based on the sparse
    ## locally weighted affinity matrix instead
    spear_h5f.close()
    spear_h5f = h5py.File(neg_euc_hdf5_file, 'r')
    full_expression = spear_h5f["infile"]
    ## plot it
    try:
        # temp_express = full_expression[sample_indices_for_plotting,:]
        # temp_express = temp_express[:,sample_indices_for_plotting]
        sns.clustermap(plotting_mat,cmap=global_cmap)
        plt.savefig(temp+'/sample_neg_euc_dist_heatmap.png',
            dpi=args.dpi,
            bbox_inches='tight')
    except:
        print("had trouble plotting the adjacency matrix used for clustering")
#####################################################################



if args.do_merger:
    print("finding transition probabilities")
    transition_probability_matrix = do_cluster_merger(sample_k_lists,optimal_centroid_indices,name_leader='final_',colors=colors)


##################################################################


def plot_2d(projection,out_plot,x_ax = '',y_ax = ''):
    global sample_id_hash, sample_k_lists, colors, args, ax, plt, temp, sample_indices_for_plotting
    print("\tPlotting",out_plot)
    plt.clf()
    for i in range(0,len(sample_k_lists)):
        temp_idxs = [idx for idx in ids_to_idxs(sample_k_lists[i]) if idx in set(sample_indices_for_plotting)]
        sample_for_plotting_idx_hash = {value:key for key, value in enumerate(sample_indices_for_plotting)}
        temp_idxs = [sample_for_plotting_idx_hash[idx] for idx in temp_idxs]
        try:
            plt.scatter(projection[temp_idxs,0],projection[temp_idxs,1],label='sample_group_'+str(i),color=colors[i],s=args.point_size)
        except:
            print("couldn't get",out_plot,"to work successfully")
            break
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(x_ax)
    plt.ylabel(y_ax)
    if out_plot != None:
        plt.savefig(temp+out_plot,
            dpi=args.dpi,
            bbox_inches='tight')

    ## get the full color vector
    out_color = np.zeros((len(list(sample_id_hash.keys())),4))
    #print(np.shape(out_color))
    for i in range(0,len(sample_k_lists)):
        temp_idxs = ids_to_idxs(sample_k_lists[i])
        #print(colors[i])
        out_color[temp_idxs,:] = colors[i]
        #print(out_color[temp_idxs])
        #sys.exit()
    return({'x':projection[:,0],
        'y':projection[:,1],
        'c':out_color,
        'xlab':x_ax,
        'ylab':y_ax})






##########################################################


# def should_clusters_be_merged(cluster1, cluster2, clust1_num, clust2_num, in_mat, exemplar_adj_mat):
#     global within_clust_max_min_dist

#     if exemplar_adj_mat[clust1_num,clust2_num]==0:
#         return(False,0)

#     # if min([len(cluster1), len(cluster2)])==1:
#     #     return(False)
#     if len(cluster1)==1 and len(cluster2)==1:
#         return(False,0)
#     # maximum minimum Euclidean dist
#     clust1_max_min_dist = within_clust_max_min_dist[clust1_num]
#     clust2_max_min_dist = within_clust_max_min_dist[clust2_num]
#     #print('clust1_max_min_dist',clust1_max_min_dist)
#     #print('clust2_max_min_dist',clust2_max_min_dist)
#     dist_across_clusters = euc_dist_across_class(cluster1, cluster2, in_mat)
#     #print(dist_across_clusters)
#     min_dist_across = np.min(dist_across_clusters)
#     #print('dist_across_clusters',dist_across_clusters)
#     dist_to_beat = 2*np.max([clust1_max_min_dist,clust2_max_min_dist])
#     #print('dist_to_beat',dist_to_beat)
#     #print('min_dist_across',min_dist_across)
#     if min_dist_across<=dist_to_beat:
#         return(True,min_dist_across)
#     else:
#         return(False,min_dist_across)



# def get_exemplar_distances(exemplar_indices, k=5):
#     global full_expression
#     ## make a k-nearest neighbor embedding
#     k=min([k,len(exemplar_indices)])
#     exemplar_distance_mat = get_half_distance_matrix(np.transpose(full_expression[:,exemplar_indices]))
#     ## make it symetric, by filling in the lower triangle
#     exemplar_distance_mat += np.transpose(exemplar_distance_mat)
#     print(exemplar_distance_mat)
#     print(np.shape(exemplar_distance_mat))
#     exemplar_adj_mat = np.zeros((len(exemplar_indices),len(exemplar_indices)),dtype = bool)
#     for exemplar_1 in range(0,len(exemplar_indices)):
#         print(exemplar_1)
#         temp_dist_vect = exemplar_distance_mat[exemplar_1,:]
#         temp_min_indices = temp_dist_vect.argsort()[:k].tolist()
#         # temp_min_indices = []
#         # for i in range(0,len(temp_min_indices_list)):
#         #     temp_min_indices.append(exemplar_indices.index(temp_min_indices_list[i]))
#         #print(temp_min_indices)
#         exemplar_adj_mat[exemplar_1,temp_min_indices] = 1
#     return(exemplar_adj_mat)

# def get_exemplar_distances_mat(exemplar_indices):
#     global full_expression
#     exemplar_distance_mat = get_half_distance_matrix(np.transpose(full_expression[:,exemplar_indices]))
#     ## make it symetric, by filling in the lower triangle
#     exemplar_distance_mat += np.transpose(exemplar_distance_mat)
#     return(exemplar_distance_mat)






if args.perplexity == None:
    ## get the average group size
    avg_grp_size = (len(title)-1)/len(sample_k_lists)
    if avg_grp_size<5:
        args.perplexity = 5
    elif avg_grp_size>100:
        args.perplexity = 100
    else:
        args.perplexity = round(avg_grp_size)
    if has_umap:
        args.perplexity = 5
    print('average group size:',avg_grp_size)
    print('perplexity is set to:',args.perplexity)

if not has_umap:
    model = TSNE(n_components=2, #init = 'pca', 
        perplexity = args.perplexity, random_state=args.rand_seed, n_iter = int(eval(args.tsne_iter)))
else:
    model = umap.UMAP(n_neighbors=args.perplexity,
                      min_dist=0.3,
                      metric='correlation')
pca_model = PCA(n_components=2)



def do_pca(in_mat, out_file = '/pca_projection.png'):
    global pca_model, out_plot_dict, temp
    pca_projection = pca_model.fit_transform(np.transpose(in_mat))
    out_plot_dict['plots'][temp+out_file] = plot_2d(pca_projection, out_file, x_ax = 'PC1', y_ax = 'PC2')
    save_dict(out_plot_dict,temp+'/clustering_plots.pkl')
    return(pca_projection)

def do_tsne(in_mat, out_file = '/tsne_projection.png'):
    global model, out_plot_dict, temp, has_umap
    if not has_umap:
        print('doing tSNE')
    else:
        print('doing UMAP')
        out_file='/umap_projection.png'
    projection = model.fit_transform(np.transpose(in_mat))
    if not has_umap:
        out_plot_dict['plots'][temp+out_file] = plot_2d(projection, out_file, x_ax = 'tSNE1', y_ax = 'tSNE2')
    else:
        out_plot_dict['plots'][temp+out_file] = plot_2d(projection, out_file, x_ax = 'UMAP1', y_ax = 'UMAP2')
    return(projection)

print('doing PCA')
full_pca = do_pca(plotting_mat)
save_dict(out_plot_dict,temp+'/clustering_plots.pkl')
try:
    #full_tsne = do_tsne(full_expression)
    # temp_mat = full_expression[sorted(optimal_centroid_indices),:]
    # temp_mat = temp_mat[:,sample_indices_for_plotting]
    full_tsne = do_tsne(plotting_mat)
except Exception as e:
    print("couldn't get the full t-sne working unfortunately...")
    print('\t'+str(e))
save_dict(out_plot_dict,temp+'/clustering_plots.pkl')


# if args.ap_clust and not args.spearman_dist and args.manual_sample_groups==None:
#     print('doing AP PCA')
#     ap_pca = do_pca(ap_results.affinity_matrix_, out_file = '/affinity_matrix_pca.png')
#     print('doing AP tSNE')
#     try:
#         ap_tsne = do_tsne(ap_results.affinity_matrix_,out_file = '/affinity_matrix_tsne.png')
#     except Exception as e:
#         print("couldn't get the ap t-sne working unfortunately...")
#         print('\t'+str(e))
# save_dict(out_plot_dict,temp+'/clustering_plots.pkl')

##################################################





##################################################
## get a vector with group number
linear_groups = []
for name in title[1:]:
    for i in range(0,len(sample_k_lists)):
        if name in sample_k_lists[i]:
            linear_groups.append(i)


if "reorder_cluster_map" in globals():
    group_reordering_vector = []
    group_order_list = list(reorder_cluster_map.dendrogram_row.reordered_ind)
    for i in range(0,len(group_order_list)):
        temp_group = group_order_list[i]
        group_reordering_vector += sample_k_lists[temp_group]
else:
    group_reordering_vector = []
    for group in sample_k_lists:
        group_reordering_vector+=group

group_reordering_vector = ids_to_idxs(group_reordering_vector)

out_plot_dict['linear_groups']=linear_groups
out_plot_dict["sample_k_lists"]=sample_k_lists
save_dict(out_plot_dict,temp+'/clustering_plots.pkl')

print('plotting some heatmaps and similarity scatters')




plt.clf()

try:
    sns.clustermap(full_expression[:,group_reordering_vector],
        col_cluster = False,
        col_colors = colors[linear_groups][group_reordering_vector],
        cmap=global_cmap)
    plt.savefig(temp+'/clustering_groups.png',
            dpi=args.dpi,
            bbox_inches='tight')
except:
    print("couldn't get the group clustered heatmap going")


if (args.ap_clust and args.manual_sample_groups==None) or (args.ap_clust and (np.shape(full_expression)[0]==np.shape(full_expression)[1])):
    plt.clf()
    if "ap_results" in globals():
        cont = True
        try:
            ap_mat = ap_results.affinity_matrix_[:,group_reordering_vector]
        except:
            print("couldn't rearrange affinity matrix")
            cont = False
        if cont:
            ap_mat = ap_mat[group_reordering_vector,:]
            #ap_mat = np.log2(ap_mat**2+1)
            print(np.shape(ap_mat))
            try:
                sns.clustermap(ap_mat,
                    col_cluster = False,
                    col_colors = colors[linear_groups][group_reordering_vector],
                    row_cluster = False,
                    row_colors = colors[linear_groups][group_reordering_vector],
                    cmap=global_cmap)
                plt.savefig(temp+'/affinity_matrix.png',
                        dpi=args.dpi,
                        bbox_inches='tight')
            except:
                print("couldn't get the affinity map figure")
            try:
                sns.clustermap(ap_mat,
                    col_cluster = True,
                    col_colors = colors[linear_groups][group_reordering_vector],
                    row_cluster = True,
                    row_colors = colors[linear_groups][group_reordering_vector],
                    cmap=global_cmap)
                plt.savefig(temp+'/clustered_affinity_matrix.png',
                        dpi=args.dpi,
                        bbox_inches='tight')
            except:
                print("couldn't get the affinity map figure")
               

if args.spearman_dist and not args.ap_clust:
    plt.clf()
    cont = True
    try:
        temp_full_mat = full_expression[:,group_reordering_vector]
    except:
        print("couldn't rearrange full_expression for spearman matrix plots")
        cont = False
    if cont:
        temp_full_mat = temp_full_mat[group_reordering_vector,:]
        #ap_mat = np.log2(ap_mat**2+1)
        print(np.shape(temp_full_mat))
        try:
            sns.clustermap(temp_full_mat,
                col_cluster = False,
                col_colors = colors[linear_groups][group_reordering_vector],
                row_cluster = False,
                row_colors = colors[linear_groups][group_reordering_vector],
                cmap=global_cmap)
            plt.savefig(temp+'/spearman_matrix.png',
                    dpi=args.dpi,
                    bbox_inches='tight')
        except:
            print("couldn't get the spearman map figure")
        try:
            sns.clustermap(temp_full_mat,
                col_cluster = True,
                col_colors = colors[linear_groups][group_reordering_vector],
                row_cluster = True,
                row_colors = colors[linear_groups][group_reordering_vector],
                cmap=global_cmap)
            plt.savefig(temp+'/clustered_spearman_matrix.png',
                    dpi=args.dpi,
                    bbox_inches='tight')
        except:
            print("couldn't get the spearmanS map figure")         


# for i in list(out_plot_dict["plots"].keys()):

#     temp_plt = out_plot_dict["plots"][i]
#     print(temp_plt)

#     sys.exit()

out_plot_dict['group_reordering_vector']=group_reordering_vector
out_plot_dict['reordered_colors']=colors[linear_groups][group_reordering_vector]


save_dict(out_plot_dict,temp+'/clustering_plots.pkl')


print('\n\n\nfinished clustering\n\n\n')