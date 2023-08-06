#!/usr/local/env python3

import argparse
try:
    from pyminer.common_functions import *
    from pyminer.pyminer_process_tad_bed import *
    from pyminer.pyminer_ensembl_rest import map_variants_to_genes
    from pyminer.pyminer_gene_term_comentions import get_comention_summary
    from pyminer.pyminer_gprofiler_converter import convert_to_ensg
except:
    from common_functions import *
    from pyminer_process_tad_bed import *
    from pyminer_ensembl_rest import map_variants_to_genes
    from pyminer_gene_term_comentions import get_comention_summary
    from pyminer_gprofiler_converter import convert_to_ensg
##############################################################


##############################################################

def convert_anno_file_to_ensg_lookup(annotation_file, id_list):
    anno_table = np.array(read_table(annotation_file))
    orig_indices = list(map(int,map(float,anno_table[1:,0].tolist())))
    orig_indices = [idx-1 for idx in orig_indices]## gprofiler's indexing is from 1
    #print(orig_indices)
    ensg_ids = anno_table[1:,3].tolist()
    ensg_to_original_id = {temp_id:[] for temp_id in ensg_ids}
    for i in range(len(ensg_ids)):
        temp_ensg = ensg_ids[i]
        temp_orig_list = ensg_to_original_id[temp_ensg]
        temp_orig_list.append(id_list[orig_indices[i]])
        ensg_to_original_id[temp_ensg] = temp_orig_list
    return(ensg_to_original_id)


def map_variants_to_original_ids(var_to_ensg, ensg_to_original_id):

    return()


def get_gene_level_info(all_variants,out_dir):
    genes = []
    for var in all_variants:
        genes += var.genes
    genes = sorted(list(set(genes)))
    #annotation_out_path = os.path.join(out_dir,"variant_mapped_gene_details")
    #variant_gene_id_path = os.path.join(out_dir,"variant_mapped_gene_ids.txt")
    #make_file('\n'.join(deepcopy(genes)),variant_gene_id_path)
    gene_symbol_dict,gene_def_dict,results = convert_to_ensg(genes)

    for var in all_variants:
        for gene in var.genes:
            print("\n",gene)
            ## make sure there was a good symbol mapping
            print(gene_symbol_dict[gene])
            ###################################################
            ######## TODO: reference ensembl api to fetch these
            if gene_symbol_dict[gene] is None:
                temp_symbol_list = [gene]
            elif gene_symbol_dict[gene] == []:
                temp_symbol_list = [gene]
            elif gene_symbol_dict[gene] == [None]:
                temp_symbol_list = [gene]
            else:
                temp_symbol_list = deepcopy(gene_symbol_dict[gene])
            ## log the reverse lookup
            for symbol in temp_symbol_list:
                var.symbol_to_gene_lookup[symbol] = gene
            ## get the output text
            temp_symbol = "|".join(temp_symbol_list)
            ## set variant's symbols
            var.gene_symbols += temp_symbol_list
            
            ## make sure that there was an appropriate mapping
            print(gene_def_dict[gene])
            if gene_def_dict[gene] is None:
                temp_def = "None"
            elif gene_def_dict[gene] == []:
                temp_def = "None"
            elif gene_def_dict[gene] == [None]:
                temp_def = "None"
            else:
                temp_def = "|".join(deepcopy(gene_def_dict[gene]))
            var.detailed_gene_info.append([var.id, gene, temp_symbol, temp_def])

    #run_cmd("pyminer_gprofiler_converter.py -annotations -ID_list "+variant_gene_id_path+" -out "+annotation_out_path)
    return(all_variants)

def process_comention_table(comention_table):
    """
    Takes in the comention table & returns a dictionary with gene symbol as key and the list of results for all search terms as the values
    """
    ## has header
    comention_table = comention_table[1:]
    symbol_lookup = {line[0]:[] for line in comention_table}
    for i in range(len(comention_table)):
        temp_symbol = comention_table[i][0]
        temp_list = symbol_lookup[temp_symbol]
        temp_list.append(comention_table[i])
        symbol_lookup[temp_symbol] = temp_list
    return(symbol_lookup)
        

def get_best_var_search_term(gene_search_term_results, temp_id = ""):
    if len(gene_search_term_results) == 0:
        leading_candidate = [[temp_id]]
    else:
        default_best = 0
        leading_candidate = [gene_search_term_results[0][0]]
        for i in range(1,len(gene_search_term_results[0])):
            leading_candidate.append("NA")
        for line in gene_search_term_results:
            if line[-2] > default_best:## second to last entry is the best score for the given gene search-term pair
                default_best = line[-2]
                leading_candidate = deepcopy(line)
    return(leading_candidate)


def do_variant_to_search_term_mapping(all_variants, search_term, no_search_quote = False, out_dir=None):
    ## first prep the variant to ensg
    genes = []
    for var in all_variants:
        genes += var.gene_symbols
    genes = sorted(list(set(genes)))
    try:
        comention_summary_table = get_comention_summary(genes, search_term, no_search_quote = no_search_quote, new_pubmed = True)## reminder that this has a header
    except:
        print("We ran into problems scraping data from the new version of PubMed, we'll try the analysis again using the old version.")
        comention_summary_table = get_comention_summary(genes, search_term, no_search_quote = no_search_quote, new_pubmed = False)## reminder that this has a header
    header = ['variant','is_nearest_gene','gene'] + comention_summary_table[0]
    symbol_to_comention_dict = process_comention_table(comention_summary_table)
    for var in all_variants:
        for symbol in var.gene_symbols:
            var.gene_search_term_comentions += symbol_to_comention_dict[symbol]
    
    output = [header]
    output_best_only = [header]
    for var in all_variants:
        print(var)
        for i in range(len(var.gene_search_term_comentions)):
            line = var.gene_search_term_comentions[i]
            symbol = line[0]## this is the location that contains the symbol (ie. first column)
            #print(line)
            #print(symbol)
            #print(var.symbol_to_gene_lookup)
            ensg = var.symbol_to_gene_lookup[symbol]
            is_nearest_gene = ensg in var.nearest_genes
            line = [var.id, is_nearest_gene, ensg] + line
            #print("\t",line)
            var.gene_search_term_comentions[i] = line
            output.append(line)
        for line in var.gene_search_term_comentions:
            print(line)
        var.best_gene_search_term_match = get_best_var_search_term(var.gene_search_term_comentions, temp_id = var.id)
        output_best_only.append(var.best_gene_search_term_match)
    
    for var in all_variants:
        print(var.best_gene_search_term_match)

    if out_dir is not None:
        write_table(deepcopy(output),os.path.join(out_dir,"variant_to_gene_search_term_comention_summary.tsv"))
        write_table(deepcopy(output_best_only),os.path.join(out_dir,"variant_to_BEST_gene_search_term_comention_summary.tsv"))
    return(all_variants)


def get_most_significant_eQTL(full_eqtl_table, out_dir):
    out_table = [full_eqtl_table[0]]
    ## go through and log all of the variants and 
    combo_ids = []
    for i in range(1,len(full_eqtl_table)):
        combo_ids.append(full_eqtl_table[i][0]+full_eqtl_table[i][2])
    combo_best_p_dict = {combo:0 for combo in combo_ids}
    ## now catelogue the greatest negative log 10 p-value
    for i in range(1,len(full_eqtl_table)):
        temp_id = full_eqtl_table[i][0]+full_eqtl_table[i][2]
        try:
            float(full_eqtl_table[i][3])
        except:
            pass
        else:
            if float(full_eqtl_table[i][3]) > combo_best_p_dict[temp_id]:
                combo_best_p_dict[temp_id] = float(full_eqtl_table[i][3])
    ## now log them in the new output file
    for i in range(1,len(full_eqtl_table)):
        temp_id = full_eqtl_table[i][0]+full_eqtl_table[i][2]
        try:
            float(full_eqtl_table[i][3])
        except:
            pass
        else:
            if float(full_eqtl_table[i][3]) == combo_best_p_dict[temp_id]:
                out_table.append(full_eqtl_table[i])
    out_eqtl_path = os.path.join(out_dir,'var_to_all_gene_BEST_eQTL_summary.tsv')
    write_table(out_table, out_eqtl_path)
    return()


def do_eqtl_mapping(all_variants, out_dir = None):
    for var in all_variants:
        var.get_eqtl_for_genes()
        #print(var.eqtls)
    if out_dir is not None:
        out_table = [['rsID','is_nearest_gene','ENSG','neg_log10_p_val','tissue','value']]
        for var in all_variants:
            for gene, list_of_tissue_eqtl_dicts in var.eqtls.items():
                if list_of_tissue_eqtl_dicts is None:
                    out_table.append([var.id, gene in var.nearest_genes, gene, "NA","NA","NA"])
                else:
                    if len(list_of_tissue_eqtl_dicts) == 0:
                        out_table.append([var.id, gene in var.nearest_genes, gene, "NA","NA","NA"])
                    else:
                        for tissue_level_dict in list_of_tissue_eqtl_dicts:
                            if ("minus_log10_p_value" in tissue_level_dict) 
                                  and ("tissue" in tissue_level_dict)
                                  and ("value"in tissue_level_dict):
                                out_table.append([var.id, gene in var.nearest_genes, gene, removeNonAscii(str(tissue_level_dict["minus_log10_p_value"])), removeNonAscii(str(tissue_level_dict["tissue"])), removeNonAscii(str(tissue_level_dict["value"]))])
                            else:
                                out_table.append([var.id, gene in var.nearest_genes, gene, "NA","NA","NA"])
        out_eqtl_path = os.path.join(out_dir,'var_to_all_gene_full_eQTL_summary.tsv')
        get_most_significant_eQTL(out_table,out_dir)
        write_table(out_table, out_eqtl_path)
    return(all_variants)


def do_var_to_ensg_mapping(variant_file,
                           out_dir,
                           species,
                           lib_dir,
                           annotation_file = None,
                           id_list_file = None,
                           search_terms = None,
                           no_search_quote = True):
    if species is not "hsapiens":
        sys.exit("we can only work with human species rsIDs right now.")
    out_dir = process_dir(out_dir)
    
    ## check if we're mapping back to the original scRNAseq IDs (this is optional)
    if id_list_file != None and annotation_file != None:
        map_back_to_original = True
    else:
        map_back_to_original = False
    
    ## check if we're doing the search term co-mention (This is optional)
    if search_terms is not None:
        do_search_term = True
    else:
        do_search_term = False

    all_variants = map_variants_to_genes(variant_file, stringdb_dir = lib_dir, out_dir = out_dir)
    
    ## get the details of the ensembl genes
    all_variants = get_gene_level_info(all_variants, out_dir)

    ## get eQTL information
    all_variants = do_eqtl_mapping(all_variants, out_dir = out_dir)

    if map_back_to_original:
        ## if we're given the id_list file, it means that we're going to map things back from the ensembl IDs to the original IDs, likely used by the scRNAseq reference
        id_list = read_file(id_list_file,'lines')
        ensg_to_original_id = convert_anno_file_to_ensg_lookup(annotation_file, id_list)
        var_to_orig_ids = map_variants_to_original_ids(all_variants, ensg_to_original_id)

    if do_search_term:
        all_variants = do_variant_to_search_term_mapping(all_variants, read_file(search_terms,'lines'), out_dir = out_dir, no_search_quote = no_search_quote)
    
    save_dict(deepcopy(all_variants),os.path.join(out_dir,"variants.pkl"))
    return


##############################################################
def pyminer_annotate_variants_to_genes_main(args):
    do_var_to_ensg_mapping(variant_file = args.variants,
                           out_dir = args.out_dir,
                           species = args.species,
                           lib_dir = args.lib_dir,
                           annotation_file = args.annotations,
                           id_list_file = args.id_list,
                           search_terms = args.search_terms,
                           no_search_quote = args.no_search_quote)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-variants",'-vars',  
        help="a text file containing rsIDs separated on new lines",
        type = str)

    parser.add_argument("-out_dir", '-out', '-o',
        help="the directory that we'll write the results to",
        type = str)

    parser.add_argument("-species", '-s',
        help="a gProfiler accepted species code. Dafault = 'hsapiens'. Note that we currently only accept human rsIDs",
        type = str,
        default = 'hsapiens')

    parser.add_argument("-annotations", "-annotation_file","-anno_dict","-anno","-a",
        help="The annotation table - usually annotations.tsv")

    parser.add_argument("-lib_dir",'-lib',  
        help="the directory that contains the tad file - often titled 'tad_dict.pkl'",
        type = str)

    parser.add_argument('-id_list','-ids',
        help="the file containing the row ids. Usually ID_list.txt",
        type = str)

    parser.add_argument("-search_terms",'-terms', "-st" ,
        help="if you want to do the gene-symbol & search term co-mention analysis, give the file in here",
        type = str)

    parser.add_argument("-no_search_quote",
        help="whether or not to include quotes for the search terms",
        action = 'store_true')

    args = parser.parse_args()
    pyminer_annotate_variants_to_genes_main(args)