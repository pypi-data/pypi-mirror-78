#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput, random
import numpy as np
try:
    from pyminer.common_functions import *
except:
    from common_functions import *
## check that we have gprofiler installed
try:
    from gprofiler import GProfiler
except:
    sys.exit('please install gprofiler; try: pip3 install gprofiler-official==0.3.5')
else:
    from gprofiler import GProfiler

#import pandas as pd
##############################################################
## basic function library
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

# all_calls = []
# def cmd(in_message, com=True):
#     global all_calls
#     if type(in_message)==list:
#         in_message = ' '.join(in_message)
#     print(in_message)
#     all_calls.append(in_message)
#     time.sleep(.25)
#     if com:
#         Popen(in_message,shell=True).communicate()
#     else:
#         Popen(in_message,shell=True)

# def check_infile(infile):
#     if os.path.isfile(infile):
#         return
#     else:
#         sys.exit(str('could not find '+infile))

# def outfile_exists(outfile):
#     if os.path.isfile(outfile):
#         statinfo = os.stat(outfile)
#         if statinfo.st_size!=0:
#             return(True)
#         else:
#             return(False)
#     else:
#         return(False)


####################################################################################


###########################
def convert_to_human(in_genes, species):
    ## setup the api
    gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)

    temp_lookup={}
    gene_symbol_dict = {}
    gene_def_dict = {}
    for g in in_genes:
        temp_lookup[g] = []
        gene_symbol_dict[g] = []
        

    # import inspect
    # code = inspect.getsource(gp.gorth)
    # print(code)
    results = gp.gorth(in_genes, 
        source_organism = species,
        target_organism='hsapiens')




    for i in range(1,len(results)):
        temp_id = results[i][1]
        temp_hu_symbol = results[i][5]
        temp_hu_def = results[i][6]
        if temp_id not in gene_symbol_dict:
            print(temp_id,"to:")
            temp_id = in_genes[int(results[i][0])-1]
            print("\t",temp_id)
        if temp_id not in gene_symbol_dict:
            pass#print('weired mapping event with:',temp_id)
        elif temp_hu_symbol != None:
            temp_symbol_list = gene_symbol_dict[temp_id]
            temp_symbol_list.append(temp_hu_symbol)
            gene_symbol_dict[temp_id] = temp_symbol_list
            gene_def_dict[temp_id] = temp_hu_def



    return(gene_symbol_dict,gene_def_dict,results)


def convert_to_ensg(in_genes, species = 'hsapiens'):

    ## setup the api
    gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)

    temp_lookup={}
    gene_symbol_dict = {}
    gene_def_dict = {}
    for g in in_genes:
        temp_lookup[g] = []
        gene_symbol_dict[g] = []
        gene_def_dict[g] = []


    results = gp.gconvert(in_genes, 
        organism = species, target='ENSG',numeric_ns="ENTREZGENE_ACC")


    for i in range(1,len(results)):
        temp_id = results[i][1]
        temp_id = temp_id.replace("ENTREZGENE_ACC:","")
        temp_hu_symbol = results[i][4]
        temp_def = results[i][5]
        if temp_id not in gene_symbol_dict:
            print(temp_id,"to:")
            temp_id = in_genes[int(results[i][0])-1]
            print("\t",temp_id)
        if temp_id not in gene_symbol_dict:
            print('weird mapping event with:',temp_id)
        elif temp_hu_symbol != None:
            temp_symbol_list = gene_symbol_dict[temp_id]
            temp_symbol_list.append(temp_hu_symbol)
            gene_symbol_dict[temp_id] = temp_symbol_list
            temp_def_dict = gene_def_dict[temp_id]
            temp_def_dict.append(temp_def)

    return(gene_symbol_dict,gene_def_dict,results)

##############################################################

def pyminer_gprofiler_converter_main(ID_list,
                                     out,
                                     species='hsapiens',
                                     annotations = False):
    ## if we will need to convert to human IDs
    if species != "hsapiens" and not annotations:
        convert = True
    else:
        convert = False


    ###########################
    ## convert id_list to a gene lookup table and write it to file

    ## load in the ID list
    temp_ID_list = read_file(ID_list)
    ID_list = []
    for temp_id in temp_ID_list:
        try:
            int(float(temp_id))
        except:
            ID_list.append(temp_id)
        else:
            ID_list.append(str(int(float(temp_id))))
            #print('found int')


    ## convert to ensg
    symbol_dict, def_dict, annotation_table = convert_to_ensg(ID_list, species)
    write_table(annotation_table,args.out+".tsv")

    for i in range(0,5):
        print(ID_list[i])
        print('\t',symbol_dict[ID_list[i]])

    save_dict((symbol_dict,def_dict),args.out+".pkl")

    ## write the ortholgoues
    if convert:
        human_symbol_dict, human_def_dict, full_orthologue_table = convert_to_human(ID_list, species)
        save_dict((human_symbol_dict, human_def_dict), args.out+".pkl")
        write_table(full_orthologue_table,args.out+".tsv")

    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ID_list",'-ids', '-IDs','-i', 
        help="a file containing gene ids separated on new lines",
        type = str)
    parser.add_argument("-out", '-outfile', '-o',
        help="the file that we'll write the results to",
        type = str)
    parser.add_argument("-species", '-s',
        help="a gProfiler accepted species code. Dafault = 'hsapiens'",
        type = str,
        default = 'hsapiens')
    parser.add_argument("-annotations",
        help="just get the annotation table",
        action = 'store_true',
        default = False)
    args = parser.parse_args()
    pyminer_gprofiler_converter_main(ID_list = args.ID_list,
                                     out = args.out,
                                     species = args.species,
                                     annotations = args.annotations)
##############################################################




##############################################################
##############################################################


##############################################################
##############################################################







