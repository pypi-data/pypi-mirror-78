# README #

### Tutorials ###

I've made some videos that walk you through the outputs as well as how to install and use PyMINEr here:
www.ScienceScott.com/pyminer

### What is this repository for? ###

* cell type identification using novel clustering algorithms that outperform some competitors when applied to both real-world and synthetic datasets
* basic statistics & enrichment analyses
* pathway analyses
* Spearman correlation-based expression graphs that enable analyses by graph theory 
* creation of in silico predicted autocrine/paracrine signaling networks within and across cell types
* creation of publication-ready visuals based on these analyses
* generation of a web page explaining the results of the run

* Future releases will contain updated clustering methods that work for reconstructing single cell lineages, among other cool functions _stay tuned_

### How do I get set up? ###

* If you're on a unix system, simply run:
***  ***
* note that PyMINEr has only been tested 

### How do I run PyMINEr? ###
PyMINEr takes as input a cleaned and normalized (typically log transformed) tab delimited 2D matrix text file.
For example:

    genes	cell_1	cell_2	...
    ACTB   5.3012	 6.3102	...
    ...	...	...	...

You can feed this text file into PyMINEr in the command line:

`pyminer.py -i expression.txt`

If you have a really big file, you can convert it to hdf5 so that you can run the pipeline outside of memory:

`tab_to_h5.py expression.txt`

This will generate 3 files:
* *expression.hdf5* 
* *ID_list.txt* the list of genes (no header line)
* *column_IDs.txt* the sample names for the columns.

That's about it. There are some other interesting things you can do though, like if you are working with something that isn't human, you should be able to pass in the argument -species, 
followed by a species code that is taken by gProfiler. This will automate tons of pathway analyses, so long as the variables you're working with can be mapped over to Ensembl gene IDs by gProfiler.
The default is homo sapiens (hsapiens).

A list of the gProfiler accepted species codes is listed here: https://biit.cs.ut.ee/gprofiler/page/organism-list

### License ###
For non-commercial use, PyMINEr is available via the AGPLv3 license. Commercial entities should inquire with scottyler89@gmail.com

### Who do I talk to? ###

* Repo owner/admin: scottyler89+bitbucket@gmail.com