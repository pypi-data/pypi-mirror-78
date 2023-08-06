#!/usr/bin/env python3
##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
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
    print('\n',in_message)
    time.sleep(.25)
    #return()
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)



##############################################################



###############################################################
###############################################################

def main(args):
    ##################################################################
    ##################################################################
    ###################### clustering ################################
    ##################################################################
    ##################################################################
    args.infile = os.path.realpath(args.infile)

    temp_dir = get_file_path(args.infile)
    all_calls = [' '.join(sys.argv)]
    ##################################################################
    def do_the_clustering(temp_dir, args, out_adj_pos, all_calls, cor_stats_file=None, neg_cor_cutoff = 1):
        #global args, out_adj_pos, all_calls
        print('performing clustering')
        ## if we're doing the clustering build up the string for the command line

        if args.do_dispersion:
            if not os.path.isdir(temp_dir+'/sample_clustering_and_summary'):
                cmd('mkdir '+temp_dir+'/sample_clustering_and_summary')
            dispersion_str = 'pyminer_get_dispersion.py -i '+args.infile
            dispersion_str += ' -out_dir '+temp_dir+'/sample_clustering_and_summary/dispersion/'
            if args.h5py:
                dispersion_str += ' -hdf5 '
                dispersion_str += ' -ID_list '+args.ID_list
            all_calls.append(dispersion_str)
            cmd(dispersion_str)

        cluster_string = 'clustering.py -i '+args.infile+' -species '+args.species
        if args.sc_clust:
            cluster_string += ' -sc_clust '
            cluster_string += ' -neg_cor_count_clust '+str(temp+'/sum_neg_cor.txt')
        if args.pre_determined_sample_k!=None:
            cluster_string += ' -sample_k_known '+str(args.pre_determined_sample_k)
        cluster_string += ' -sample_cluster_iter '+str(args.sample_cluster_iter)
        if args.var_norm_for_clust:
            cluster_string += ' -var_norm '
        if args.neg_cor_clust and not args.sc_clust:
            ### this is broken...
            ## need to figure this out...
            cluster_string += ' -neg_cor_clust '+str(cor_stats_file)
            cluster_string += ' -neg_cor_cutoff '+str(neg_cor_cutoff)
            cluster_string += ' -first_neg_neighbor '
            cluster_string += ' -pos_adj_list '+out_adj_pos
        if not args.spearman_clust:
            cluster_string += ' -no_spearman_clust '
            
        if args.ap_clust:
            cluster_string += ' -ap '
        if args.louvain_clust:
            cluster_string += ' -louvain_clust '
        if args.h5py:
            cluster_string += ' -hdf5 '
            if args.ID_list == None:
                sys.exit('for hdf5, we need the ID_list argument')
            else:
                cluster_string += ' -ID_list '+args.ID_list
            if args.columns == None:
                sys.exit('for hdf5, we need the ID_list argument')
            else:
                cluster_string += ' -columns '+args.columns

        if args.merge:
            cluster_string += ' -merge '

        if args.do_dispersion:
            cluster_string += " -clust_on_genes "+temp_dir+'/sample_clustering_and_summary/dispersion/locally_overdispersed_boolean_table.txt'

        if args.cluster_on_genes!=None:
            cluster_string += " -clust_on_genes "+args.cluster_on_genes

        if args.leave_mito_ribo:
            cluster_string += " -leave_mito_ribo "

        cluster_string += ' -rand_seed '+str(args.rand_seed)
        if args.manual_sample_groups!=None:
            cluster_string += ' -manual_sample_groups '+args.manual_sample_groups
        cluster_string += ' -block_size '+str(args.block_size)
        all_calls.append(cluster_string)
        cmd(cluster_string)


    ##################################################################


    if args.h5py:
        do_h5_py=True
        import h5py
        if args.ID_list==None:
        	sys.exit("\nwhen using the hdf5 format, you must\nsupply the -ID_list as another argument")
        title = ''
    else:
        do_h5_py=False


    temp=str(args.infile).split('/')
    temp=('/').join(temp[:-1])

    if args.ID_list!=None:
        ID_list_path=args.ID_list
        IDlist = read_file(ID_list_path,'lines')
        make_file('\n'.join(IDlist),temp+'/ID_list.txt')
    else:
        IDlist=[]
        first = True
        for line in fileinput.input(args.infile):
            if first:
                first = False
                pass
            else:
                temp_line = line.split('\t')
                IDlist.append(temp_line[0])
        make_file('\n'.join(IDlist),temp+'/ID_list.txt')


    ID_hash={gene:i for i, gene in enumerate(IDlist)}
    id_file_name = temp+'/ID_list.txt'
    ###########################################################################
    ###########################################################################
    ################### call all of the other scripts #########################
    ###########################################################################
    ###########################################################################

    ################################################
    ## get gene annotations
    annotation_prefix = temp+'/annotations'
    annotation_call = 'pyminer_gprofiler_converter.py -i '+id_file_name
    annotation_call += ' -o '+annotation_prefix
    annotation_call += ' -s '+args.species
    annotation_call += ' -annotations'
    cmd(annotation_call)

    ## get the human orthologues if we don't have human ids
    if args.species != 'hsapiens':
        orthologue_prefix = temp+'/human_orthologues'
        convert_call = 'pyminer_gprofiler_converter.py -i '+id_file_name
        convert_call += ' -o '+orthologue_prefix
        convert_call += ' -s '+args.species
        cmd(convert_call)

    ################################################
    ## 3: build the network(s)
    ## if we're doing a single network:
    if args.rho_cutoff!=None:
        if args.rho_cutoff > 1.0 or args.rho_cutoff<0:
            sys.exit('please use a rho cutoff between zero and one. We recommend not using this argument at all to allow for the built in False Positive Rate (FPR) algorithm to take over. If using scRNAseq, try something in the range of 0.25-0.35. For bulk RNAseq, try something closer to 0.70 - 0.90.')

    out_adj = temp+'/adj_list_rho.tsv'
    adj_call_string = 'mat_to_adj_list.py -i '+args.infile+' -o '+out_adj+' -id_list '+temp+'/ID_list.txt '
    if args.rho_cutoff!=None:
        adj_call_string+=' -rho '+str(args.rho_cutoff)
    if args.h5py:
        adj_call_string += ' -hdf5 '
    adj_call_string += ' -block_size '+str(args.block_size)
    if args.sc_clust:
        adj_call_string += ' -sc_clust '
    if args.prop:
        adj_call_string += ' -prop '
    adj_call_string += " -FPR_multiple "+str(args.FPR_multiple)
    adj_call_string += ' -rand_seed '+str(args.rand_seed)
    all_calls.append(adj_call_string)
    cmd(adj_call_string)

    #######################
    ## 3.5: subset the positive/negative correlations

    pos_neg_count = np.zeros((len(IDlist),2))

    out_adj_pos = out_adj[:-4]+'_dedup_pos.tsv'
    cmd('rm '+out_adj_pos)
    pos_f_out=open(out_adj_pos,'a')

    out_adj_neg = out_adj[:-4]+'_dedup_neg.tsv'
    cmd('rm '+out_adj_neg)
    neg_f_out=open(out_adj_neg,'a')

    counter = 0
    first = True
    for line in fileinput.input(out_adj[:-4]+'_dedup.tsv'):
        if first:
            print('reading ',out_adj[:-4]+'_dedup.tsv')
            #print(float(temp_line[-1]))
            pos_f_out.write(line)
            neg_f_out.write(line)
            first = False
        else:
            temp_line = strip_split(line)
            #print(float(temp_line[-1]))
            try:
                float(temp_line[-1])
            except:
                print('error at line:',counter)
                print('\t',line)
            if float(temp_line[-1])>0:
                pos_f_out.write(line)
                pos_neg_count[ID_hash[temp_line[0]]][0]+=1
                pos_neg_count[ID_hash[temp_line[1]]][0]+=1
            else:
                neg_f_out.write(line)
                pos_neg_count[ID_hash[temp_line[0]]][1]+=1
                pos_neg_count[ID_hash[temp_line[1]]][1]+=1
        counter+=1
    pos_f_out.close()
    neg_f_out.close()

    ## log some stats about how many positive and negative relationships there are
    pos_neg_count = pos_neg_count.tolist()
    for i in range(0,len(pos_neg_count)):
        pos_neg_count[i] = [IDlist[i]] + pos_neg_count[i]

    pos_neg_count = [['ID','num_pos_cor','num_neg_cor']]+ pos_neg_count

    write_table(pos_neg_count, temp+'/positive_negative_cor_counts.txt')

    ################################################
    ## do feature selection



    ########################## clustering #############################
    if args.manual_sample_groups!=None:
        do_the_clustering(temp_dir, args, out_adj_pos, all_calls)
        args.manual_sample_groups = temp_dir+'sample_clustering_and_summary/sample_k_means_groups.txt'
    elif args.neg_cor_clust:
        do_the_clustering(temp_dir, args, out_adj_pos, all_calls,cor_stats_file=temp+'/positive_negative_cor_counts.txt', neg_cor_cutoff = args.neg_cor_cutoff)
        args.manual_sample_groups = temp_dir+'sample_clustering_and_summary/sample_k_means_groups.txt'
    else:
        ## do the clustering if it is needed
        if not args.h5py or not args.neg_cor_clust:
            if args.do_sample_clustering:
                do_the_clustering(temp_dir, args, out_adj_pos, all_calls)
                args.manual_sample_groups = temp_dir+'sample_clustering_and_summary/sample_k_means_groups.txt'
            elif args.manual_sample_groups==None:
                ## if we aren't going to be doing the clustering, we'll need to pretend that these are all from the same group
                ## to do this we'll write the sample_k_means_groups_file 
                if not args.h5py:
                    first = True
                    for temp_line in fileinput.input(args.infile):
                        if first:
                            title = np.array((temp_line.strip('\n')).split('\t'), dtype='U32')
                            first = False
                            break
                    fileinput.close()
                else:
                    title = np.array(read_file(args.columns,'lines'))
                ##############################################
                sample_names = title[1:]
                sample_k_table = [0]*(len(sample_names))
                sample_k_table = list(zip(sample_names, [0]*len(sample_names)))

                ##make the manual sample groups true, and make the file
                out_sample_group_table = np.array(sample_k_table)
                cmd('mkdir '+temp_dir+'sample_clustering_and_summary')
                write_table(out_sample_group_table,temp_dir+'sample_clustering_and_summary/sample_k_means_groups.txt')

                ## after we finish the clustering (or not), re-direct the manual sample groups to the 
                ## output sample group identity file
                args.manual_sample_groups = temp_dir+'sample_clustering_and_summary/sample_k_means_groups.txt'




        if args.manual_sample_groups!=None:
            manual_sample_groups_file = args.manual_sample_groups
        #    manual_sample_groups = read_table(manual_sample_groups_file)
            sample_k_table = read_table(manual_sample_groups_file)
            manual_sample_groups = True
            sample_cluster_ids = []
            for i in range(0,len(sample_k_table)):
                
                ## THIS IS IMPORTANT
                ## here we assume that the samples are all listed in the same order as in '-infile'
                ## we also assume that the group indexing starts at 0
                sample_cluster_ids.append(sample_k_table[i][1])
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
        else:
            args.manual_sample_groups = False

        import random
        random.seed(args.rand_seed)
        np.random.seed(args.rand_seed)

        many_variables = False
        very_big_file = False


        if '-big_file_do_z' in sys.argv:
            big_file_do_z=True
        else:
            big_file_do_z=False

    if args.sample_cluster_only:
        sys.exit('done with clustering')

    ################################################
    ## : enrichment & significance
    if True:#not args.h5py:
        stats_call = 'get_stats.py -i '+args.infile+' -sample_groups '+args.manual_sample_groups+' -FDR '+str(args.FDR_cutoff)+' -Zscore '+str(args.zscore_cutoff)
        if args.species != None:
            stats_call += str(' -s '+args.species)
        if args.h5py:
            stats_call += ' -hdf5 '
            if args.ID_list == None:
                sys.exit('for hdf5, we need the ID_list argument')
            else:
                stats_call += ' -ID_list '+args.ID_list
            if args.columns == None:
                sys.exit('for hdf5, we need the ID_list argument')
            else:
                stats_call += ' -columns '+args.columns
        if args.processes is not None:
            stats_call += ' -processes '+str(args.processes)
        all_calls.append(stats_call)
        cmd(stats_call)
        if not os.path.isdir(temp+"/sample_clustering_and_summary/significance/"):
            cmd("mkdir "+temp+"/sample_clustering_and_summary/significance/")
        make_file(stats_call,temp+"/sample_clustering_and_summary/significance/stats_call.txt")

    ################################################
    ## combine the gprofiler results
    if os.path.isdir(temp+"/sample_clustering_and_summary/significance/gprofiler"):
        combine_gprofiler_str = "combine_gprofiler_results.py -i "+temp+"/sample_clustering_and_summary/significance/gprofiler/"
        combine_gprofiler_str +=" -o "+temp+"/sample_clustering_and_summary/significance/"
        all_calls.append(combine_gprofiler_str)
        cmd(combine_gprofiler_str)



    ################################################
    ## get and plot highly expressed marker genes
    group_means_file = temp+"/sample_clustering_and_summary/"+"k_group_means.txt"
    aov_file = temp+"/sample_clustering_and_summary/significance/"+"groups_1way_anova_results.txt"
    annotation_dict = temp+"/annotations.pkl"
    high_marker_out_dir = temp+"/sample_clustering_and_summary/significance/high_markers/"
    cluster_pkl = temp+"/sample_clustering_and_summary/clustering_plots.pkl"

    if os.path.isdir(temp+"/sample_clustering_and_summary/significance/"):
        cmd("mkdir "+high_marker_out_dir)
        get_markers_call = 'get_high_marker_genes.py -m '+group_means_file
        get_markers_call += ' -sig '+aov_file
        get_markers_call += ' -out '+high_marker_out_dir
        get_markers_call += ' -annotation_dict '+annotation_dict
        cmd(get_markers_call)
        all_calls.append(get_markers_call)

        plot_subset_file = high_marker_out_dir+"subset_input.txt"
        marker_plot_call = "plot_gene_subset.py -i "+args.infile+" -noi "+plot_subset_file
        marker_plot_call += " -heatmap "
        marker_plot_call += " -ids "+id_file_name
        marker_plot_call += " -o "+high_marker_out_dir
        marker_plot_call += " -cluster_pkl "+cluster_pkl
        if args.h5py:
            marker_plot_call += ' -hdf5 '
            if args.ID_list == None:
                sys.exit('for hdf5, we need the ID_list argument')
            else:
                marker_plot_call += ' -ID_list '+args.ID_list
            if args.columns == None:
                sys.exit('for hdf5, we need the ID_list argument')
            else:
                marker_plot_call += ' -columns '+args.columns
        cmd(marker_plot_call)
        all_calls.append(marker_plot_call)

    ################################################
    ## 4: network analysis
    ## check if the enrichment file exists
    #cmd('mkdir '+temp+'/graphs')
    cmd('mkdir '+temp+'/pos_cor_graphs')

    full_network_plot_call = "plot_network.py -id_list "+temp+'/ID_list.txt'+" -adj "+out_adj+" -plot_all  -out_dir "+temp+"/graphs"
    pos_cor_network_call = "plot_network.py -id_list "+temp+'/ID_list.txt'+" -adj "+out_adj_pos+" -plot_all  -out_dir "+temp+"/pos_cor_graphs"

    if os.path.isfile(temp+"/sample_clustering_and_summary/k_group_enrichment.txt"):
        full_network_plot_call+=" -node_attrs "+temp+"/sample_clustering_and_summary/k_group_enrichment.txt -range "+str(args.zscore_cutoff)+",-"+str(args.zscore_cutoff)
        pos_cor_network_call+=" -node_attrs "+temp+"/sample_clustering_and_summary/k_group_enrichment.txt -range "+str(args.zscore_cutoff)+",-"+str(args.zscore_cutoff)

    #cmd(full_network_plot_call)
    all_calls.append(pos_cor_network_call)
    cmd(pos_cor_network_call)



    ################################################
    ## analyze genes of interest

    def process_noi(nodes_of_interest):
        noi_table=[]
        for i in range(0,len(nodes_of_interest)):
            if '\t' in nodes_of_interest[i]:
                noi_table.append(nodes_of_interest[i].split('\t'))
            elif '::' in nodes_of_interest[i]:
                noi_table.append(nodes_of_interest[i].split('::'))
            else:
                noi_table.append([nodes_of_interest[i],nodes_of_interest[i]])

        # print(noi_table)
        ## also make the ailias look-up dictionary
        alias_dict={}
        ## make the string that would be passed through to command line if needed
        pass_through_arg =""
        ## and the final list of nodes in the dataset
        final_nodes = []
        for i in range(0,len(noi_table)):
            # print(i)
            # print(noi_table[i])
            alias_dict[noi_table[i][0]]=noi_table[i][1]
            pass_through_arg+=","+noi_table[i][0]+'::'+noi_table[i][1]
            final_nodes.append(noi_table[i][0])
        ## remove the leading comma
        pass_through_arg=pass_through_arg[1:]

        return(alias_dict, pass_through_arg, final_nodes)



    if args.noi != None:
        ## first check if it's a path
        if os.path.isfile(args.noi):
            noi_list = read_file(args.noi,'lines')
        else:
            ## check if it's a comma separated list of ids
            temp_nodes_of_interest = args.noi.split(',')

        alias_dict, pass_through_arg, temp_nodes_of_interest = process_noi(noi_list)
        
        print(temp_nodes_of_interest)
        

        final_noi_list = []
        for noi in temp_nodes_of_interest:
            if noi in IDlist:
                final_noi_list.append(str(noi))
            else:
                print("couldn't find "+str(noi)+" in the IDs...")
        print('getting degrees of separation for:')
        for noi in final_noi_list:
            print('\t',noi)

        #print(final_noi_list)
        

        ## now run the call
        noi_call = "get_degrees_of_separation_from_adjacency_list.py -adj "+out_adj_pos
        noi_call += " -ids "+temp+"/ID_list.txt"
        noi_call += " -noi "+','.join(final_noi_list)
        noi_call += " -out_dir "+temp+'/genes_of_interest'
        cmd('mkdir '+temp+'/genes_of_interest')
        all_calls.append(noi_call)
        cmd(noi_call)
        

        ## if the plots file is there plot the color over the positions
        plot_subset_call = 'plot_gene_subset.py -i '+args.infile
        plot_subset_call += " -out_dir "+temp+'/genes_of_interest'
        plot_subset_call += " -noi "+pass_through_arg
        plot_subset_call += " -id_list "+temp+'/ID_list.txt'
        plot_subset_call += " -cluster_pkl "+temp+"/sample_clustering_and_summary/clustering_plots.pkl"
        if args.h5py:
            plot_subset_call += ' -hdf5 '
            plot_subset_call += ' -cols '+temp+'/column_IDs.txt'
        all_calls.append(plot_subset_call)
        cmd(plot_subset_call)





    #################################################
    if not args.no_cell_signals:
        cmd('mkdir '+temp+'/autocrine_paracrine_signaling/')
        cell_signals_call = "cell_signals.py -i "+temp+'/sample_clustering_and_summary/significance/significant_and_enriched_boolean_table.txt '
        cell_signals_call += ' -o '+temp+'/autocrine_paracrine_signaling/'
        cell_signals_call += ' -species '+args.species
        if args.string_db_dir[-1]!='/':
            args.string_db_dir+='/'
        cell_signals_call += ' -sdb '+args.string_db_dir
        all_calls.append(cell_signals_call)
        cmd(cell_signals_call)
        if os.path.isfile(temp+'/autocrine_paracrine_signaling/all_cell_type_specific_interactions_gprofiler.txt'):
            combine_gprofiler2_str="combine_gprofiler_results.py -i "+temp+'/autocrine_paracrine_signaling/all_cell_type_specific_interactions_gprofiler.txt'
            combine_gprofiler2_str+=' -o '+temp+'/autocrine_paracrine_signaling/'
            all_calls.append(combine_gprofiler2_str)
            cmd(combine_gprofiler2_str)


    #################################################
    if os.path.isfile(temp+'/pos_cor_graphs/communities.txt'):
        community_analysis = "pyminer_analyze_communities.py -community_table "+temp+"/pos_cor_graphs/communities.txt -out_dir "+temp+"/pos_cor_graphs/community_analysis -z_score_table "+temp+"/sample_clustering_and_summary/k_group_enrichment.txt -species "+args.species
        community_analysis += ' -ad '+temp+'/annotations.pkl'
        cmd(community_analysis)


    ################################################
    ## summarize the results via the website generator
    website_call = "make_website.py -i "+temp_dir
    all_calls.append(website_call)


    make_file('\n'.join(all_calls),temp+'/PyMINEr_call_log.txt')


    cmd(website_call, com=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()


    ## global arguments
    parser.add_argument(
        '-infile','-in','-i','-input',
        dest='infile',
        type=str)

    parser.add_argument(
        "-hdf5",'-h5py',
        help='if the "-infile" is an hdf5 file whose main array name is "infile". This argument also requires "-ID_list" as a separate argument.',
        dest='h5py',
        action='store_true',
        default = False)
    parser.add_argument(
        '-ID_list','-IDs','-ids',
        help = "A new line delimited file with no title line that contains the IDs associated with each row, in the correct order",
        dest='ID_list',
        type=str)
    parser.add_argument(
        '-columns','-cols',
        help = "A new line delimited file with no title line that contains the sample IDs associated with each column, in the correct order",
        dest='columns',
        type=str)

    parser.add_argument("-rand_seed",
        type = int,
        default = 12345)


    ########################################################
    ## define which steps to do (ie: sample clustering, build networks, etc)
    parser.add_argument(
        "-networks_only",'-net_only',
        help='only find the networks and write adjacency list(s)',
        dest='mineOnly',
        action='store_true',
        default = False)

    parser.add_argument(
        "-sample_cluster_only",
        help='only do PyMINEr clustering',
        dest='sample_cluster_only',
        action='store_true',
        default = False)

    parser.add_argument(
        "-no_sample_cluster","-no_sample_clust",
        help='skip the sample clustering',
        dest='do_sample_clustering',
        action='store_false',
        default = True)

    parser.add_argument(
        "-cluster_on_all",
        help='cluster on all variables, without looking at dispersion',
        dest='do_dispersion',
        action='store_false',
        default = True)


    parser.add_argument(
        "-cluster_on_genes","-clust_on_genes","-clust_genes",
        help='If there is a specific set of genes you want to cluster on, supply the gene ids in this text file.'
        )

    parser.add_argument(
        "-leave_mito_ribo",
        help='If we should leave the mitochondrial and ribosomal genes for clustering',
        action='store_true',
        default = False)



    # parser.add_argument(
    #     "-neg_cor_cutoff",
    #     help='for negative correlation based clustering, what should the cutoff be? (default = 20)',
    #     type = int,
    #     default = 15)

    parser.add_argument(
        "-beta_test",
        help='set the paramaters for beta_testing',
        dest = "sc_clust",
        action='store_true',
        default = False)


    ########################################################
    ## sample clustering options


    parser.add_argument(
        "-sample_k_clusters_known",'-sample_k_known',
        help='if you know how many groups there should be',
        dest = 'pre_determined_sample_k',
        type = int)

    parser.add_argument(
        "-sample_cluster_iter","-clust_iter",
        help='How many iterations of clustering should we do. This can take some time, but higher iterations will give better results. Default = 10',
        dest = 'sample_cluster_iter',
        type = int,
        default = 10)
    parser.add_argument(
        "-var_norm_for_clust","-var_norm",
        help='normalize the variables for sample clustering',
        dest='var_norm_for_clust',
        action='store_true',
        default = True)
    parser.add_argument(
        "-no_var_norm",
        help='do not normalize the variables for sample clustering',
        dest='var_norm_for_clust',
        action='store_false',
        default = True)
    parser.add_argument(
        "-neg_cor_clust",
        help='cluster based on variables with negative correlations',
        action='store_true',
        default = False)
    parser.add_argument(
        "-no_spearman_clust",
        help='do not use the spearman similarity matrix to do the clustering. The default is to use the symetric Spearman correlation matrix of all samples against each other.',
        dest='spearman_clust',
        action='store_false',
        default = True)
    parser.add_argument(
        "-ap_clust", '-ap',
        help='if you want to use affinity propagation clustering',
        action='store_true',
        default = False)
    parser.add_argument(
        "-louvain_clust",
        help='if you want to use louvain clustering',
        action='store_true',
        default = False)
    parser.add_argument(
        "-merge", 
        help='if you want to perform cluster merger analysis',
        action='store_true',
        default = False)


    parser.add_argument(
        "-manual_sample_groups",
        help='if you know how which samples belong to which groups, feed in a file that has the samples in the first column, and their group number (index starting at 0), in the second column. The IDs must be in the same order as in the infile too.',
        dest = 'manual_sample_groups',
        type = str)

    parser.add_argument(
        "-species",
        help='species to use for gProfiler analysis',
        dest = 'species',
        default = 'hsapiens',
        type = str)

    ########################################################
    ## enrichment options
    parser.add_argument(
        "-anova_FDR_cutoff","-FDR_cutoff",
        help='The Benjamini Hochberg corrected FDR value cutoff for calling a variable significantly different between groups.',
        dest = 'FDR_cutoff',
        type = float,
        default = 0.05)

    parser.add_argument(
        "-zscore_cutoff",
        help='The Z-score cutoff for calling a variable enriched in a given group.',
        dest = 'zscore_cutoff',
        type = float,
        default = 2.0)

    parser.add_argument(
        "-processes",
        help='The number of processes for running the stats',
        dest = 'processes',
        type = int,
        default = None)

    ########################################################
    ## network detection options
    parser.add_argument("-spearman_only",
        dest = "spearman_only",
        action = 'store_true',
        default = False)

    parser.add_argument("-rho_cutoff",'-rho',
        dest = "rho_cutoff",
        help = "Suggested to leave this blank, but you can provide your own cutoff instead of allowing PyMINEr to set it for you. This is the absolute value of the spearman rho to use for a cutoff. If using scRNAseq, try something in the range of 0.25-0.35. For bulk RNAseq, try something closer to 0.70 - 0.90.",
        type = float)


    parser.add_argument("-prop","-proportaionality",
        action = 'store_true',
        default = False, 
        help="if you only want to use proportionality instead of Spearman")


    parser.add_argument("-block_size",
        help = 'how many variables will be used at once for correlation analyzis; this helps keep memory requirements down and prevents a segmentation fault memory error',
         type = int,
         default = 5000)

    parser.add_argument(
        "-FPR_multiple",'-mult',
        help="the multiple to use for FPR based anti-correlation feature selection. Only use this if you really know what you're doing.",
        type = int,
        default = 15)


    ########################################################
    ## if you already have a(n) adjacency list(s)
    # parser.add_argument(
    #   '-network1','-adj1','-adj_list1','-network','-net1','-in_mine1',
    #   help = "if you already have an adjacency list, we can use that instead of building up a network from scratch.",
    #   dest='in_mine1',
    #   type=str)
    # parser.add_argument(
    #   '-network2','-adj2','-adj_list2','-net2','-in_mine2',
    #   help = "if you have a second adjacency list for a network comparison, pass the path to this option.",
    #   dest='in_mine2',
    #   type=str)
    # parser.add_argument(
    #   '-name1',
    #   dest='control_name',
    #   default = 'network1',
    #   type=str)
    # parser.add_argument(
    #   '-name2',
    #   dest='disease',
    #   default = 'network2',
    #   type=str)

    ###################################################
    ## for getting degree of separation from genes of iterest
    parser.add_argument(
        "-genes_of_interest",'-nodes_of_interest','-goi','-noi',
        help="if you have guesses about genes of interest a priori, we'll get the degree of separation from those genes in the primary analysis. This can either be a file with genes each on a new line, or it can be a comma separated list of genes.",
        dest = "noi",
        type = str)

    ###################################################
    ## cell signals options
    parser.add_argument(
        "-no_cell_signals",
        help="if you don't want to do the autocrine paracrine signaling network prediction",
        action = 'store_true',
        default = False)
    parser.add_argument(
        "-string_db_dir",'-stringdb_dir','-sdb',
        help="If the stringDB directory isn't in /usr/local/lib/cell_signals/, you'll have to tell PyMINEr where to look. This is often the case if you don't have a global (sudo) install of PyMINEr.",
        dest = "string_db_dir",
        default = '/usr/local/lib/cell_signals/',
        type = str)

    ############################################
    ## aesthetics options
    parser.add_argument(
        "-dpi",
        help='dots per inch for the output figures',
        dest = "dpi",
        type = int,
        default = 360)

    parser.add_argument(
        "-verbose",
        help='prints out some extra lines; this is primarily for troubleshooting',
        dest='verbose',
        action='store_true',
        default = False)
    args = parser.parse_args()

    if args.cluster_on_genes:
        #args.leave_mito_ribo = True
        args.do_dispersion = False

    if args.neg_cor_clust or args.sc_clust:
        args.do_dispersion = False

    #print(dir(args))
    ##################################################################
    # if args.dividing_col != 0:
    #     single_network=False
    #     mannwhit=True
    # else:
    #     single_network=True
    #     mannwhit=False

    ###################
    # log_fold=True
    # log_expression=False
    # rainbow=True
    # no_express=False
    # express_only=False
    # do_spearman = True
    # co_regulatory_network=True

    # ## page rank options that won't change
    # page_ranks=True
    # pr_iters=50 ## this is a totally arbitrary default
    # pr_alpha=0.85
    # weighted_analysis=True

    # ## clustering options that won't change
    # cluster_prob=False
    # first_prob = True

    # if args.manual_sample_groups!=None:
    #     args.do_sample_clustering=False
    main(args)
