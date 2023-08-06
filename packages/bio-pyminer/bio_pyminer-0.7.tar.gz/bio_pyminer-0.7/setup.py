
import setuptools
import glob
import gzip
import shutil
import os
from copy import deepcopy
##############################################

LIB_DEST = '/usr/local/lib/cell_signals/'

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read()

script_list = []
for script in glob.glob("pyminer/*.py"):
    if '__init__' not in script:
        script_list.append(script)

setuptools.setup(
     name='bio_pyminer',  
     version='0.7',
     author="Scott Tyler",
     author_email="scottyler89@gmail.com",
     description="PyMINEr: automated biologic insights from large datasets.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     install_requires = install_requires,
     url="https://scottyler892@bitbucket.org/scottyler892/pyminer",
     packages=setuptools.find_packages(),
     scripts = script_list,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Affero General Public License v3",
         "Operating System :: OS Independent",
     ],
 )


lib_list = []
for lib_file in glob.glob("lib/*"):
    lib_list.append(lib_file)
print("\n\ncopying over data files")
if not os.path.isdir(LIB_DEST):
    os.mkdir(LIB_DEST)
for lib_file in lib_list:
    if lib_file[:-3] == '.gz':
        with gzip.open(lib_file, 'rb') as f_in:
            new_file_name = deepcopy(lib_file).replace('.gz','')
            new_file_name = new_file_name.replace('lib/','')
            new_file_name = os.path.join(LIB_DEST,new_file_name)
            print("copying",lib_file,"to",new_file_name)
            with open(new_file_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        with open(lib_file, 'rb') as f_in:
            new_file_name = lib_file.replace('lib/','')
            new_file_name = os.path.join(LIB_DEST,new_file_name)
            print("copying",lib_file,"to",new_file_name)
            with open(new_file_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
