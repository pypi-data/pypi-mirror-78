#!/usr/bin/env python3
import argparse
import fileinput
import os
import sys
from copy import deepcopy
import numpy as np
import pickle
from sklearn import metrics
import networkx as nx

try:
    from pyminer.common_functions import *
    from pyminer.pyminer_ensembl_rest import get_genes_from_locus, EnsemblRestClient
except:
    from common_functions import *
    from pyminer_ensembl_rest import get_genes_from_locus, EnsemblRestClient
#####################################################################

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

# def make_table(lines,delim, num_type = float):
#     #print(num_type)
#     for i in range(0,len(lines)):
#         lines[i]=lines[i].strip()
#         lines[i]=lines[i].split(delim)
#         for j in range(0,len(lines[i])):
#             try:
#                 float(lines[i][j])
#             except:
#                 lines[i][j]=lines[i][j].replace('"','')
#             else:
#                 if num_type == float:
#                     lines[i][j]=float(lines[i][j])
#                 elif num_type == int:
#                     lines[i][j]=int(float(lines[i][j]))
#                 else:
#                     lines[i][j]=num_type(lines[i][j])
#     return(lines)


# def strip_split(line, delim = '\t'):
#     return(line.strip('\n').split(delim))

# def get_file_path(in_path):
#     in_path = in_path.split('/')
#     in_path = in_path[:-1]
#     in_path = '/'.join(in_path)
#     return(in_path+'/')

# def read_table(file, sep='\t',num_type=float):
#     return(make_table(read_file(file,'lines'),sep,num_type=num_type))
    
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

#####################################################################

#####################################################################

def get_contigs(in_file):
    temp_contigs = []
    first = True
    for line in fileinput.input(in_file):
        if first:
            first = False
        else:
            temp_line = strip_split(line)
            if temp_line[0] not in temp_contigs:
                temp_contigs.append(temp_line[0])
    fileinput.close()
    print("found these contigs:")
    for contig in temp_contigs:
        print("\t",contig)
    return(temp_contigs)


def populate_contig_dict(contig_dict, in_file):
    all_binding_sites = read_table(in_file)
    for i in range(1,len(all_binding_sites)):
        site = all_binding_sites[i]
        temp_cont = contig_dict[site[0]]
        temp_cont.append(site)
        contig_dict[site[0]] = temp_cont
    return(contig_dict)


def get_current_edges(cur_row, cur_index):
    cur_row = np.array(cur_row)
    indices = np.where(cur_row == True)[0]
    all_edges = []
    for index in indices:
        if index > cur_index:
            all_edges.append((cur_index,index))
    return(all_edges)


def get_insulator_sites_from_adj_mat(adj_mat):
    print(adj_mat)
    print("constructing graph")
    G = nx.Graph()
    G.add_nodes_from(list(range(adj_mat.shape[0])))
    for i in range(adj_mat.shape[0]):
        G.add_edges_from(get_current_edges(adj_mat[i,:],i))
    print("identifying connected components")
    comps = list(nx.connected_components(G))
    for i in range(len(comps)):
        comps[i] = sorted(list(map(int,list(comps[i]))))
    return(comps)


def get_rearranged_insulator_sites(non_gene_contig_list, insulator_site_lists):
    ## go through and replace the indices with the actual insulator site entry
    for i in range(len(insulator_site_lists)):
        for j in range(len(insulator_site_lists[i])):
            temp_idx = insulator_site_lists[i][j]
            insulator_site_lists[i][j] = non_gene_contig_list[temp_idx]
    return(insulator_site_lists)


def get_contig_gene_dict(lib_dir):
    ## read in the gene_contig_loci.tsv file
    ## "Gene stable ID","Gene name","Chromosome/scaffold name","Gene start (bp)","Gene end (bp)" <- has this header
    gene_annotations = np.array(read_table(os.path.expanduser(os.path.join(lib_dir, "gene_contig_loci.tsv")), num_convert = int))[1:,:]
    contigs = sorted(list(set(gene_annotations[:,2].tolist())))
    for i in range(len(contigs)):
        try:
            float(contigs[i])
        except:
            pass
        else:
            contigs[i] = str(int(float(contigs[i])))
    print("found these contigs in the gene reference file:\n\t",contigs)
    gene_contig_dict = {}
    for contig in contigs:
        ## find the indices for this contig
        #print("\n",contig)
        contig_indices = np.where(gene_annotations[:,2] == contig)[0]
        #print("contig_indices:",contig_indices)
        gene_contig_dict[contig] = gene_annotations[contig_indices,:]
        #print(gene_contig_dict[contig])
    return(gene_contig_dict)

##################################################
class gene_contig_lookup():
    def __init__(self,gene_cont_array):
        self.gene_cont_array = gene_cont_array
        print(self.gene_cont_array)
        
        self.processess_gene_cont_array()


    def get_return_lists(self):
        ## this is to match the chip binding site format
        ## chr, start, end, element(in this case gene), center, score(in this case "NA"), element_type(in this case "gene")
        self.return_list = []
        print("setting return lists")
        for i in range(self.gene_cont_array.shape[0]):
            temp_cont = self.gene_cont_array[i][2]
            start = self.start_bp_array[i]
            end = self.end_bp_array[i]
            center = self.center_bp_array[i]
            element = self.gene_cont_array[i][0]#+","+self.gene_cont_array[i][1]
            self.return_list.append([temp_cont,start,end,element,center,"NA","gene"])
            #print(self.return_list[-1])
        return


    def processess_gene_cont_array(self):
        temp_loci = np.array(self.gene_cont_array[:,np.array([3,4])],dtype = float)
        self.start_bp_array = np.min(temp_loci, axis = 1)
        self.end_bp_array = np.max(temp_loci, axis = 1)
        self.center_bp_array = np.mean(temp_loci, axis=1)
        self.gene_aray=self.gene_cont_array[:,0]
        self.symbol_array = self.gene_cont_array[:,2]
        self.contig_array = self.gene_cont_array[:,2]
        self.get_return_lists()
        return


    def check_for_uniform_direction(self,up1,up2,down1,down2):
        if up1 != up2:
            return(False)
        if up2 != down1:
            return(False)
        if down1 != down2:
            return(False)
        return(True)


    def get_genes(self, upstream_bp, downstream_bp):
        ## return all of the genes that have any degree of overlap with these start end end locations
        up_1_direction = np.array((self.start_bp_array-upstream_bp) >= 0, dtype = int)
        up_2_direction = np.array((self.end_bp_array-upstream_bp) >= 0, dtype = int)
        down_1_direction = np.array((self.start_bp_array-downstream_bp) >= 0, dtype = int)
        down_2_direction = np.array((self.end_bp_array-downstream_bp) >= 0, dtype = int)
        gene_loci = []
        sum_direction_array = up_1_direction+up_2_direction+down_1_direction+down_2_direction
        ## these are all of the indices where some elements are upstream, or downstream of the locus at hand, but they're not all uniformly up or down (0 or 4). This means that there is some locus overlap
        gene_indices = np.where((sum_direction_array>0) & (sum_direction_array<4))[0].tolist()
        for idx in gene_indices:
            gene_loci.append(self.return_list[idx])
        # for i in range(up_1_direction.shape[0]):
        #     ## if all of the elements are not uniformly positive or negative, it means that there is some
        #     ## overlap with this gene and the two loci provided
        #     if not self.check_for_uniform_direction(up_1_direction[i],up_2_direction[i],down_1_direction[i],down_2_direction[i]):
        #         # print(i)
        #         # print(self.return_list[i])
        #         gene_loci.append(self.return_list[i])
        return(gene_loci)

##################################################
def populate_contig_with_genes(all_insulator_sites, gene_contig_array):
    ## the insulator sites are a list of lists with all binding sites that should be linked together
    ## we need to figure out which genes to put in the chuncks in between those insulator sites, then add them to interveining lists of lists
    ## We'll iterate to the locations BETWEEN the insulator sites & populate a new array with genes that have
    if len(all_insulator_sites)==[]:
        if len(gene_contig_array)>0:
            return(gene_contig_array)
    try:
        all_insulator_sites[0][0][0]
    except:
        return()
        print(all_insulator_sites)
        print(gene_contig_array)
    # if all_insulator_sites[0][0][0]=="chrCHR_HG107_PATCH":
    #     print(all_insulator_sites)
    #     print(gene_contig_array)
    if type(gene_contig_array)==str:#"None":
        return(all_insulator_sites) 

    ###################
    ## prepare the gene contig for lookup 
    gene_lookup_obj = gene_contig_lookup(gene_contig_array)
    rearranged_contig = []

    #######################################################################
    ## first make a temprory pseudo-contig with only the insulator sites. We're mainly doing this to get the boundaries
    all_insulator_sites_contig = contig_obj("dummy",all_insulator_sites, finalize = False)

    ##### take care of the special case in which we're looking at the first locus - before the first insulator site
    ## first append the 
    temp_genes = gene_lookup_obj.get_genes(0,all_insulator_sites_contig.contig_tads[0].start)
    # print("\ngetting genes for beginning:")
    # print("\t",0,all_insulator_sites_contig.contig_tads[0].start)
    # for element in temp_genes:
    #     print(element)
    if len(temp_genes) > 0:
        rearranged_contig.append(temp_genes)
    ## append the first insulator locus
    rearranged_contig.append(all_insulator_sites[0])
    #####
    #sys.exit("done setting first set of genes")

    ## now take care of the middle
    for i in range(1,len(all_insulator_sites)-1):
        if i%100 == 0:
            print("\t",i,"/",len(all_insulator_sites))
        ## get the start and end location of this locus
        ################################################
        temp_start = all_insulator_sites_contig.contig_tads[i-1].end
        temp_end = all_insulator_sites_contig.contig_tads[i].start
        temp_genes = gene_lookup_obj.get_genes(temp_start, temp_end)
        rearranged_contig.append(temp_genes)
        ## then append the insulator locus
        rearranged_contig.append(all_insulator_sites[i])
        ################################################

    ## take care of the end - i.e. after the last insulator site
    rearranged_contig.append(all_insulator_sites[-1])
    temp_genes = gene_lookup_obj.get_genes(all_insulator_sites_contig.contig_tads[-1].end,9999999999)
    if len(temp_genes)>0:
        rearranged_contig.append(temp_genes)
    return(rearranged_contig)


def get_start_end_array(start_site, end_site):
    start_end_array = np.zeros((len(start_site),2))
    for i in range(0,len(start_site)):
        start_end_array[i,0] = start_site[i]
        start_end_array[i,1] = end_site[i]
    return(start_end_array)


def get_overlap_adj_mat(start_end_array):
    print("getting overlap_adj_mat")
    overlap_adj_mat = np.array(np.zeros((start_end_array.shape[0],start_end_array.shape[0])),dtype = bool)

    for i in range(start_end_array.shape[0]):
        ## return all of the genes that have any degree of overlap with these start end end locations
        upstream_bp = start_end_array[i,0]
        downstream_bp = start_end_array[i,1]
        up_1_direction = np.array((start_end_array[:,0]-upstream_bp) >= 0, dtype = int)## are the other genes' start downstream of the current gene's start
        up_2_direction = np.array((start_end_array[:,1]-upstream_bp) >= 0, dtype = int)## are the other genes' end downstream of the current gene's start
        down_1_direction = np.array((start_end_array[:,0]-downstream_bp) >= 0, dtype = int)## are the other genes' start downstream of the current gene's end
        down_2_direction = np.array((start_end_array[:,1]-downstream_bp) >= 0, dtype = int)## are the other genes' end downstream of the current gene's end
        gene_loci = []
        sum_direction_array = up_1_direction+up_2_direction+down_1_direction+down_2_direction
        ## these are all of the indices where some elements are upstream, or downstream of the locus at hand, but they're not all uniformly up or down (0 or 4). This means that there is some locus overlap
        gene_indices = np.where((sum_direction_array>0) & (sum_direction_array<4))[0]
        #print("\n")
        # for temp_array in [up_1_direction,up_2_direction,down_1_direction,down_2_direction]:
        #     print(temp_array)
        #print("sum:",sum_direction_array)
        #print(gene_indices)
        overlap_adj_mat[i,gene_indices]=True
    return(overlap_adj_mat)


def combine_adj_mats(adj_mat_centers, adj_mat_overlap):
    print("combining adj mats")
    print("centers\n",adj_mat_centers)
    print("overlap\n",adj_mat_overlap)
    if adj_mat_overlap.shape != adj_mat_centers.shape:
        print("adj_mat_centers.shape",adj_mat_centers.shape)
        print("adj_mat_overlap.shape",adj_mat_overlap.shape)

    final_adj_mat = adj_mat_centers + adj_mat_overlap
    if final_adj_mat.shape != adj_mat_centers.shape:
        print("final_adj_mat.shape",final_adj_mat.shape)
        print("adj_mat_centers.shape",adj_mat_centers.shape)
        print("adj_mat_overlap.shape",adj_mat_overlap.shape)
        sys.exit()
    return(final_adj_mat)

def get_center_adj_mat(center_site, dist_cutoff):
    center_site = np.array(center_site).reshape(-1, 1)
    dist_mat = np.abs(metrics.pairwise_distances(center_site, center_site))
    
    ## boolean if centers are within 150
    adj_mat_centers = dist_mat <= dist_cutoff
    return(adj_mat_centers)


def get_insulator_clusters_from_binding_sites(full_contig_list, lib_dir, contig_gene_array, dist_cutoff = 150):
    print("\nfinding all insulator clusters")
    non_gene_contig_list = []
    center_site = []
    start_site = []
    end_site = []

    ## filter the input for nly the non-gene elements
    for i in range(len(full_contig_list)):
        if full_contig_list[i][-1]!="gene":
            non_gene_contig_list.append(full_contig_list[i])
            center_site.append(float(full_contig_list[i][4]))
            start_end = [float(full_contig_list[i][1]),float(full_contig_list[i][2])]
            start_site.append(min(start_end))
            end_site.append(max(start_end))


    if len(non_gene_contig_list) > 1:
        ## if this contig actually has insulator elements
        print("getting adj_mat_centers")
        adj_mat_centers = get_center_adj_mat(center_site, dist_cutoff)
        
        ## now double check for overlap of any sites
        start_end_array = get_start_end_array(start_site, end_site)
        adj_mat_overlap = get_overlap_adj_mat(start_end_array)

        ## now combine the adjacency matrices
        adj_mat = combine_adj_mats(adj_mat_centers, adj_mat_overlap)
        print(adj_mat)

        insulator_site_indices = get_insulator_sites_from_adj_mat(adj_mat)
        all_insulator_sites = get_rearranged_insulator_sites(non_gene_contig_list, insulator_site_indices)
        for insulator_site in all_insulator_sites:
            print("\n") 
            for site in insulator_site:
                print("\t",site)
    else:
        all_insulator_sites = []
    rearranged_contig = populate_contig_with_genes(all_insulator_sites, contig_gene_array)
    return(rearranged_contig)


def get_temp_contig_gene_array(contig_gene_dict, contig):
    if contig in contig_gene_dict:
        print("found",contig)
        print(contig_gene_dict[contig])
        return(contig_gene_dict[contig])
    elif contig[3:] in contig_gene_dict:
        print("found",contig[3:])
        return(contig_gene_dict[contig[3:]])
    elif 'chr'+contig in contig_gene_dict:
        print("found",'chr'+contig)
        return(contig_gene_dict['chr'+contig])
    else:
        print("\n\ncouldn't find",contig,"in the gene reference file\n\n")
        return("None")



def filter_binding_site_dict(contig_dict, lib_dir, verbose = False, do_graph_clust = True):
    ## go through and figure out where the boundaries are
    all_contigs = sorted(list(contig_dict.keys()))
    rearranged_contig_dict = {}
    contig_gene_dict = get_contig_gene_dict(lib_dir)
    for contig in all_contigs:
        print("rearranging",contig)
        rearranged_contig = []
        
        ## figure out if we're starting with an insulator site or genes 
        temp_cont = contig_dict[contig]
        if do_graph_clust:
            rearranged_contig = get_insulator_clusters_from_binding_sites(temp_cont, lib_dir, get_temp_contig_gene_array(contig_gene_dict,contig))
        else:
            ##########################################################################
            if temp_cont[0][-1] == "gene":
                in_genes = True
            else:
                in_genes = False

            ## set up the loop
            cur_elements = []## this will hold the temporary elements of the insulator or gene set
            previous_locus = 0
            for i in range(len(temp_cont)):
                ## condition to find switch
                if in_genes:
                    if temp_cont[i][-1]=="gene":
                        ## in genes & continuing
                        cur_elements.append(temp_cont[i])
                    else:
                        if verbose:
                            print('\n')
                            for el in cur_elements:
                                print('\t',el)
                        ## in genes & not continuing
                        rearranged_contig.append(cur_elements)
                        ## re-set and 
                        in_genes = False
                        cur_elements = [temp_cont[i]]
                if not in_genes:
                    if temp_cont[i][-1]!="gene":
                        ## not in genes and continuing
                        cur_elements.append(temp_cont[i])
                    else:
                        if verbose:
                            print('\n')
                            for el in cur_elements:
                                print('\t',el)
                        ## not in genes and not continuing
                        rearranged_contig.append(cur_elements)
                        ## change_in_genes to True
                        in_genes = True
                        cur_elements = [temp_cont[i]]
        ##########################################################################
        rearranged_contig_dict[contig] = rearranged_contig

    return(rearranged_contig_dict)


class locus():
    def __init__(self,
                 locus_clump):
        self.contig=""
        self.start = None
        self.end = None
        self.genes = []
        self.annotations = ""
        self.locus_type = "between_insulators"
        ## for genes we'll set the gene list in the first pass, but not the boundaries
        ## for insulator sites, we'll set the boundaries, but not the genes in the first pass
        ## this variable will help us keep track of whether or not we're finished processing the given locus
        self.finished = False
        self.process_locus(locus_clump)


    def process_locus(self, locus_clump):
        if locus_clump == []:
            print("Nothing in this locus")
            return(None)
        # try:
        #     locus_clump[0][0]
        # except:
        #     print(locus_clump)
        self.contig = locus_clump[0][0]
        if locus_clump[0][-1] == "gene":
            self.locus_type = "gene"
        else:
            self.locus_type = "insulator"
        
        if self.locus_type == "gene":
            ## here we 
            self.process_gene(locus_clump)
        else:
            ##
            self.process_insulator(locus_clump)
        self.add_annotations(locus_clump)


    def add_annotations(self,locus_clump):
        annotation_list = []
        for i in range(len(locus_clump)):
            annotation_list.append(','.join(list(map(str,locus_clump[i]))))
        annotation_list = '|'.join(annotation_list)
        self.annotations = annotation_list
        return


    def process_gene(self, locus_clump):
        ## we won't set the boundaries, just the genes
        print("Found genes")
        for i in range(len(locus_clump)):
            self.genes.append(locus_clump[i][3])
        return


    def process_insulator(self, locus_clump):
        ## we won't set the genes, just the boundaries
        all_positions = []
        for i in range(0,len(locus_clump)):
            #print(locus_clump[i])
            all_positions.append(locus_clump[i][1])
            all_positions.append(locus_clump[i][2])
        self.start = min(all_positions)
        self.end = max(all_positions)
        #self.genes = sorted(list(set(self.genes + get_genes_from_locus(self.contig, self.start, self.end))))
        return


    def set_loci(self, upstream = None, downstream = None):
        ## check that upstream and downstream are insulators
        ## if not, print descriptive error
        if upstream == None:
            self.start = 0
        else:
            self.start = upstream.end+1
        if downstream == None:
            self.end = 99999999999
        else:
            self.end = downstream.start-1
        ## also set the contig if it's between insulator loci
        if self.locus_type == "between_insulators":
            if upstream is not None:
                self.contig = upstream.contig
            elif downstream is not None:
                self.contig = downstream.contig
            else:
                sys.exit("There's something seriously wrong with this contig")
            ## sanity check that the upstream ends upstream 
            if self.start > self.end:
                print("\n\n\nself.start < self.end:",self.start < self.end)
                print("self.start",self.start)
                print("self.end" , self.end)
                print("Upstream:\n",upstream)
                print("Downstream:\n",downstream)
                sys.exit("something went wrong with getting the up and downstream loci. Look above^^")
        self.finished = True
        return()


    def set_genes(self, upstream = None, downstream = None):
        if self.locus_type == "gene":
            return
        ## now we look for genes in the upstream and downstream if they exist & set our current genes to these
        if upstream != None:
            if upstream.locus_type == "gene":
                self.genes += upstream.genes
            else:
                print("'\twe got an upstream insulator site next to another insulator site")
                print("\t\t",upstream,"\n")
                print("\t\t",self,"\n")
                print("\t\t",downstream)
                sys.exit()
        else:
            self.start = 0
        if downstream != None:
            if downstream.locus_type == "gene":
                self.genes += downstream.genes
            else:
                print("'\twe got a downstream insulator site next to another insulator site")
                print("\t\t",upstream,"\n")
                print("\t\t",self,"\n")
                print("\t\t",downstream)
                ex
                sys.exit()
        else:
            self.end = 99999999999
        self.finished = True
        return


    def update_up_and_down(self, upstream = None, downstream = None, update = None):
        if update == "loci":
            self.set_loci(upstream = upstream, downstream = downstream)
        elif update == "genes":
            self.set_genes(upstream = upstream, downstream = downstream)
        return


    def get_output_line(self):
        ## contig, start, end, genes, annotatons
        out_line = [self.contig, str(int(self.start)), str(int(self.end)), self.locus_type, str(','.join(deepcopy(self.genes))), self.annotations] 
        return(out_line)

    def get_non_gene_elements(self):
        ## contact ensembl to get the non-gene elements overlapping with this span of genome
        client = EnsemblRestClient()
        temp_contig = self.contig
        if temp_contig[:3]=="chr":
            temp_contig = temp_contig[3:]
        self.regulatory_elements = client.get_regulatory_elements_from_region(temp_contig, str(int(self.start)), str(int(self.end)), feat = ["regulatory"])
        temp_anno_list = []
        for r in self.regulatory_elements["regulatory"]:
            temp_anno_list.append(r["description"]+","+str(r["id"])+","+str(r["seq_region_name"])+":"+str(r["start"])+"-"+str(r["end"]))
        self.annotations = "|".join(temp_anno_list)
        print(self.annotations,"\n")
        return()

    def __str__(self):
        return('\t'.join(self.get_output_line()))


###########################################################
class contig_obj():
    def __init__(self, name, list_of_locus_clumps, finalize = True):
        self.name = name
        self.all_gene_entries = []
        self.contig_tads = []
        self.process_contig(list_of_locus_clumps)
        if finalize:
            self.finalize_loci()
            self.prepare_for_lookup()

    def process_contig(self, list_of_locus_clumps):
        print("processing locus clumps for:",self.name)
        if len(list_of_locus_clumps) > 0:
            for element_set in list_of_locus_clumps:
                print(element_set)
                self.contig_tads.append(locus(element_set))
                for element in element_set:
                    if element[-1]=='gene':
                        self.all_gene_entries.append(element)
        ## now we log the start and end loci of all elements for easy lookup later
        self.gene_start_end = np.zeros((len(self.all_gene_entries),2))
        for i in range(len(self.all_gene_entries)):
            sites = [int(self.all_gene_entries[i][1]),int(self.all_gene_entries[i][2])]
            self.gene_start_end[i,0] = min(sites)
            self.gene_start_end[i,1] = max(sites)
        else:
            print('\tno genes or insulator sites in this contig; skipping')
        self.all_gene_entries = np.array(self.all_gene_entries)
        return


    def get_nearest_gene(self, start, end):
        if self.gene_start_end.shape[0]==0:
            return([])
        start_dist = np.abs(start - self.gene_start_end)
        print(start_dist)
        end_dist = np.abs(end - self.gene_start_end)
        print(end_dist)
        nearest_distance_for_all_elements = np.min(np.minimum.reduce([start_dist, end_dist]), axis = 1)
        print(nearest_distance_for_all_elements)
        nearest_gene_idx = np.where(nearest_distance_for_all_elements == np.min(nearest_distance_for_all_elements))[0]
        print(nearest_gene_idx)
        temp_genes = []
        for idx in range(nearest_gene_idx.shape[0]):
            #print(self.all_gene_entries[nearest_gene_idx[idx]])
            temp_genes.append(self.all_gene_entries[nearest_gene_idx[idx]][3])
        temp_genes = list(set(temp_genes))
        return(temp_genes)


    def update_non_gene_genes(self):
        ## TODO convert to counting to allow for boundary skipping
        ## first set the empty ranges
        for i in range(0,len(self.contig_tads)):
            if self.contig_tads[i].locus_type != "gene":
                temp_upstream = None
                temp_downstream = None
                ## first find the first available upstream "gene" locus
                upstream_idx = i
                upstream_gene_clump_count = 0
                found_up_genes = False
                while upstream_idx > 0 and not found_up_genes:
                    upstream_idx -= 1
                    if self.contig_tads[upstream_idx].locus_type == "gene":
                        upstream_gene_clump_count += 1
                        temp_upstream = self.contig_tads[upstream_idx]
                        found_up_genes = True

                ## next find the first available downstream "gene" locus
                downstream_idx = i
                downstream_gene_clump_count = 0
                found_down_genes = False
                while downstream_idx < len(self.contig_tads)-1 and not found_down_genes:
                    downstream_idx += 1
                    #print(downstream_idx,len(self.contig_tads))
                    if self.contig_tads[downstream_idx].locus_type == "gene":
                        downstream_gene_clump_count += 1
                        temp_downstream = self.contig_tads[downstream_idx]
                        found_down_genes = True


                self.contig_tads[i].update_up_and_down(upstream = temp_upstream, downstream = temp_downstream, update="genes")
        return()


    def update_non_insulator_loci(self):
        ## this finds the boundaries of all the 
        for i in range(0,len(self.contig_tads)):
            if self.contig_tads[i].locus_type != "insulator":
                if i == 0:
                    temp_upstream = None
                else:
                    temp_upstream = self.contig_tads[i-1]
                if i == len(self.contig_tads)-1:
                    temp_downstream = None
                else:
                    temp_downstream = self.contig_tads[i+1]
            
                self.contig_tads[i].update_up_and_down(upstream = temp_upstream, downstream = temp_downstream, update="loci")

    def update_between_insulator_elements(self):
        if True:
            return
        for i in range(0,len(self.contig_tads)):
            if self.contig_tads[i].locus_type == "between_insulators":
                self.contig_tads[i].get_non_gene_elements()
        return


    def finalize_loci(self):
        print("finalizing loci for",self.name)
        self.update_non_insulator_loci()
        self.update_non_gene_genes()
        self.update_between_insulator_elements()
        return

    def prepare_for_lookup(self):
        self.start_end_loci = np.zeros((len(self.contig_tads), 2))
        for i in range(len(self.contig_tads)):
            self.start_end_loci[i,0]=self.contig_tads[i].start
            self.start_end_loci[i,1]=self.contig_tads[i].end
        ## in the case where a tad contains no genes or insulator sites, give it a null set so that it plays nice with everything else
        if len(self.contig_tads)==0:
            self.start_end_loci = np.array(([[0,9999999999]]))
        return

    def get_single_tad_idx_site(self, bp):
        """
        Takes in a single base number & gets the tad that contains it
        """
        abs_dist_mat = np.abs(self.start_end_loci-bp)
        min_abs_dist = np.min(abs_dist_mat, axis = 1)
        nearest_tad_idx = np.where(min_abs_dist == np.min(min_abs_dist))[0][0]
        return(nearest_tad_idx)


    def get_tad_for_site(self, bp_start, bp_end = None):
        """
        Takes a base pair start and end number as input and finds the tad locus that contains the input base pair number
        We allow for start and end sites for things like multi-base deltions, cnvs, etc that are not single point mutants
        """
        tad_idx_start = self.get_single_tad_idx_site(bp_start)
        if bp_end != None:
            tad_idx_end = self.get_single_tad_idx_site(bp_end)
        else:
            tad_idx_end = tad_idx_start
        ## plus one because the last tad idx is inclusive, while fancy subsetting is not inclusive of the last idx
        return(self.contig_tads[tad_idx_start:tad_idx_end+1])


    def get_genes_from_bp_site(self, bp_start, bp_end = None):
        tad_set = self.get_tad_for_site(bp_start = bp_start, bp_end = bp_end)
        temp_genes = []
        tad_annotations = []
        tad_list = []
        for tad in tad_set:
            temp_genes += tad.genes
            tad_annotations.append([tad.contig, tad.start, tad.end, tad.locus_type, tad.annotations])
            tad_list.append(tad)
        temp_genes = sorted(list(set(temp_genes)))
        return(temp_genes, tad_annotations, tad_list)

###########################################################

def process_rearranged_contigs_to_tads(contig_dict):
    print("\n\nprocessing contigs into tads\n")
    all_contigs = sorted(list(contig_dict.keys()))
    tad_dict = {}
    ## go through each contig
    for contig in all_contigs:
        print("\t",contig, len(contig_dict[contig]))
        tad_dict[contig] = contig_obj(contig, contig_dict[contig])
    return(tad_dict)


def process_bed(in_dir):
    in_file = os.path.expanduser(os.path.join(in_dir, "chip_tad_boundaries_hg38.bed"))
    if not os.path.isfile(in_file):
        print("in_file:",in_file)
        sys.exit("we coudn't find the input file!:"+in_file)
    #### we'll do a few passes
    ## first to make all the contigs
    contig_dict = {contig:[] for contig in get_contigs(in_file)}
    ## and populate it with the binding sites
    contig_dict = populate_contig_dict(contig_dict, in_file)
    ## rearrange into chunks of elements that belong together
    rearranged_contig_dict = filter_binding_site_dict(contig_dict, in_dir)
    ## then we'll get the intervals of the tad boundaries
    tad_dict = process_rearranged_contigs_to_tads(rearranged_contig_dict)
    out_file = os.path.expanduser(os.path.join(in_dir,'tad_dict.pkl'))
    print("\n\nwriting the output file:",out_file)
    save_dict(tad_dict, out_file)
    print("Done")
    # ## As a test, we'll look up some loci
    # print("\n\n\nchr1:1,000,000\n")
    # for tad in tad_dict["chr1"].get_tad_for_site(1000000):
    #     print('\t',tad)
    # print("\n\n\nchr1:1,000,000:2,000,000\n")
    # for tad in tad_dict["chr1"].get_tad_for_site(1000000,2000000):
    #     print('\t',tad)

    # print("\n\ngenes:\n",tad_dict["chr1"].get_genes_from_bp_site(1000000))
    # print("\n\ngenes:\n",tad_dict["chr1"].get_genes_from_bp_site(1000000,2000000))

    ### write the output


#####################################################################

def main(args):
    process_bed(args.stringdb_dir)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-stringdb_dir",'-sdb',
        help='The directory containing the StringDB action files. Note that this HAS to be the sorted bed file of CTFC/cohesin binding sites.',
        type = str,
        default = '~/bin/pyminer/lib/')

    args = parser.parse_args()
    main(args)