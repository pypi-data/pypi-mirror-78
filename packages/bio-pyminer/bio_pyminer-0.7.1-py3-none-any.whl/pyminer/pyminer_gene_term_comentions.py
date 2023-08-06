#!/usr/local/env python3

import argparse
#from requests_html import HTMLSession
#import urllib
import requests
import time
from bs4 import BeautifulSoup as bs
from copy import deepcopy
try:
    from pyminer.common_functions import *
except:
    from common_functions import *
##############################################################

def get_web_html(url, tries = 3, timeout = 0.5, use_requests = True):
    if requests:
        resp = requests.get(url)
        if str(resp) == "<Response [200]>":
            return(resp.text)
        else:
            print("couldn't connect!")
            time.sleep(.25)
            return(get_web_html(url,tries = tries -1, timeout = timeout, use_requests = use_requests))
    print("\t",url)
    if tries == 0:
        return("")
    #global session
    session = HTMLSession()
    html_text = ""
    # Use the object above to connect to needed webpage
    try:
        resp = session.get(url, timeout = timeout)
    except:
        print("\t\tcouldn't connect to the url")
        try:
            session.close()
        except:
            print("\t\tCouldn't close session!")
        return(get_web_html(url, tries = tries-1, timeout = timeout+0.25))
    else:
        try:
            resp.html.render()
        except:
            print("\t\tcouldn't render it!; we'll return what we got anyway")
            html_text = str(resp.html.html)
        else:
            html_text = str(resp.html.html)
    try:
        resp.close()
        session.close()
    except:
        print("\t\tCouldn't close session!")
    return(html_text)


def extract_counts(line):
    line = line.split(' ')
    line = line[-1]
    return(int(line))


def count_from_html(html):
    if html == "":
        return("")
    soup = bs(html,"lxml")
    p_list = soup.findAll('h3')
    counts = 1
    for p in p_list:
        #out_text += " . "+p.text
        #print(p.text)
        if "Items: " in p.text:
            counts = extract_counts(p.text)
            return(counts)
    return(counts)


def get_search_count(url):
    temp_html = get_web_html(url)
    count = count_from_html(temp_html)
    return(count)

def prep_url(term1,term2='', no_search_quote = False, base = 'https://www.ncbi.nlm.nih.gov/pubmed/?term='):
    term1 = term1.split(' ')
    term1 = '"'+"+".join(term1)+'"'
    search_term = term1
    if term2 != '':
        term2 = term2.split(' ')
        if not no_search_quote:
            term2 = '"'+"+".join(term2)+'"'
        else:
            term2 = "+".join(term2)
        search_term = term1+"+"+term2
    return(base+search_term+"+NOT+(GWAS)")


def count_from_html_new_pubmed(html):
    if html == "":
        return("")
    soup = bs(html,"lxml")
    p_list = soup.findAll('div', {'class':"results-amount"})
    counts = 1
    for p in p_list:
        values = p.findAll('span', {'class':"value"})
        if len(values) == 0:
            return(0)
        for value in values:
            value_text = value.get_text()
            value_text = value_text.replace(',','')
            #print(value_text)
            if "No results" in value_text:
                counts = 0
                return(counts)
            try:
                int(value_text)
            except:
                print("Something went wrong with:", value_text)
            else:
                counts = int(value_text)
                return(counts)
    return(counts)


def prep_new_pubmed_url(term1, term2='', no_search_quote = False):
    return(prep_url(term1, term2=term2, no_search_quote = no_search_quote, base = "https://pubmed.ncbi.nlm.nih.gov/?term="))


def get_new_pubmed_search_count(url):
    temp_html = get_web_html(url)
    count = count_from_html_new_pubmed(temp_html)
    return(count)


def get_single_search_count(term1, no_search_quote = False, new_pubmed = False):
    if term1 == "None":
        return(0)
    if not new_pubmed:
        term1_url = prep_url(term1, no_search_quote = no_search_quote)
        term1_count = get_search_count(term1_url)
    else:
        term1_url = prep_new_pubmed_url(term1, no_search_quote = no_search_quote)
        term1_count = get_new_pubmed_search_count(term1_url)
    print(term1,'\t',term1_count)
    return(term1_count)
    

def get_pubmed_comentions(term1, term2, no_search_quote = False, new_pubmed = False):
    if term1=="None" or term2 == "None":
        return(0)
    if not new_pubmed:
        combined_url = prep_url(term1, term2= term2, no_search_quote = no_search_quote)
        combined_count = get_search_count(combined_url)
    else:
        combined_url = prep_new_pubmed_url(term1, term2= term2, no_search_quote = no_search_quote)
        combined_count = get_new_pubmed_search_count(combined_url)
    print(term1, '\t', term2,'\t',combined_count)
    return(combined_count)


def get_all_result_comparisons(genes,search_term, no_search_quote = False, new_pubmed = False):
    gene_counts = {gene:get_single_search_count(gene, new_pubmed = new_pubmed) for gene in genes}## we will always put the gene in quotes
    search_term_counts = {term:get_single_search_count(term, no_search_quote = no_search_quote, new_pubmed = new_pubmed) for term in search_term}## for some special cases, we won't put the search term in quotes
    combined_counts = {}
    for gene in genes:
        for term in search_term:
            ## if one of them doesn't show up at all on it's own - they can't be found together, so we'll just short circuit it and return zero for this
            if search_term_counts[term] > 0 and gene_counts[gene] > 0:
                combined_counts[gene+term] = get_pubmed_comentions(gene, term, no_search_quote = no_search_quote, new_pubmed = new_pubmed)
            else:
                combined_counts[gene+term] = 0
    return(gene_counts,search_term_counts,combined_counts)


def get_percent_overlap(num,den):
    if min([num,den])==0:
        return(0.)
    else:
        return(num/den)


def get_comention_summary(genes, search_term, out_dir = None, no_search_quote = False, new_pubmed = False):
    gene_counts,search_term_counts,combined_counts = get_all_result_comparisons(genes, search_term, no_search_quote = no_search_quote, new_pubmed = new_pubmed)
    output = [["gene_symbol","search_term","gene_total","search_term_total","combined_total","percent_overlap_of_gene","percent_overlap_of_term","max_percent_overlap","search_url"]]
    for gene in genes:
        for term in search_term:
            gene_overlap_per = get_percent_overlap(combined_counts[gene+term],gene_counts[gene])
            term_overlap_per = get_percent_overlap(combined_counts[gene+term],search_term_counts[term])
            if new_pubmed:
                temp_url = prep_new_pubmed_url(gene, term, no_search_quote = no_search_quote)
            else:
                temp_url = prep_url(gene, term, no_search_quote = no_search_quote)
            output.append([gene,
                           term,
                           gene_counts[gene],
                           search_term_counts[term],
                           combined_counts[gene+term],
                           gene_overlap_per,
                           term_overlap_per,
                           max([gene_overlap_per,term_overlap_per]),
                           temp_url])
    if out_dir is not None:
        out_path = os.path.join(out_dir,"gene_symbol_comention_summary.tsv")
        write_table(deepcopy(output),out_path)
    return(output)


def get_comentions_from_files(gene_file, search_term_file, out_dir, no_search_quote = False):
    search_term = read_file(search_term_file, 'lines')
    genes = read_file(gene_file, 'lines')
    get_comention_summary(genes, search_term, out_dir, new_pubmed = True, no_search_quote = no_search_quote)


##############################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-genes", '-g',
        help="The file containing gene symbols that we'll look up",
        type = str)

    parser.add_argument("-search_terms","-search","-terms","-st", 
        help="the file with search terms that we'll look for co-mentions with the genes for",
        type = str)

    parser.add_argument("-no_search_quote",
        help="whether or not to include quotes for the search terms",
        action = 'store_true')

    parser.add_argument("-out_dir", '-out', '-o',
        help="the directory that we'll write the results to",
        type = str)

    args = parser.parse_args()

    get_comentions_from_files(args.genes, args.search_terms, args.out_dir, no_search_quote = args.no_search_quote)