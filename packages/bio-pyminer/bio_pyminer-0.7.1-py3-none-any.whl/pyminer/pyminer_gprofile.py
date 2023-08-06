#!/usr/bin/env python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse
from subprocess import Popen
from operator import itemgetter
import gc, fileinput, random
import numpy as np
import argparse
from copy import deepcopy
##############################################################
##############################################################
## check that we have gprofiler installed
try:
    from gprofiler import GProfiler
except:
    sys.exit('please install gprofiler; try: pip3 install gprofiler-official')
else:
    from gprofiler import GProfiler

##############################################################
##############################################################
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

all_calls = []
def cmd(in_message, com=True):
	global all_calls
	if type(in_message)==list:
		in_message = ' '.join(in_message)
	print(in_message)
	all_calls.append(in_message)
	time.sleep(.25)
	if com:
		Popen(in_message,shell=True).communicate()
	else:
		Popen(in_message,shell=True)

def check_infile(infile):
	if os.path.isfile(infile):
		return
	else:
		sys.exit(str('could not find '+infile))

def outfile_exists(outfile):
	if os.path.isfile(outfile):
		statinfo = os.stat(outfile)
		if statinfo.st_size!=0:
			return(True)
		else:
			return(False)
	else:
		return(False)
##############################################################
##############################################################



## fix for entrez...
def process_genes(in_genes):
    out_genes = []
    for gene in in_genes:
        try:
            float(gene)
        except:
            out_genes.append(gene)
        else:
            temp_gene = str(int(float(gene)))
            out_genes.append(temp_gene)
    return(out_genes)


def do_gprofiler_analysis(infile, out, species = 'hsapiens', background = None, verbose = False, silent = True):
    ## setup the api
    gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)

    ## import the gene names
    genes = read_file(args.infile, linesOraw = 'lines')

    if args.verbose:
        print("genes:\n",genes)

    if args.background != None:
        if os.path.isfile(args.background):
            temp_bg = read_file(args.background,linesOraw = 'lines')
        else:
            temp_bg = str(args.background)
            temp_bg = temp_bg.split(',')
        if args.verbose:
            print("Background:\n",temp_bg)
        result = gp.gprofile(process_genes(genes), custom_bg = temp_bg, organism = args.species)
    else:
        result = gp.gprofile(process_genes(genes), organism = args.species)

    if args.verbose:
        print(result)
        for line in result:
            print(line)

    if args.out == None:
        args.out = args.infile[:-4]+'_gProfiler.txt'

    write_table(deepcopy(result), args.out)
    if silent:
        return()
    else:
        return(results)


#####################################################

if __name__ == "__main__":

    parser = argparse.ArgumentParser()


    parser.add_argument("-infile",'-i', '-input', 
        help="a file containing gene ids separated on new lines",
        type = str)

    parser.add_argument("-out", '-outfile', '-o',
        help="the file that we'll write the results to",
        type = str)

    parser.add_argument("-species", '-s',
        help="a gProfiler accepted species code. Dafault = 'hsapiens'",
        type = str,
        default = 'hsapiens')

    parser.add_argument("-background", '-b',
        help="If you are going to use a custom background provide either a comma separated list (no spaces), or a file with genes on a new line each.",
        type = str,
        default = None)

    parser.add_argument(
        "-verbose","-v",
        action="store_true")

    args = parser.parse_args()

    do_gprofiler_analysis(args.infile, args.out, species = args.species, background = args.background, verbose = args.verbose, silent = True)






