#!/usr/local/env python3

from gprofiler import GProfiler
from clustering import get_density, plot_densities, remove_zeros



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
##########################################################################



#######################################################
## SECTION 1

def get_neg_cor_clust(neg_cor_clust):
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
    neg_cor_vect_noZero = remove_zeros(neg_cor_vect[:])
    pos_cor_vect_noZero = remove_zeros(pos_cor_vect[:])

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

    ########################################################
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
    return()



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
##########################################################################################################





##########################################################################################################
## SECTION 2



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

#####
## set up a quick-search dictionary
print(len(usable_indices))
print(len(clust_gene_ids))
usable_id_hash = {key:value for value, key in enumerate(clust_gene_ids)}
##
#####

## remove the mito and ribo genes

def rm_ribo_mito(species, infile_original_dir):
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
            if int(annotations[i][0])-1 in usable_indices:
                #print("\tproblem mapping",temp_original_id,"but we'll include it")
                final_clust_gene_ids.append(ID_list[int(annotations[i][0])-1])
                final_clust_gene_idxs.append(int(annotations[i][0])-1)
    clust_gene_ids = list(set(final_clust_gene_ids))
    clust_gene_idxs = list(set(final_clust_gene_idxs))
    usable_indices = clust_gene_idxs
    ### 
    print(len(usable_indices),"currenlty usable indices")
    temp_usable_indices = list(set(usable_indices))
    return(temp_usable_indices, clust_gene_idxs, clust_gene_ids)


##########################################################
def remove_sparse(full_expression, temp_usable_indices):
## remove genes that are only expressed in a very small number of cells
    remove_sparse=True
    if remove_sparse and args.clust_on_genes == None:
        print('removing genes that are only observed in 5 percent or less of cells, or greater than 50 cells, whichever is lower:')
        cutoff = min([np.shape(full_expression)[1]*.05,50])
        print("\t",cutoff,"cells")
        usable_indices = []
        for i in temp_usable_indices:
            num_seen = np.sum(np.array(full_expression[i,:]>0,dtype=int))
            if num_seen >= cutoff:
                usable_indices.append(i)
        print(len(temp_usable_indices)-len(usable_indices),'genes removed because of sparse expression')
        print(len(usable_indices),'used for clustering')
        clust_gene_idxs = usable_indices[:]
        clust_gene_ids = [IDlist[idx] for idx in usable_indices]
    return(usable_indices, clust_gene_idxs, clust_gene_ids)
##########################################################
##########################################################
################# end feature selection ##################
##########################################################
##########################################################
##########################################################

## /SECTION 2

############################
def non_dispersion_feat_select(remove_ribo_mito = True):

    if args.neg_cor_clust != None:
        get_neg_cor_clust(neg_cor_clust)

    if remove_ribo_mito:
        usable_indices, clust_gene_idxs, clust_gene_ids = rm_ribo_mito(species, infile_original_dir)

    if not clust_on_genes:
        usable_indices, clust_gene_idxs, clust_gene_ids = remove_sparse(full_expression, usable_indices)
    return(usable_indices, clust_gene_idxs, clust_gene_ids)

############################

if __name__ == '__main__':

    non_dispersion_feat_select(neg_cor_clust = args.neg_cor_clust,
                               neg_cor_percentile_cutoff = args.percentile_cutoff,
                               out_dir = args.out_dir,
                               remove_ribo_mito = args.remove_ribo_mito)