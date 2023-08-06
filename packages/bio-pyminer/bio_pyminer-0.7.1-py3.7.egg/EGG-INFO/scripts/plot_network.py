#!/home/scott/anaconda3.7/bin/python3
import pickle, scipy, sys,  fileinput, gc, os
from networkx import *
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
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
############################################################################################
##############################################################
import argparse
parser = argparse.ArgumentParser()

def valid_layout(in_arg):
	if in_arg in ['spring','spectral','circle','random','shell']:
		return(in_arg)
	else:
		msg = '\n'+in_arg+" is not a valid layout, specify one of the following:\n'spring','spectral','circle','random','shell'"
		raise argparse.ArgumentTypeError(msg)

parser.add_argument("-graph",'-g',
    help="if you already have a graph object that was saved by this program, we can just use that instead of recalculating everything",
    type = str)
parser.add_argument("-id_list",'-id','-ID','-IDs','-ids', 
    help="these are sorted IDs matching the order of the original input dataset")
parser.add_argument("-adj_list","-adj", 
    help="this file contains the adjacency list which will make the graph")
parser.add_argument("-rand_seed", 
    help="the random seed used in generating the layout",
    type = int,
    default = 12345678)
parser.add_argument("-no_default_plot", "-no_default",
    help="Don't do the default plot with red nodes",
    action = 'store_true',
    default = False)
parser.add_argument("-node_color","-nc", 
    help="Name of the node attribute(s) (separated by commas) to be used for coloring the nodes. As currently implemented, this only works for continuous variables")
parser.add_argument("-color_scheme",'-cs', 
    help="matplotlib color scheme for the node colors if used",
    default = "bwr")
parser.add_argument("-layout", 
    help="the layout algorithm used",
    type = valid_layout,
    default = "spring")
parser.add_argument("-redo_layout", 
    help="If you already have a graph, but want to re-do the layout",
    action = 'store_true',
    default = False)
parser.add_argument("-layout_iters", 
    help="number of iterations to be used in generating the graph layout",
    type = int,
    default = 35)
parser.add_argument("-k", 
    help="the desired distance between each node",
    type = float,
    default = 0.25)
parser.add_argument("-directed", 
    help="whether or not the graph is directed",
    action = 'store_true',
    default = False)
parser.add_argument("-output", '-out_dir',
    help="the directory to place the graph files in",
    type = str)
parser.add_argument("-node_attribute_lists",'-node_attributes','-node_atts','-node_attrs', 
    help="1 or more files (comma separated list) containing file(s) for logging node attributes",
    type = str)
parser.add_argument("-edge_attribute_lists",'-edge_atts', 
    help="this is the leading string for generating the saved graph, as well as the images",
    type = str)
parser.add_argument("-show_intermediates", 
    help="NOT YET SUPPORTED - whether or not to show the intermediate graphs while the layout algorithm is iterating",
    type = bool)
parser.add_argument("-verbose", '-v',
    help="whether or not to show some verbose trouble shooting lines",
    action = 'store_true')
parser.add_argument("-min_comp_size", 
    help="the minimum size of a component for plotting. Units are percent of dataset in largest component (default = 10.0, must be 0-100)",
    type = float,
    default = 10.)
parser.add_argument("-dpi", 
    help="dots per inch for plotting networks",
    type = int,
    default = 360)
parser.add_argument("-plot_all", 
    help="if you want to plot all of the attributes",
    default = False,
    action = 'store_true')
parser.add_argument("-dont_replot", 
    help="if you want to re-plot the attributes, but don't want to, including those which were already plotted before in the output directory",
    default = True,
    action = 'store_false',
    dest = 'replot')
parser.add_argument("-dont_save", 
    help="if you don't want to save the graphpkl",
    default = True,
    action = 'store_false',
    dest = 'save')
parser.add_argument("-float_color_range",'-range', '-color_range', '-col_range', 
    help="a comma delimited range of two floats which give the low and high end for showing expression levels. This can be used to enhance contrast of an image.",
    type = str)
parser.add_argument("-subset_nodes", 
    help="to plot a specific subset of nodes in the graph",
    type = str)
args = parser.parse_args()

##############################################################
if args.output[-1]!='/':
    args.output+='/'

np.random.seed(args.rand_seed)
import random
random.seed(args.rand_seed)


if args.float_color_range != None:
    if ',' not in args.float_color_range:
        sys.exit('float_color_range must be comma delimited')
    express_range = args.float_color_range.split(',')
    express_range[0] = float(express_range[0])
    express_range[1] = float(express_range[1])
    min_express = min(express_range)
    max_express = max(express_range)
else:
    min_express = None
    max_express = None
#######################################
def get_id_list_if_none():
    ## if we don't have any id list given as an argument, we'll generate the id_list from 
    ## the adj list
    global args
    id_list = []
    first = True
    for line in fileinput.input(args.adj_list):
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            id_list+=temp_line[:2]
    return(sorted(list(set(id_list))))

#######################################
if args.adj_list == None and args.graph == None:
	G = lollipop_graph(4,6)
	num_edge = 6
#######################################
else:
    if args.graph != None:
        ## read in the input graph
        in_graph = import_dict(args.graph)
        G = in_graph['graph']
        ID_list = G.nodes()
        if 'positions' in in_graph:
            pos = in_graph['positions']
            num_node = number_of_nodes(G)
            num_edge = number_of_edges(G)
    else:
		## read in the IDs for setting up the layout of the adj matrix
        if args.id_list == None:
            ID_list = get_id_list_if_none()
        else:
            ID_list = read_file(args.id_list, "lines")
        num_node = len(ID_list)
        if args.directed:
        	G = DiGraph()
        else:
        	G = Graph()
        ID_hash = {}

        ## add the nodes to the graph
        print('\nadding the nodes to the graph\n')
        for i in range(0,len(ID_list)):
        	ID_hash[ID_list[i]] = i
        	G.add_node(ID_list[i])

        ## go through the adj_list and add the edges
        print('\nadding the edges to the graph\n')
        num_edge = 0
        first = True
        for line in fileinput.input(args.adj_list):
        	if first:
        		first = False
        	else:
        		num_edge+=1
        		temp_line = strip_split(line)
        		G.add_edge(temp_line[0],temp_line[1])

args.min_comp_size = len(ID_list)*args.min_comp_size/100
##################################################################
empty_node_dict = {}
all_nodes = G.nodes()
for n in all_nodes:
    empty_node_dict[n]=0

def get_empty_node_dict(G):
    empty_node_dict = {}
    all_nodes = G.nodes()
    for n in all_nodes:
        empty_node_dict[n]=0
    return(empty_node_dict)
##################################################################
## get the comminities based on the louvain method described in:
## Fast unfolding of communities in large networks,
## Vincent D Blondel, Jean-Loup Guillaume, Renaud Lambiotte, Renaud Lefebvre, Journal of Statistical Mechanics: Theory and Experiment 2008(10), P10008 
############################################################
def normalize_PR_dict(pr_dict):
    nodes = list(pr_dict.keys())
    original_pr = []
    for node in nodes:
        original_pr.append(pr_dict[node])
    original_pr_array = np.array(original_pr)
    original_pr_array = original_pr_array - np.min(original_pr_array)
    original_pr_array = original_pr_array / np.max(original_pr_array)
    norm_pr_dict = {}
    for i in range(0,len(nodes)):
        node = nodes[i]
        norm_pr_dict[node] = original_pr_array[i]
    return(norm_pr_dict)


def get_LPR(G, community_dict):
    ## takes in a graph, and it's partitions.
    ## Returns the dictionary of local page ranks
    ## calculate within community page-rank
    print('finding Local PageRank (LPR)')
    LPR_dict = get_empty_node_dict(G)
    all_nodes = list(LPR_dict.keys())
    ## get the list of all unique communities
    all_com_list = set(community_dict.values())
    #print(list(community_dict.keys()))
    all_com_dict = {com:[] for com in all_com_list}
    for node in all_nodes:
        temp_com = community_dict[node]
        temp_node_list = all_com_dict[temp_com]
        temp_node_list.append(node)
        all_com_dict[temp_com] = temp_node_list
    for com in all_com_list:
        temp_nodes = all_com_dict[com]
        if len(temp_nodes)>=5:
            temp_subgraph = G.subgraph(temp_nodes)
            temp_pr_dict = pagerank(temp_subgraph)
            ## now normalize it within this community
            temp_pr_dict = normalize_PR_dict(temp_pr_dict)
            for node in temp_pr_dict.keys():
                LPR_dict[node] = temp_pr_dict[node]
                #print(node,temp_pr_dict[node])
    return(LPR_dict)


############################################################

if community_installed:
    print('\nfinding the communities\n')
    if nx.get_node_attributes(G,'community') == {}:
        try:
            partition = community.best_partition(G)
        except:
            community_installed = False
        else:
            pr = pagerank(G)#,nstart=0.15)
            LPR = get_LPR(G, partition)
            partition_table = [['ID','community', 'Local_PageRank', 'PageRank']]
            for i in ID_list:
                partition[i]='community_'+str(partition[i])
                partition_table.append([i,partition[i], LPR[i], pr[i]])

            try:
                set_node_attributes(G,pr,name = "PageRank")
            except:
                set_node_attributes(G,'PageRank',pr)
            try:
                set_node_attributes(G,partition,name = "community")
            except:
                set_node_attributes(G,'community',partition)
            try:
                set_node_attributes(G,LPR,name = "LPR")
            except:
                set_node_attributes(G,'LPR',LPR)

        write_table(partition_table,args.output+'communities.txt')
    else:
        print('already done!')


##################################################################
print('\nfinding the connected components\n')
comps = connected_components(G)

## figure out which nodes to plot based on the connected component size
big_comp_nodes = []
small_comp_nodes = []
for i in comps:
	if len(i)>=args.min_comp_size:
		big_comp_nodes += i
	else:
		small_comp_nodes += i
print(len(big_comp_nodes),'nodes were found in the components larger than',args.min_comp_size)

large_comp_G = G.subgraph(big_comp_nodes)
#large_comp_G.remove_nodes_from(small_comp_nodes)



##################################################################
####### calculate the positions based on the given layout ########

if 'pos' not in vars().keys() or args.redo_layout:#args.graph == None or args.graph_positons == None:
	print('\ncalculating the node positions in the graph\n(this could take a while)\n')
	layout_function_dict = {'spring':spring_layout,'spectral':spectral_layout,
	'circle':circular_layout,'random':random_layout,'shell':shell_layout}

	layout_alg = layout_function_dict[args.layout]
	if args.layout == 'spring':
		pos=layout_alg(large_comp_G,iterations=args.layout_iters,k=args.k, seed=args.rand_seed)
	else:
		pos=layout_alg(large_comp_G, seed=args.rand_seed)
else:
	pass
gc.collect()
##################################################################
## import node attributes


def process_node(temp_node):
    try:
        float(temp_node)
    except:
        return(temp_node)
    else:
        return(str(float(temp_node)))



if args.node_attribute_lists != None:
    list_of_na_files = args.node_attribute_lists.split(',')
    for f in list_of_na_files:
        temp_attr_table = read_table(f)
        for i in range(1,len(temp_attr_table[0])):
            temp_attr_name = temp_attr_table[0][i]
            temp_attr_name = temp_attr_name.replace('/','|')
            print('\nsetting the node attribute:',temp_attr_name,'\n')
            temp_attr_dict = empty_node_dict.copy()
            print(list(temp_attr_dict.keys())[:5])
            for n in range(1,len(temp_attr_table)):
                temp_node = process_node(temp_attr_table[n][0])
                if temp_node in temp_attr_dict:
                    temp_attr_dict[temp_node] = temp_attr_table[n][i]
                else:
                    ## this means that we couldn't find the node from the
                    ## attr list in the graph
                    if args.verbose:
                        print(temp_node,"not in temp_attr_dict")
                    pass
            try:
                print("temp_attr_name",temp_attr_name)
                set_node_attributes(G,temp_attr_dict,name = temp_attr_name)
            except:
                set_node_attributes(G,temp_attr_name,temp_attr_dict)

##################################################################
## import edge attributes



##################################################################

## node and edge sizes
node_size = 2.5

edge_width = 2.5/np.sqrt(number_of_edges(G))

gc.collect()
##################################################################
## plot the graph
## select some random edges to draw so that it can do it in a reasonable amnt of time
try:
    all_edges=list(large_comp_G.edges)
except:
    all_edges=list(large_comp_G.edges())
#print(all_edges)
num_edge = int(1e6)
if len(all_edges)>num_edge:
    new_order= all_edges[:]
    np.random.shuffle(all_edges)
    subset_edges = new_order[:num_edge]
else:
    subset_edges = all_edges

if args.no_default_plot == False:

    print('\nplotting the graph\n')
    out_graph_plot = draw(large_comp_G,pos, node_shape = 'o', linewidths = 0, 
    	node_size = node_size, width = edge_width, font_size=0)


    if args.output != None:
        ## save the image
        if args.output[-1]!='/':
            args.output+='/'
        plt.savefig(args.output+'full_graph.png',dpi=args.dpi,bbox_inches='tight')
        plt.clf()
    else:
        plt.show()
gc.collect()
##################################################################
## either save or display the graph(s)
##############
def get_color_from_var(in_attr_dict):
    if is_categorical(in_attr_dict):
        return(get_vals_from_dict(get_color_from_cat(in_attr_dict)))
    else:
        return(get_vals_from_dict(get_color_from_float(in_attr_dict)))

def get_vals_from_dict(val_map):
    global large_comp_G
    vals = [val_map[node] for node in large_comp_G.nodes()]
    return(vals)

def get_color_from_cat(in_attr_dict):
    all_vals = []
    for n in sorted(list(in_attr_dict.keys())):
        all_vals.append(in_attr_dict[n])
    unique_entries = sorted(list(set(all_vals)))
    num_vars = len(unique_entries)
    cat_to_float_dict = {}
    for entry in enumerate(unique_entries):
        cat_to_float_dict[entry[1]]=entry[0]/(num_vars)

    ## update the in_attr_dict to be float rather than cat
    for n in in_attr_dict.keys():
        in_attr_dict[n]=cat_to_float_dict[in_attr_dict[n]]

    return(get_color_from_float(in_attr_dict))

def is_categorical(in_attr_dict):
    global large_comp_G
    ## first we need to figure out if it's a float or a categorical variable
    ## the first sign that we have a categorical var is if there are strings
    ## in the attribute dict
    is_categorical_bool = False
    all_vals = []
    for n in in_attr_dict.keys():
        all_vals.append(in_attr_dict[n])
        if type(in_attr_dict[n]) == str:
            is_categorical_bool = True
    
    ## no we can check how variant the vector is
    ## if there are not that many unique values compared to the number of nodes
    ## then it's probably categorical
    ## by default this is set to 10%
    #num_unique = len(list(set(all_vals)))
    #if number_of_nodes(G)/10 > num_unique:
    #    is_categorical_bool = True

    return(is_categorical_bool)


def get_color_from_float(in_attr_dict):
    global min_express, max_express

    if min_express != None:
        print('setting mins to:',min_express)
        print('setting maxs to:',max_express)
        for n in in_attr_dict.keys():
            if in_attr_dict[n] > max_express:
                #print('setting',in_attr_dict[n],'to',max_express)
                in_attr_dict[n] = max_express
            elif in_attr_dict[n] < min_express:
                #print('setting',in_attr_dict[n],'to',min_express)
                in_attr_dict[n] = min_express
            else:
                pass

    #### do linear normalization between 0 and 1
    ## get the min
    
    temp_min = None
    for n in in_attr_dict.keys():
        #print(n)
        #print('temp_min',temp_min)
        if temp_min == None:
            temp_min = in_attr_dict[n]
        else:
            if temp_min > in_attr_dict[n]:
                temp_min = in_attr_dict[n]
                #print('temp_min',temp_min)
            else:
                pass
    ## subtract min
    #print('temp_min',temp_min)
    for n in in_attr_dict.keys():
        in_attr_dict[n] = in_attr_dict[n]-temp_min

    ## get the max
    temp_max = None
    for n in in_attr_dict.keys():
        #print(n)
        #print('temp_max',temp_max)
        if temp_max == None:
            temp_max = in_attr_dict[n]
            #print('temp_max',temp_max)
        else:
            if temp_max < in_attr_dict[n]:
                temp_max = in_attr_dict[n]
                #print('temp_max',temp_max)
            else:
                pass
    # divide max
    #print('temp_max',temp_max)
    for n in in_attr_dict.keys():
        if temp_max == 0:
            in_attr_dict[n] = 0
        else:
            in_attr_dict[n] = in_attr_dict[n]/temp_max

    return(in_attr_dict)

#####################
## get the names of all attributes
def get_attrs():
    global large_comp_G
    for i in iter(large_comp_G.node.items()):
        first_node = i[1]
        break
    return(list(first_node.keys()))
#####################


if args.output != None:
    if args.node_color != None or args.plot_all:
        ## if it's a big graph, we'll only plot a subset of the edges
        ## Not implemented yet
        # all_edges = list(large_comp_G.edges())
        # max_edges = int(min([1e5,len(all_edges)]))
        # sample_edges = random.sample(all_edges,max_edges)
        ## plot the other node colors
        plt.clf()
        if args.node_color != None:
            node_color_list = args.node_color.split(',')
        if args.plot_all:
            node_color_list = get_attrs()
        for nc in node_color_list:
            if args.replot or not os.path.isfile(args.output+nc+'.png'):
                plt.clf()
                print('\nplotting the',nc,'graph')
                #val_map = get_color_from_float(get_node_attributes(G,nc))
                #values = [val_map[node] for node in G.nodes()]
                temp_nodes = list(large_comp_G.nodes())

                if is_categorical(get_node_attributes(large_comp_G,nc)):
                    ## check to see if we've already logged the values for plotting
                    if get_node_attributes(large_comp_G,nc+"_values") == {}:
                        ## if we haven't, then do it
                        values = get_color_from_var(get_node_attributes(large_comp_G,nc))
                        ## now log them
                        new_val_dict = {}
                        for i in range(len(temp_nodes)):
                            new_val_dict[temp_nodes[i]] = values[i]
                        set_node_attributes(large_comp_G, new_val_dict, name = nc+'_values')
                    else:
                        ## if we have then just use those again
                        temp_values_dict = get_node_attributes(large_comp_G,nc+"_values")

                        print('retreiving previously used categorical colors')
                        values = []
                        for i in range(len(temp_nodes)):
                            values.append(temp_values_dict[temp_nodes[i]])
                else:
                    ## if it's not categorical, we can just get the numeric attributes directly
                    values = get_color_from_var(get_node_attributes(large_comp_G,nc))

                #print('\t',values)
                if is_categorical(get_node_attributes(large_comp_G,nc)):
                    print('\tis categorical')
                    temp_colors = 'gist_rainbow'#'pipy_spectral'#'Set1'
                else:
                    print("\tisn't categorical")
                    temp_colors = args.color_scheme
                ## convert the values to colors
                temp_cmap = plt.get_cmap(temp_colors)
                temp_value_colors = []
                for v in values:
                    temp_value_colors.append(temp_cmap(v))
                values = temp_value_colors
                if args.subset_nodes != None:
                    temp_subset = read_file(args.subset_nodes, 'lines')
                    subset_hash = {key:value for value, key in enumerate(temp_subset)}
                    final_subset = []
                    final_values = []
                    for i in range(0,len(temp_nodes)):
                        if temp_nodes[i] in subset_hash:
                            final_subset.append(temp_nodes[i])
                            final_values.append(values[i])
                    temp_nodes = final_subset
                    values = final_values
                draw(large_comp_G,pos, cmap=plt.get_cmap(temp_colors),
                    node_color = values, node_shape = 'o', linewidths = 0, 
                    node_size = node_size, width = edge_width, font_size=0,
                    nodelist=temp_nodes,
                    edgelist=subset_edges)
                #draw_networkx_nodes(G,pos,nodelist=list(G.nodes()),
                #    cmap=plt.get_cmap(temp_colors),
                #    node_color = values,
                #    node_size = node_size,
                #    linewidths = 0)
                ## save the image
                plt.savefig(args.output+nc+'.png',
                    dpi=args.dpi,
                    bbox_inches='tight')
                gc.collect()
            else:
                if os.path.isfile(args.output+nc+'.png'):
                    print('\n',args.output+nc+'.png', 'already exists\nskipping')
                gc.collect()
        gc.collect()

#################################################
## save the graphs
if args.output != None and args.save:
    print('\nsaving the graph\n')
    ## save the graph
    save_dict({'graph':large_comp_G,'positions':pos},args.output+'large_comps.graphpkl')
    
    save_dict({'graph':G},args.output+'full_graph_full.graphpkl')