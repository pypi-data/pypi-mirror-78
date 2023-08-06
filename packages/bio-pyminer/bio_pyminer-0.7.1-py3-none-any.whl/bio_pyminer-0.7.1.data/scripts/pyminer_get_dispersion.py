#!/home/scott/anaconda3.7/bin/python3
##import dependency libraries
import sys,time,glob,os,pickle,fileinput, random, h5py
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from sklearn.neighbors import RadiusNeighborsRegressor as neighbors

import matplotlib.pyplot as plt
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
            table[i]=delim.join(str(table[i]))+'\n'
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



##############################################################



##############################################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-infile","-i", 
    help="the input expression matrix",
    type = str)
parser.add_argument("-out_dir", '-out','-o',
    help="the directory for output files",
    type = str)
parser.add_argument("-log", 
    help="log transform the means",
    action = 'store_true',
    default = False)
parser.add_argument("-hdf5", 
    help="the input file is an hdf5 file",
    action = 'store_true',
    default = False)
parser.add_argument("-ids", '-ID_list','-id_list',
    help="if an hdf5 file is used, we'll need the list of IDs",
    type = str)
parser.add_argument("-z_cutoff", "-z",
    help="the cutoff for how many standard deviations over the mean residual should be considered overdispersed. Default = 0.5",
    type = float,
    default = .5)
args = parser.parse_args()
if args.out_dir[-1]!='/':
	args.out_dir+='/'
if not os.path.isdir(args.out_dir):
    cmd('mkdir '+args.out_dir)
##############################################################
gc.enable()
## read in the input file
if not args.hdf5:
    in_mat_str = np.array(read_table(args.infile))
    in_mat = np.array(in_mat_str[1:,1:],dtype=float)
    ID_list = in_mat_str[1:,0].tolist()
    del in_mat_str
else:
    ## read in the hdf5 file
    print('reading hdf5 file:\n\t',args.infile)
    h5f = h5py.File(args.infile, 'r')
    in_mat=h5f["infile"]
    ID_list = read_file(args.ids,'lines')




if args.log:
    if np.min(in_mat)<0.0:
        print("can't log transform with negative values... Bringing the matrix up to min = 1")
        in_mat+=min(in_mat)
    in_mat = np.log2(1 + in_mat)



## calculate the means
means = np.mean(in_mat,axis=1)
## calculate the coefficient of variance
variance = np.std(in_mat,axis=1)#/(means+1)
## square the coefficient of variance
variance*=variance

## remove the nans

print(np.sum(np.isnan(variance)))
variance[np.isnan(variance)]=0
print(np.sum(np.isnan(variance)))


linear_dim = np.shape(means)


## plot (a random sample of) the relationship between the coefficient of variance and means
max_sample_size = 50000
sample_size = min([max_sample_size,linear_dim[0]])
if sample_size < max_sample_size:
	print('sampling the distribution for',sample_size,'points')
	index_vect  = np.arange(linear_dim[0])
	np.random.shuffle(index_vect)
	sample = index_vect[:sample_size].tolist()
	## always include the min and max values for interpolation
	x_max_index = np.where(np.array(means) == np.max(means))[0][0]
	x_min_index = np.where(np.array(means) == np.min(means))[0][0]
	#print(sample)
	#print(type(sample))
	#sample = sample.tolist()
	if x_max_index not in sample:
		sample.append(x_max_index)
	if x_min_index not in sample:
		sample.append(x_min_index)
	#print(sample)
	print(type(sample))
else:
    sample = np.arange(linear_dim[0], dtype =  int).tolist()
    #print(sample)
    #sys.exit()

sample = np.sort(sample)
## remove the indices where the variance is zero
keep_sample = np.where(variance[sample]>0)[0]
sample = sample[keep_sample]

plt.scatter(means[sample], variance[sample], c = 'black', s = 0.5)#,xlab = 'mean',ylab = 'CV')
#plt.show()
#sys.exit()

## do the lowess fit. This returns the expected values of the variance
print('calculating the best fit curve')

## 

neigh = neighbors(radius = 1.0, weights = 'uniform', leaf_size = 30)
mean_max = max(means)
mean_min = min(means)
sds_min = min(variance)

## first calculate the lowess curve on the sample
lowess_estimates_sample = lowess(variance[sample]-sds_min+1,means[sample]-mean_min+1, delta = 0.01*mean_max)-1
# lowess_estimates_sample[:,0] = lowess_estimates_sample[:,0] + mean_min
# lowess_estimates_sample[:,1] = lowess_estimates_sample[:,1] + sds_min

## remove the nans 
lowess_estimates_sample[np.isnan(lowess_estimates_sample)]=0

print(lowess_estimates_sample)

## remove x ties from the lowess as this messes up the interpolation
values, indices = np.unique(lowess_estimates_sample[:,0], return_index=True)
lowess_estimates_sample = np.array(lowess_estimates_sample[indices,:])
print(lowess_estimates_sample)
print(type(lowess_estimates_sample))
#sys.exit()

## then interpolate the curve to smooth it out and provide the nearest neighbor regression with the needed coverage
from scipy.interpolate import interp1d

# ## positive control
# x = np.linspace(0, 10, num=11, endpoint=True)
# print(x)
# y = np.cos(-x**2/9.0)
# print(y)
# f2 = interp1d(x, y, kind='cubic')
# print(f2)
# xnew = np.linspace(0, 10, num=41, endpoint=True)
# print(xnew)
# print(f2(xnew))

print(np.shape(lowess_estimates_sample[:,0]))
print(np.shape(lowess_estimates_sample[:,1]))

## cross the spread
print("original_min_max:",min(lowess_estimates_sample[:,0]),max(lowess_estimates_sample[:,0]))


epsilon = (max(lowess_estimates_sample[:,0]) - min(lowess_estimates_sample[:,0]))*0.01
print('epsilon:',epsilon)

#make the new x values evenly spaced a
temp_min = min(lowess_estimates_sample[:,0])# - epsilon
temp_max = max(lowess_estimates_sample[:,0])# + epsilon
new_x = np.linspace(temp_min,temp_max, num=sample_size, endpoint = True)
#new_x = np.linspace(temp_min,temp_max, num=sample_size, endpoint = True)
#new_x[0] = temp_min
#new_x[-1] = temp_max

interpolation = interp1d(lowess_estimates_sample[:,0], lowess_estimates_sample[:,1], kind='cubic')


print("new_min_max:",min(new_x),max(new_x))
print(new_x)

## interpolate the lowess function
new_y = interpolation(new_x)
print(new_x,new_y)

## get the interplated lowess ready for nearest neighbor regression
train_x = np.array([[x] for x in lowess_estimates_sample[:,0].tolist()])
train_y = lowess_estimates_sample[:,1]

full_x = np.array([[x] for x in means.tolist()])
#train_x = full_x[sample]
#train_y = variance[sample]

print(train_x)
print(train_y)
#neigh.fit(train_x,train_y)
print(new_x)
print(new_y)
new_x = np.array([[x] for x in new_x.tolist()])

#plt.clf()
plt.scatter(new_x,new_y, c = 'red', s = 0.75)
plt.savefig(args.out_dir+'local_fit.png',dpi=600,bbox_inches='tight')
#plt.show()
#sys.exit()
neigh.fit(new_x,new_y)

## now calculate the values for everything else
bin_size = 100000
total_vars = len(means)
bins = []
cur_bin = 0
while cur_bin<total_vars:
	bins.append(min(cur_bin, total_vars))
	cur_bin+=bin_size

bins.append(total_vars)
print(bins)

lowess_estimates = np.zeros((len(means),))
# for i in range(1,len(bins)):
# 	print("working on",bins[i-1],bins[i])
# 	# if i%50000 == 0:
# 	# 	print('\t',bins[i]/len(means))
# 	lowess_estimates[bins[i-1]:bins[i]] += neigh.predict(full_x[bins[i-1]:bins[i]])

for i in range(0,total_vars):
    x_dif_vect = np.abs(full_x[i]-new_x)
    closest_idx = int(np.argmin(x_dif_vect))
    lowess_estimates[i]=new_y[closest_idx]
    



#lowess_estimates = neigh.predict(full_x)

#lowess_estimates = lowess(variance[sample]+1,means[sample]+1)-1#, return_sorted = False)#, frac = 1e-3, delta = 1e-10*max(means))
#lowess_estimates = [x[0] for x in lowess_estimates]


#plt.scatter(means[sample],lowess_estimates[sample],c='red',s=0.5)
#plt.savefig(args.out_dir+'local_fit_sample.png',dpi=600,bbox_inches='tight')
#plt.show()
#sys.exit()
## calculate the residuals
print('getting the residuals')
residuals = variance - lowess_estimates


# print(lowess_estimates)
# # sys.exit()
# print(residuals - variance)
# sys.exit()
print('sample_means',means[:10])
print('sample_estimates',lowess_estimates[:10])
print('sample_CVs',variance[:10])
print('sample_residuals',residuals[:10])


## reshape it back into the table
resid_table = residuals

print(np.sum(np.isnan(residuals)))
nan_idx = np.where(np.isnan(residuals))[0]

print('nan means',means[nan_idx])
print('nan sds',variance[nan_idx])
print('nan estimates',lowess_estimates[nan_idx])
print('nan resid',residuals[nan_idx])


#print(np.nan_std(residuals))
st_dev_resid = np.std(residuals)
print('sd residuals:',st_dev_resid)

st_dev_cutoff = st_dev_resid*args.z_cutoff
print('residual cutoff for overdispersion:',st_dev_cutoff)

## plot the residuals
plt.clf()
plt.scatter(means[sample],residuals[sample], c = 'black', s = 0.5)#,xlab = 'mean',ylab = 'CV')
plt.plot([min(means),max(means)],[0,0],c='red')
## find the significant residuals
resid_sample = residuals[sample]
mean_sample = means[sample]
sig_indices = np.where(resid_sample >= st_dev_cutoff)[0]
plt.scatter(mean_sample[sig_indices], resid_sample[sig_indices], c = 'blue', s = 2)
plt.savefig(args.out_dir+'residuals.png',dpi=600,bbox_inches='tight')
#plt.show()


## determine which genes are locally overdispersed
print('calculating local overdispersion')
local_overdispersion_bool_table = resid_table >= st_dev_cutoff

print('number of overdispersed genes:')
number_overdispersed_per_group = np.sum(local_overdispersion_bool_table, axis = 0)
print(number_overdispersed_per_group)



## get the boolean overdispersed table ready for writing to file
#print(np.shape(local_overdispersion_bool_table))
#print(local_overdispersion_bool_table)
local_overdispersion_bool_table = np.array(local_overdispersion_bool_table,dtype = str)
#print(local_overdispersion_bool_table)
local_overdispersion_bool_table=local_overdispersion_bool_table.tolist()
print(local_overdispersion_bool_table[:5],len(local_overdispersion_bool_table))
print(np.shape(means)[0])
## add the gene names
gene_names = ID_list
for i in range(0,(np.shape(means)[0])):
    #print(i)
    local_overdispersion_bool_table[i] = [gene_names[i]] + [local_overdispersion_bool_table[i]]


local_overdispersion_bool_table=np.array(local_overdispersion_bool_table, dtype = str)
print(local_overdispersion_bool_table)
print(np.shape(local_overdispersion_bool_table))

write_table(local_overdispersion_bool_table,args.out_dir+'/locally_overdispersed_boolean_table.txt')




