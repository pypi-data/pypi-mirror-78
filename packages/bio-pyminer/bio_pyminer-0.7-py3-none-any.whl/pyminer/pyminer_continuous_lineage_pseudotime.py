#!/usr/bin/env python3
import sys, os, glob, time
import numpy as np
import random
#import scipy
from subprocess import Popen
from time import sleep
#from scipy.stats import spearmanr
#from time import time
import fileinput,pickle
from math import floor
#from scipy.stats import gaussian_kde
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
#import seaborn as sns
import h5py
from copy import deepcopy
import networkx as nx
from scipy.stats import rankdata
from scipy.interpolate import interp1d
from statsmodels.nonparametric.smoothers_lowess import lowess
import ray
import multiprocessing
try:
    from pyminer.common_functions import *
    from pyminer.pyminer_common_stats_functions import *
    from pyminer.pyminer_common_stats_functions import no_p_spear, get_Z_cutoff, fast_single_spear
    from pyminer.pyminer_get_lincs import get_cell_cycle, do_single_lincs_analysis_from_files
    from pyminer.aux.pyminer_get_lincs import get_cell_cycle, do_single_lincs_analysis_from_files
except:
    from common_functions import *
    from pyminer_common_stats_functions import *
    from pyminer_common_stats_functions import no_p_spear, get_Z_cutoff, fast_single_spear
    from pyminer_get_lincs import get_cell_cycle, do_single_lincs_analysis_from_files
    from aux.pyminer_get_lincs import get_cell_cycle, do_single_lincs_analysis_from_files
###########################################################

def get_cell_type_gene_halfway_point(mean_express_array,
                                     gene_names,
                                     gene_rho_vect,
                                     abs_rho_cutoff,
                                     cell_type_index_vect,
                                     gene_progression_dir):
    ## select the genes that are significantly above the rho cutoff
    pos_idxs = np.where(gene_rho_vect>=abs_rho_cutoff)[0]
    ## select the genes that are sinificantly below the rho cutoff
    neg_idxs = np.where(gene_rho_vect<=-1*abs_rho_cutoff)[0]
    #########
    ## get the gene expression "halfway" point. Essentially, this is 
    ## like the 'inflection point'-ish in which the expression goes up or down towards it's 'destination' expression level
    gene_mean_max = np.max(mean_express_array[:,cell_type_index_vect],axis=1)
    gene_mean_min = np.min(mean_express_array[:,cell_type_index_vect],axis=1)
    gene_halfway = (gene_mean_max+gene_mean_min)/2
    ## create a binary matrix that indicates
    greater_than_half_mean_mat = lambda i:  mean_express_array[i,:] > gene_halfway[i]
    less_than_half_mean_mat = lambda i:  mean_express_array[i,:] < gene_halfway[i]
    ## positives will increase with cell_type_index_vect
    halfway_positives = lambda i: np.argmax(greater_than_half_mean_mat(i)[cell_type_index_vect])
    ## negatives will decrease with cell_type_index_vect
    halfway_negatives = lambda i: np.argmax(less_than_half_mean_mat(i)[cell_type_index_vect])
    ## evaluate them
    pos_gene_halfway_points = [halfway_positives(idx) for idx in pos_idxs]
    neg_gene_halfway_points = [halfway_negatives(idx) for idx in neg_idxs]
    print("finished getting halfway points")
    ## make a dictionary to return the results
    pos_dict={}
    neg_dict={}
    print(gene_names[:5])
    for i in range(len(pos_idxs)):
        idx = pos_idxs[i]
        pos_dict[gene_names[idx]]=pos_gene_halfway_points[i]
    for i in range(len(neg_idxs)):
        idx = neg_idxs[i]
        neg_dict[gene_names[idx]]=neg_gene_halfway_points[i]
    up_down_dict = {"pos":pos_dict,"neg":neg_dict}
    #write_up_down_res(up_down_dict, cell_type_index_vect, gene_progression_dir)
    return(up_down_dict)


def get_all_paths_in_subgraph(sub_graph, stem_cell_id):
    ## get the leaves
    degree_dict = dict(sub_graph.degree())
    leaves = []
    for key, degree in degree_dict.items():
        if degree == 1:
            leaves.append(key)
    ## go through each leaf & get the shortest path from the stem cell 
    all_paths = []
    for leaf in leaves:
        all_paths.append(nx.shortest_path(sub_graph, source=stem_cell_id, target = leaf))
    return(all_paths)


def get_max_from_dict(in_dict,temp_set):
    temp_winner = None
    temp_win_val = -99999999
    for key in in_dict.keys():
        #print(key,":",in_dict[key])
        if key in temp_set:
            #print(temp_win_val)
            if in_dict[key]>temp_win_val:
                temp_win_val = in_dict[key]
                temp_winner = key
    return(temp_winner)


def get_all_lineage_paths(lineage_dict, stem_cell_id = None):
    ## stem cell is the one with highest page rank
    pr_dict = nx.pagerank(lineage_dict["graph"])
    commun_btwn_cent_dict = nx.communicability_betweenness_centrality(lineage_dict['graph'])
    ## maybe make a plot?
    #perhaps
    ## for each component, the the shortest path from stem cell to leaf
    comps = nx.connected_components(lineage_dict['graph'])
    all_paths = []
    for comp in comps:
        temp_nodes = deepcopy(set(comp))
        #print(temp_nodes)
        if stem_cell_id is None:
            #temp_stem = get_max_from_dict(pr_dict,temp_nodes)
            temp_stem = get_max_from_dict(commun_btwn_cent_dict,temp_nodes)
        else:
            temp_stem = stem_cell_id
        print("temp stem cell:",temp_stem)
        if temp_stem in temp_nodes:
            temp_subgraph = lineage_dict["graph"].subgraph(temp_nodes)
            all_paths += get_all_paths_in_subgraph(temp_subgraph,temp_stem)
        else:
            pass
    ## returns a list of lists with all of the paths to construct
    return(all_paths)


def get_small_distance_mat(distance_mat, exemplar_indices, scale = False):
    if type(exemplar_indices)==np.ndarray:
        exemplar_indices = exemplar_indices.tolist()
    small_dist_mat = np.zeros((np.shape(distance_mat)[0],len(exemplar_indices)))
    ## go through each of the exemplars and populate the small distance mat
    for ex in range(len(exemplar_indices)):
        ex_idx = exemplar_indices[ex]
        small_dist_mat[:,ex] = distance_mat[:,ex_idx]
    ## now, we'll change the self distance to equal the minimum non-zero distance to itself. Otherwise, exemplars will stand out like sore thumbs
    ## because realistically, if you were to actually measure the same transcriptome twise, the Euclidean distance would actually still be large 
    ## because of the random sampling. So in essense we're correcting for technical variability in measurements.
    # for ex in range(len(exemplar_indices)):
    #     ex_idx = exemplar_indices[ex]
    #     non_zero_indices = np.where(small_dist_mat[:,ex]>0)[0]
    #     small_dist_mat[ex_idx,ex] = np.min(small_dist_mat[non_zero_indices,ex])
    ## if we need to scale, then we'll scale
    if scale:
        small_dist_mat[:,ex] -= np.mean(small_dist_mat[:,ex])
        small_dist_mat[:,ex] /= np.std(small_dist_mat[:,ex])
    return(small_dist_mat)


def interpolate(x, y, n=20000, kind="cubic"):
    ## x is position on the manifold trajectory, y is the matrix of distances where each column is distance to exemplar
    new_x = (np.arange(n)/(n-1)) * np.max(x)
    interp_y = np.zeros((n,y.shape[1]))
    for i in range(y.shape[1]):
        temp_interp_func = interp1d(x, y[:,i], kind = kind)
        interp_y[:,i]=temp_interp_func(new_x)
    return(new_x, interp_y)


def lowess_smooth(full_path_x, full_path_y, frac = 0.175):
    ## first interpolate to prevent lowess from sometimes doing absolutely nothing...
    full_path_x, full_path_y = interpolate(full_path_x, full_path_y, n=full_path_x.shape[0]*2, kind="linear")
    lowess_y = np.zeros(full_path_y.shape)
    for i in range(full_path_y.shape[1]):
        temp_fit = lowess(full_path_y[:,i],full_path_x,frac=frac)
        lowess_y[:,i]=temp_fit[:,1]
    return(full_path_x,lowess_y)

#################################################

def get_local_clusters_on_path(lineage_path, current_cluster):
    if current_cluster == lineage_path[0]:
        return(lineage_path[:2])
    if current_cluster == lineage_path[-1]:
        return(lineage_path[-2:])
    if current_cluster not in lineage_path:
        print("current_cluster not in lineage_path")
    clust_loc = np.where(np.array(lineage_path)==current_cluster)[0][0]
    return(lineage_path[(clust_loc-1):(clust_loc+2)])


@ray.remote
def ray_get_closest_x_position(idx_list,
                               small_dist_mat, 
                               full_path,
                               lineage_path,
                               smooth_topology_matrix_x,
                               smooth_topology_matrix_y,
                               linear_groups):
    min_cap = np.nanmin(smooth_topology_matrix_x)
    max_cap = np.nanmax(smooth_topology_matrix_x)
    new_x_dict = {}
    for idx in idx_list:
        #### get the pertinent cell types
        ## this version of the local small_dist_mat is all cells in rows, and the ordered progression
        ## of 
        local_clust_set = set(get_local_clusters_on_path(lineage_path, linear_groups[idx]))
        group_progression = np.array(linear_groups)[full_path]
        local_clusts = []
        for i in range(len(full_path)):
            if group_progression[i] in local_clust_set:
                local_clusts.append(i)
        ## now get the Euclidean distance along this sub-space
        sum_sq_euc_dist = np.sum((small_dist_mat[idx,local_clusts] - smooth_topology_matrix_y[:,local_clusts])**2, axis = 1)
        best_x_fit = np.where(sum_sq_euc_dist == np.min(sum_sq_euc_dist))[0].tolist()[0]
        #print(best_x_fit)
        ## here is where we clip the ends of the fit, so that we only include cells that are actually along the given trajectory
        #if (best_x_fit!= 0) and (best_x_fit != np.shape(sum_sq_euc_dist)[0]):
        #    print(best_x_fit,np.shape(sum_sq_euc_dist)[0])
        if smooth_topology_matrix_x[best_x_fit] != max_cap and smooth_topology_matrix_x[best_x_fit] != min_cap:
            new_x_dict[idx] = smooth_topology_matrix_x[best_x_fit]
        elif idx in full_path:
            new_x_dict[idx] = smooth_topology_matrix_x[best_x_fit]
    return(new_x_dict)


def get_cell_embeddings_on_given_trajectory(small_dist_mat, 
                                            smooth_topology_matrix_x,
                                            smooth_topology_matrix_y,
                                            full_path,
                                            lineage_path,
                                            sample_k_lists,
                                            linear_groups,
                                            processes = None):
    if processes == None:
        processes = multiprocessing.cpu_count()
    pertinent_cell_indices = []
    for cell_type in lineage_path:
        pertinent_cell_indices += sample_k_lists[cell_type]
    index_lists = ray_get_indices_from_list(processes,pertinent_cell_indices)
    ## put the ray objects & make the calls
    ray.init()
    ray_small_dist_mat = ray.put(small_dist_mat)
    ray_smooth_topology_matrix_x = ray.put(smooth_topology_matrix_x)
    ray_smooth_topology_matrix_y = ray.put(smooth_topology_matrix_y)
    ray_calls = []
    for p in range(processes):
        ray_calls.append(ray_get_closest_x_position.remote(index_lists[p],
                                                           ray_small_dist_mat,
                                                           full_path,
                                                           lineage_path,
                                                           ray_smooth_topology_matrix_x,
                                                           ray_smooth_topology_matrix_y,
                                                           linear_groups))
    all_ray_dict_results = ray.get(ray_calls)
    ray.shutdown()
    ## start out with nans & populate for cells that are actually on the topology
    current_x_position = [np.nan]*small_dist_mat.shape[0]
    for temp_dict in all_ray_dict_results:
        for key, value in temp_dict.items():
            current_x_position[key]=value
    current_x_position = np.array(current_x_position)
    return(current_x_position)


#################################################
def are_connected_at_cutoff(temp_subgraph, pr_dict, temp_cutoff, start, end):
    temp_nodes = [key for key, value in pr_dict.items() if value>temp_cutoff]
    ## if one of them isn't in the subgraph, then they definitely can't be connected
    if start not in temp_nodes or end not in temp_nodes:
        return(False)
    ## if they are both in the graph, then we'll check that they are still connected
    temp_subgraph = temp_subgraph.subgraph(temp_nodes)
    if end in nx.node_connected_component(temp_subgraph, start):
        return(True)
    else:
        return(False)


def get_pr_cutoff(temp_subgraph, pr_dict, pr_vect, start, end):
    ## binary search for correct page rank cutoff
    # https://www.pyblog.in/programming/binary-search-in-python/
    n = len(pr_vect)
    L = 0
    R = n-1
    while L < R:
        mid = floor((L+R)/2)
        #print("L:",L)
        #print("R:",R)
        #print("mid:",mid)
        if are_connected_at_cutoff(temp_subgraph, pr_dict, pr_vect[mid], start, end):
            L = mid + 1
        elif not are_connected_at_cutoff(temp_subgraph, pr_dict, pr_vect[mid], start, end):
            R = mid - 1
        else:
            return(pr_vect[mid])
    return (pr_vect[L])


def get_minimal_graph(temp_subgraph, start, end):
    ## first filter for only points that are actually between the start and end
    print("getting minimally connected graph by page rank")
    ## find the maximum page rank cutoff at which the exemplars are still connected
    pr_dict = nx.pagerank(temp_subgraph)
    pr_vect = sorted(list(set(pr_dict.values())))
    pr_cutoff = get_pr_cutoff(temp_subgraph, pr_dict, pr_vect, start, end)
    print("current PR cutoff:",pr_cutoff)
    temp_nodes = [key for key, value in pr_dict.items() if value>=(pr_cutoff-1e-10)]
    print("start in temp_nodes:",start in temp_nodes)
    print("end in temp_nodes:",end in temp_nodes)
    return(temp_subgraph.subgraph(temp_nodes), pr_dict)


def filter_graph_for_between(temp_subgraph, start_exemplar, end_exemplar, small_dist_mat, local_clusts):
    all_nodes = sorted(list(temp_subgraph.nodes()))
    small_dist_mat = small_dist_mat[:,local_clusts]
    ## get the direction of all pertinent points to each of the two exemplars
    direction_to_start = np.array((small_dist_mat[start_exemplar,:] - small_dist_mat)>=0,dtype=int)
    direction_to_end = np.array((small_dist_mat[end_exemplar,:] - small_dist_mat)>=0,dtype=int)
    #print(direction_to_start)
    #print(direction_to_end)
    ## if they're going in the same direction, taking the difference will sum to zero.
    ## This means that the point is not between the two exemplars in Euclidean space & will therefore be removed.
    all_dims_in_same_dir_binary_mat = np.abs(direction_to_start - direction_to_end)
    #print(all_dims_in_same_dir_binary_mat)
    any_in_diff_direction = np.sum(all_dims_in_same_dir_binary_mat, axis = 1)
    #print(any_in_diff_direction)
    temp_node_idxs = set(np.where(any_in_diff_direction!=0)[0])
    original_node_set = set(all_nodes)
    temp_nodes = temp_node_idxs.intersection(original_node_set)
    #print(temp_node_idxs)
    #temp_nodes = np.array(all_nodes,dtype=int)[temp_node_idxs].tolist()
    ## add back in the exemplars. B/C of floating pt errors, sometimes they don't get included
    temp_nodes = temp_nodes.union({start_exemplar, end_exemplar})
    #print(temp_nodes)
    #print(start_exemplar in temp_nodes)
    #print(end_exemplar in temp_nodes)
    return(temp_subgraph.subgraph(temp_nodes))


def get_custom_shortest_path(temp_subgraph, start_exemplar, end_exemplar, distance_mat, small_dist_mat, start_clust, end_clust, do_minimal = True):
    if do_minimal:
        temp_subgraph = filter_graph_for_between(temp_subgraph, start_exemplar, end_exemplar, small_dist_mat, [start_clust, end_clust])
        temp_subgraph, pr_dict = get_minimal_graph(temp_subgraph, start_exemplar, end_exemplar)
    all_sp = list(nx.all_shortest_paths(temp_subgraph, source=start_exemplar, target=end_exemplar, weight = None))
    sp_distances = np.zeros(len(all_sp))
    for i in range(len(all_sp)):
        sp = all_sp[i]
        path_edges = set(zip(sp,sp[1:]))
        sp_dist = 0
        for path in path_edges:
            sp_dist+=(distance_mat[path[0],path[1]]*-1)
            #sp_dist+=(pr_dict[path[0]]*pr_dict[path[1]])
        sp_distances[i]=sp_dist
    #central_dist = np.median(sp_distances)
    #dist_to_central_dist = (sp_distances-central_dist)**2
    best_path_idx = np.where(sp_distances==np.min(sp_distances))[0]
    #best_path_idx = np.where(sp_distances==np.max(sp_distances))[0]
    #best_path_idx = np.where(dist_to_central_dist==np.min(dist_to_central_dist))[0]
    return(all_sp[best_path_idx[0]])

#################################################
#################################################
## plotting functions

def pos1_to_pos2_interpolate(pos1,pos2,steps=30, rm_nans = True):
    ## takes in two pos dicts, and returns a list of length steps with all of the updates
    all_points = []
    for key in set(pos2.keys()).intersection(set(pos1.keys())):
        num_nan1 = np.sum(np.isnan(pos1[key]))
        num_nan2 = np.sum(np.isnan(pos2[key]))
        total_nan = num_nan1+num_nan2
        #print("\t",total_nan)
        #print(pos1[key])
        #print(pos2[key])
        if total_nan > 0:
            pass
        else:
            all_points.append(key)
    dims = pos1[all_points[0]].shape
    rate_of_change = {point:np.zeros(dims) for point in all_points}
    #pos_list = [deepcopy(empty_pos) for step in range(steps)]
    for point in all_points:
        #print(point)
        #step_size = (pos2[point] - pos1[point])/steps
        rate_of_change[point] = (pos2[point] - pos1[point])/steps
        # for axis in range(pos1[point].shape[0]):
        #     #print("\t",axis)
        #     step_size = (pos2[point][axis] - pos1[point][axis])/steps
        #     #print("\t",pos1[point][axis],"to",pos2[point][axis], "in",steps,"steps")
        #     #print(step_size)
        #     if pos1[point][axis]!=pos2[point][axis]:
        #         temp_axis = crange(pos1[point][axis], pos2[point][axis]+step_size, step_size)
        #     else:
        #         temp_axis = [pos1[point][axis]]*steps
        #     #print(temp_axis)
        #     for step in range(steps):
        #         #print("\t\t",step)
        #         #print(pos_list[step][point][axis])
        #         pos_list[step][point][axis]=temp_axis[step]
    return(rate_of_change, steps)


def get_pos_from_init(init_dict,sample_k_lists, init_scale_fact = .75):
    out_pos_init = {}
    for i in range(len(sample_k_lists)):
        for cell in sample_k_lists[i]:
            out_pos_init[cell] = init_dict[i]*init_scale_fact
    return(out_pos_init)


def get_positions(subject_network, lineage_dict, sample_k_lists, transition_probability, seed = 123456):
    ## first we'll calculate the initial positions by lineage graph
    full_clust_network = nx.from_numpy_matrix(transition_probability)
    #pos_init_dict = nx.spring_layout(full_clust_network)
    pos3d_init_dict = nx.spring_layout(full_clust_network, dim=3, seed = seed)
    #full_pos_init_dict = get_pos_from_init(pos_init_dict, sample_k_lists)
    full_pos3d_init_dict = get_pos_from_init(pos3d_init_dict, sample_k_lists)
    #print("plotting 2D coords")
    #pos = linear_norm_pos_dict(nx.spring_layout(subject_network, pos = full_pos_init_dict))
    print("plotting 3D coords")
    pos3d = linear_norm_pos_dict(nx.spring_layout(subject_network, pos = full_pos3d_init_dict, dim=3, seed = seed))
    #return(pos, pos3d)
    return(None, pos3d)


# @ray.remote
# def spin_3d(fig,ax,plt,angle_set,temp_out_dir):
@ray.remote
def spin_3d(ax,angle_set,temp_out_dir):
    for angle in angle_set:
        ax.view_init(30, angle)
        out_file = os.path.join(temp_out_dir,"angle_"+str(angle)+".jpg")
        plt.savefig(out_file,
                    dpi=175,
                    bbox_inches='tight')
    return()


def plot_3d(subject_network, pos3d, expanded_color_vect, temp_out_dir, full_path=None, spin=True, processes = None):
    ## helped by: https://www.idtools.com.au/3d-network-graphs-python-mplot3d-toolkit/
    print("plotting the path in 3D")
    print(subject_network)
    angle = 0
    node_size = 2.5
    edge_width = 2.5/np.sqrt(nx.number_of_edges(subject_network))
    fig = plt.figure(figsize=(10,7))
    ax = Axes3D(fig)
    ## plot the edges
    for key, value in pos3d.items():
        if key%1000 == 0:
            print("plotting point#",key)
        xi = value[0]
        yi = value[1]
        zi = value[2]
        # Scatter plot
        dummy_point = ax.scatter(xi, yi, zi, c=[expanded_color_vect[key]], s=node_size, linewidths = 0, alpha=0.7)
    if full_path is not None:
        path_edges = set(zip(full_path,full_path[1:]))
        for i,j in enumerate(path_edges):
            #print(i,j)
            x = np.array((pos3d[j[0]][0], pos3d[j[1]][0]))
            y = np.array((pos3d[j[0]][1], pos3d[j[1]][1]))
            z = np.array((pos3d[j[0]][2], pos3d[j[1]][2]))
            # Plot the connecting lines
            #print(x,y,z)
            dummy_line = ax.plot(x, y, z, c='black', linewidth = 6)
            ## try to make the animation
            #animation = FuncAnimation(fig, func=animate_3d_spin, frames=range(360), interval=10)
            #plt.show()
            ## set the camera and save
    ax.set_axis_off()
    if processes==None:
        processes = multiprocessing.cpu_count()
    all_angles = ray_get_indices_from_list(processes,np.arange(0,360,2).tolist())
    ray_calls = []
    ray.init()
    for angle_set in all_angles:
        #ray_calls.append(spin_3d.remote(fig,ax,plt,angle_set,temp_out_dir))
        ray_calls.append(spin_3d.remote(ax,angle_set,temp_out_dir))
    ray.get(ray_calls)
    ray.shutdown()
    return(fig)

#################################################
#################################################
## fix tips
def fix_tips(subject_network, 
             start_exemplar, 
             end_exemplar, 
             small_dist_mat, 
             distance_mat,
             original_full_path, 
             lineage_path, 
             sample_k_lists,
             linear_groups):
    start_clust = lineage_path[0]
    end_clust = lineage_path[-1]
    ## first, figure out which of the points on the full path is the first point belonging to the second cluster
    linear_groups = np.array(linear_groups)
    print("\tstart_exemplar:",start_exemplar,"from clust:",linear_groups[start_exemplar])
    print("\tend_exemplar:",end_exemplar,"from clust:",linear_groups[end_exemplar])
    vector_of_cluster_membership = linear_groups[original_full_path]
    print("lineage_path",lineage_path)
    print("vector_of_cluster_membership",vector_of_cluster_membership)
    get_dist_from_pt_beginning = np.min(np.where(vector_of_cluster_membership != start_clust)[0])
    get_dist_from_pt_end = np.max(np.where(vector_of_cluster_membership != end_clust)[0])
    new_beginning_comparison_idx = original_full_path[get_dist_from_pt_beginning]
    new_end_comparison_idx = original_full_path[get_dist_from_pt_end]
    print("\tfirst pt not in first clust is pt#:",new_beginning_comparison_idx,"from clust:",linear_groups[new_beginning_comparison_idx])
    print("\tlast pt not in final clust is pt#:",new_end_comparison_idx,"from clust:",linear_groups[new_end_comparison_idx])
    ## get the new beginning and destination points
    # get the points in the first cluster, and find the one that maximizes distance from the first point in the second cluster
    points_in_current_cluster = sample_k_lists[start_clust]
    local_clusts = get_local_clusters_on_path(lineage_path, start_clust)
    sum_sq_euc_dist = np.sum((small_dist_mat[new_beginning_comparison_idx,local_clusts] - small_dist_mat[:,local_clusts])**2, axis = 1)
    #sum_sq_euc_dist += np.sum((small_dist_mat[start_exemplar,local_clusts] - small_dist_mat[:,local_clusts])**2, axis = 1)
    sum_sq_euc_dist = sum_sq_euc_dist[points_in_current_cluster]
    best_x_fit = np.where(sum_sq_euc_dist == np.max(sum_sq_euc_dist))[0].tolist()[0]
    new_beginning_pt_idx = points_in_current_cluster[best_x_fit]
    print("new_beginning_pt_idx",new_beginning_pt_idx,"from clust:",linear_groups[new_beginning_pt_idx])
    # get the points in the LAST cluster, and find the one that maximizes distance from the first point in the second cluster
    points_in_current_cluster = sample_k_lists[end_clust]
    local_clusts = get_local_clusters_on_path(lineage_path, end_clust)
    sum_sq_euc_dist = np.sum((small_dist_mat[new_end_comparison_idx,local_clusts] - small_dist_mat[:,local_clusts])**2, axis = 1)
    #sum_sq_euc_dist += np.sum((small_dist_mat[end_exemplar,local_clusts] - small_dist_mat[:,local_clusts])**2, axis = 1)
    sum_sq_euc_dist = sum_sq_euc_dist[points_in_current_cluster]
    best_x_fit = np.where(sum_sq_euc_dist == np.max(sum_sq_euc_dist))[0].tolist()[0]
    new_end_pt_idx = points_in_current_cluster[best_x_fit]
    print("new_end_pt_idx",new_end_pt_idx,"from clust:",linear_groups[new_end_pt_idx])
    ## subset the graph for the first cluster
    temp_subgraph = subject_network.subgraph(sample_k_lists[start_clust])
    new_beginning_extension = get_custom_shortest_path(temp_subgraph, start_exemplar, new_beginning_pt_idx, distance_mat, small_dist_mat, start_clust, end_clust)[1:][::-1]
    full_path = new_beginning_extension + original_full_path
    ## add the extension to the end
    temp_subgraph = subject_network.subgraph(sample_k_lists[end_clust])
    new_end_extension = get_custom_shortest_path(temp_subgraph, end_exemplar, new_end_pt_idx, distance_mat, small_dist_mat, start_clust, end_clust)[1:]
    full_path = full_path + new_end_extension
    return(full_path)


#################################################
def get_pertienent_cells_and_ordered_mat(small_dist_mat, 
                                         distance_mat, 
                                         subject_network, 
                                         lineage_path, 
                                         exemplar_indices, 
                                         sample_k_lists,
                                         processes,
                                         out_dir,
                                         linear_groups,
                                         expanded_color_vect = None,
                                         pos = None,
                                         pos3d = None):
    # temp_out_dir = os.path.join(out_dir,'_'.join(map(str,deepcopy(lineage_path))))
    # if not os.path.exists(temp_out_dir):
    #     os.makedirs(temp_out_dir)
    full_path = []
    ## get the shortest path from each exemplar
    print("getting cell embeddings along lineage")
    print("\tgetting path")
    for i in range(0,len(lineage_path)-1):
        start_clust = lineage_path[i]
        end_clust = lineage_path[i+1]
        start_exemplar = exemplar_indices[start_clust]
        end_exemplar = exemplar_indices[end_clust]
        ## first subset the embedding for only the pertinent cell types
        temp_nodes = sample_k_lists[start_clust] + sample_k_lists[end_clust]
        temp_subgraph = subject_network.subgraph(temp_nodes)
        if len(full_path)==0:
            full_path += get_custom_shortest_path(temp_subgraph, start_exemplar, end_exemplar, distance_mat, small_dist_mat, start_clust, end_clust)
            #full_path += nx.shortest_path(temp_subgraph, source=start_exemplar, target=end_exemplar, weight = None)#"weight")
            #full_path += nx.shortest_path(temp_subgraph, source=start_exemplar, target=end_exemplar, weight = "weight")
        else:
            full_path += get_custom_shortest_path(temp_subgraph, start_exemplar, end_exemplar, distance_mat, small_dist_mat, start_clust, end_clust)[1:]
                #full_path += nx.shortest_path(temp_subgraph, source=start_exemplar, target=end_exemplar, weight = None)[1:]#"weight")
                #full_path += nx.shortest_path(temp_subgraph, source=start_exemplar, target=end_exemplar, weight = "weight")[1:]
        ##################################
        ## now we fix the tips of the path
    original_full_path = deepcopy(full_path)
    full_path = fix_tips(subject_network, exemplar_indices[lineage_path[0]], exemplar_indices[lineage_path[-1]], small_dist_mat, distance_mat, full_path, lineage_path, sample_k_lists, linear_groups)
    #full_path = lineage_path
    print("\toriginal_full_path:",original_full_path)
    print("\t\tbest path was:",full_path)
    ##
    # if plot:
    #     #######################
    #     ## plot it
    #     ##
    #     node_size = 2.5
    #     edge_width = 2.5/np.sqrt(nx.number_of_edges(subject_network))
    #     path_edges = set(zip(full_path,full_path[1:]))
    #     expanded_color_vect = [cluster_dict["color_vect"][i] for i in cluster_dict["linear_groups"]]
    #     ##
    #     print("plotting 2D",subject_network,full_path)
    #     plt.clf()
    #     nx.draw(subject_network,pos,node_color=expanded_color_vect,node_size = node_size, width = edge_width)
    #     nx.draw_networkx_nodes(subject_network,pos,nodelist=full_path,node_color='r',node_size = node_size*5, width = edge_width)
    #     nx.draw_networkx_edges(subject_network,pos,edgelist=path_edges,edge_color='r',node_size = node_size, width = 10)
    #     ##
    #     plt.axis('equal')
    #     plt.show()
    # ##############################################
    ## get the pseudotime-like X position, by adding weights successively going from one node to the next
    ## the Y position that will be loess smoothed are the rows of the full small_dist_mat
    #print("check1")
    #####################################
    #####################################
    new_small_dist_mat = np.zeros((small_dist_mat.shape[0],len(full_path)))
    for i in range(len(full_path)):
        temp_full_vect = distance_mat[:,full_path[i]]
        new_small_dist_mat[:,i]=temp_full_vect
    #####################################
    #####################################
    full_path_x = np.zeros((len(full_path)))
    full_path_y = np.zeros((len(full_path),new_small_dist_mat.shape[1]))
    full_path_y[0,:]=new_small_dist_mat[full_path[0],:]
    for i in range(1,len(full_path)):
        ## first get the edge
        prev_idx = full_path[i-1]
        cur_idx = full_path[i]
        cur_x_position = distance_mat[prev_idx,cur_idx] + full_path_x[i-1]
        full_path_x[i] = cur_x_position
        full_path_y[i,:]= new_small_dist_mat[cur_idx,:]
    ## because we use negative squared euclidean distance, 
    # we'll just multiply it by -1 to bring it back into positive space, so things are more intuitive
    full_path_x *= -1
    #print("check2")
    smooth_x, smooth_y = lowess_smooth(full_path_x, full_path_y)
    #print("check3")
    new_x, new_y = interpolate(smooth_x, smooth_y)
    #new_x, new_y = interpolate(full_path_x, full_path_y)
    ## interpolate the shortest path mat to a semi-continuous topology using a loess fit in exemplar-distance space
    #new_y2 = lowess_smooth(new_x, new_y)
    # if plot:
    #     print("plotting scatters")
    #     plt.clf()
    #     plt.scatter(new_x, new_y[:,0])
    #     plt.scatter(smooth_x, smooth_y[:,0])
    #     plt.scatter(full_path_x, full_path_y[:,0])
    #     plt.show()
    print("\tgetting embeddings of all cells along lineage")
    cell_embeddings = get_cell_embeddings_on_given_trajectory(new_small_dist_mat, 
                                                              new_x,
                                                              new_y,
                                                              full_path,
                                                              lineage_path,
                                                              sample_k_lists,
                                                              linear_groups,
                                                              processes = None)
    return(cell_embeddings, full_path)


@ray.remote
def ray_cor(cell_embeddings,temp_gene, shuffle=False):
    return(fast_single_spear(cell_embeddings,temp_gene, shuffle=shuffle))

def get_embedding_correlations(cell_embeddings, full_expression, processes = None):
    if processes==None:
        processes = multiprocessing.cpu_count()
    # get the null distribution and real correlations
    null_cor_vect = np.zeros((full_expression.shape[0]))
    gene_cor_vect = np.zeros((full_expression.shape[0]))
    # i=0
    # while i < null_cor_vect.shape[0]:
    #     if i% 2000 == 0 and i!=0:
    #         print("\tworking on gene:",i)
    #     ray.init()
    #     ray_calls = []
    #     temp_idx_list = []
    #     for p in range(processes):
    #         if i < null_cor_vect.shape[0]:
    #             temp_gene = deepcopy(np.array(full_expression[i,:]))
    #             ray_calls.append(ray_cor.remote(cell_embeddings,temp_gene, shuffle=True))
    #             temp_idx_list.append(i)
    #             i+=1
    #     temp_result = ray.get(ray_calls)
    #     ray.shutdown()
    #     for i in range(len(temp_idx_list)):
    #         idx = temp_idx_list[i]
    #         gene_cor_vect[idx]=temp_result[i][0]
    #         null_cor_vect[idx]=temp_result[i][1]
    for i in range(full_expression.shape[0]):
        if i% 2000 == 0 and i!=0:
            print("\tworking on gene:",i)
            #print(null_cor_vect[i-100:i])
            #print(gene_cor_vect[i-100:i])
        #temp_gene = deepcopy(np.array(full_expression[i,:]))
        actual_res, shuffled_res = fast_single_spear(cell_embeddings,full_expression[i,:], shuffle=True)
        gene_cor_vect[i]=actual_res
        null_cor_vect[i]=shuffled_res
    cutoff = get_Z_cutoff(null_cor_vect, z = 7.5, positive = True)
    gene_cor_vect[np.isnan(gene_cor_vect)]=0
    print(np.sum(np.abs(gene_cor_vect)>cutoff), "significant correlations found")
    return(gene_cor_vect, null_cor_vect, cutoff)


###########################################################

def reverse_weights(subject_network):
    for u,v,d in subject_network.edges(data=True):
        d['weight']=(d['weight']-1)*-1
    return(subject_network)

###########################################################
def get_max_name_cor_idx(gene_names,gene_cor_vect):
    gene_idx=np.where(gene_cor_vect == np.nanmax(gene_cor_vect))[0][0]
    print("max:",gene_names[gene_idx],":",gene_cor_vect[gene_idx])
    return(gene_names[gene_idx], gene_cor_vect[gene_idx], gene_idx)


def get_min_name_cor_idx(gene_names,gene_cor_vect):
    gene_idx=np.where(gene_cor_vect == np.nanmin(gene_cor_vect))[0][0]
    print("min:",gene_names[gene_idx],":",gene_cor_vect[gene_idx])
    return(gene_names[gene_idx], gene_cor_vect[gene_idx], gene_idx)


def get_gene_cor_and_idx(gene_names, goi, gene_cor_vect):
    try:
        gene_idx = np.where(np.array(gene_names)==goi)[0][0]
    except:
        ## if we couldn't find the gene
        print("WARNING: couldn't find gene of interest:",goi)
        return(None,None)
    return(gene_cor_vect[gene_idx], gene_idx)


@ray.remote
def ray_scatter_wrapper(arg_list):
    for args in arg_list:
        ray_plot_scatter(*args)
    return()

def ray_plot_scatter(cell_embeddings,
                     gene_cor,
                     expanded_color_vect,
                     temp_gene,
                     out_dir,
                     lineage_path,
                     gene_name="",
                     do_rank = True,
                     y_jitter = True):
    fig = plt.figure()
    valid_indices = np.where(np.logical_not(np.isnan(cell_embeddings)))[0]
    ## subset the gene_subset for 
    try:
        gene_subset = temp_gene[valid_indices]
    except:
        gene_subset = temp_gene[:,valid_indices]
    #print("gene index:",gene_idx)
    if do_rank:
        x = rankdata(cell_embeddings[valid_indices], method="dense")
        y = rankdata(gene_subset,method="dense")
    else:
        x = cell_embeddings[valid_indices]
        y = gene_subset
    if y_jitter:
        y=y+np.random.random(valid_indices.shape)
    try:
        plt.scatter(x, y,
                   s=1,
                   c = expanded_color_vect[valid_indices,:])
    except:
        plt.scatter(x, y,
                   s=1,
                   c = expanded_color_vect[valid_indices])
    temp_title = str(gene_name)+'\nRho:'+str(round(gene_cor,2))
    fig.suptitle(temp_title, fontsize=15)
    path_name = "_".join(map(str,lineage_path))
    out_file = os.path.join(out_dir,path_name+"|"+gene_name+".png")
    plt.savefig(out_file,
                dpi=600,
                bbox_inches='tight')
    return


def plot_scatter(cell_embeddings,
                 gene_cor_vect,
                 cluster_dict,
                 full_expression,
                 out_dir,
                 lineage_path,
                 do_rank = True,
                 gene_names=None,
                 plot_min=False,
                 plot_max=False,
                 gene_idx=None,
                 goi = None,
                 y_jitter = True,
                 alias = None):
    fig = plt.figure()
    valid_indices = np.where(np.logical_not(np.isnan(cell_embeddings)))[0]
    expanded_color_vect = np.array([cluster_dict["color_vect"][i] for i in cluster_dict["linear_groups"]])
    #print("gene index:",gene_idx)
    if plot_min and gene_idx is None and goi is None:
        gene_idx=np.where(gene_cor_vect == np.nanmin(gene_cor_vect))[0][0]
        print("min:",gene_names[gene_idx],":",gene_cor_vect[gene_idx])
        #temp_gene = full_expression[gene_idx,:]
    #print("gene index:",gene_idx)
    if plot_max and gene_idx is None and goi is None:
        gene_idx=np.where(gene_cor_vect == np.nanmax(gene_cor_vect))[0][0]
        print("max:",gene_names[gene_idx],":",gene_cor_vect[gene_idx])
        #temp_gene = full_expression[gene_idx,:]
    #print("gene index:",gene_idx)
    if gene_idx is None and goi is not None:
        gene_idx = np.where(np.array(gene_names)==goi)[0][0]
    #print("gene index:",gene_idx)
    if gene_idx is not None:
        temp_gene = full_expression[gene_idx,:]
        gene_subset = temp_gene[valid_indices]
    else:
        gene_subset = temp_gene[:,valid_indices]
    #print("gene index:",gene_idx)
    if do_rank:
        x = rankdata(cell_embeddings[valid_indices], method="dense")
        y = rankdata(gene_subset,method="dense")
    else:
        x = cell_embeddings[valid_indices]
        y = gene_subset
    if y_jitter:
        y=y+np.random.random(valid_indices.shape)
    try:
        plt.scatter(x, y,
                   s=1,
                   c = expanded_color_vect[valid_indices,:])
    except:
        plt.scatter(x, y,
                   s=1,
                   c = expanded_color_vect[valid_indices])
    if alias is None:
        temp_title = str(gene_names[gene_idx])+'\nRho:'+str(round(gene_cor_vect[gene_idx],2))
    else:
        temp_title = str(alias)+'\nRho:'+str(round(gene_cor_vect[gene_idx],2))
    fig.suptitle(temp_title, fontsize=15)
    path_name = "_".join(map(str,lineage_path))
    out_file = os.path.join(out_dir,path_name+"|"+gene_names[gene_idx]+".png")
    plt.savefig(out_file,
                dpi=600,
                bbox_inches='tight')
    return


@ray.remote
def ray_parallel_fade(all_alpha_list, pos3d, frame_indices_list, temp_out_dir, expanded_color_vect, full_path=None):
    for current_frame in frame_indices_list:
        temp_alpha_vect = all_alpha_list[current_frame]
        print("working on frame:",current_frame)
        print(temp_alpha_vect)
        angle = 0
        node_size = 2.5
        edge_width = 2.5/np.sqrt(len(list(pos3d.keys())))
        plt.clf()
        fig = plt.figure(figsize=(10,7))
        ax = Axes3D(fig)
        ax.view_init(30, 0)
        ## plot the nodes
        for key, value in pos3d.items():
            temp_alpha = temp_alpha_vect[key]
            # if key%1000 == 0:
            #     print("plotting point#",key)
            xi = value[0]
            yi = value[1]
            zi = value[2]
            # Scatter plot
            dummy_point = ax.scatter(xi, yi, zi, c=[expanded_color_vect[key]], s=node_size, linewidths = 0, alpha=temp_alpha)
        ## plot the lines
        if full_path is not None:
            path_edges = set(zip(full_path,full_path[1:]))
            for i,j in enumerate(path_edges):
                #print(i,j)
                x = np.array((pos3d[j[0]][0], pos3d[j[1]][0]))
                y = np.array((pos3d[j[0]][1], pos3d[j[1]][1]))
                z = np.array((pos3d[j[0]][2], pos3d[j[1]][2]))
                # Plot the connecting lines
                #print(x,y,z)
                #temp_line_alpha = max([np.min(temp_alpha)/.75,.25])
                temp_line_alpha = max([np.min(temp_alpha)/.75,0])
                dummy_line = ax.plot(x, y, z, c='black', linewidth = 6, alpha = temp_line_alpha)
        ## save it
        out_file = os.path.join(temp_out_dir,"frame_"+str(current_frame)+".jpg")
        ax.set_axis_off()
        plt.savefig(out_file,
                    dpi=175,
                    bbox_inches='tight')
    return()


def one_d_vect_to_3d_pos_dict(cell_embeddings):
    pos={}
    for idx in range(cell_embeddings.shape[0]):
        pos[idx]=np.array([cell_embeddings[idx],0,0])
    return(pos)


####################
## this block from here: https://stackoverflow.com/questions/50299172/python-range-or-numpy-arange-with-end-limit-include
def cust_range(*args, rtol=1e-05, atol=1e-08, include=[True, False]):
    """
    Combines numpy.arange and numpy.isclose to mimic
    open, half-open and closed intervals.
    Avoids also floating point rounding errors as with
    >>> numpy.arange(1, 1.3, 0.1)
    array([1. , 1.1, 1.2, 1.3])

    args: [start, ]stop, [step, ]
        as in numpy.arange
    rtol, atol: floats
        floating point tolerance as in numpy.isclose
    include: boolean list-like, length 2
        if start and end point are included
    """
    # process arguments
    if len(args) == 1:
        start = 0
        stop = args[0]
        step = 1
    elif len(args) == 2:
        start, stop = args
        step = 1
    else:
        assert len(args) == 3
        start, stop, step = tuple(args)
    # determine number of segments
    n = (stop-start)/step + 1
    # do rounding for n
    if np.isclose(n, np.round(n), rtol=rtol, atol=atol):
        n = np.round(n)
    # correct for start/end is exluded
    if not include[0]:
        n -= 1
        start += step
    if not include[1]:
        n -= 1
        stop -= step
    return np.linspace(start, stop, int(n))

def crange(*args, **kwargs):
    return cust_range(*args, **kwargs, include=[True, True])

def orange(*args, **kwargs):
    return cust_range(*args, **kwargs, include=[True, False])


###################


def linear_norm_pos_dict(pos, axes = None):
    all_keys = list(pos.keys())
    dim = pos[all_keys[0]].shape
    if axes is None:
        axes = np.arange(dim[0]).tolist()
    min_vect = np.zeros(dim)
    max_vect = np.zeros(dim)
    ## get the mins and maxes
    for key, value in pos.items():
        for axis in range(dim[0]):
            min_vect[axis] = min([min_vect[axis],value[axis]])
    ## subtract the mins
    for key, value in pos.items():
        for axis in range(dim[0]):
            if axis in axes:
                temp_vect = value
                temp_vect[axis]=temp_vect[axis]-min_vect[axis]
                pos[key]=temp_vect
    ## divide by maxes
    ## get the mins and maxes
    for key, value in pos.items():
        for axis in range(dim[0]):
            max_vect[axis] = max([max_vect[axis],value[axis]])
    for key, value in pos.items():
        for axis in range(dim[0]):
            if axis in axes:
                temp_vect = value
                temp_vect[axis]=temp_vect[axis]/max_vect[axis]
                pos[key]=temp_vect
    return(pos)


def update_loc(orig_vect, rate_of_change, current_frame):
    return(orig_vect + (rate_of_change * (current_frame+1)))


@ray.remote
def unfold_subset(frame_indices_list,
                  temp_pos3d,
                  rate_of_change,
                  expanded_color_vect,
                  temp_out_dir,
                  frame_count_offset,
                  total_frames=30,
                  full_path=None,
                  alpha = 0.7):
    for current_frame in frame_indices_list:
        #temp_pos3d = pos_list[current_frame]
        print("working on frame:",current_frame)
        angle = 0
        node_size = 2.5
        edge_width = 2.5/np.sqrt(len(list(temp_pos3d.keys())))
        plt.clf()
        fig = plt.figure(figsize=(10,7))
        ax = Axes3D(fig)
        ## start out at (30,0) need to get to 270
        #angle_vect = crange(360,270,-90/len(pos_list))
        angle_vect1 = crange(30,-90,(-90-30)/(total_frames-1))
        angle_vect2 = crange(0,-90,-90/(total_frames-1))
        #ax.view_init(angle_vect[current_frame], 90)
        ax.view_init(angle_vect1[current_frame], angle_vect2[current_frame])
        #ax.view_init(-90,90)
        ## plot the nodes
        valid_points = set(rate_of_change.keys())
        for key in valid_points:
            value = temp_pos3d[key]
            #for key, value in temp_pos3d.items():
            # if key%1000 == 0:
            #     print("plotting point#",key)
            new_value = update_loc(value, rate_of_change[key], current_frame)
            xi = new_value[0]
            yi = new_value[1]
            zi = new_value[2]
            # Scatter plot
            dummy_point = ax.scatter(xi, yi, zi, c=[expanded_color_vect[key]], s=node_size, linewidths = 0, alpha=alpha)
        ## plot the lines
        if full_path is not None:
            path_edges = set(zip(full_path,full_path[1:]))
            for i,j in enumerate(path_edges):
                #print(i,j)
                start_loc = update_loc(temp_pos3d[j[0]], rate_of_change[j[0]], current_frame)
                end_loc = update_loc(temp_pos3d[j[1]], rate_of_change[j[1]], current_frame)
                x = np.array((start_loc[0], end_loc[0]))
                y = np.array((start_loc[1], end_loc[1]))
                z = np.array((start_loc[2], end_loc[2]))
                # Plot the connecting lines
                #print(x,y,z)
                dummy_line = ax.plot(x, y, z, c='black', linewidth = 6, alpha = 0.25)
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_zlim(0,1)
        #plt.show()
        #ax.set_axis_off()
        ## save it
        out_file = os.path.join(temp_out_dir,"frame_"+str(current_frame+frame_count_offset)+".jpg")
        plt.savefig(out_file,
                    dpi=175,
                    bbox_inches='tight')
    return()


def unfold_3d(cell_embeddings,
              pos3d,
              expanded_color_vect,
              temp_out_dir,
              full_path=None,
              fade_rate = 0.05,
              initial_alpha = 0.7,
              processes = None):
    current_frame = 0
    print("plotting the path in 3D")
    angle = 0
    node_size = 2.5
    edge_width = 2.5/np.sqrt(cell_embeddings.shape[0])
    plt.clf()
    fig = plt.figure(figsize=(10,7))
    ax = Axes3D(fig)
    ax.view_init(30, 0)
    ## plot the edges
    for key, value in pos3d.items():
        if key%1000 == 0:
            print("plotting point#",key)
        xi = value[0]
        yi = value[1]
        zi = value[2]
        # Scatter plot
        dummy_point = ax.scatter(xi, yi, zi, c=[expanded_color_vect[key]], s=node_size, linewidths = 0, alpha=0.7)
    if full_path is not None:
        path_edges = set(zip(full_path,full_path[1:]))
        for i,j in enumerate(path_edges):
            #print(i,j)
            x = np.array((pos3d[j[0]][0], pos3d[j[1]][0]))
            y = np.array((pos3d[j[0]][1], pos3d[j[1]][1]))
            z = np.array((pos3d[j[0]][2], pos3d[j[1]][2]))
            # Plot the connecting lines
            #print(x,y,z)
            dummy_line = ax.plot(x, y, z, c='black', linewidth = 6)
            ## try to make the animation
            #animation = FuncAnimation(fig, func=animate_3d_spin, frames=range(360), interval=10)
            #plt.show()
            ## set the camera and save
    ax.set_axis_off()
    ## plot the original scene
    out_file = os.path.join(temp_out_dir,"frame_"+str(current_frame)+".jpg")
    current_frame+=1
    plt.savefig(out_file,
                dpi=175,
                bbox_inches='tight')
    ## fade out the non-pertinent cells
    alpha_vect = np.ones(cell_embeddings.shape) * initial_alpha
    alpha_delta_vect = np.array(np.isnan(cell_embeddings),dtype=float)* -1 * fade_rate
    all_alpha_list = []
    while np.min(alpha_vect) > 0:
        print(np.min(alpha_vect),np.max(alpha_vect))
        alpha_vect += alpha_delta_vect
        alpha_vect[alpha_vect<0] = 0
        all_alpha_list.append(deepcopy(alpha_vect))
    ## make sure it actually went to zero - sometimes it doesn't b/c of floating point error
    alpha_vect += alpha_delta_vect
    alpha_vect[alpha_vect<0] = 0
    all_alpha_list.append(alpha_vect)
    ## now plot them
    ray.init()
    ray_calls = []
    if processes==None:
        processes = multiprocessing.cpu_count()
    ray_pos3d = ray.put(pos3d)
    frame_indices_list = get_indices(processes,len(all_alpha_list))
    for i in range(len(frame_indices_list)):
        ray_calls.append(ray_parallel_fade.remote(all_alpha_list, ray_pos3d, frame_indices_list[i], temp_out_dir, expanded_color_vect, full_path))
    ray.get(ray_calls)
    ray.shutdown()
    ## now unfold
    valid_indices = np.where(np.logical_not(np.isnan(cell_embeddings)))[0].tolist()
    rank_embeddings = deepcopy(cell_embeddings)
    rank_embeddings[valid_indices] = rankdata(cell_embeddings[valid_indices],method="dense")
    #pos_list = pos1_to_pos2_interpolate(linear_norm_pos_dict(pos3d),linear_norm_pos_dict(one_d_vect_to_3d_pos_dict(rankdata(cell_embeddings,method="dense")),[0]))
    rate_of_change, total_frames = pos1_to_pos2_interpolate(linear_norm_pos_dict(pos3d),linear_norm_pos_dict(one_d_vect_to_3d_pos_dict(rank_embeddings),[0]))
    index_lists = get_indices(processes,total_frames)
    ray_calls = []
    ray.init()
    ray_pos3d = ray.put(pos3d)
    ray_rate_of_change = ray.put(rate_of_change)
    for idx_list in index_lists:
        # unfold_subset(frame_indices_list,
        #           temp_pos3d,
        #           pos_rate_of_change,
        #           expanded_color_vect,
        #           temp_out_dir,
        #           frame_count_offset,
        #           total_frames=30,
        #           full_path=None,
        #           alpha = 0.7)
        ray_calls.append(unfold_subset.remote(idx_list,
                                              ray_pos3d,
                                              ray_rate_of_change,
                                              expanded_color_vect,
                                              temp_out_dir,
                                              len(all_alpha_list),## just for continuing the count
                                              total_frames = total_frames,
                                              full_path=full_path,
                                              alpha = 0.7))
    ray.get(ray_calls)
    ray.shutdown()
    return()


def get_continuous_lineage_pseudotimes(exemplar_indices,
                                       lineage_dict,
                                       distance_mat,
                                       subject_network,
                                       mean_express_array,
                                       sample_k_lists,
                                       full_expression,
                                       gene_names,
                                       out_dir,
                                       linear_groups,
                                       cluster_dict,
                                       stem_cell_id = None,
                                       processes = None,
                                       plot = True,
                                       goi_dict = {},
                                       seed = 123456):
    ## first get the stem cell & lineage paths for each connected component of the lineage graph
    all_lineage_paths = get_all_lineage_paths(lineage_dict, stem_cell_id=stem_cell_id)
    small_dist_mat = get_small_distance_mat(distance_mat, exemplar_indices, scale=False)
    ## invert the weights in the network so that the weighted shortest paths 
    ## correctly views it as distance rather than connection strength
    #subject_network2 = reverse_weights(subject_network)
    expanded_color_vect = [cluster_dict["color_vect"][i] for i in cluster_dict["linear_groups"]]
    lineage_path = all_lineage_paths[1]
    #lineage_path = all_lineage_paths[-1]
    all_cell_embeddings = []
    all_gene_cor = []
    all_cutoffs = []
    gene_ordering_dicts = []
    temp_out_dirs = []
    two_d_embed_scatters_dirs = []
    three_d_spin_dirs = []
    gene_progression_dirs = []
    ## now go through each lineage path
    all_results = {}
    if plot:
        pos, pos3d = get_positions(subject_network, lineage_dict, sample_k_lists, np.array(cluster_dict["transition_probability"].data), seed = seed)
        all_results["pos"]=pos
        all_results["pos3d"]=pos3d
    for lineage_path in all_lineage_paths:
        print(lineage_path)
        temp_out_dir = process_dir(os.path.join(out_dir,'_'.join(map(str,deepcopy(lineage_path)))))
        two_d_embed_scatters = process_dir(os.path.join(temp_out_dir,'pseudotime_scatters'))
        three_d_spin_dir = process_dir(os.path.join(temp_out_dir,'threeD_spin'))
        gene_progression_dir = process_dir(os.path.join(temp_out_dir,'ordered_gene_progression'))
        ## log where they are
        temp_out_dirs.append(temp_out_dir)
        two_d_embed_scatters_dirs.append(two_d_embed_scatters) 
        three_d_spin_dirs.append(three_d_spin_dir)
        gene_progression_dirs.append(gene_progression_dir)
        ## get the shortest path between all of the exemplars and other cells in the embedding matrix
        cell_embeddings, full_path = get_pertienent_cells_and_ordered_mat(small_dist_mat, 
                                                                         distance_mat, 
                                                                         subject_network, 
                                                                         lineage_path, 
                                                                         exemplar_indices, 
                                                                         sample_k_lists,
                                                                         processes,
                                                                         three_d_spin_dir,
                                                                         linear_groups)
        # len(set(cell_embeddings[np.logical_not(np.isnan(cell_embeddings))]))
        # cell_embeddings[np.logical_not(np.isnan(cell_embeddings))].shape
        # np.nanmax(cell_embeddings)
        # cell_embeddings == np.nanmax(cell_embeddings)
        # np.sum(cell_embeddings == np.nanmax(cell_embeddings))
        # np.sum(cell_embeddings == np.nanmin(cell_embeddings))
        all_cell_embeddings.append(cell_embeddings)
        ##
        ## now that we have an "X-axis" (pseudotime-like) embedding of all cells along the trajectory,
        ## subset the original expression matrix, (maybe just throw it into memmory?)
        ## 1) recalculate the null background and actual correlations of X embeddings vs Y expression
        ## 2) using that empiric FPR cutoff, and actual spearman rhos
        ## 2.1) segregate the genes into positive and negative
        ## 2.2) assign the significant genes to a cell-type level position along the X-embedding
        ##
        ## now we'll get the gene level correlations
        print("getting correlations of all genes with this trajectory")
        gene_cor_vect, null_cor_vect, cutoff = get_embedding_correlations(cell_embeddings, full_expression)
        all_gene_cor.append(gene_cor_vect)
        all_cutoffs.append(cutoff)
        gene_ordering_dicts.append(get_cell_type_gene_halfway_point(mean_express_array,
                                                                          gene_names,
                                                                          gene_cor_vect,
                                                                          cutoff,
                                                                          lineage_path,
                                                                          gene_progression_dir))
        if plot:
            if processes == 1:
                plot_scatter(cell_embeddings,gene_cor_vect,cluster_dict,full_expression,two_d_embed_scatters,lineage_path,gene_names=gene_names,plot_min=True)
                plot_scatter(cell_embeddings,gene_cor_vect,cluster_dict,full_expression,two_d_embed_scatters,lineage_path,gene_names=gene_names,plot_max=True)
                for goi, alias in goi_list.items():
                    plot_scatter(cell_embeddings,gene_cor_vect,cluster_dict,full_expression,two_d_embed_scatters,lineage_path,gene_names=gene_names,goi=goi, alias = alias)
            else:
                ray.init()
                ray_args = []
                # (cell_embeddings,
                #      gene_cor,
                #      expanded_color_vect,
                #      temp_gene,
                #      out_dir,
                #      lineage_path,
                #      gene_name="",
                #      do_rank = True,
                #      y_jitter = True)
                ## add the min and max
                # min
                expanded_color_vect = np.array([cluster_dict["color_vect"][i] for i in cluster_dict["linear_groups"]])
                name, cor, idx = get_max_name_cor_idx(gene_names,gene_cor_vect)
                ray_args.append((cell_embeddings,
                                                         cor,
                                                         expanded_color_vect,
                                                         full_expression[idx,:],
                                                         two_d_embed_scatters,
                                                         lineage_path,
                                                         name))
                # max
                name, cor, idx = get_min_name_cor_idx(gene_names,gene_cor_vect)
                ray_args.append((cell_embeddings,
                                                         cor,
                                                         expanded_color_vect,
                                                         full_expression[idx,:],
                                                         two_d_embed_scatters,
                                                         lineage_path,
                                                         name))
                ## now add the genes of interest
                for orig_id, alias in goi_dict.items():
                    cor, idx = get_gene_cor_and_idx(gene_names, orig_id, gene_cor_vect)
                    if idx is not None:
                        ray_args.append((cell_embeddings,
                                                                 cor,
                                                                 expanded_color_vect,
                                                                 full_expression[idx,:],
                                                                 two_d_embed_scatters,
                                                                 lineage_path,
                                                                 alias))
                ray_calls = ray_get_indices_from_list(processes, ray_args)
                for i in range(len(ray_calls)):
                    ray_calls[i]=ray_scatter_wrapper.remote(ray_calls[i])
                ## now 
                ray.get(ray_calls)
                ray.shutdown()
            ## now plot in 3D!
            plot_3d(subject_network, 
                    pos3d, 
                    expanded_color_vect, 
                    three_d_spin_dir, 
                    full_path=full_path,
                    processes=processes)
            unfold_3d(cell_embeddings,
                      pos3d,
                      expanded_color_vect,
                      three_d_spin_dir,
                      full_path=full_path,
                      fade_rate = 0.05,
                      initial_alpha = 0.7,
                      processes=processes)
    all_results["all_lineage_paths"]=all_lineage_paths
    all_results["all_cell_embeddings"]=all_cell_embeddings
    all_results["all_gene_cor"]=all_gene_cor
    all_results["all_cutoffs"]=all_cutoffs
    all_results["gene_ordering_dicts"]=gene_ordering_dicts
    all_results["expanded_color_vect"]=expanded_color_vect
    all_results["temp_out_dir"] = temp_out_dirs
    all_results["two_d_embed_scatters"] = two_d_embed_scatters_dirs
    all_results["three_d_spin_dir"] = three_d_spin_dirs
    all_results["gene_progression_dir"] = gene_progression_dirs
    return(all_results)


def do_continuous_lineage_analysis(infile,
                                   distance_mat_file,
                                   lineage_dict_file,
                                   cluster_dict_file,
                                   subject_network_file,
                                   mean_express_file,
                                   out_dir,
                                   hdf5=False,
                                   cols = None,
                                   gene_names = None,
                                   stem_cell_id = None,
                                   plot=True,
                                   processes = None,
                                   goi_file=None,
                                   seed=123456,
                                   human_symbol_dict_file = None):
    ###########
    lineage_dict = import_dict(lineage_dict_file)
    ###########
    if hdf5:
        row_names = read_file(gene_names,'lines')
        title = read_file(cols,'lines')
        print('reading in hdf5 file')
        h5f = h5py.File(infile, 'r')
        full_expression=h5f["infile"]
    else:
        full_expression_str = read_table(infile)
        title = full_expression_str[0]
        full_expression_np = np.array(full_expression_str)
        row_names = full_expression_np[1:,0]
        full_expression = np.array(full_expression_np[1:,1:],dtype = float)
    mean_express_array = np.array(np.array(read_table(mean_express_file))[1:,1:],dtype = float)
    #
    cell_names = title[1:]
    cluster_dict = import_dict(cluster_dict_file)
    linear_groups = cluster_dict["linear_groups"]#np.array(np.array(read_table(cluster_file))[:,1],dtype=float).tolist()
    sample_k_lists = get_sample_k_lists(linear_groups)
    ## get the exemplars
    exemplar_indices = cluster_dict["exemplar_indices"]
    ## read in the distance matrix hdf5
    dist_mat_h5 = h5py.File(distance_mat_file, 'r')
    distance_mat = dist_mat_h5["infile"]
    ## import the subject/cell network
    subject_network = import_dict(subject_network_file)
    #
    if processes == None:
        processes = multiprocessing.cpu_count()
    #
    if goi_file is not None:
        temp_goi_table = read_table(goi_file)
        goi_dict = {}
        if len(temp_goi_table[0]) == 2:
            for line in temp_goi_table:
                goi_dict[line[0]]=line[1]
        elif len(temp_goi_table[0]) == 1:
            for line in temp_goi_table:
                goi_dict[line[0]]=line[0]
        else:
            sys.exit("something wrong with GOI table.\n"+str(len(temp_goi_table[0]))+"columns")
    else:
        goi_dict = {}
    ## do the analysis after processing
    all_results = get_continuous_lineage_pseudotimes(exemplar_indices,
                                                     lineage_dict,
                                                     distance_mat,
                                                     subject_network,
                                                     mean_express_array,
                                                     sample_k_lists,
                                                     full_expression,
                                                     row_names,
                                                     out_dir,
                                                     linear_groups,
                                                     cluster_dict,
                                                     plot=plot,
                                                     stem_cell_id = stem_cell_id,
                                                     processes = processes,
                                                     goi_dict = goi_dict,
                                                     seed = 123456)
    do_lincs_lineage(all_results,human_symbol_dict_file,out_dir)
    return(all_results)


#####################################################################################

def get_susbet_from_up_down(i, cell_type_index_vect, up_dict, down_dict):
    cur_cell_type = cell_type_index_vect[i]
    up_ids = [key for key, value in up_dict.items() if value==cur_cell_type]
    down_ids = [key for key, value in down_dict.items() if value==cur_cell_type]
    #print(i,len(up_ids),"up")
    #print(i,len(down_ids),"down")
    return(up_ids, down_ids)


def write_up_down_res(up_down_dict, cell_type_index_vect, gene_progression_dir, cell_cycle_dict = None, human_symbol_dict = None, reverse = False):
    ## reorganize them to group them by the cell-type that they rise and fall on
    if reverse:
        print("REVERSING")
        cell_type_index_vect = cell_type_index_vect[::-1]
        global_down = list(up_down_dict["pos"].keys())
        global_up = list(up_down_dict["neg"].keys())
        down_dict = up_down_dict["pos"]
        up_dict = up_down_dict["neg"]
    else:
        global_up = list(up_down_dict["pos"].keys())
        global_down = list(up_down_dict["neg"].keys())
        down_dict = up_down_dict["neg"]
        up_dict = up_down_dict["pos"]
    traj_id = "start:"+"_".join(map(str,cell_type_index_vect))+":end"
    top_dir = process_dir(os.path.join(gene_progression_dir,traj_id))
    full_traj_dir = process_dir(os.path.join(top_dir, "full_trajectory"))
    #full_traj_dir = process_dir(os.path.join(gene_progression_dir, str(cell_type_index_vect[0])+"_vs_"+str(cell_type_index_vect[-1])))
    ## do the forward
    ## going from beginning to the end will be pos cor
    #pos_dir = processes_dir(os.path.join(top_dir,str(cell_type_index_vect[-1])))
    #neg_dir = processes_dir(os.path.join(top_dir,"towards_"+str(cell_type_index_vect[0])))
    all_genes_changed_on_traj = global_up + global_down
    all_up_genes = '\n'.join(list(map(str,global_up)))
    all_down_genes = '\n'.join(list(map(str,global_down)))
    ## write the global up and down along the trajectory
    fwd_file = os.path.join(full_traj_dir,str(cell_type_index_vect[-1])+'.txt')
    rev_file = os.path.join(full_traj_dir,str(cell_type_index_vect[0])+'.txt')
    make_file(all_up_genes,fwd_file)
    make_file(all_down_genes,rev_file)
    if human_symbol_dict != None:
        out_file = os.path.join(full_traj_dir,"one_shot_drugs:"+"_".join(map(str,cell_type_index_vect))+"_single_treatments.tsv")
        print(out_file)
        do_single_lincs_analysis_from_files(fwd_file,
                                            rev_file, 
                                            cell_cycle_dict, 
                                            human_symbol_dict, 
                                            out_file)
    ## now go through the step-wise results and write them
    all_stages = []
    cell_type_id = []
    all_lincs_files = [out_file]
    for i in range(len(cell_type_index_vect)):
        up_ids, down_ids = get_susbet_from_up_down(i, cell_type_index_vect, up_dict, down_dict)
        if len(up_ids)+len(down_ids) > 0:
            all_stages.append([up_ids, down_ids])
            cell_type_id.append(cell_type_index_vect[i])
    if len(all_stages)>1:
        ## if there's only one stage, then just keeping all 
        for i in range(len(all_stages)):
            stage_id = "stage_"+str(i+1)+":inflection_point_at_cluster:"+str(cell_type_id[i])
            temp_stage_dir = process_dir(os.path.join(top_dir,stage_id))
            stage_prefix = traj_id+"|"+"stage_"+str(i+1)
            temp_up_file = os.path.join(temp_stage_dir,stage_prefix+"_up.txt")
            temp_down_file = os.path.join(temp_stage_dir,stage_prefix+"_down.txt")
            up_save='\n'.join(map(str,deepcopy(all_stages[i][0])))
            down_save='\n'.join(map(str,deepcopy(all_stages[i][1])))
            make_file(up_save, temp_up_file)
            make_file(down_save, temp_down_file)
            print(stage_id)
            lincs_out_file = os.path.join(temp_stage_dir,stage_prefix+"_single_treatments.tsv")
            all_lincs_files.append(lincs_out_file)
            do_single_lincs_analysis_from_files(temp_up_file,
                                            temp_down_file, 
                                            cell_cycle_dict, 
                                            human_symbol_dict, 
                                            lincs_out_file)
    return(all_lincs_files)


def do_lincs_lineage(all_results, human_symbol_dict_file, master_out_dir):
    if type(human_symbol_dict_file)==dict:
        pass
    else:
        human_symbol_dict, human_def_dict = import_dict(human_symbol_dict_file)
    if human_symbol_dict != None:
        all_lincs_files = []
        cell_cycle_dict = get_cell_cycle(human_symbol_dict)
        for i in range(len(all_results["gene_ordering_dicts"])):
            up_down_dict = all_results["gene_ordering_dicts"][i]
            cell_type_index_vect = all_results["all_lineage_paths"][i]
            gene_progression_dir = all_results["gene_progression_dir"][i]
            all_lincs_files += write_up_down_res(up_down_dict, 
                                                      cell_type_index_vect, 
                                                      gene_progression_dir, 
                                                      cell_cycle_dict,
                                                      human_symbol_dict)
            all_lincs_files += write_up_down_res(up_down_dict, 
                                                      cell_type_index_vect, 
                                                      gene_progression_dir, 
                                                      cell_cycle_dict,
                                                      human_symbol_dict,
                                                      reverse = True)
        collate_lincs(master_out_dir, all_lincs_files)
    return()


#####################################################################################
if __name__ == "__main__":
    ###########################################################
    parser = argparse.ArgumentParser()

    parser.add_argument("-infile", '-i',
        help="the original input dataset.")

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

    parser.add_argument("-human_symbol_dict", 
                        help="the pickled file created by pyminer_gprofiler_converter.py. This is typically 'human_orthologues.pkl'",
                        type = str)

    parser.add_argument("-distance_mat", '-dm',
                        help="the path to the full distance matrix as hdf5. Usually called 'sample_clustering_and_summary/rho_dicts/neg_euc_dist.hdf5'.")

    parser.add_argument("-lineage_dict_file", '-ld',
                        help="the lineage dictionary generated by lineage_analysis.py. This will usually be called 'lineage_dict.pkl'")

    parser.add_argument("-subject_network_file")
    
    parser.add_argument("-mean_express_file")

    parser.add_argument("-out_dir", '-o',
        help="the directory for the ouptut")

    args = parser.parse_args()
    ###########################################################
    all_results = do_continuous_lineage_analysis(args.infile,
                                             args.distance_mat_file,
                                             args.lineage_dict_file,
                                             args.cluster_dict_file,
                                             args.subject_network_file,
                                             args.mean_express_file,
                                             args.out_dir,
                                             goi_file = args.goi_file,
                                             hdf5=args.hdf5,
                                             cols = args.columns,
                                             gene_names = args.ID_list,
                                             stem_cell_id = None,
                                             plot=plot,
                                             processes = args.processes,
                                             seed = args.seed,
                                             human_symbol_dict_file = args.human_symbol_dict)
    ############################################################

initial_alpha=0.7
fade_rate=0.05
plot=False
processes = None
stem_cell_id = None
hdf5 = True
cols = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/column_IDs.txt"
gene_names = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/ID_list.txt"
infile = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/ind4567_merged_cr1258inf_sr5011inf_log2.hdf5"
lineage_dict_file = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/lineage_analysis/lineage_dict.pkl"
distance_mat_file = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/sample_clustering_and_summary/rho_dicts/neg_euc_dist.hdf5"
cluster_dict_file = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/sample_clustering_and_summary/clustering_plots.pkl"
subject_network_file = '/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/sample_clustering_and_summary/cell_embedding.graphpkl'
cluster_file = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/sample_clustering_and_summary/sample_k_means_groups.txt"
mean_express_file = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/sample_clustering_and_summary/k_group_means.txt"
out_dir = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/lineage_analysis/trajectory_plots/"
goi_file = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/goi.txt"
human_symbol_dict_file = "/home/scott/Documents/scRNAseq/human_breast_cancer_organoid_GSE113196/analysis/annotations.pkl"
seed = 123456


all_results = do_continuous_lineage_analysis(infile,
                                             distance_mat_file,
                                             lineage_dict_file,
                                             cluster_dict_file,
                                             subject_network_file,
                                             mean_express_file,
                                             out_dir,
                                             goi_file = goi_file,
                                             hdf5=hdf5,
                                             cols = cols,
                                             gene_names = gene_names,
                                             stem_cell_id = None,
                                             plot=plot,
                                             processes = processes,
                                             seed = seed,
                                             human_symbol_dict_file=human_symbol_dict_file)

