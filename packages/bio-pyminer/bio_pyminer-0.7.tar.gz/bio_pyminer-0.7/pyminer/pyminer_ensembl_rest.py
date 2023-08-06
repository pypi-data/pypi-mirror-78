#!/usr/bin/env python3
import time
import os
import pickle
import sys
import json
import time
import argparse
from subprocess import Popen
from copy import deepcopy

# Python 2/3 adaptability
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError
######################################################################
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

def make_table(lines,delim, num_type = float):
    #print(num_type)
    for i in range(0,len(lines)):
        lines[i]=lines[i].strip()
        lines[i]=lines[i].split(delim)
        for j in range(0,len(lines[i])):
            try:
                float(lines[i][j])
            except:
                lines[i][j]=lines[i][j].replace('"','')
            else:
                if num_type == float:
                    lines[i][j]=float(lines[i][j])
                elif num_type == int:
                    lines[i][j]=int(float(lines[i][j]))
                else:
                    lines[i][j]=num_type(lines[i][j])
    return(lines)


def get_file_path(in_path):
    in_path = in_path.split('/')
    in_path = in_path[:-1]
    in_path = '/'.join(in_path)
    return(in_path+'/')


def read_table(file, sep='\t',num_type=float):
    return(make_table(read_file(file,'lines'),sep,num_type=num_type))
    

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


######################################################################
## 

######################################################################

## the below block of code was built from:
## https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client
class EnsemblRestClient(object):
    def __init__(self, server='http://rest.ensembl.org', reqs_per_sec=15):
        self.server = server
        self.reqs_per_sec = reqs_per_sec
        self.req_count = 0
        self.last_req = 0
    def perform_rest_action(self, endpoint, hdrs=None, params=None):
        if hdrs is None:
            hdrs = {}
        if 'Content-Type' not in hdrs:
            hdrs['Content-Type'] = 'application/json'
        if params:
            endpoint += '?' + urlencode(params)
        data = None
        print(endpoint)
        # check if we need to rate limit ourselves
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req
            if delta < 1:
                time.sleep(1 - delta)
            self.last_req = time.time()
            self.req_count = 0
        try:
            request = Request(self.server + endpoint, headers=hdrs)
            response = urlopen(request)
            content = response.read()
            if content:
                data = json.loads(content)
            self.req_count += 1
        except HTTPError as e:
            # check if we are being rate limited by the server
            if e.code == 429:
                if 'Retry-After' in e.headers:
                    retry = e.headers['Retry-After']
                    time.sleep(float(retry))
                    self.perform_rest_action(endpoint, hdrs, params)
            else:
                sys.stderr.write('Request failed for {0}: Status code: {1.code} Reason: {1.reason}\n'.format(endpoint, e))
        return data
    def get_variants(self, species, symbol):
        genes = self.perform_rest_action(
            endpoint='/xrefs/symbol/{0}/{1}'.format(species, symbol), 
            params={'object_type': 'gene'}
        )
        if genes:
            stable_id = genes[0]['id']
            variants = self.perform_rest_action(
                '/overlap/id/{0}'.format(stable_id),
                params={'feature': 'variation'}
            )
            return variants
        return None


    def get_regulatory_elements_from_region(self, contig, start, end, feat = ["regulatory","other_regulatory", "motif"]):
        out_dict = {}
        for f in feat:
            endpoint = "/overlap/region/human/"+contig+":"+start+".."+end
            endpoint += "?feature="+f
            print('\n\n\n',endpoint)
            temp_locus_response = self.perform_rest_action(endpoint)#, params = "feature=gene")
            print(temp_locus_response,'\n\n\n')
            out_dict[f] = temp_locus_response
        return(out_dict)

######################################################################


def run(species, symbol):
    ## help with resful: http://rest.ensembl.org/?content-type=text/html
    ## http://rest.ensembl.org/variation/human/rs1199776527
    ## http://rest.ensembl.org/overlap/region/human/7:140924917..140924917?feature=gene
    ## http://rest.ensembl.org/info/variation/consequence_types/
    ###### eqtl with result
    ## http://rest.ensembl.org/eqtl/variant_name/human/rs7683255
    ###### eqtl without result
    ## http://rest.ensembl.org/eqtl/variant_name/human/rs1310656119 
    client = EnsemblRestClient()
    variants = client.get_variants(species, symbol)
    if variants:
        for v in variants:
            print('{seq_region_name}:{start}-{end}:{strand} ==> {id} ({consequence_type})'.format(**v))

######################################################################

class variant_obj():
    def __init__(self,client,rsID):
        self.id = rsID
        self.var_details = {}
        self.genes = []## these are in Ensembl format
        self.nearest_genes = []## this is a list in case there are several genes that overlap with the variant locus
        self.all_locus_response = []
        self.mapped_loci = []
        self.prot_muts = []
        self.trans_muts = []
        ## general mutation info
        self.var_is_bad = False
        self.mutation_type = None
        ## regulatory element info
        self.regulatory_elements = []
        self.regulatory = []
        self.other_regulatory = []
        self.motif = []
        ## tad info
        self.tad_boundaries_crossed = 0
        self.tads = []
        self.tad_annotations = []
        ## gene info
        self.detailed_gene_info = []
        self.gene_symbols = []## mapped through gProfiler to symbols from Ensembl
        self.symbol_to_gene_lookup = {}## this is for the reverse lookup after finding gene symbol information to go back to the gene that that symbol come from
        ## search term info
        self.gene_search_term_comentions = []## search of the gene symbols that mapped from this variant to the search terms
        self.best_gene_search_term_match = []
        ## eqtls
        self.eqtls={}
        ## scRNAseq mapping
        self.scRNAseq_ids = []
        self.get_direct_cause(client,self.id)


    def check_bad(self, in_consequence):
        types_of_mutations_acceptable = ['3_prime_UTR_variant','5_prime_UTR_variant','coding_sequence_variant','feature_truncation','frameshift_variant','incomplete_terminal_codon_variant','inframe_deletion','inframe_insertion','mature_miRNA_variant','missense_variant','NMD_transcript_variant','non_coding_transcript_exon_variant','protein_altering_variant','splice_acceptor_variant','splice_donor_variant','splice_region_variant','start_lost','start_retained_variant','stop_gained','stop_lost','stop_retained_variant','transcript_ablation','transcript_amplification']
        if in_consequence in types_of_mutations_acceptable:
            return(True)
        else:
            return(False)


    def is_bad_mutation(self,var_details):
        if "most_severe_consequence" in var_details:
            self.mutation_type = var_details["most_severe_consequence"]
            if self.check_bad(self.mutation_type):
                return(True)
        return(False)


    def set_all_loci(self, var_details):
        genes = []
        if var_details == {}:
            ## take care of the null case in which it wasn't mappable
            self.mapped_loci.append({"contig":"NA", "start":0, "end":0})
        else:
            ## one approach is to get the intervals and look that up 
            for locus in var_details["mappings"]:
                #print(locus)
                if locus["assembly_name"]=="GRCh38":
                    temp_contig = locus["seq_region_name"]
                    temp_start = locus["start"]
                    if "end" in locus:
                        temp_end = locus["end"]
                    else:
                        temp_end = deepcopy(temp_start)
                    interval = [temp_start,temp_end]
                    start = int(min(interval))
                    end = int(max(interval))
                    self.mapped_loci.append({"contig":temp_contig, "start":start, "end":end})
                    if temp_contig[:3] != "chr":
                        self.mapped_loci.append({"contig":"chr"+temp_contig, "start":start, "end":end})
                    else:
                        self.mapped_loci.append({"contig":temp_contig[3:], "start":start, "end":end})
        print("\n\n",self.mapped_loci,"\n\n")
        return


    def ensp_to_ensg(self, client, ensp_list=[]):
        if len(ensp_list)==0:
            return([])
        enst_list = []
        for ensp in ensp_list:
            #https://rest.ensembl.org/documentation/info/overlap_translation
            temp_response = client.perform_rest_action("/overlap/translation/"+ensp+"?feature=transcript_variation;type="+self.mutation_type+";content-type=application/json")
            if temp_response is None:
                pass
            else:
                for element in temp_response:
                    if element['id'] == self.id:
                        enst_list.append(element["Parent"])
                        for key, value in element.items():
                            print(key, '\n\t',value)
        enst_list = sorted(list(set(enst_list)))
        print(enst_list)
        ensg_list = self.enst_to_ensg(client, enst_list)
        print(ensg_list)
        return(ensg_list)


    def enst_to_ensg(self, client, enst_list=[]):
        if len(enst_list)==0:
            return([])
        ensg_list = []
        for enst in enst_list:
            temp_response = client.perform_rest_action("/lookup/id/"+enst+"?expand=1;content-type=application/json?feature=Parent")
            if temp_response is None:
                pass
            else:
                ensg_list.append(temp_response["Parent"])
        ensg_list = sorted(list(set(ensg_list)))
        print(ensg_list)
        #sys.exit()
        return(ensg_list)


    def get_var_recoder(self, client, var_details):
        print(var_details)
        self.var_details = var_details
        #### this is to replace get_gene_from_var in only the aspect of variant annotation if var_is_bad
        ## We will need to set nearest gene as well as var details, and return the list genes that are annotated as causal (in ENSG format)
        endpoint = "/variant_recoder/human/"+self.id+"?content-type=application/json"
        temp_locus_response = client.perform_rest_action(endpoint)#[0]## zero because this is a list, that only has one element because we're only requesting one variant at a time
        if temp_locus_response is None:
            print("\n\nSOMETHING WENT WRONG WITH VARIANT ANNOTATION\ndefaulting back to original get_gene_from_var function that will simply set it to all genes with overlap")
            return(self.get_gene_from_var(client, var_details))
        if len(temp_locus_response) == 0:
            print("\n\nSOMETHING WENT WRONG WITH VARIANT ANNOTATION\ndefaulting back to original get_gene_from_var function that will simply set it to all genes with overlap")
            return(self.get_gene_from_var(client, var_details))
        ## get all of the proteins and transcripts that this variant changes
        else:
            ## we got a successful reply
            print("we got a successful annotation:",len(temp_locus_response),"results")
            for key, value in temp_locus_response[0].items():
                print(key)
                print("\t",value)
            ensp_list = []
            enst_list = []
            for resp in temp_locus_response:## each snp
                print('\n\n',resp.keys())
                if "hgvsp" in resp:
                    for element in resp["hgvsp"]:
                        self.prot_muts.append(element)
                        if element[:4]=="ENSP":
                            temp_element = element.split(':')
                            temp_element = temp_element[0].split('.')
                            ## after the colon is the actual mutation annotation
                            ensp_list.append(temp_element[0])
                if "hgvsc" in resp:
                    for element in resp["hgvsc"]:
                        self.trans_muts.append(element)
                        if element[:4]=="ENST":
                            ## after the colon is the actual mutation annotation
                            temp_element = element.split(':')
                            temp_element = temp_element[0].split('.')
                            enst_list.append(temp_element[0])
            print(self.prot_muts)
            print(self.trans_muts)
            print(ensp_list)
            print(enst_list)
            if len(ensp_list)>0:
                temp_ensg = self.ensp_to_ensg(client, ensp_list)
                print("protein coding mutations in:")
                print('\t',temp_ensg)
            else:
                temp_ensg = self.enst_to_ensg(client, enst_list)
                print("transcript variant in:")
                print('\t',temp_ensg)
            #sys.exit()
            self.nearest_genes = temp_ensg
            if len(temp_ensg)==0:
                return(self.get_gene_from_var(client, var_details))
            else:
                return(temp_ensg)
            ## "/lookup/id/ENST00000496384?expand=1;content-type=application/json?feature=Parent"


    def get_vep_res(self, client, var_details):
        ## http://rest.ensembl.org/vep/human/id/rs1504215?content-type=application/json
        #print(var_details)
        self.var_details = var_details
        #### this is to replace get_gene_from_var in only the aspect of variant annotation if var_is_bad
        ## We will need to set nearest gene as well as var details, and return the list genes that are annotated as causal (in ENSG format)
        endpoint = "/vep/human/id/"+self.id+"?content-type=application/json"
        response = client.perform_rest_action(endpoint)
        if response is None:
            print("\n\ngot a weird response from VEP. Going to use the old overlap approach\n\n")
            return(self.get_gene_from_var(client, var_details))
        #############################
        ## if we got a valid response....
        all_bad_genes = []
        ## this endpoint can take multiple variants, but we're doing it one at a time for the sake of staying sane
        response = response[0]
        ## now look at the transcript_consequences
        for trans_result in response["transcript_consequences"]:
            for consequence in trans_result["consequence_terms"]:
                if self.check_bad(consequence):
                    print(self.id+":\t",trans_result["gene_id"],":",consequence)
                    all_bad_genes.append(trans_result["gene_id"])
        ensg_list = sorted(list(set(all_bad_genes)))
        self.nearest_genes = ensg_list
        print(self.nearest_genes)
        return(ensg_list)


    def get_gene_from_var(self, client, var_details):
        print(var_details)
        self.var_details = var_details
        genes = []
        self.all_locus_response = []
        ## one approach is to get the intervals and look that up 
        for locus in var_details["mappings"]:
            #print(locus)
            if locus["assembly_name"]=="GRCh38":
                temp_contig = locus["seq_region_name"]
                temp_start = locus["start"]
                if "end" in locus:
                    temp_end = locus["end"]
                else:
                    temp_end = deepcopy(temp_start)
                interval = [temp_start,temp_end]
                start = str(min(interval))
                end = str(max(interval))
                endpoint = "/overlap/region/human/"+temp_contig+":"+start+".."+end+"?feature=gene"
                print(endpoint)
                temp_locus_response = client.perform_rest_action(endpoint)#, params = "feature=gene")
                self.all_locus_response.append(temp_locus_response)
                print('\n',temp_locus_response)
                if temp_locus_response is not None:
                    for entry in temp_locus_response:
                        if "gene_id" in entry:
                            genes.append(entry["gene_id"])
                            self.nearest_genes.append(entry["gene_id"])
        genes = sorted(list(set(genes)))
        return(genes)


    def get_mutation_type(self,client,variant, tries = 3):
        endpoint = "/variation/human/"+variant
        var_details = client.perform_rest_action(endpoint = endpoint)
        if var_details == None and tries > 0:
            time.sleep(.25)
            self.get_mutation_type(client, variant, tries = tries-1)
            return
        if var_details == None:
            var_details = {}
        print(var_details)
        self.var_is_bad = self.is_bad_mutation(var_details)
        print(self.var_is_bad)
        if self.var_is_bad:
            print("getting vep results")
            self.genes = self.get_vep_res(client, var_details)
            #self.genes = self.get_var_recoder(client,var_details)
            #self.genes = self.get_gene_from_var(client,var_details)
        else:
            self.genes = []
        ## set the loci regardless
        self.set_all_loci(var_details)
        return


    # def get_regulatory_elements_for_var(self, contig, start, end, feat = ["regulatory","other_regulatory", "motif"]):## used to include "peak" as well, but it was too cluttered
    #     out_dict = {}
    #     for f in feat:
    #         endpoint = "/overlap/region/human/"+contig+":"+start+".."+end
    #         endpoint += "?feature="+f
    #         print('\n\n\n',endpoint)
    #         temp_locus_response = client.perform_rest_action(endpoint)#, params = "feature=gene")
    #         print(temp_locus_response,'\n\n\n')
    #     return(temp_locus_response)


    def get_regulatory_elements_for_var(self):
        client = EnsemblRestClient()
        self.regulatory_elements = []
        for locus in self.mapped_loci:## dictionary object with contig, start, end
            ### because Ensembl now accepts "chr" leader, we'll not include it for the sake of non-duplication
            if locus["contig"][:3] != "chr":
                temp_response = client.get_regulatory_elements_from_region(locus["contig"], str(locus["start"]), str(locus["end"]))
                print(temp_response)
                if temp_response is not None:
                    if temp_response["regulatory"] is not None:
                        self.regulatory += temp_response["regulatory"]
                    if temp_response["other_regulatory"] is not None:
                        self.other_regulatory += temp_response["other_regulatory"]
                    if temp_response["motif"] is not None:
                        self.motif += temp_response["motif"]
        return


    def get_direct_cause(self,client,variant):
        ## first figure out if it's in the bad mutation type
        self.get_mutation_type(client,variant)
        ## if it is, get the gene
        ## if it's not, get the tad genes
        if not self.var_is_bad:
            self.get_regulatory_elements_for_var()
        return()


    def get_eqtl_for_genes(self):
        client = EnsemblRestClient()
        for gene in self.genes:
            endpoint = "/eqtl/variant_name/homo_sapiens/"+self.id+"?stable_id="+gene+";statistic=p-value"
            temp_locus_response = client.perform_rest_action(endpoint)#, params = "feature=gene")
            self.eqtls[gene] = temp_locus_response
        return()

    #############################################3
    ## set the strings

    def get_reg_str(self,r):
        return(r["description"]+","+str(r["id"])+","+str(r["seq_region_name"])+":"+str(r["start"])+"-"+str(r["end"]))


    def get_other_reg_str(self,r):
        return(r["description"]+","+str(r["so_accession"])+","+str(r["seq_region_name"])+":"+str(r["start"])+"-"+str(r["end"]))

    def get_motif_str(self,r):
        return(r["transcription_factor_complex"]+","+str(r["stable_id"])+","+str(r["seq_region_name"])+":"+str(r["start"])+"-"+str(r["end"]))

    def get_str_for_reg_element(self,r):
        if r["feature_type"] == "regulatory":
            return(self.get_reg_str(r))
        if r["feature_type"] == "other_regulatory":
            return(self.get_other_reg_str(r))
        if r["feature_type"] == "motif":
            return(self.get_motif_str(r))
        else:
            for key in sorted(r.keys()):
                print(key)
            print(r)
            sys.exit()

    def get_regulatory_str(self):
        ## set the defaults
        reg_str = "NA"
        other_reg_str = "NA"
        motif_str = "NA"

        ## get the regulatory str
        if self.regulatory != []:
            temp_reg_list = []
            for reg_dict in self.regulatory:
                temp_reg_list.append(self.get_str_for_reg_element(reg_dict))
            ## sometimes tehre are duplicates
            temp_reg_list = sorted(list(set(temp_reg_list)))
            reg_str = '|'.join(temp_reg_list)

        ## get the other_regulatory
        if self.other_regulatory != []:
            temp_other_reg_list = []
            for other_reg_dict in self.other_regulatory:
                temp_other_reg_list.append(self.get_str_for_reg_element(other_reg_dict))
            temp_other_reg_list = sorted(list(set(temp_other_reg_list)))
            other_reg_str = '|'.join(temp_other_reg_list)

        ## get the motif strings
        if self.motif != []:
            temp_motif_list = []
            for reg_dict in self.motif:
                temp_motif_list.append(self.get_str_for_reg_element(reg_dict))
            temp_motif_list = sorted(list(set(temp_motif_list)))
            motif_str = '|'.join(temp_motif_list)        
        
        ## Join the results and return them
        return('\t'.join([reg_str, other_reg_str, motif_str]))

    def get_locus_str(self):
        locus_out_list = [] 
        for temp_locus in self.mapped_loci:
            if temp_locus["contig"][:3]=="chr":
                pass
            else:
                locus_out_list.append(temp_locus["contig"]+":"+str(temp_locus["start"])+"-"+str(temp_locus["end"]))
        locus_out_list = sorted(locus_out_list)
        return("|".join(locus_out_list))

    def get_tad_str(self):
        tad_list = []
        for tad in self.tad_annotations:
            tad_list.append(tad[0]+":"+str(int(tad[1]))+"-"+str(int(tad[2]))+","+tad[3])
        return("|".join(tad_list))

    def get_ensembl_link(self):
        return("https://useast.ensembl.org/Homo_sapiens/Location/View?db=core;source=dbSNP;v="+self.id+";vdb=variation")

    def __str__(self):
        temp_str_list = [self.id,self.get_locus_str(),','.join(deepcopy(self.nearest_genes)),','.join(deepcopy(self.genes)), self.get_tad_str(), self.mutation_type, self.get_ensembl_link(), self.get_regulatory_str()]
        temp_str_list = list(map(str,temp_str_list))
        return("\t".join(temp_str_list))
####################################################################################


def get_genes_from_locus(contig, start, end):
    client = EnsemblRestClient()
    genes = []
    if contig[:3] == "chr":
        contig = contig[3:]
    endpoint = "/overlap/region/human/"+contig+":"+str(int(float(start)))+".."+str(int(float(end)))+"?feature=gene"
    temp_locus_response = client.perform_rest_action(endpoint)#, params = "feature=gene")
    if temp_locus_response == None:
        return([])
    for entry in temp_locus_response:
        if "gene_id" in entry:
            genes.append(entry["gene_id"])
    genes = sorted(list(set(genes)))
    return(genes)


######################################################################################

def get_tad_variants(all_variants, tad_file):
    tad_dict = import_dict(tad_file)
    for variant in all_variants:
        if variant.genes == []:
            ## now we get the genes for the intergenic and intronic
            #print("finding the TAD mapping for",variant)
            for mapping in variant.mapped_loci:
                temp_contig = mapping["contig"]
                if temp_contig in tad_dict:
                    temp_genes, temp_tad_annotations, tad_list =  tad_dict[temp_contig].get_genes_from_bp_site(mapping["start"], mapping["end"])
                    variant.genes += temp_genes
                    if len(temp_tad_annotations)>0:
                        if temp_tad_annotations[0] != None:
                            variant.tad_annotations += temp_tad_annotations
                    if len(tad_list)>0:
                        variant.tads+=tad_list
        print(variant)
        # for mapping in variant.mapped_loci:
        #     print("\t",mapping)
        # print("\tnum tad elements:",len(variant.tad_annotations),variant.tad_annotations)
    return(all_variants)

def summarize_all_variants(all_variants, out_dir):
    header = ["variant","mapped_loci",'nearest_gene',"gene_mappings","TAD_mapping","most_pathologic_impact", "ensembl_viewer_link", "regulatory_annotation","other_regulatory_annotation","motif_annotation"]
    out_text = '\t'.join(header)+"\n"+'\n'.join(list(map(str,all_variants)))
    make_file(out_text,os.path.join(out_dir,"variant_summary.tsv"))
    return


def set_nearest_gene(all_variants,tad_file):
    tad_dict = import_dict(tad_file)
    for variant in all_variants:
        print(variant)
        ## now we get the genes for the intergenic and intronic
        #print("finding the TAD mapping for",variant)
        if variant.var_is_bad:
            print("already have annotations for\n\t",variant)
            pass
            ## if it's a bad mutation, give it the annotation 
            #variant.nearest_genes = deepcopy(variant.genes)
        else:
            for mapping in variant.mapped_loci:
                temp_contig = mapping["contig"]
                if temp_contig in tad_dict:
                    print(temp_contig, mapping["start"], mapping["end"])
                    nearest_gene = tad_dict[temp_contig].get_nearest_gene(mapping["start"], mapping["end"])
                    variant.nearest_genes += nearest_gene
                    variant.nearest_genes = list(set(variant.nearest_genes))
    return(all_variants)



def map_variants_to_genes(var_file, stringdb_dir, out_dir):
    ## check that the tad file is present
    tad_file = os.path.join(stringdb_dir,"tad_dict.pkl")
    if not os.path.isfile(tad_file):
        print("we couldn't find the tad file!\n",tad_file)
        sys.exit()
    ## do the analysis
    print('\nreading variants')
    variants = read_file(var_file,'lines')
    ## start the ensembl restful client
    client = EnsemblRestClient()
    all_variants = []
    for variant in variants:
        print("\n\n",variant)
        all_variants.append(variant_obj(client,variant))
    all_variants = get_tad_variants(all_variants = all_variants, 
                                    tad_file = tad_file)
    all_variants = set_nearest_gene(all_variants, tad_file)
    summarize_all_variants(deepcopy(all_variants), out_dir)

    return(all_variants)






#####################################################################

#####################################################################

def main(args):
    map_variants_to_genes(var_file = args.infile, 
                          stringdb_dir = args.stringdb_dir, 
                          out_dir = args.out)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    ## global arguments
    parser.add_argument(
        '-infile','-in','-i',
        dest='infile',
        help="the text file with an rsID list",
        type=str)

    parser.add_argument(
        "-stringdb_dir",'-sdb',
        help='The directory containing the StringDB action files',
        type = str,
        default = '/usr/local/lib/cell_signals/')

    parser.add_argument(
        '-out','-o',
        help="the output file containing the rsID mapping ",
        type=str)

    args = parser.parse_args()
    main(args)