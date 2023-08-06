#!/home/scott/anaconda3.7/bin/python3
##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import pandas as pd
from scipy.stats import rankdata
from matplotlib.colors import LinearSegmentedColormap
try:
    from pyminer.common_functions import *
except:
    from common_functions import *
# ##############################################################
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



# ##############################################################












import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
	'-infile','-in','-i','-input',
	dest='infile',
	type=str)

parser.add_argument("-nodes_of_interest", "-noi","-nodes",
    help="the nodes that you want to subset and get their degrees of separation from")

parser.add_argument("-out_dir", "-o", "-out",
    help="the directory to place the output file(s)")

parser.add_argument("-cluster_pkl", 
    help="the file created by clustering.py that stores the plots")

parser.add_argument(
    '-no_cluster','-no_clust',
    help = "if you don't want the heatmap to cluster the genes together, but rather, just want it to be in the order that you input them.",
    dest = "cluster",
    default = True,
    action = 'store_false')
parser.add_argument(
    '-only_heatmap','-heatmap',
    help = "if you only want the heatmap",
    dest = "only_heatmap",
    default = False,
    action = 'store_true')
parser.add_argument(
    '-no_rank',
    help = "if you don't want the heatmap rank transformed",
    default = False,
    action = 'store_true')

## hdf5 options
parser.add_argument(
    '-hdf5',
    help = 'The input file is an HDF5 file',
    default = False,
    action = 'store_true')

parser.add_argument(
    "-ID_list","-ids","-id_list",
    help = 'If we are using an hdf5 file, give the row-wise IDs in this new line delimeted file',
    type = str)

parser.add_argument(
    "-columns","-cols",
    help = 'If we are using an hdf5 file, give the column-wise IDs in this new line delimeted file',
    type = str)




args = parser.parse_args()
##############################################################

def ids_to_idxs(in_ids):
    global ID_hash
    temp_index_list = [ID_hash[i] for i in in_ids]
    return(temp_index_list)


def process_noi(nodes_of_interest):
    #check if there are aliases
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
##########################
######################################


def linear_normalize(vect):
    vect = vect - min(vect)
    vect = vect/max(vect)
    return(vect)


def vect_to_color(vect,style='hot'):
    vect = linear_normalize(vect)
    cmap = cm.get_cmap(name=style)
    cmap = LinearSegmentedColormap.from_list("WhRd", ((1,1,1),(1,0,0)), N=256)
    return(cmap(vect))

def draw_plot(plot,exemplars,color_vect, colorize_by_gene = None):
    global all_group_ids, plt, full_expression, ID_list, ID_hash
    plt.clf()

    ## get the colorized vector if need be
    if colorize_by_gene!=None:
        ## fix for entrez..
        try:
            float(colorize_by_gene)
        except:
            colorize_by_gene = colorize_by_gene
        else:
            colorize_by_gene = str(float(colorize_by_gene))
        expression_vect = full_expression[ID_hash[colorize_by_gene],:]
        expression_vect = rankdata(expression_vect,method='min')
        colorized_vect = vect_to_color(expression_vect,style='Reds')

    if colorize_by_gene!=None:
        plt.scatter(plot["x"],plot["y"],
                edgecolor='k',#plot["c"],
                facecolor=colorized_vect,
                s=10,
                linewidths=0.075)
    else:
        plt.scatter(plot["x"],plot["y"],
                color=plot["c"],
                s=10,
                linewidths=0.075)
    plt.xlabel(plot['xlab'])
    plt.ylabel(plot['ylab'])




def lin_norm_rows(in_mat,min_range=0,max_range=1):
    in_mat = np.transpose(np.array(in_mat))
    in_mat = in_mat - np.min(in_mat, axis = 0)
    in_mat = in_mat / np.max(in_mat, axis = 0)
    in_mat[np.isnan(in_mat)]=0
    return(np.transpose(in_mat))


def names_to_alias(names):
    global alias_dict
    aliases=[]
    for i in range(0,len(names)):
        ## fix for entrez..
        try:
            float(names[i])
        except:
            temp_id = names[i]
        else:
            temp_id = str(int(float(names[i])))
        aliases.append(alias_dict[temp_id])
    return(aliases)



#######################################

if args.nodes_of_interest != None:
	## check if it's a file
	if os.path.isfile(args.nodes_of_interest):
		nodes_of_interest = read_file(args.nodes_of_interest,'lines')
	else:
		## check if it's a comma separated list of ids
		nodes_of_interest = args.nodes_of_interest.split(',')
		# nodes_of_interest = args.nodes_of_interest
		# nodes_of_interest = nodes_of_interest.split(',')
else:
    nodes_of_interest = None



alias_dict, pass_through_arg, temp_nodes_of_interest = process_noi(nodes_of_interest)
print(pass_through_arg)


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
	sys.exit('-out_dir is a required argument')

print(ID_list[:5])
## double check that the ids are found
nodes_of_interest=[]
for i in range(0,len(temp_nodes_of_interest)):
    ## fix for entrez..
    try:
        float(temp_nodes_of_interest[i])
    except:
        temp_id = temp_nodes_of_interest[i]
    else:
        temp_id = str(float(temp_nodes_of_interest[i]))
    if temp_id in ID_hash:
        nodes_of_interest.append(temp_id)
    else:
        print("couldn't find",temp_id)

if len(nodes_of_interest)==0:
    sys.exit("couldn't find any of the desired genes")

## import expression data
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

ID_list = row_names[:]
ID_hash = {name:idx for idx,name  in enumerate(ID_list)}


############################################




# single_cell_type_table = read_table(args.single_groups,num_type=int)
# single_group_lists = reorganize_single_type_table(single_cell_type_table)

#############################################



## read in the plots
cluster_result_dict = import_dict(args.cluster_pkl)
print(list(cluster_result_dict.keys()))

linear_groups = cluster_result_dict['linear_groups']
sample_k_lists = cluster_result_dict["sample_k_lists"]


##################################
args.out_dir = process_dir(args.out_dir)

# if args.out_dir[:-1]!= '/':
# 	args.out_dir+='/'
##################################


## plot the heatmap
group_reordering_vector=np.array(cluster_result_dict['group_reordering_vector'])
reordered_colors=np.array(cluster_result_dict['reordered_colors'])


#######################################################
## get the column labels

reordered_array = list(np.array(linear_groups)[np.array(group_reordering_vector)])
#print(reordered_array)
reordered_groups = [reordered_array[0]]
#print(reordered_groups)
for i in range(1,len(reordered_array)):
	#print(int(reordered_array[i]))
	#print(reordered_groups[-1])
	if int(reordered_array[i])!=int(reordered_groups[-1]):
		reordered_groups.append(reordered_array[i])

#print(reordered_groups)

cluster_lists = sample_k_lists[:]
temp_label_lists = []
for i in range(0,len(cluster_lists)):
	temp_list = ['']*len(cluster_lists[i])
	temp_list[int(len(temp_list)/2)] = i
	temp_label_lists.append(temp_list)

heatmap_x_labels = []
for i in reordered_groups:
	heatmap_x_labels+=temp_label_lists[i]
#print(heatmap_x_labels)

#######################################################

# print(group_reordering_vector)
# print(reordered_colors)
# sys.exit()
original_order = ids_to_idxs(nodes_of_interest)
# from scipy import stats
# original_order_rank = np.array(stats.rankdata(original_order)-1,dtype=int)
# print(original_order_rank)
original_order_dict = {j:i for i,j in enumerate(original_order)}


subset_indices = sorted(original_order)
original_order_vector = []
for i in subset_indices:
    ## fix for entrez..
    try:
        float(ID_list[i])
    except:
        temp_id = ID_list[i]
    else:
        temp_id = str(int(float(ID_list[i])))
    print(i,original_order_dict[i], temp_id, alias_dict[temp_id])
    original_order_vector.append(original_order_dict[i])

new_order_dict = {i:j for i,j in enumerate(original_order_vector)}
original_order_rank=np.zeros((len(original_order_vector)),dtype=int)
for i in range(0,len(original_order_vector)):
    index = original_order_vector[i]
    original_order_rank[index]=i
original_order_rank=original_order_rank.tolist()


original_order_names = np.array(ID_list)[original_order]
subset_sorted_names = np.array(ID_list)[subset_indices]
subset_indices = np.array(subset_indices)
print(subset_indices)
if np.shape(subset_indices)[0]==0:
    sys.exit('no subset found...')
subset_array = np.zeros((subset_indices.shape[0],full_expression.shape[1]))
for i in range(subset_indices.shape[0]):
    temp_idx = subset_indices[i]
    subset_array[i,:] = np.array(full_expression[temp_idx,:])


# if not args.cluster:
#     ## put them back in the input order
#     subset_array=subset_array[original_order_rank,:]
#     subset_sorted_names = subset_sorted_names[original_order_rank]

## do the linear normalization
subset_array = lin_norm_rows(subset_array[:,group_reordering_vector])

## Z-score
# import scipy
# subset_array = scipy.stats.zscore(subset_array,axis=1)
# subset_array = lin_norm_rows(subset_array)
# ## mean center
#subset_array = subset_array - np.transpose(np.array([np.mean(subset_array,axis=1)]))

if not args.no_rank:
    from scipy.stats import rankdata
    for i in range(0,np.shape(subset_array)[0]):
        subset_array[i] = rankdata(subset_array[i,:],method='min')
else:
    ## if we're not doing rank, do Z-score
    from scipy.stats import zscore
    subset_array = zscore(subset_array, axis = 1)
    subset_array[subset_array>3] = 3
    subset_array[subset_array<-3] = -3
#subset_array = np.log2(subset_array)


name_col = np.array(names_to_alias(subset_sorted_names))
print(name_col)
name_col_df = pd.DataFrame({"name_col":name_col},index=list(range(len(subset_sorted_names))))
#subset_df = np.hstack((name_col, subset_array))
subset_df = pd.DataFrame(data=subset_array)
subset_df = pd.concat([name_col_df,subset_df],axis=1)
print(subset_df)
#subset_df = subset_df.set_index([list(range(len(subset_sorted_names))),"name_col"])
subset_df = subset_df.set_index([list(original_order_rank),"name_col"])
subset_df.columns = heatmap_x_labels
print(subset_df)

## set some stuff around if we are or are not clustering the rows
if not args.cluster:
    print(original_order_rank)
    orig_subset_df = subset_df
    #subset_df=subset_df.reindex(original_order_rank)
    subset_df = subset_df.iloc[original_order_rank,:]
    print(subset_df)
    row_cluster = False
else:
    row_cluster = True

print(subset_df)

#print(subset_df[:5,:5])

subset_sorted_aliases = names_to_alias(subset_sorted_names)
if not args.cluster:
    original_order_aliases = names_to_alias(original_order_names)
    for i in (zip(original_order_names,original_order_aliases)):
        print(i)

try_reorder=False

if args.no_rank:
    global_cmap = sns.color_palette("coolwarm", 256)
else:
    global_cmap = cm.get_cmap(name="hot")

## actually plot the heatmap finally...
## get the non-empty colnames
indices_to_plot_for_names = np.where(np.array(heatmap_x_labels)!='')[0]
#indices_to_plot_for_names = np.where(np.array(heatmap_x_labels)=='')[0]
none_indices = np.where(np.array(heatmap_x_labels)=='')[0].tolist()
#print(none_indices[:5])
plot_names = np.array(heatmap_x_labels)
plot_names[none_indices]=None
print(indices_to_plot_for_names)
xticklabels = False#[None]*len(heatmap_x_labels)
try:
    sub = sns.clustermap(subset_df,
        col_cluster = False,
        row_cluster = row_cluster,
        col_colors = reordered_colors,
        yticklabels = True,
        #xticklabels=xticklabels,
        cmap=global_cmap)
except:
    ## if it were too big to plot successfully, just do a subset
    sample = np.arange((np.shape(subset_df)[0]))
    subset_length = min([np.shape(subset_df)[0],400])
    np.random.shuffle(sample)
    sub_sample = np.sort(sample[:subset_length])
    sub = sns.clustermap(np.array(subset_df)[sub_sample,:],
        col_cluster = False,
        row_cluster = row_cluster,
        col_colors = reordered_colors,
        yticklabels = True,
        #xticklabels=xticklabels,
        cmap=global_cmap)

## this sets the heatmap labels on the x axis
sub.ax_heatmap.xaxis.set_ticks(indices_to_plot_for_names)
sub.ax_heatmap.xaxis.set_ticklabels(plot_names[indices_to_plot_for_names])

plt.setp(sub.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
plt.setp(sub.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)

# plt.tight_layout()
# plt.show()
plt.savefig(args.out_dir+'genes_of_interest_subset_heatmap.png',
    dpi=600,
    bbox_inches='tight')

if args.only_heatmap:
    sys.exit()

#sys.exit()
# ## plot the nodes of interest on the tSNE and PCAs
for noi in nodes_of_interest:
    ## fix for entrez..
    try:
        float(noi)
    except:
        noi = noi
    else:
        noi = str(int(float(noi)))
    for plot in cluster_result_dict["plots"]:
        # for k in [plot].keys():
        #     print(k)
        #     print(plot[k])
        draw_plot(cluster_result_dict["plots"][plot],cluster_result_dict["exemplar_indices"],cluster_result_dict["color_vect"],colorize_by_gene = noi)
        temp_plot_out = plot.split('/')
        temp_plot_out = temp_plot_out[-1]
        plt.savefig(args.out_dir+temp_plot_out[:-4]+'_'+alias_dict[noi]+'.png',
            dpi=600,
            bbox_inches='tight')


