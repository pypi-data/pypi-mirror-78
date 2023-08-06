#!/usr/bin/env python3

import fileinput, h5py, argparse, os, sys, scipy
import numpy as np
from scipy.sparse import csc_matrix, lil_matrix

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str, help = "this must be a tab delimited file which will be converted to the hdf5 format (output will be created with the same filename with the .hdf5 extention)")
<<<<<<< HEAD
# parser.add_argument('-sparse', 
# 	                action="store_true",
# 	                help = "add this argument if you want to make it a sparse (scipy csc format)")
=======
parser.add_argument('-sparse', 
	                action="store_true",
	                help = "add this argument if you want to make it a compressed matrix. Takes up less space, but is slower")
>>>>>>> d362fc61e0a62383450b5d042be8c77c99e4bbc6

args = parser.parse_args()

args.infile = os.path.abspath(args.infile)
# if args.sparse:
# 	import h5sparse as h5py
###################################################
## first read through the input tab delim 
## file to see the dimentions of the input matrix
print('reading in the file, please wait')
line_count = 0
cols = None
col_names = None
ID_list = [] ## the variable names (the length here will also be the number of rows in the .h5 matrix)
for line in fileinput.input(args.infile):
	line = line.strip()
	line = line.split('\t')
	if line_count % 1000==0:
		print('\tline',line_count)
	if line_count==0:
		## note that the number of columns for the
		## hdf5 file will be cols-1 because the first
		## column in the input file will be the 
	    cols = len(line)
	    col_names = line
	else:
		if cols!=len(line):
			sys.exit('there is a line ('+str(line_count)+') has an inconsistent number of rows with previous rows')
		ID_list.append(line[0])
		
		
	line_count += 1

fileinput.close()

##########################

def make_file(contents,path):
    f=open(path,'w')
    if isinstance(contents,list):
        f.writelines(contents)
    elif isinstance(contents,str):
        f.write(contents)
    f.close()

temp=str(args.infile).split('/')
temp=('/').join(temp[:-1])

make_file('\n'.join(col_names),temp+'/column_IDs.txt')
make_file('\n'.join(ID_list),temp+'/ID_list.txt')


##########################

print('we detected '+str(len(ID_list))+'\t'+'data rows')
print('   and      '+str(cols-1)+'\t'+'data cols')

print()
###################################################

print("now we will make the hdf5 file and populate it with the values from your input dataset")

outfile = os.path.splitext(args.infile)[0]+'.hdf5'
f = h5py.File(outfile, "w")

## set up the data matrix (this assumes float32)
if False:#args.sparse:
	dset = lil_matrix((len(ID_list),cols-1))
	#dset = csc_matrix((len(ID_list),cols-1))
	#dset = f.create_dataset("infile", (len(ID_list),cols-1), dtype=csc_matrix)
else:
<<<<<<< HEAD
	dset = f.create_dataset("infile",
		                    (len(ID_list),cols-1),
		                    dtype=np.float32,
		 			        fillvalue=0.,
                            compression='gzip',
                            compression_opts=9)
=======
	if args.sparse:
		dset = f.create_dataset("infile",
			                    (len(ID_list),cols-1),
			                    dtype=np.float32,
			 			        fillvalue=0.,
	                            compression='gzip',
	                            compression_opts=9)
	else:
		dset = f.create_dataset("infile",
			                    (len(ID_list),cols-1),
			                    dtype=np.float32)
>>>>>>> d362fc61e0a62383450b5d042be8c77c99e4bbc6

## populate dset with the values from the input dataset
line_count = 0
for line in fileinput.input(args.infile):
	line = line.strip()
	line = line.split('\t')
	if line_count % 1000==0:
		print('\tline',line_count)
	if line_count==0:
	## the first line should be column headers, so it is not included
		pass
	else:
		dset[(line_count-1),:] = np.array(list(map(np.float32, line[1:])))
		
		
	line_count += 1

## close the input file
fileinput.close()

## close the hdf5 file
if False:#args.sparse:
	f["infile"]=csc_matrix(dset)
f.close()


################


## validate the hdf5 file
#h5f = h5py.File(outfile, 'r')
#
#print(h5f["infile"][0])










