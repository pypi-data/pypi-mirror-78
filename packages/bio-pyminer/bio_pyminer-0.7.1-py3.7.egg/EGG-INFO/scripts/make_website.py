#!/home/scott/anaconda3.7/bin/python3
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
    print(in_message)
    time.sleep(.25)
    if com:
        Popen(in_message,shell=True).communicate()
    else:
        Popen(in_message,shell=True)

#######################################################

parser = argparse.ArgumentParser()



parser.add_argument(
    '-base_dir','-in','-i','-input',
    dest='base_dir',
    type=str)


args = parser.parse_args()
########################################################
########################################################
if args.base_dir[:-1]!='/':
    args.base_dir+='/'

out_file = args.base_dir + "PyMINEr_summary.html"
base_dir = args.base_dir

if base_dir[-1]!='/':
    base_dir+='/'


########################################################
############# add the various elements #################
from PIL import Image
def get_img_dims(img):
    image = Image.open(img)
    w, h = image.size
    ## reduce size so it fits on the screne
    reduction_factor = w/600
    return(int(w/reduction_factor), int(h/reduction_factor))

def add_h2(title):
    return("\n\t<h2>"+str(title)+"</h2>\n")

def add_h3(title):
    return("\n\t<h3>"+str(title)+"</h3>\n")

def add_p(p):
    return('\t\t\t<p>'+str(p)+'</p>\n')

def add_file_link(f,name):
    return('<a href='+str(f)+'>'+str(name)+'</a>\n')

def add_file_link_list(f,name):
    return('<li><a href='+str(f)+'>'+str(name)+'</a></li>\n')

def add_br():
    return('<br></br>\n')

def add_img(img,alt, base_dir= None):
    if os.path.isfile(img):
        w, h = get_img_dims(img)
        return('<div><img src="'+str(img)+'" alt="'+str(alt)+'" width="'+str(w)+'" height="'+str(h)+'"></div>\n')
    else:
        if base_dir != None:
            curr_dir = os.getcwd()
            os.chdir(base_dir)
            final_text = add_img(img, alt)
            os.chdir(curr_dir)
            return(final_text)
        print("\tWARNING: couldn't find:"+img)
        return(add_br())

def add_button_head(text):
    return("""<button class="collapsible">"""+str(text)+"""</button>
<div class="content">""")



def add_tab_header(section_name, default_open=False):
    out_head = "<div id='"+section_name+"' class='w3-container w3-border city'"
    if not default_open:
        out_head += ' style="display:none"'
    else:
        out_head += ' style="display: block;"'
    out_head += '>'
    return(out_head)



def add_table(in_table):
    ## start the table
    out_table_str = """<table style="width:100%">\n"""
    for i in range(len(in_table)):
        out_table_str+="\t<tr>\n"
        for j in range(len(in_table[i])):
            out_table_str+="\t<th>"+str(in_table[i][j])+"</th>\n"
        out_table_str+="\t</tr>\n"
    out_table_str+="</table>\n"
    return(out_table_str)


def parse_file_name(img):
    old_name = img[:-4]
    temp_name = old_name.split('_')
    temp_name = ' '.join(temp_name)
    return(old_name,temp_name)



def add_clustering(base_dir):
    os.chdir(base_dir)
    cluster_str = ""
    cluster_str+=add_tab_header("Clustering")
    #cluster_str+=add_h2('Clustering')
    #cluster_str+=add_button_head('Clustering')
    ## check if anti_correlation clustering was done
    if os.path.isfile(base_dir+'sig_neg_count_vs_total_neg_count.png'):
        ## if it is, start annotating
        cluster_str+=add_h3("Negative Control Bootstrap Shuffling")
        cluster_str+=add_p("Here, PyMINEr shuffled up your data to make it randomized. This will maintain the overall distribution of your data, while at the same time randomizing it so that we can come up with a reasonable cutoff for performing the anti-correlation based feature selection. Shown below is the distribution of all randomized Spearman rhos.")
        cluster_str+=add_img("boostrap_cor_rhos.png", 'boot_all')
        cluster_str+=add_p("Here are just the negative correlations from the shuffled up dataset.")
        cluster_str+=add_img("boostrap_neg_cor_rhos.png", 'boot_neg')
        cluster_str+=add_p("Here is a scatter plot that shows the number of total negative correlations observed for each gene (y-axis), and the log2 number of significant negative correlations (x-axis). All of the genes to the left/below the black line were used for clustering.")
        cluster_str+=add_img("sig_neg_count_vs_total_neg_count.png","sig_vs_total_neg")
        cluster_str+=add_p("Similarly, here is a plot showing the ratio of significant to non-sigificant. Everything to the right was used for clustering.")

    ## link to the file with all of the sample annotations
    cluster_str+=add_h3("Clustering Results:")
    cluster_str+=add_file_link("sample_clustering_and_summary/sample_k_means_groups.txt",'sample group annotations')

    ## get the images from the sample_clustering_and_summary folder
    os.chdir(base_dir+"sample_clustering_and_summary/")
    additional_images=[]
    for item in glob.glob("*.png"):
        additional_images.append(item)
    os.chdir(base_dir)
    if len(additional_images)>0:
        cluster_str+=add_h3('Here are some additional images:')
        for img in additional_images:
            old_name = img[:-4]
            temp_name = old_name.split('_')
            temp_name = ' '.join(temp_name)
            cluster_str+=add_p(temp_name)
            cluster_str+=add_img("sample_clustering_and_summary/"+img,old_name)
    
    static_files = []
    cluster_str+='\n</div>\n'
    cluster_str+='\n</div>\n'
    os.chdir(base_dir)
    return(cluster_str)



def add_statistics(base_dir):
    stats_str = ""
    stats_str+=add_tab_header("Differential Expression")
    #stats_str+=add_h2("Statistics")
    #stats_str+=add_button_head("Statistics")
    stats_str+=add_h3("basic stats")
    stats_str+=add_p("If you find some interesting genes that are different between groups, here are the:")
    stats_str+=add_file_link("sample_clustering_and_summary/k_group_means.txt",'group means')
    stats_str+=add_p('and...')
    stats_str+=add_file_link("sample_clustering_and_summary/k_group_sd.txt",'group standard deviations')
    stats_str+=add_p('as well as the')
    # stats_str+=add_file_link("sample_clustering_and_summary/sample_var_enrichment_Zscores.txt",'sample-wise Z-scores')
    # stats_str+=add_p('and...')
    stats_str+=add_file_link("sample_clustering_and_summary/k_group_enrichment.txt",'group level Z-scores')
    stats_str+=add_h3("statistical comparisons")
    sig_dir = "sample_clustering_and_summary/significance/"

    stats_str+=add_file_link(sig_dir+'groups_1way_anova_results.txt',"Benjamini-Hoschberg corrected 1-way Anovas")
    stats_str+=add_p("For just getting a high-level view of the differences between cell-types, the pathway analysis of these results may be more interesting. Those are a couple tabs down. Looking at the gene expression module usage and the pathways associated with those modules can also be very useful for figuring out the functions of the genes being expressed in a cluster.")
    stats_str+='\n</div>\n'
    stats_str+='\n</div>\n'
    return(stats_str)

def add_gene_enrichment(base_dir):
    os.chdir(base_dir)
    sig_dir = "sample_clustering_and_summary/significance/"
    enrich_str = ""
    enrich_str+=add_tab_header("Cluster Pathway Analysis")
    #enrich_str+=add_h2("Gene Enrichment in Groups")
    #enrich_str+=add_button_head("Gene enrichment in groups")
    enrich_str+=add_h3("Significantly enriched genes in each group")
    enrich_str+=add_p("Below is a file that contains a table with genes on the left, and groups in columns. If a gene is considered significantly enriched, that means that the BH corrected 1-way Anova was significant, and the gene had a high Z-score in that particular group. If a gene is significantly enriched in that group, the value is True in the corresponding cell in the table, False if it was not significantly enriched.")
    enrich_str+=add_file_link(sig_dir+"/significant_and_enriched_boolean_table.txt","True/False significantly enriched table")
    enrich_str+=add_p("alternatively, you can use these separated files that simply have the list of significantly enriched genes for each group:")
    enrich_str+=add_button_head('Genes enriched in each group')
    os.chdir(sig_dir)
    enrich_files=[]
    for item in glob.glob("*_significant_enriched.txt"):
        enrich_files.append(item)
    enrich_files = sorted(enrich_files)
    if len(enrich_files)>0:
        enrich_str+="\t\t\t\t<ul>\n"
        for img in enrich_files:
            old_name = img[:-4]
            temp_name = old_name.split('_')
            temp_name = ' '.join(temp_name)
            #enrich_str+=add_p(temp_name)
            enrich_str+=add_file_link(sig_dir+img,old_name)
            enrich_str+=add_br()

        enrich_str+="\t\t\t\t</ul>\n"

    enrich_str+="\t\t</div>"# end the sub-button
    enrich_str+=add_br()

    os.chdir(base_dir)
    pathway_dir = sig_dir+'gprofiler/'
    os.chdir(pathway_dir)
    enrich_path=[]
    for item in glob.glob("*.txt"):
        enrich_path.append(item)
    os.chdir(base_dir)
    enrich_path = sorted(enrich_path)
    if len(enrich_path)>0:
        #enrich_str+=add_h3('Pathway Enrichment for Each Group:')
        enrich_str+=add_button_head('Pathway enrichment for each group')
        if os.path.isfile(sig_dir+"/combined_neg_log10p_gprofiler.txt"):
            enrich_str+=add_p("Below is a combined file with all of the pathways that came out of the analysis of the above genes, enriched in the different groups. We've also created a new algorithm for ranking the importance of these pathways (not to boast, but I'm kind of proud of it). It's based on the information/entropy of the -log10(p-vals). If you look at the -log10(p-vals) at the top of the list, you should find pathways that are really high in some groups and really low in other groups. The overall formula is calculated by taking the sum(KL-divergance)*range(-log10(p-vals)). The KL-divergence is looking for a difference in the distribution between the observed -log10(p-vals) and the distribution expected from an uninformative vector of -log10(p-vals) (this is a Gaussian null hypothesis). Then we multiply the sum(KL-divergance) by the range of -log10(p-vals) to let the most significant pathways with lots of information/low entropy rise to the top.")
            enrich_str+=add_file_link(sig_dir+"/combined_neg_log10p_gprofiler.txt",'combined pathway analyses')
            enrich_str+=add_p("and here is a file that has a normalized metric that ranks each pathway for their individual importance within each group. It would be useful to sort each of these and see what rises to the top for each 'cell type' or whatever your groups are.")
            enrich_str+=add_file_link(sig_dir+'/individual_class_importance.txt', 'individual class importance')
            enrich_str+=add_p("Below are all of the individual results so that you find which genes were in which pathways in individual groups:")
            enrich_str+=add_button_head("individual pathway files")
        enrich_str+="\t\t\t\t<ul>\n"
        for img in enrich_path:
            old_name = img[:-4]
            temp_name = old_name.split('_')
            temp_name = ' '.join(temp_name)
            #enrich_str+=add_p(temp_name)
            enrich_str+=add_file_link(pathway_dir+img,old_name)
            enrich_str+=add_br()


        if os.path.isfile(sig_dir+"/combined_neg_log10p_gprofiler.txt"):
            enrich_str+="\n\t\t</div>\n"

        enrich_str+="\t\t\t\t</ul>\n"
        enrich_str+="\n\t\t</div>\n"#end the sub-button
        enrich_str+=add_br()

    enrich_str+='\n</div>\n'
    return(enrich_str)


def add_community_pathway_annotation(com, individual_class_importance_table):
    if type(individual_class_importance_table) != np.ndarray:
        return(add_br())
    print(individual_class_importance_table)
    ## get the top 5 pathways
    ## first get the right column
    header = individual_class_importance_table[0,:]
    temp_col = np.where(header == com+"_gprofiler.txt")[0]
    print(temp_col)
    print(com,individual_class_importance_table[1:,temp_col])
    most_sig_order = np.argsort(np.array(individual_class_importance_table[1:,temp_col].tolist(),dtype=np.float32), axis = 0)[::-1] + 1
    #print(individual_class_importance_table[most_sig_order,temp_col])
    #print(most_sig_order)
    keep_rows = []
    for i in range(0,5):
        temp_row = most_sig_order[i]
        ## check if it's actually significant first
        print(individual_class_importance_table[temp_row,temp_col])
        if float(individual_class_importance_table[temp_row,temp_col]) > 0:
            keep_rows.append(temp_row)
    ## go through the rows that we're keeping & summarize them
    out_table = [["term_id","term_def","importance_metric"]]
    for i in keep_rows:
        temp_line = [individual_class_importance_table[i,1][0],individual_class_importance_table[i,3][0],individual_class_importance_table[i,temp_col][0]]
        out_table.append(temp_line)
    return(add_table(out_table)+add_br())


def add_community_top_markers(base_dir, com, community_annotations_file, top_n_markers = 15):
    com_marker_str = ""
    com_marker_str += add_button_head("top marker genes of "+com+" (defined by high Local PageRank)")
    ## read in the community annotations file
    try:
        com_anno_table = read_table(community_annotations_file)
    except:
        cur_dir = os.getcwd()
        os.chdir(base_dir)
        com_anno_table = read_table(community_annotations_file)
        os.chdir(cur_dir)
    else:
        com_anno_table = read_table(community_annotations_file)
    num_lines = min([len(com_anno_table),top_n_markers])
    temp_table = com_anno_table[:num_lines]
    # for i in range(len(temp_table)):
    #     print(temp_table[i])

    com_marker_str += add_p("this is a list of the top genes that are most central to this hub, and will therefore likely make good marker genes.")
    com_marker_str += add_table(temp_table)
    # print(add_table(temp_table))
    # sys.exit()
    com_marker_str += "</div>"## ends the button tab


    return(com_marker_str)



def add_community_str(base_dir, com, individual_class_importance_table):
    com_str = ""
    com_str += add_h3("Community module usage")
    com_str += add_community_pathway_annotation(com, individual_class_importance_table)
    com_dir = os.path.join(os.path.join("pos_cor_graphs/community_analysis/",com))
    community_annotations_file = os.path.join(com_dir,"community_ids_annotated.tsv")
    com_str += add_community_top_markers(base_dir, com, community_annotations_file)
    com_str += add_file_link(community_annotations_file,"This is the list of genes in the community.")
    com_str += add_br()
    com_str += add_file_link(os.path.join(com_dir,"TukeyHSD.tsv"),"This is the differential module usage across groups")
    com_str += add_p("And here is a plot showing the module usage across groups.")
    com_str += add_img(os.path.join(com_dir,"group_z_scores.png"),"Group Z-scores", base_dir = base_dir)
    com_str += add_br()
    com_str += add_p("This is where this community is in the network graph.")
    com_str += add_img(os.path.join(com_dir,"community.png"),"community subset", base_dir = base_dir)
    return(com_str)



def add_graph(base_dir):
    graph_str=""
    #graph_str+=add_h2("Expression graphs")
    #graph_str+=add_button_head("Expression graphs")
    graph_str+=add_tab_header("Gene Expression Networks")
    graph_str+=add_h3("Adjacency Lists:")
    adj_list_list = []
    os.chdir(base_dir)
    for f in glob.glob("*"):
        if 'adj_list' in f:
            adj_list_list.append(f)
    print(adj_list_list)
    for f in adj_list_list:
        if '_pos.tsv' in f:
            pos_adj = f
        elif '_neg.tsv' in f:
            neg_adj = f
        else:
            total_adj = f
    # graph_str+=add_p('Full adjacency list:')[:-6]+'</p>'
    # print(base_dir+total_adj)
    graph_str+="\t\t\t\t<ul>\n"
    graph_str+=add_file_link(total_adj,'Full adjacency list')
    graph_str+=add_br()
    graph_str+=add_file_link(pos_adj,'Positive correlation (co-expression) adjacency list')
    graph_str+=add_br()
    graph_str+=add_file_link(neg_adj,'Negative correlation adjacency list')
    graph_str+=add_br()
    graph_str+="\t\t\t\t</ul>\n"

    graph_str+=add_h2("Co-expression graph plots:")
    coexpression_graph_dir = "pos_cor_graphs/"
    graph_str+=add_h3("This is a 'hairball' view of a Spearman coexpression network of your data, where each point represents a gene, and the lines are whether or not a gene is correlated with another gene. The closer two genes are to each other, the more correlated they are.")
    graph_str+=add_img(coexpression_graph_dir+"full_graph.png",'Co-expression graph')
    if os.path.isfile(coexpression_graph_dir+"community.png"):
        graph_str+=add_h3("This is a graph of all the communities of genes that are coordinately regulated in your dataset")
        graph_str+=add_img(coexpression_graph_dir+"community.png",'communities')

    ## 
    community_dir = os.path.join(coexpression_graph_dir,"community_analysis")
    if os.path.isdir(community_dir):
        graph_str+=add_button_head('Analysis of individual communities')
        os.chdir(community_dir)
        ## first add the significance and pathway files
        graph_str+=add_br()
        graph_str+=add_file_link(os.path.join(base_dir, community_dir, "global_statistics.tsv"),"Here are the stats (BH corrected 1-way anova) for differential module usage among groups.")
        graph_str+=add_br()
        graph_str+=add_file_link(os.path.join(base_dir, community_dir, "combined_neg_log10p_gprofiler.txt"),"-log10(p-val) for the pathways associated with each module")
        graph_str+=add_br()
        individual_class_importance_file = os.path.join(base_dir, community_dir, "individual_class_importance.txt")
        graph_str+=add_file_link(individual_class_importance_file,"The unique pathways of each module (individual class importance).")
        graph_str+=add_br()
        ## second add the folders for each individual community
        print(os.getcwd())
        community_dirs = []
        for file in glob.glob('*'):
            if os.path.isdir(file):
                if file != 'gprofiler':
                    print(file)
                    community_dirs.append(file)

        ## catelogue how many genes are in each community
        com_num_dict = {}
        com_num_list = []
        for com in community_dirs:
            com_num_dict[com] = len(read_file(os.path.join(com,"community_ids.txt"),"lines"))
            com_num_list.append(com_num_dict[com])

        ## sort based on size
        new_order = np.argsort(np.array(com_num_list))[::-1]
        community_dirs = np.array(community_dirs)[new_order].tolist()
        if os.path.isfile(individual_class_importance_file):
            individual_class_importance_table = np.array(read_table(individual_class_importance_file))
        else:
            individual_class_importance_table = "None"
        for com in community_dirs:
            graph_str+=add_button_head(com+" ("+str(com_num_dict[com])+" nodes)")
            graph_str+=add_community_str(base_dir, com, individual_class_importance_table)
            graph_str+="\n\t\t</div>\n"
            #graph_str+=add_br()


        #graph_str+="\n\t\t</div>\n"
        graph_str+=add_br()
        graph_str+="\n\t</div>\n"
        os.chdir('../..')
        print(os.getcwd())

    if os.path.isfile(coexpression_graph_dir+"PageRank.png"):
        graph_str+=add_h3("PageRank is a metric for how well connected a gene is in the coexpression network")
        graph_str+=add_img(coexpression_graph_dir+"PageRank.png",'Page-Rank')
    if os.path.isfile(coexpression_graph_dir+"LPR.png"):
        graph_str+=add_h3("Local PageRank is a derivative of both Louvain-modularity based community detection and PageRank. It essentially calculates a normalized PageRank within each module to quantify local connectivy throughout the graph.")
        graph_str+=add_img(coexpression_graph_dir+"LPR.png",'Local PageRank')
    graph_str+=add_h3("Here are the Z-scores for each group overlaid on the co-expression graph (red means it's enriched in that group, blue means it's low expression or not expressed):")

    ## find all of the pertinent files, and
    graph_str+=add_button_head('Z-score overlaid co-expression graphs')
    os.chdir(coexpression_graph_dir)
    extra_images = []
    for file in glob.glob('*.png'):
        if 'sample_group' in file:
            extra_images.append(file)
    extra_images = sorted(extra_images)
    os.chdir(base_dir)
    for img in extra_images:
        new,old = parse_file_name(img)
        graph_str+=add_p(new)
        graph_str+=add_img(coexpression_graph_dir+img, new)
    graph_str+="\n\t\t</div>\n"
    #graph_str+=add_br()
    graph_str+="\n\t</div>\n"
    graph_str+="\n\t</div>\n"
    return(graph_str)


def add_img_list(list_of_images,temp_dir):
    output = ""
    for img in list_of_images:
        new,old = parse_file_name(img)
        output+=add_p(new)
        output+=add_img(temp_dir+img, new)
    return(output)


def add_genes_of_interest(base_dir):
    goi_str=""
    goi_dir = 'genes_of_interest/'
    goi_str+=add_tab_header('Genes Of Interest')
    if os.path.isdir(goi_dir):
        #goi_str+=add_button_head('Genes of interest')
        goi_str+=add_p("An interesting way to use the structure of the graphs generated by PyMINEr is looking at how far away all genes in your dataset are away from your genes of interest. We've shown in the PyMINEr paper that there are many types of functional enrichment that correlate with how far away a gene is from another gene in the graph network. For example, close to a transcription factor are more likely to have a binding site for that transcription factor when compared to a gene that's father away from it. There is also an increased probability that two genes will encoded proteins that have a physical intereaction when those two genes are directly connected (i.e. 1-degree of separation).")
        goi_str+=add_p('below is a file containing a table that has the distance of all genes in the genome away from your gene(s) of interest.')
        goi_str+=add_file_link(goi_dir+'genes_of_interest_shortest_path_list.txt','Shortest path of all genes away from your genes of interest')
        goi_str+=add_p('Below is a heatmap of your genes of interest:')
        goi_str+=add_img(goi_dir+'genes_of_interest_subset_heatmap.png','genes of interest heatmap')

        ## collect the other images
        os.chdir(goi_dir)
        additional_images = []
        for f in glob.glob('*.png'):
            if f != 'genes_of_interest_subset_heatmap.png':
                additional_images.append(f)
        goi_str+=add_button_head("additional plots for your genes of interest")
        os.chdir(base_dir)
        goi_str+=add_img_list(sorted(additional_images),goi_dir)
        goi_str+='\n\t\t</div>\n'

        goi_str+="\n</div>\n"
    else:
        goi_str+=add_p("We didn't find any genes of interest to analyze. For future usage - if you do want to provide a list of genes to make some special plots for, you can include a text file that has the names of the genes, with the option of a second column for an alias. Provide that file after the -goi argument.")
    goi_str+="\n</div>\n"
    return(goi_str)


def add_autocrine_paracrine(base_dir):
    ap_dir = "autocrine_paracrine_signaling/"
    ap_str=""
    ap_str += add_tab_header("Autocrine/Paracrine Signaling")
    if not os.path.isdir(ap_dir):
        add_p("Something went wrong & we didn't get any autocrine and paracrine signaling results. There might have been an error within the run.")
    else:
        #ap_str+=add_button_head("Autocrine/paracrine signaling")
        ap_str+=add_p("Below are the predicted signaling networks")
        ap_str+=add_file_link(ap_dir+'all_cell_cell_interaction_summary.txt','Number of interactions between all of the groups')
        ap_str+=add_br()
        ap_str+=add_file_link(ap_dir+'all_cell_type_specific_interactions.txt','A detailed summary of each autocrine/paracrine interaction')
        ap_str+=add_br()
        ap_str+=add_file_link(ap_dir+'all_cell_type_specific_interactions_gprofiler.txt','A detailed summary of the pathways signaling across and within groups')
        ap_str+=add_br()
        ap_str+=add_file_link(ap_dir+'combined_neg_log10p_gprofiler.txt','A table of negative log10 p-values that for each pathway in each interaction. (Zero just means it did not reach signficance)')
        ap_str+=add_br()
        ap_str+=add_file_link(ap_dir+'individual_class_importance.txt','A table of the individual importance of each pathway for the given group')
    ap_str += "\n</div>\n"
    return(ap_str)
        #combined_neg_log10p_gprofiler.txt
        #individual_class_importance.txt


def add_gene_annotations(base_dir):
    anno_str=""
    anno_str+=add_tab_header("Gene Annotations",default_open=True)
    anno_str+=add_h3("Genes Annotations")
    if os.path.isfile("annotations.tsv"):
        anno_str+=add_p("Here are the annotations for your genes. You can use this in excel using v-lookup if you want to get gene symbols or definitions for any of the other files.")
        anno_str+=add_file_link("annotations.tsv","Annotation file")
    if os.path.isfile("human_orthologues.tsv"):
        anno_str+=add_br()
        anno_str+=add_file_link("human_orthologues.tsv","Human orthologues to your genes")
    anno_str+=add_h3("Clustering")
    anno_str+=add_p("The first step as identifying cell-type/-state clusters. This process includes feature selection followed\
     by clustering (usually either by locally weighted Louvain-modularity, or affinity propagation depending on the arguments that you used). The clustering tab has some plots that show traditional things like PCA/UMAP, etc")
    anno_str+=add_h3("Differential Expression")
    anno_str+=add_p("This section holds links to .tsv format tables that run the statistics \
        that compare the clusters \
        to each other. Plots are on other tabs, this one is just tables.")
    anno_str+=add_h3("Genes Of Interest")
    anno_str+=add_p("If you gave a file to the -goi argument that holds some genes of interest, \
        the plots generated for those genes of interest are included in this section.")
    anno_str+=add_h3("Cluster Pathway Analysis")
    clust_str="""Tables that show the pathway analysis results, based on """
    clust_str+="""<a href="https://www.ncbi.nlm.nih.gov/pubmed/17478515" target="_blank">gProfiler</a>"""
    clust_str+=" as well as PyMINEr's custom information theory based prioritization of those pathways."
    anno_str+=add_p(clust_str)
    anno_str+=add_h3("Unique Marker Genes")
    anno_str+=add_p("")
    anno_str+=add_h3("Gene Expression Networks")
    anno_str+=add_p("")
    anno_str+=add_h3("Autocrine/Paracrine Signaling")
    anno_str+=add_p("")
    anno_str+='\n</div>\n'
    return(anno_str)

def add_high_marker_genes(base_dir):
    marker_str = ""
    marker_dir = "sample_clustering_and_summary/significance/high_markers/"
    marker_str = ""
    marker_str += add_tab_header("Unique Marker Genes")
    if not os.path.isfile(marker_dir+'marker_gene_annotations.tsv'):
        marker_str+=add_p("No marker genes found")
    else:
        #marker_str+=add_button_head("Highly expressed group-specific markers")
        marker_str+=add_p("PyMINEr analyzes the mean expression of each sample group and then looks for genes that meet three criteria.")
        #marker_str+=add_br()
        marker_str+=add_p("\t1) The gene is significant by 1-way ANOVA (after BH correction, alpha=0.05).")
        #marker_str+=add_br()
        marker_str+=add_p("\t2) The distance between the group with highest mean expression and second highest expression is calculated. If a gene is in the top 90th percentile of this calculation, it can make it through.")
        #marker_str+=add_br()
        marker_str+=add_p("\t3) A metric called the q-value is calculated (usually to identify outliers). The q-value is the ratio of the value calculated in number 2 compared to the range of sample group means. It's essentially what percent of the range is attributable to the distance between the highest expressing group vs the second highest expressing group.")
        #marker_str+=add_br()
        marker_str+=add_p("If all three of these criteria are, met you'll find it with an annotated group in the file below. Note that if you have several very closely related groups, there might not be many highly expressed genes that are exclusivly expressed in an individual group. In this case, you might need several markers at once to descriminate them.")
        #marker_str+=add_br()
        marker_str+=add_file_link(marker_dir+'marker_gene_annotations.tsv',"Highly expressed marker genes")
        marker_str+=add_img(marker_dir+'genes_of_interest_subset_heatmap.png',"High expression marker genes")
        marker_str+='\n</div>\n'
    marker_str+='\n</div>\n'
    return(marker_str)

def add_to_container(container, new_tab_name):
    """"""
    if container[1]=="":
        container[1]="""\n\t<button class="w3-bar-item w3-button tablink w3-red" onclick="openCity(event,'"""+new_tab_name+"""')">"""+new_tab_name+"""</button>\n"""
    else:
        container[1]+="""\n\t<button class="w3-bar-item w3-button tablink" onclick="openCity(event,'"""+new_tab_name+"""')">"""+new_tab_name+"""</button>\n"""
    return(container)


def compile_web_page(header, container, body, tail):

    container = '\n'.join(container)
    final_page = '\n'.join([header, container, body, tail])
    return(final_page)

###########################################################
def pyminer_make_website(base_dir):
    os.chdir(base_dir)

    ## first add the generic heading
    web_header = """<!DOCTYPE html>
    <html>

    <title>PyMINEr Results</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">

    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    .collapsible {
        background-color: #777;
        color: white;
        cursor: pointer;
        padding: 18px;
        width: 100%;
        border: none;
        text-align: left;
        outline: none;
        font-size: 15px;
    }

    .active, .collapsible:hover {
        background-color: #555;
    }

    .content {
        padding: 0 18px;
        display: none;
        overflow: hidden;
        background-color: #f1f1f1;
    }
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #dddddd;
    }
    </style>
    </head>

    <body>


    <div class="w3-container w3-teal">
       <h1><a href="https://www.sciencedirect.com/science/article/pii/S2211124719300920" target="_blank">PyMINEr</a> Results</h1>
    </div>



    """

    container_text = ["""    <div class="w3-container">
      
      <div class="w3-bar w3-black">""","","""  </div>\n        </div>"""]

    body = ""
    body+=add_gene_annotations(base_dir)
    container_text = add_to_container(container_text, "Gene Annotations")
    body+=add_clustering(base_dir)
    container_text = add_to_container(container_text, "Clustering")
    body+=add_statistics(base_dir)
    container_text = add_to_container(container_text, "Differential Expression")
    body+=add_genes_of_interest(base_dir)
    container_text = add_to_container(container_text, "Genes Of Interest")
    body+=add_gene_enrichment(base_dir)
    container_text = add_to_container(container_text, "Cluster Pathway Analysis")
    body+=add_high_marker_genes(base_dir)
    container_text = add_to_container(container_text, "Unique Marker Genes")
    body+=add_graph(base_dir)
    container_text = add_to_container(container_text, "Gene Expression Networks")
    body+=add_autocrine_paracrine(base_dir)
    container_text = add_to_container(container_text, "Autocrine/Paracrine Signaling")


    tail="""

    <script>
    function openCity(evt, cityName) {
      var i, x, tablinks;
      x = document.getElementsByClassName("city");
      for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablink");
      for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" w3-red", "");
      }
      document.getElementById(cityName).style.display = "block";
      evt.currentTarget.className += " w3-red";
    }
    </script>



    <script>
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
    </script>



    </body>
    </html>



    """

    out_web = compile_web_page(web_header, container_text, body, tail)


    ###########################################################
    out_web = out_web.replace('//','/')
    out_web = out_web.replace(base_dir,'')

    make_file(out_web,out_file)
    return()



if __name__ == "__main__":
    ####################
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-base_dir','-in','-i','-input',
        dest='base_dir',
        type=str)
    args = parser.parse_args()
    ####################
    base_dir = os.path.join(args.base_dir)


    pyminer_make_website(base_dir)
#cmd('firefox '+out_file)
