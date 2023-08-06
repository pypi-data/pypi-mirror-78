#!/usr/bin/env python3

import fileinput, h5py, argparse, os, sys
import numpy as np

try:
    from pyminer.common_functions import *
except:
    from common_functions import *


def h5_to_tab(infile, rows, cols, out):
	infile = os.path.abspath(infile)
	out = os.path.abspath(out)
	## read the hdf5
	h5f = h5py.File(infile, 'r')
	in_mat = h5f["infile"]
	row_labs = read_file(rows)
	col_labs = read_file(cols)
	## will need to add new line only to non-last lines
	counter_end = len(row_labs)-1
	counter = 0
	## set up the output file
	f = open(out, 'w')
	## write the first line
	f.write('\t'.join(col_labs)+'\n')
	## write the subsequent lines
	for i in range(len(row_labs)):
		if counter % 1000==0:
			print('\tline',counter)
		temp_line = [row_labs[i]]+list(map(str,in_mat[i,:].tolist()))
		temp_line = '\t'.join(temp_line)
		if i != counter_end:
			temp_line+='\n'
		else:
			print("reached the end of the file:",counter)
		f.write(temp_line)
		counter+=1
	h5f.close()
	f.close()
	return()





if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-infile','-i',
		                type=str,
		                help = "this must be a tab delimited file which will be converted to the hdf5 format (output will be created with the same filename with the .hdf5 extention)")
	parser.add_argument('-rows','-ID_list', '-ids',
		                type=str,
		                help = "")
	parser.add_argument('-cols','-columns',
		                type=str,
		                help = "")
	parser.add_argument('-out','-o',
		                type=str,
		                help = "")
	args = parser.parse_args()
	h5_to_tab(args.infile, args.rows, args.cols, args.out)