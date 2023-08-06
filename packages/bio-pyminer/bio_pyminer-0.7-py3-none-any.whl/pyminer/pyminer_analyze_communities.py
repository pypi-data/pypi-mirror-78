#!/usr/bin/env python3
import pickle, scipy, sys,  fileinput, gc, os
from networkx import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mstats, rankdata
import seaborn as sns
import pandas as pd
import time
from copy import deepcopy
from scipy.stats.mstats import f_oneway as aov
from subprocess import Popen
from statsmodels.stats.multicomp import pairwise_tukeyhsd as TukeyHSD
from statsmodels.stats.libqsturng import psturng

try:
    import community
except:
    community_installed = False
    print('https://github.com/taynaud/python-louvain is a requirement for finding communites')
else:
    import community
    community_installed = True
gc.enable()
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

def strip_split(line, delim = '\t'):
    return(line.strip('\n').split(delim))


def process_dir(in_dir):
    ## process the output dir
    in_dir = os.path.join(in_dir)
    if not os.path.isdir(in_dir):
        os.makedirs(in_dir)
    return(in_dir)
############################################################################################
## this function was adopted from emre's stackoverflow answer found here:
## https://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python
def correct_pvalues_for_multiple_testing(pvalues, correction_type = "Benjamini-Hochberg"):                
    """                                                                                                   
    consistent with R - print correct_pvalues_for_multiple_testing([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    from numpy import array, empty
    pvalues = array(pvalues)
    n = int(pvalues.shape[0])
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        for rank, vals in enumerate(values):
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue
    elif correction_type == "Benjamini-Hochberg":
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]
        values.sort()
        values.reverse()
        new_values = []
        for i, vals in enumerate(values):
            rank = n - i
            pvalue, index = vals
            new_values.append((n/rank) * pvalue)
        for i in range(0, int(n)-1):
            if new_values[i] < new_values[i+1]:
                new_values[i+1] = new_values[i]
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]
    return new_pvalues

def get_tukey(vals, groups):
    try:
        res = TukeyHSD(vals, groups)
    except:
        return([['group_1','group_2',"TukeyHSD_p_values"],["NA","NA","1"]])
    print('\n\n',res)
    first_group_vector = ['group_1']
    second_group_vector = ['group_2']
    for i in range(res.groupsunique.shape[0]):
        for j in range(i,res.groupsunique.shape[0]):
            if i != j:
                first_group_vector.append(res.groupsunique[i])
                second_group_vector.append(res.groupsunique[j])

    p_vals = psturng(np.abs(res.meandiffs / res.std_pairs), len(res.groupsunique), res.df_total)
    p_values = ['TukeyHSD_p_values'] + np.array(p_vals,dtype=str).tolist()
    for p in range(0,len(p_values)):
        if p_values[p]=='0.001':
            p_values[p] = '<0.001'

    print(p_values)
    out_table = np.transpose(np.vstack((first_group_vector, second_group_vector, p_values)))
    return (out_table)
############################################################################################
##############################################################
import argparse
parser = argparse.ArgumentParser()


parser.add_argument("-community_table",
                    help="the table annotating the ")
parser.add_argument("-id_subset",
                    help="a file that contains all of the gene IDs in the current module to be plotted")
parser.add_argument("-z_score_table",
                    help="the table of cluster level Z-scores")
parser.add_argument("-module_size_cutoff",
                    help="how big is the smallest module that we should analyze? (default = 15)",
                    default = 15)
parser.add_argument("-species",
                    help="for pathway analysis, we'll need the species (default = hsapiens)",
                    default = "hsapiens")
parser.add_argument("-name",
                    help="if you only have a sinlge input list, you can name it here",
                    default = "community")
parser.add_argument('-annotation_dict','-ad',
                    dest='symbol_def_dict',
                    type=str)
parser.add_argument("-out_dir",
                    help="the output directory")


##############################################################

def do_gprofiler(ids, out_dir, gprofiler_out_dir, background, species, name = 'community'):
    bg_file = os.path.join(out_dir,'background.txt')
    make_file('\n'.join(background), bg_file)
    com_file = os.path.join(out_dir,'community_ids.txt')
    make_file('\n'.join(ids), com_file)
    gprofiler_out_file = os.path.join(gprofiler_out_dir,name+'_gprofiler.txt')
    cmd('pyminer_gprofile.py -i '+com_file+' -b '+bg_file+' -species '+species+' -o '+gprofiler_out_file)
    return


def get_gene_annotations(ids, symbol_dict, def_dict):
    out_anno = []
    for i in range(len(ids)):
        temp_node = ids[i]
        if len(symbol_dict[temp_node]) == 0:
            out_anno.append([temp_node, "None", "None"])
        else:
            for j in range(len(symbol_dict[temp_node])):
                out_anno.append([temp_node, symbol_dict[temp_node][j], def_dict[temp_node][j]])
                #print(temp_node, symbol_dict[temp_node][j], def_dict[temp_node][j])
    return(out_anno)


def pr_annotation(in_table, pr_dict):
    if pr_dict == None:
        return(in_table)
    pr_vect = []
    for i in range(0,len(in_table)):
        ## first col is gene
        in_table[i].append(pr_dict[in_table[i][0]])
        pr_vect.append(pr_dict[in_table[i][0]])
    ## sort the table based on highest page rank
    pr_vect_order = np.argsort(np.array(pr_vect)).tolist()[::-1]
    in_table = np.array(in_table)
    # print(in_table)
    # print(np.shape(in_table))
    # print(pr_vect_order)
    in_table = in_table[pr_vect_order,:].tolist()
    return(in_table)


def get_med_table(z_array_header, z_array_subset, name, out_dir):
    #print(z_array_subset)
    temp_gmean = np.median(z_array_subset, axis = 0).tolist()
    out_table = [['id',name]]
    for i in range(len(z_array_header)):
        out_table.append([z_array_header[i], temp_gmean[i]])
    write_table(out_table, os.path.join(out_dir, 'median_module_usage.tsv'))
    return()


def analyze_subset(ids, 
                   z_array,
                   z_array_header,
                   id_list,
                   id_hash, 
                   out_dir,
                   gprofiler_out_dir,
                   species,
                   symbol_dict,
                   def_dict,
                   name = 'community',
                   background = None,
                   pr_dict = None):
    ## if there isn't a background, just use everything in the dataset
    if background == None:
        background = id_list

    ## first thing to do is catelogue the index of the ids from the z-array
    temp_idxs = sorted([id_hash[temp_id] for temp_id in ids])
    
    z_subset_array = z_array[temp_idxs,:]
    ## z_subset_array_rank = rankdata(z_subset_array, method = 'min')

    ## get the median for each group
    get_med_table(deepcopy(z_array_header), z_subset_array, name, out_dir)

    ## strip the header of 'sample_group_'
    for i in range(0,len(z_array_header)):
        z_array_header[i]=z_array_header[i].replace('sample_group_','')
    z_subset_lists = [z_subset_array[:,i].tolist() for i in range(z_subset_array.shape[1])]
    temp_aov_f, temp_aov_p = aov(z_subset_lists)
    print('\t\tnominal F/p',temp_aov_f, temp_aov_p)
    ## now plot the results

    #####################
    ## we will use the actual data for display & rank transformed Z-scores for Tukey HSD

    # z_subset_rank = pd.DataFrame(z_subset_array_rank)
    # z_subset_rank.columns = z_array_header
    # z_subset_rank = z_subset_rank.melt(var_name='groups', value_name='z-scores')


    z_subset = pd.DataFrame(z_array[temp_idxs,:])
    z_subset.columns = z_array_header
    z_subset = z_subset.melt(var_name='groups', value_name='z-scores')

    plt.clf()
    sns.violinplot(x="groups",y="z-scores", data = z_subset)
    plt.savefig(os.path.join(out_dir,"group_z_scores.png"),
                dpi=300,
                bbox_inches='tight')

    ## do the post-hoc tests
    tukey_table = get_tukey(z_subset["z-scores"],z_subset["groups"])
    write_table(tukey_table, os.path.join(out_dir,'TukeyHSD.tsv'))

    ## write the annotation file in the output directory
    temp_gene_annotations = get_gene_annotations(ids, symbol_dict, def_dict)
    temp_gene_annotations = pr_annotation(temp_gene_annotations, pr_dict = pr_dict)
    write_table(temp_gene_annotations, os.path.join(out_dir,'community_ids_annotated.tsv'))


    ## do the gprofiler analysis of this module
    do_gprofiler(ids, out_dir, gprofiler_out_dir, background, species, name = name)

    cmd("plot_network.py -node_color community -subset_nodes "+os.path.join(out_dir,"community_ids.txt")+" -out_dir "+out_dir+" -graph "+os.path.join(os.path.dirname(os.path.dirname(out_dir)),"large_comps.graphpkl")+" -no_default -dont_save")
    

    return (temp_aov_f, temp_aov_p, z_subset, temp_gene_annotations)


def combine_community_level_global_stats(out_dir, 
                                         com_names,
                                         f,
                                         p,
                                         p_correct):
    output = [['community_names', "F_statistic","nominal_p","BH_corrected_p"]]
    for i in range(len(com_names)):
        output.append([com_names[i],
                       f[i],
                       p[i],
                       p_correct[i]])
    write_table(output,os.path.join(out_dir,'global_statistics.tsv'))
    return



def make_pr_dict(community_table):
    pr_dict = {}
    ## this table has a header, so start at 1
    for i in range(1,community_table.shape[0]):
        pr_dict[community_table[i,0]] = float(community_table[i,2])
    return(pr_dict)


def do_community_level_analyses(z_array, 
                                z_array_header,
                                community_file, 
                                id_list, ## this is for the z-score table
                                id_hash, ## for z-score table
                                out_dir,
                                species,
                                symbol_dict,
                                def_dict,
                                module_size_cutoff = 15):

    ## first go through getting all of the modules & figure out how big they are
    community_table = np.array(read_table(community_file))
    pr_dict = make_pr_dict(community_table)

    ## catelogue all of the communities & their members
    all_communities = set(community_table[1:,1].tolist())
    community_dict = {com:[] for com in all_communities}
    for i in range(1,community_table.shape[0]):
        temp_com = community_table[i,1]
        temp_com_list = community_dict[temp_com]
        temp_com_list.append(community_table[i,0])
        community_dict[temp_com] = temp_com_list

    ## get the final list of all the communities to include in the actual analysis
    final_analysis_coms = []
    for com in all_communities:
        if len(community_dict[com]) >= module_size_cutoff:
            final_analysis_coms.append(com)

    ## catelogue all of the genes included for the appropriate background in doing pathway analysis
    all_genes_for_gprofiler_bg = []
    for com in final_analysis_coms:
        all_genes_for_gprofiler_bg += community_dict[com]

    ## now go through each module & run the analyses
    out_dir = process_dir(out_dir)
    gprofiler_out_dir = process_dir(os.path.join(out_dir,'gprofiler'))
    stats_f = []
    stats_p = []
    z_subset_lists = []
    community_gene_annotations = []
    com_out_dir_dict = {}
    for com in final_analysis_coms:
        temp_out_dir = process_dir(os.path.join(out_dir,com))
        com_out_dir_dict[com] = temp_out_dir
        print('\tworking on',com,len(community_dict[com]))
        temp_stats_results = analyze_subset(community_dict[com], 
                                            z_array,
                                            z_array_header,
                                            id_list,
                                            id_hash, 
                                            temp_out_dir,
                                            gprofiler_out_dir,
                                            species,
                                            symbol_dict,
                                            def_dict,
                                            background = all_genes_for_gprofiler_bg,
                                            name = com,
                                            pr_dict = pr_dict)
        stats_f.append(temp_stats_results[0])
        stats_p.append(temp_stats_results[1])
        z_subset_lists.append(temp_stats_results[2])
        community_gene_annotations.append(temp_stats_results[3])
    ## correct for multipel comparisons
    stats_p_correct = correct_pvalues_for_multiple_testing(stats_p)
    combine_community_level_global_stats(out_dir, 
                                         final_analysis_coms,
                                         stats_f,
                                         stats_p,
                                         stats_p_correct)

    cmd('combine_gprofiler_results.py -i '+gprofiler_out_dir+' -o '+out_dir)


    return


def do_module_analysis(z_score_table,
                       out_dir,
                       species = 'hsapiens',
                       symbol_def_dict = None,
                       community_file = None,
                       id_subset = None,
                       module_size_cutoff = 15,
                       name = 'community'):
    """
    Takes in either the community table & makes subdirs in the outdir for each community larger than the cutoff size
     OR 
    a subset of ids & plots the result directly in the out dir.

    """
    if (community_file == None) and (id_subset == None):
        sys.exit("need either the community table or a subset of ids to work on")
    if (community_file != None) and (id_subset != None):
        sys.exit("can only work with either a community table or an id subset")
    
    ## no matter what, we'll need to use the z-score table, so we can process it now
    z_table = np.array(read_table(z_score_table))
    z_array_header = z_table[0,1:].tolist()
    id_list = z_table[1:,0].tolist()
    id_hash = {key:value for value, key in enumerate(id_list)}
    z_array = np.array(z_table[1:,1:],dtype = np.float32)

    ## import the annotation dict
    symbol_dict, def_dict = import_dict(symbol_def_dict)

    ## if we are doing the full community analysis
    if (community_file != None) and (id_subset == None):
        print("doing community analysis")
        do_community_level_analyses(z_array, 
                                    z_array_header,
                                    community_file, 
                                    id_list, ## this is for the z-score table
                                    id_hash, ## for z-score table
                                    out_dir,
                                    species,
                                    symbol_dict,
                                    def_dict,
                                    module_size_cutoff = module_size_cutoff)

    ## if there is just a subset of genes that we want to work with
    if (community_file == None) and (id_subset != None):
        print("doing enrichment analysis on your defined gene-set")
        ## read it in
        subset_ids = read_file(id_subset,'lines')
        analyze_subset(subset_ids, 
                        z_array,
                        z_array_header,
                        id_list,
                        id_hash, 
                        out_dir,
                        out_dir,
                        species,
                        symbol_dict, def_dict,
                        name = name)
    return



if __name__=="__main__":
    args = args = parser.parse_args()
    do_module_analysis(args.z_score_table, 
                       args.out_dir,
                       species = args.species,
                       community_file = args.community_table,
                       id_subset = args.id_subset,
                       symbol_def_dict = args.symbol_def_dict,
                       module_size_cutoff = args.module_size_cutoff,
                       name = args.name)
