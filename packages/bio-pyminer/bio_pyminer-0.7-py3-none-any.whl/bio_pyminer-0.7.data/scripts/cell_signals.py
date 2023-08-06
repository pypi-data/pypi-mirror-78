#!/home/scott/anaconda3.7/bin/python3

##import dependency libraries
import sys,time,glob,os,pickle,fileinput,argparse, random
from time import sleep
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

all_calls = []
def cmd(in_message, com=True):
    global all_calls, time, sleep
    if type(in_message)==list:
       in_message = ' '.join(in_message)
    print(in_message)
    all_calls.append(in_message)
    #time.sleep(.25)
    sleep(0.25)
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

import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    "-gene_lists",
    help='a comma separated list of files that contain the enriched genes for each cell type.',
    type = str)

parser.add_argument(
    "-gene_table",'-bool_table','-in_table',
    help='A boolean True False table indicating whether a gene should be included in each cell types list.',
    type = str)

parser.add_argument(
    "-organism",'-species','-s',
    help='which organism are we using. (Use the -species_codes to print out a list of all supported species and their codes).',
    type = str,
    default = 'hsapiens')

parser.add_argument(
    "-species_codes",
    help='print out a list of all supported species and their codes.',
    action = 'store_true',
    default = False)

parser.add_argument(
    "-convert_to_human",
    help='if using a non-mouse/human species, it may be useful to convert to human, as these interactions will be more complete. Note that you will still have to provide an -organism argument so that we know what species to convert from.',
    action = 'store_true',
    default = False)

parser.add_argument(
    "-out_dir",'-out','-o',
    help='The output directory to use. If it does not exist, it will be created.',
    type = str)


parser.add_argument(
    "-stringdb_dir",'-sdb',
    help='The directory containing the StringDB action files',
    type = str,
    default = '/usr/local/lib/cell_signals/')

args = parser.parse_args()
##############################################################
##############################################################

organism_action_files = {
    'hsapiens':'9606.protein.actions.v11.0.txt',
    'mmusculus':'10090.protein.actions.v11.0.txt'
}


if args.organism not in organism_action_files:
    args.convert_to_human = True

## check that we have gprofiler installed
try:
    from gprofiler import GProfiler
except:
    sys.exit('please install gprofiler; try: pip3 install gprofiler-official')
else:
    from gprofiler import GProfiler

gp = GProfiler('PyMINEr_'+str(random.randint(0,int(1e6))), want_header = True)

##############################################################
##############################################################
if args.species_codes:
    print("""
Ensembl

    aaegypti — Aedes aegypti
    acarolinensis — Anolis carolinensis
    agambiae — Anopheles gambiae
    amelanoleuca — Ailuropoda melanoleuca
    amexicanus — Astyanax mexicanus
    aplatyrhynchos — Anas platyrhynchos
    btaurus — Bos taurus
    celegans — Caenorhabditis elegans
    cfamiliaris — Canis familiaris
    choffmanni — Choloepus hoffmanni
    cintestinalis — Ciona intestinalis
    cjacchus — Callithrix jacchus
    cporcellus — Cavia porcellus
    csabaeus — Chlorocebus sabaeus
    csavignyi — Ciona savignyi
    dmelanogaster — Drosophila melanogaster
    dnovemcinctus — Dasypus novemcinctus
    dordii — Dipodomys ordii
    drerio — Danio rerio
    ecaballus — Equus caballus
    eeuropaeus — Erinaceus europaeus
    etelfairi — Echinops telfairi
    falbicollis — Ficedula albicollis
    fcatus — Felis catus
    gaculeatus — Gasterosteus aculeatus
    ggallus — Gallus gallus
    ggorilla — Gorilla gorilla
    gmorhua — Gadus morhua
    hsapiens — Homo sapiens
    itridecemlineatus — Ictidomys tridecemlineatus
    lafricana — Loxodonta africana
    lchalumnae — Latimeria chalumnae
    loculatus — Lepisosteus oculatus
    mdomestica — Monodelphis domestica
    meugenii — Macropus eugenii
    mfuro — Mustela putorius furo
    mgallopavo — Meleagris gallopavo
    mlucifugus — Myotis lucifugus
    mmulatta — Macaca mulatta
    mmurinus — Microcebus murinus
    mmusculus — Mus musculus
    nleucogenys — Nomascus leucogenys
    oanatinus — Ornithorhynchus anatinus
    oaries — Ovis aries
    ocuniculus — Oryctolagus cuniculus
    ogarnettii — Otolemur garnettii
    olatipes — Oryzias latipes
    oniloticus — Oreochromis niloticus
    oprinceps — Ochotona princeps
    pabelii — Pongo abelii
    panubis — Papio anubis
    pcapensis — Procavia capensis
    pformosa — Poecilia formosa
    pmarinus — Petromyzon marinus
    psinensis — Pelodiscus sinensis
    ptroglodytes — Pan troglodytes
    pvampyrus — Pteropus vampyrus
    rnorvegicus — Rattus norvegicus
    saraneus — Sorex araneus
    scerevisiae — Saccharomyces cerevisiae
    sharrisii — Sarcophilus harrisii
    sscrofa — Sus scrofa
    tbelangeri — Tupaia belangeri
    tguttata — Taeniopygia guttata
    tnigroviridis — Tetraodon nigroviridis
    trubripes — Takifugu rubripes
    tsyrichta — Tarsius syrichta
    ttruncatus — Tursiops truncatus
    vpacos — Vicugna pacos
    xmaculatus — Xiphophorus maculatus
    xtropicalis — Xenopus tropicalis

Ensembl Genomes Fungi

    aclavatus — Aspergillus clavatus
    aflavus — Aspergillus flavus
    afumigatus — Aspergillus fumigatus
    afumigatusa1163 — Aspergillus fumigatusa1163
    agossypii — Ashbya gossypii
    anidulans — Aspergillus nidulans
    aniger — Aspergillus niger
    aoryzae — Aspergillus oryzae
    aterreus — Aspergillus terreus
    bcinerea — Botrytis cinerea
    bgraminis — Blumeria graminis f. sp. hordei DH14
    cgloeosporioides — Colletotrichum gloeosporioides
    cgraminicola — Colletotrichum graminicola
    chigginsianum — Colletotrichum higginsianum
    cneoformans — Cryptococcus neoformans
    corbiculare — Colletotrichum orbiculare
    dseptosporum — Dothistroma septosporum
    fculmorum — Fusarium culmorum UK99
    ffujikuroi — Fusarium fujikuroi
    fgraminearum — Fusarium graminearum
    foxysporum — Fusarium oxysporum
    fpseudograminearum — Fusarium pseudograminearum
    fsolani — Fusarium solani
    fverticillioides — Fusarium verticillioides
    ggraminis — Gaeumannomyces graminis
    kpastoris — Komagataella pastoris
    lmaculans — Leptosphaeria maculans
    mlaricipopulina — Melampsora larici-populina 98AG31
    moryzae — Magnaporthe oryzae
    mpoae — Magnaporthe poae
    mviolaceum — Microbotryum violaceum p1A1 Lamole
    ncrassa — Neurospora crassa
    nfischeri — Neosartorya fischeri
    pgraminis — Puccinia graminis
    pgraminisug99 — Puccinia graminis Ug99
    pnodorum — Phaeosphaeria nodorum
    pstriiformis — Puccinia striiformis f. sp. tritici PST-130 str. Race 130
    pteres — Pyrenophora teres f. teres 0-1
    ptriticina — Puccinia triticina
    ptriticirepentis — Pyrenophora tritici-repentis Pt-1C-BFP
    scerevisiae — Saccharomyces cerevisiae
    scryophilus — Schizosaccharomyces cryophilus
    sjaponicus — Schizosaccharomyces japonicus
    soctosporus — Schizosaccharomyces octosporus
    spombe — Schizosaccharomyces pombe
    sreilianum — Sporisorium reilianum SRZ2
    ssclerotiorum — Sclerotinia sclerotiorum
    tmelanosporum — Tuber melanosporum
    treesei — Trichoderma reesei
    tvirens — Trichoderma virens
    umaydis — Ustilago maydis
    vdahliae — Verticillium dahliae
    vdahliaejr2 — Verticillium dahliae JR2
    ylipolytica — Yarrowia lipolytica
    ztritici — Zymoseptoria tritici

Ensembl Genomes Metazoa

    aaegypti — Aedes aegypti
    acephalotes — Atta cephalotes
    adarlingi — Anopheles darlingi
    agambiae — Anopheles gambiae
    aglabripennis — Anoplophora glabripennis
    amellifera — Apis mellifera
    apisum — Acyrthosiphon pisum
    aqueenslandica — Amphimedon queenslandica
    avaga — Adineta vaga
    bantarctica — Belgica antarctica
    bimpatiens — Bombus impatiens
    bmalayi — Brugia malayi
    bmori — Bombyx mori
    cbrenneri — Caenorhabditis brenneri
    cbriggsae — Caenorhabditis briggsae
    celegans — Caenorhabditis elegans
    cgigas — Crassostrea gigas
    cjaponica — Caenorhabditis japonica
    cquinquefasciatus — Culex quinquefasciatus
    cremanei — Caenorhabditis remanei
    cteleta — Capitella teleta
    dananassae — Drosophila ananassae
    derecta — Drosophila erecta
    dgrimshawi — Drosophila grimshawi
    dmelanogaster — Drosophila melanogaster
    dmojavensis — Drosophila mojavensis
    dpersimilis — Drosophila persimilis
    dplexippus — Danaus plexippus
    dponderosae — Dendroctonus ponderosae
    dpseudoobscura — Drosophila pseudoobscura
    dpulex — Daphnia pulex
    dsechellia — Drosophila sechellia
    dsimulans — Drosophila simulans
    dvirilis — Drosophila virilis
    dwillistoni — Drosophila willistoni
    dyakuba — Drosophila yakuba
    hmelpomene — Heliconius melpomene
    hrobusta — Helobdella robusta
    iscapularis — Ixodes scapularis
    lanatina — Lingula anatina
    lcuprina — Lucilia cuprina
    lgigantea — Lottia gigantea
    lloa — Loa loa
    lsalmonis — Lepeophtheirus salmonis
    mcinxia — Melitaea cinxia
    mdestructor — Mayetiola destructor
    mleidyi — Mnemiopsis leidyi
    mscalaris — Megaselia scalaris
    nvectensis — Nematostella vectensis
    nvitripennis — Nasonia vitripennis
    obimaculoides — Octopus bimaculoides
    ovolvulus — Onchocerca volvulus
    phumanus — Pediculus humanus
    ppacificus — Pristionchus pacificus
    rprolixus — Rhodnius prolixus
    sinvicta — Solenopsis invicta
    smansoni — Schistosoma mansoni
    smaritima — Strigamia maritima
    smimosarum — Stegodyphus mimosarum
    spurpuratus — Strongylocentrotus purpuratus
    sratti — Strongyloides ratti
    sscabiei — Sarcoptes scabiei
    tadhaerens — Trichoplax adhaerens
    tcastaneum — Tribolium castaneum
    tkitauei — Thelohanellus kitauei
    tspiralis — Trichinella spiralis
    turticae — Tetranychus urticae
    znevadensis — Zootermopsis nevadensis

Ensembl Genomes Plants

    alyrata — Arabidopsis lyrata
    atauschii — Aegilops tauschii
    athaliana — Arabidopsis thaliana
    atrichopoda — Amborella trichopoda
    bdistachyon — Brachypodium distachyon
    bnapus — Brassica napus
    boleracea — Brassica oleracea
    brapa — Brassica rapa
    bvulgaris — Beta vulgaris subsp. vulgaris
    ccrispus — Chondrus crispus
    cmerolae — Cyanidioschyzon merolae
    creinhardtii — Chlamydomonas reinhardtii
    gmax — Glycine max
    gsulphuraria — Galdieria sulphuraria
    hvulgare — Hordeum vulgare
    lperrieri — Leersia perrieri
    macuminata — Musa acuminata
    mtruncatula — Medicago truncatula
    obarthii — Oryza barthii
    obrachyantha — Oryza brachyantha
    oglaberrima — Oryza glaberrima
    oglumaepatula — Oryza glumaepatula
    oindica — Oryza sativa indica
    olongistaminata — Oryza longistaminata
    olucimarinus — Ostreococcus lucimarinus
    omeridionalis — Oryza meridionalis
    onivara — Oryza nivara
    opunctata — Oryza punctata
    orufipogon — Oryza rufipogon
    osativa — Oryza sativa Japonica
    ppatens — Physcomitrella patens
    ppersica — Prunus persica
    ptrichocarpa — Populus trichocarpa
    sbicolor — Sorghum bicolor
    sitalica — Setaria italica
    slycopersicum — Solanum lycopersicum
    smoellendorffii — Selaginella moellendorffii
    stuberosum — Solanum tuberosum
    taestivum — Triticum aestivum
    tcacao — Theobroma cacao
    tpratense — Trifolium pratense
    turartu — Triticum urartu
    vvinifera — Vitis vinifera
    zmays — Zea mays
    """)
    sys.exit()

##############################################################
##############################################################



def get_name_from_path(in_path):
    temp_name = in_path.split('/')
    temp_name = temp_name[-1]
    temp_name = temp_name[:-4]
    return(temp_name)

def get_gene_lists_from_files(in_files):
    all_gene_list_files = in_files.split(',')
    cell_type_ids = []
    for gene_list in all_gene_list_files:
        cell_type_ids.append(get_name_from_path(gene_list))

    ## get the gene lists for each cell type
    gene_lists = []
    gene_ids = []
    for cell in all_gene_list_files:
        temp_genes = read_file(cell)
        gene_lists.append(temp_genes)
        gene_ids += temp_genes
    gene_ids = list(set(gene_ids))
    return(cell_type_ids, gene_ids, gene_lists)

def get_gene_lists_from_bool_table(in_file):
    """
    here, we take in the boolean table with columns corresponding
    to the cell type names, with the body of the table consisting of
    True or False. This will be directly translated into a boolean numpy array
    so syntax is important in this array.
    """
    bool_table = read_table(in_file)
    cell_type_ids = bool_table[0][1:]
    bool_table = np.array(bool_table)
    gene_ids = list(set(bool_table[1:,0].tolist()))
    gene_lists = []
    ## set up the empty lists
    for i in range(1, np.shape(bool_table)[1]):
        gene_lists.append([])
    ## populate the 
    for i in range(1,np.shape(bool_table)[0]):
        ## go through each row in the table (barring the )
        for j in range(1, np.shape(bool_table)[1]):
            if bool_table[i,j]=='True':
                gene_lists[j-1].append(bool_table[i,0])
    
    ## make them all upper case
    for i in range(0,len(gene_ids)):
        gene_ids[i]=str(gene_ids[i]).upper()

    for i in range(0,len(gene_lists)):
        for j in range(0,len(gene_lists[i])):
            gene_lists[i][j]=str(gene_lists[i][j]).upper()

    return(cell_type_ids, gene_ids, gene_lists)


def convert_to_ensp(in_genes, gene_lists):
    global args, gp
    temp_lookup={}
    gene_symbol_dict = {}
    for g in in_genes:
        temp_lookup[g] = []
        


    results = gp.gconvert(in_genes, 
        organism = args.organism, target='ENSP')


    for r in range(1,len(results)):
        ## the original ID
        g = results[r][1]
        ## the current orthologue list
        try:
            temp_lookup[g]
        except:
            pass
            # print('weird mapping event:')
            # print(results[r])
        else:
            if results[r][4] != None:
                gene_symbol_dict[results[r][3]]=results[r][4]
            if results[r][3] != None:
                temp_list = temp_lookup[g]
                temp_list += [results[r][3]]
                temp_lookup[g]=temp_list

    gene_lists = convert_list_of_lists_by_dict(gene_lists,temp_lookup)
    new_gene_ids = []
    for k in list(temp_lookup.keys()):
        new_gene_ids += temp_lookup[k]
    new_gene_ids= list(set(new_gene_ids))

    for gene in new_gene_ids:
        if gene not in gene_symbol_dict:
            gene_symbol_dict[gene]="None"


    return(new_gene_ids, gene_lists, gene_symbol_dict)


def get_orthologue_dicts(in_genes,source_organism, target_organism, orthologues = True, ensp_convert = False):
    global args, gp
    temp_org_to_human = {}

    ## each gene will get a list for its orthologues
    for g in in_genes:
        temp_org_to_human[g] = []

    results = gp.gorth(in_genes, 
        source_organism = source_organism, 
        target_organism=target_organism,
        numeric_ns=True)


    for r in range(1,len(results)):

        ## the original ID
        g = results[r][1]
        ## the current orthologue list
        try:
            temp_org_to_human[g]
        except:
            pass
            # print('weird mapping event:')
            # print(results[r])
        else:
            if results[r][4] != None:
                temp_list = temp_org_to_human[g]
                temp_list += [results[r][4]]
                temp_org_to_human[g]=temp_list

    human_to_temp_org = {}
    return(temp_org_to_human,human_to_temp_org)

def convert_list_of_lists_by_dict(gene_lists,temp_org_to_human):
    ## set up the new gene list
    new_gene_lists = []
    for i in range(len(gene_lists)):
        new_gene_lists.append([])
    ## convert the original gene lists to the IDs
    for i in range(len(gene_lists)):
        for j in range(len(gene_lists[i])):
            new_gene_lists[i]+=temp_org_to_human[gene_lists[i][j]]
    return(new_gene_lists)


def update_converted_genes(temp_org_to_human, gene_ids, gene_lists):
    new_gene_ids = []
    for k in list(temp_org_to_human.keys()):
        new_gene_ids += temp_org_to_human[k]
    new_gene_ids= list(set(new_gene_ids))
    if None in new_gene_ids:
        new_gene_ids.pop(None)

    new_gene_lists=convert_list_of_lists_by_dict(gene_lists,temp_org_to_human)

    return(new_gene_ids, new_gene_lists)

def get_receptors_and_secreted(in_genes):
    global gp

    secreted_go = ['GO:0005615','GO:0005576','GO:0044421']
    receptor_go = ["GO:0009897","GO:0031232","GO:0031233","GO:0071575"," GO:0098591","GO:0031362","GO:0098567","GO:0009986","GO:0005886","GO:0042923","GO:0016021"]#,'GO:0005904']

    results = gp.gconvert(gene_ids, 
        organism = args.organism, target='GO')


    # print(results[0])
    # print(results[1])
    # print(results[2])
    # print(results[3])

    all_go_terms = []
    receptor_list = []
    secreted_list = []
    for i in range(1,len(results)):
        if results[i][3] not in all_go_terms:
            all_go_terms.append(results[i][3])
        if results[i][3] in receptor_go:
            receptor_list.append(results[i][1])
        if results[i][3] in secreted_go:
            secreted_list.append(results[i][1])
    receptor_list = list(set(receptor_list))
    secreted_list = list(set(secreted_list))
    return(receptor_list, secreted_list)

def filter_enriched_lists_for_subcellular_localization(receptor_list, secreted_list, gene_lists):
    receptor_gene_lists = []
    secreted_gene_lists = []
    for g in range(len(gene_lists)):
        receptor_gene_lists.append([])
        secreted_gene_lists.append([])

    for i in range(0,len(gene_lists)):
        for j in range(0,len(gene_lists[i])):
            if gene_lists[i][j] in receptor_list:
                receptor_gene_lists[i].append(gene_lists[i][j])
            if gene_lists[i][j] in secreted_list:
                secreted_gene_lists[i].append(gene_lists[i][j])
    return(receptor_gene_lists,secreted_gene_lists)

def clean_names(in_vect):
    name1 = in_vect[0].split('.')
    name2 = in_vect[1].split('.')
    name1 = name1[-1]
    name2 = name2[-1]
    in_vect[0] = name1
    in_vect[1] = name2
    return(in_vect)

def subset_action_table(receptor_or_secreted_list,db_file):
    print('this may take a minute....')
    ## construct a dictionary for the receptor or secreted list
    receptor_or_secreted_dict = {j:i for i, j in enumerate(receptor_or_secreted_list)}
    print(len(list(receptor_or_secreted_dict.keys())), 'receptor_or_secreted_dict')
    all_ids = []
    line_count = 0
    out_table = []
    activation_dict = {}
    inhibition_dict = {}
    other_dict = {}
    first = True
    for line in fileinput.input(db_file):
        line_count+=1
        if line_count % 1e5 == 0:
            print('\t',line_count,'\t',len(out_table))
        temp_line = strip_split(line)
        if first:
            first = False
            #out_table.append(temp_line) 
        else:
            temp_line = clean_names(temp_line)


            ## check if the two genes are in the receptor or secreted list
            # holy shit this way of checking if something is in a dictionary is so much
            # faster than checking if they're in a list... good to know...
            # I'm talking like, orders of magnitude faster...
            # I've wasted so much time waiting on this step. Now it takes seconds o...
            cont1 = True
            try:
                receptor_or_secreted_dict[temp_line[0]]
            except:
                cont1=False
            if cont1:
                all_ids.append(temp_line[0])

            cont2 = True
            try:
                receptor_or_secreted_dict[temp_line[1]]
            except:
                cont2=False
            if cont2:
                all_ids.append(temp_line[1])

            if cont1 and cont2:
            #if temp_line[0] in receptor_or_secreted_list and temp_line[1] in receptor_or_secreted_list:
                temp_id = temp_line[0]+":"+temp_line[1]
                if temp_line[2] == 'binding': 
                    out_table.append(temp_line)
                elif temp_line[2] == 'activation':
                    activation_dict[temp_id] = True
                elif temp_line[2] == 'inhibition':
                    inhibition_dict[temp_id] = True
                else:
                    if temp_id not in other_dict:
                        other_dict[temp_id]=temp_line[2]
                    else:
                        if other_dict[temp_id] != 'None':
                            temp_thingy = other_dict[temp_id]
                            temp_thingy = ','+temp_line[2]
                        if temp_thingy[0]==',':
                            temp_thingy=temp_thingy[1:]
                        other_dict[temp_id] = temp_thingy

    fileinput.close()
    all_ids = list(set(all_ids))
    return(out_table, activation_dict, inhibition_dict, other_dict,all_ids)

def annotate_interactions_for_activation_and_inhibition(action_table, activation_dict, inhibition_dict, other_dict):
    print('annotating the interactions for directionality and type of action....')
    action_table[0] = action_table[0][:11]+['activation/inhibition','other_action']+action_table[0][11:]
    # print(action_table[0])
    for i in range(1,len(action_table)):
    #     for l in enumerate(action_table[i]):
    #         print(l)
        temp_id = str(action_table[i][9])+":"+str(action_table[i][10])
        activation_term = 'None'
        other_action_term = 'None'
        if temp_id in activation_dict:
            activation_term = 'activation'
        if temp_id in inhibition_dict:
            activation_term = 'inhibition'
        if temp_id in other_dict:
            other_action_term = other_dict[temp_id]
        action_table[i] = action_table[i][:11]+[activation_term,other_action_term]+action_table[i][11:]
    return(action_table)



def gene_lists_to_symbol_lists(gene_lists, gene_symbol_dict):
    gene_symbol_lists = []
    for c in range(len(gene_lists)):
        gene_symbol_lists.append([])
        for gene in gene_lists[c]:
            temp_symbol = gene_symbol_dict[gene]
            if temp_symbol not in gene_symbol_lists[c]:
                gene_symbol_lists[c].append(temp_symbol)
    return(gene_symbol_lists)

def gene_symbol_lists_to_dicts(gene_symbol_lists):
    gene_symbol_list_dicts = []
    for i in range(0,len(gene_symbol_lists)):
        gene_symbol_list_dicts.append({j:w for w, j in enumerate(gene_symbol_lists[i])})
    return(gene_symbol_list_dicts)
##############################################################
##############################################################




##############################################################
##############################################################
print('\n')
if args.gene_table!=None:
    cell_type_ids, gene_ids, gene_lists = get_gene_lists_from_bool_table(args.gene_table)


if args.gene_lists!=None:
    cell_type_ids, gene_ids, gene_lists = get_gene_lists_from_files(args.gene_lists)

print(len(gene_ids))

#################
## print out some basic summaries on the input data
print(len(cell_type_ids),'cell types found')
print(cell_type_ids[:min([4,len(cell_type_ids)])],'...\n')

print(len(gene_ids),'genes found')
print(gene_ids[:min([4,len(gene_ids)])],'...\n')

## make a hash table to look up the index from a cell type name
cell_type_idx_dict = {key:value for value, key in enumerate(cell_type_ids)}
# for c in cell_type_ids:
#     print(c, cell_type_idx_dict[c])
#################

#################
## if we need to convert over to human ids, this is the first thing we'll need to do
if args.convert_to_human:
    print('converting to human')
    temp_org_to_human, human_to_temp_org = get_orthologue_dicts(gene_ids, args.organism, 'hsapiens')
    #get_orthologue_dicts(gene_ids[:10], args.organism, 'hsapiens')

    ## update the gene_ids and gene_lists to reflect the conversion to human
    gene_ids, gene_lists = update_converted_genes(temp_org_to_human, gene_ids, gene_lists)
    args.organism = 'hsapiens'
    print('\n\nfinished converting IDs\n\n')

    print('gene IDs now look like:')
    print(gene_ids[:4],'...\n')
    print('enrichment lists now look like:')
    print('\t',cell_type_ids[0])
    print('\t\t',gene_lists[0][:3])
    print('\t',cell_type_ids[1],'...')
    print('\t\t',gene_lists[1][:3],'...\n\n')



#################
print('Converting IDs to ENSP format.')
print('This is needed for cross-referencing the StringDB database later\n')


# for i in range(0,len(gene_lists)):
#     l=gene_lists[i]
#     if "ENSG00000139874" in l:
#         print('found "ENSG00000139874" in',i)

gene_ids, gene_lists, gene_symbol_dict = convert_to_ensp(gene_ids, gene_lists)
gene_symbol_lists = gene_lists_to_symbol_lists(gene_lists, gene_symbol_dict)
gene_symbol_list_dicts = gene_symbol_lists_to_dicts(gene_symbol_lists)


# for i in range(0,len(gene_lists)):
#     l=gene_lists[i]
#     if "ENSP00000267377" in l:
#         print('found "ENSP00000267377" in',i)



print('finished converting to ENSPs\n')
print('gene IDs now look like:')
print(gene_ids[:4],'...\n')
print('enrichment lists now look like:')
print('\t',cell_type_ids[0])
print('\t\t',gene_lists[0][:3])
#print('\t',cell_type_ids[1],'...')
#print('\t\t',gene_lists[1][:3],'...\n\n')


symbols = list(gene_symbol_dict.keys())
print(len(symbols))
for i in range(0,5):
    print(symbols[i], gene_symbol_dict[symbols[i]])
#sys.exit()

#####################################################################################
#####################################################################################
###################   go term filter for subcellular localization   #################
#####################################################################################
#####################################################################################

print('getting subcellular localizations\n')
receptor_list, secreted_list = get_receptors_and_secreted(gene_ids)


print('found',len(receptor_list),'plasma membrane')
print('found',len(secreted_list),'extracellular')

# print("in receptor list?:","ENSP00000267377" in receptor_list)
# print("in secreted list?:","ENSP00000267377" in secreted_list)

## if there are any extracellular genes in the plasma membrane gene lists, pop them out
## we only want loose ligands in the secreted list 
for r in receptor_list:
    # print(r)
    # print(secreted_list[:10])
    if r in secreted_list:
        print('removing',r,gene_symbol_dict[r],"from secreted, because it's also annotated as being in the plasma membrane")
        secreted_list.pop(secreted_list.index(r))

# for r in secreted_list:
#     # print(r)
#     # print(secreted_list[:10])
#     if r in receptor_list:
#         print('removing',r,gene_symbol_dict[r],"from receptor, because it's also annotated as being in the secreted")
#         receptor_list.pop(receptor_list.index(r))


print('found',len(receptor_list),'plasma membrane')
print('found',len(secreted_list),'extracellular')
receptor_or_secreted_list = list(set(receptor_list + secreted_list))

print(len(receptor_or_secreted_list), 'receptors and secreted genes found')

# if "ENSP00000267377" in receptor_or_secreted_list:
#     print("found ENSP00000267377 in receptor_or_secreted_list")
# else:
#     print("Couldn't find ENSP00000267377 in receptor or secreted!")
#     sys.exit()

## set up a dictionary with the info needed about each gene for writing to file later
gene_detail_dict = {}
for g in gene_ids:
    if g in receptor_list:
        gene_detail_dict[g]=[g,gene_symbol_dict[g],'plasma_membrane']
    if g in secreted_list:
        gene_detail_dict[g]=[g,gene_symbol_dict[g],'extracellular']

## subset the enriched gene lists for each subcellular localization
receptor_gene_lists, secreted_gene_lists = filter_enriched_lists_for_subcellular_localization(receptor_list, secreted_list, gene_lists)

## print out some summaries
print('plasma membrane:')
for i in range(0,len(cell_type_ids)):
    temp_list = receptor_gene_lists[i]
    temp_list_len = len(receptor_gene_lists[i])
    print('\t',cell_type_ids[i],temp_list_len)
    if temp_list_len!=0:
        print('\t\t',receptor_gene_lists[i][0:min([temp_list_len,3])],'...')

print('\nextracellular:')
for i in range(0,len(cell_type_ids)):
    temp_list = secreted_gene_lists[i]
    temp_list_len = len(secreted_gene_lists[i])
    print('\t',cell_type_ids[i],temp_list_len)
    if temp_list_len!=0:
        print('\t\t',secreted_gene_lists[i][0:min([temp_list_len,3])],'...')


# for i in range(0,len(secreted_gene_lists)):
#     l=secreted_gene_lists[i]
#     if "ENSP00000267377" in l:
#         print('found "ENSP00000267377" in secreted_gene_lists',i)


# for i in range(0,len(receptor_gene_lists)):
#     l=receptor_gene_lists[i]
#     if "ENSP00000267377" in l:
#         print('found "ENSP00000267377" in receptor_gene_lists',i)

#####################################################################################
#####################################################################################
###################   cross reference all of the receptor and secreted   ############
###################       lists with the StringDB action database        ############
#####################################################################################
#####################################################################################

if args.organism in organism_action_files:
    db_file = args.stringdb_dir+organism_action_files[args.organism]

#########
## first we'll load into memory only the interactions that stand
## a chance of being pertinent to our dataset
print('\n\nloading in the interaction table')
action_table, activation_dict, inhibition_dict, other_dict, all_included_bg = subset_action_table(receptor_or_secreted_list,db_file)
print(len(action_table)-1,'interactions among the genes remaining')

# for i in range(0,len(action_table)):
#     if "ENSP00000267377" in action_table[i]:
#         print("found ENSP00000267377 in action_table:",action_table[i])


#########
## convert that to an action dictionary so that we can look up the details quickly later
# first make a unique key for the interaction lists
action_dict = {}
symbol_interaction_dict = {}
for line in action_table:
    temp_id = line[0]+":"+line[1]
    #print(temp_id)
#    if line[0] in gene_symbol_dict and line[1] in gene_symbol_dict:
    temp_symbol_id = gene_symbol_dict[line[0]]+":"+gene_symbol_dict[line[1]]
# else:
#     temp_symbol_id = None
    # print(temp_id,temp_symbol_id)
    if temp_symbol_id not in symbol_interaction_dict:
        symbol_interaction_dict[temp_symbol_id]=True
    if temp_id not in action_dict:
        action_dict[temp_id] = [line]
    else:
        temp_list = action_dict[temp_id]
        temp_list.append(line)
        action_dict[temp_id] = temp_list



def get_empty_interaction_lists():
    global gene_lists
    interaction_lists = []
    for i in range(0,len(gene_lists)):
        interaction_lists.append([])
        for j in range(0,len(gene_lists)):
            interaction_lists[i].append([])
    return(interaction_lists)

interaction_lists = get_empty_interaction_lists()



interaction_title_line = [["autocrine_paracrine",
"cell_type_1","gene_1","gene_1_symbol","gene_1_location",
"cell_type_2","gene_2","gene_2_symbol","gene_2_location",
"gene1","gene2","action","inhibition","directional","is_direction","score"]]
out_summary_table = [["cell_type_1","cell_type_2","count"]]
out_table = interaction_title_line[:]


## make the cell type enrichment dicts
gene_list_dict = []
for i in range(0,len(gene_lists)):
    temp_gene_dict = {j:i for i, j in enumerate(gene_lists[i])}
    gene_list_dict.append(temp_gene_dict)


def get_cell_types_gene_enriched_in(gene):
    global gene_list_dict, gene_lists, cell_type_ids
    gene_cell_types = []
    for i in range(0,len(cell_type_ids)):
        cur_cell_type = True
        try:
            gene_list_dict[i][gene]
        except:
            cur_cell_type = False
        if cur_cell_type:
            gene_cell_types.append(cell_type_ids[i])
    # ## just for trouble shooting
    # if gene =="ENSP00000357461" or gene == "ENSP00000383938":
    #     print('\n\n',gene_cell_types,'\n\n')
    return(gene_cell_types)



## go through the action_dict & find what cell types are enriched for each of the genes
cell_type_interaction_count = np.zeros((len(cell_type_ids),len(cell_type_ids)))
all_interactions = list(action_dict.keys())

# for interaction in all_interactions:
#     if "ENSP00000267377" in interaction:
#         print("found ENSP00000267377 in all_interactions:",interaction)

print('cateloguing which cell types have the interactions')
for interaction_idx in range(0,len(all_interactions)):
    if interaction_idx %500 == 0:
        print('\t',interaction_idx,'\t',interaction_idx/len(all_interactions))
    interaction = all_interactions[interaction_idx]
    genes = interaction.split(':')
    gene1 = genes[0]
    gene2 = genes[1]
    gene1_symbol = gene_symbol_dict[gene1]
    gene2_symbol = gene_symbol_dict[gene2]
    ## go through all of the cell types and find which cell types are enriched for the genes
    gene1_cell_types = get_cell_types_gene_enriched_in(gene1)
    gene2_cell_types = get_cell_types_gene_enriched_in(gene2)



    ## write the output for each of the combinations of cell types
    for cell_type_1 in gene1_cell_types:
        for cell_type_2 in gene2_cell_types:
            if cell_type_1 == cell_type_2:
                out_line =['autocrine']
            else:
                out_line = ['paracrine']
            cell_type_1_idx = cell_type_idx_dict[cell_type_1]
            cell_type_2_idx = cell_type_idx_dict[cell_type_2]
            interaction_lists[cell_type_1_idx][cell_type_2_idx].append(gene1_symbol)
            #if gene2_symbol not in interaction_lists[i][j]:
            interaction_lists[cell_type_1_idx][cell_type_2_idx].append(gene2_symbol)
            out_line += [cell_type_1]+gene_detail_dict[gene1]
            out_line += [cell_type_2]+gene_detail_dict[gene2]
            for line in action_dict[gene1+":"+gene2]:
                out_table.append(out_line+line)

            cell_type_interaction_count[cell_type_1_idx,cell_type_2_idx]+=1

for i in range(0,len(cell_type_ids)):
    cell_type_1 = cell_type_ids[i]
    for j in range(i,len(cell_type_ids)):
        cell_type_2 = cell_type_ids[j]

        temp_count = cell_type_interaction_count[i,j]

        out_summary_table.append([cell_type_1,cell_type_2,temp_count])
## will need to catalogue the number remaining
#out_summary_table.append([cell_type_1,cell_type_2,temp_count])



if False:
    ## go through all the receptor receptor pairs
    for i in range(0,len(gene_lists)):
        gene_list_1 = gene_lists[i]
        cell_type_1 = cell_type_ids[i]
        print(cell_type_1)
        for j in range(i,len(gene_lists)):
            cell_type_2 = cell_type_ids[j]
            gene_list_2 = gene_lists[j]
            print('\t',cell_type_2)
            temp_count = 0
            for gene1 in gene_list_1:
                gene1_symbol = gene_symbol_dict[gene1]
                for gene2 in gene_list_2:
                    gene2_symbol = gene_symbol_dict[gene2]
                    out_line = None

                    g1_g2=True
                    g2_g1=True
                    try:
                        action_dict[gene1+":"+gene2][0]
                    except:
                        g1_g2=False
                    try:
                        action_dict[gene2+":"+gene1][0]
                    except:
                        g2_g1=False


                    if g1_g2:#ene1+":"+gene2 in action_dict:
                        #if action_dict[gene1+":"+gene2]!=[]:
                            
                        #if gene1_symbol not in interaction_lists[i][j]:
                        interaction_lists[i][j].append(gene1_symbol)
                        #if gene2_symbol not in interaction_lists[i][j]:
                        interaction_lists[i][j].append(gene2_symbol)
                        if cell_type_1 == cell_type_2:
                            out_line = ['autocrine']
                        else:
                            out_line = ['paracrine']
                        out_line += [cell_type_1]+gene_detail_dict[gene1]
                        out_line += [cell_type_2]+gene_detail_dict[gene2]
                        temp_count+=1
                        for line in action_dict[gene1+":"+gene2]:
                            out_table.append(out_line+line)
                                                
                    if g2_g1:#ene2+":"+gene1 in action_dict:
                        #if action_dict[gene2+":"+gene1]!=[]:
                        #if gene1_symbol not in interaction_lists[i][j]:
                        interaction_lists[i][j].append(gene1_symbol)
                        #if gene2_symbol not in interaction_lists[i][j]:
                        interaction_lists[i][j].append(gene2_symbol)
                        if cell_type_1 == cell_type_2:
                            out_line = ['autocrine']
                        else:
                            out_line = ['paracrine']
                        out_line += [cell_type_2]+gene_detail_dict[gene2]
                        out_line += [cell_type_1]+gene_detail_dict[gene1]
                        temp_count+=1
                        for line in action_dict[gene2+":"+gene1]:
                            out_table.append(out_line+line)
                            #print(out_table[-1])
                            
            print('\t\t',temp_count)
            out_summary_table.append([cell_type_1,cell_type_2,temp_count])

## annotate the action table for the mechanism of interaction
out_table = annotate_interactions_for_activation_and_inhibition(out_table, activation_dict, inhibition_dict, other_dict)

## remove the duplicates in the interaction_lists:
for i in range(0,len(interaction_lists)):
    for j in range(0,len(interaction_lists[i])):
        interaction_lists[i][j]=list(set(interaction_lists[i][j]))


out_summary_table_copy = out_summary_table[:]
out_table_copy = out_table[:]



if not os.path.isdir(args.out_dir):
    cmd('mkdir '+args.out_dir)

write_table(out_table_copy,args.out_dir+'/all_cell_type_specific_interactions.txt')
write_table(out_summary_table_copy,args.out_dir+'/all_cell_cell_interaction_summary.txt')


##########################################################
##########################################################
## get gprofiler results from each of the interaction lists
def key_in_dict(key, in_dict):
    in_it = True
    try:
        in_dict[key]
    except:
        in_it = False
    return(in_it)


def get_gprofiler_on_interaction_lists(interaction_lists, bg = None):
    global args, gp, time
    print('getting the pathway analysis for each cell type interactions...')

    output_gprofiler = [['cell_type_1','cell_type_2']]
    for i in range(0,len(interaction_lists)):
        ## wait for a random amount of time so that we don't overload the server
        random_time_lag = np.random.randint(low=25,high=100)/100
        sleep(random_time_lag)
        for j in range(i,len(interaction_lists)):
            print('\t',cell_type_ids[i],cell_type_ids[j],":",len(interaction_lists[i][j]),'genes')
            if bg == None:
                temp_gprofile_results = gp.gprofile(interaction_lists[i][j], organism = args.organism)
            else:
                temp_gprofile_results = gp.gprofile(interaction_lists[i][j], custom_bg = bg, organism = args.organism)
            if i==0 and j == 0 and temp_gprofile_results!=[]:
                output_gprofiler[0] += temp_gprofile_results[0]
            for q in range(1,len(temp_gprofile_results)):
                output_gprofiler.append([cell_type_ids[i],cell_type_ids[j]]+temp_gprofile_results[q])
    return(output_gprofiler)

def see_if_symbols_interact(symbol1,symbol2):
    global symbol_interaction_dict
    temp_key = str(symbol1)+":"+str(symbol2)
    if key_in_dict(temp_key,symbol_interaction_dict):
        return(True)
    temp_key = str(symbol2)+":"+str(symbol1)
    if key_in_dict(temp_key,symbol_interaction_dict):
        return(True)
    return(False)


def filter_and_annoatate_genes(in_gene_list, cell_type_1, cell_type_2, test_time=False):
    global symbol_interaction_dict, gene_symbol_lists, cell_type_idx_dict, gene_symbol_list_dicts
    if cell_type_1 != cell_type_2:
        paracrine = True
    else:
        paracrine = False
    in_gene_list = in_gene_list.split(',')
    if len(in_gene_list)==1:
        return("None")
    cell_type_1_idx = cell_type_idx_dict[cell_type_1]
    cell_type_2_idx = cell_type_idx_dict[cell_type_2]
    #cell_type_enriched_ids_1=gene_symbol_lists[cell_type_1_idx]
    #cell_type_enriched_ids_2=gene_symbol_lists[cell_type_2_idx]
    cell_type_enriched_dict_1=gene_symbol_list_dicts[cell_type_1_idx]
    cell_type_enriched_dict_2=gene_symbol_list_dicts[cell_type_2_idx]
    
    ## first make all fully crossed interaction_pairs
    if test_time:
        print('making pairs')
        start = time()
    fully_crossed_possible_pairs = []
    for i in range(0,len(in_gene_list)):
        for j in range(i,len(in_gene_list)):
            #if in_gene_list[j]+":"+in_gene_list[i] not in fully_crossed_possible_pairs:
            fully_crossed_possible_pairs.append(in_gene_list[i]+":"+in_gene_list[j])
            #fully_crossed_possible_pairs.append(in_gene_list[j]+":"+in_gene_list[i])
    fully_crossed_possible_pairs = list(set(fully_crossed_possible_pairs))
    filtered_pairs = []
    if test_time:
        print('\t',time()-start)
        print('\tlooking at fully_crossed_possible_pairs in interaction dict')
        start = time()
    for i in range(0,len(fully_crossed_possible_pairs)):
        cont = True
        try:
            symbol_interaction_dict[fully_crossed_possible_pairs[i]]
        except:
            cont = False
        if cont:#fully_crossed_possible_pairs[i] in symbol_interaction_dict:
            filtered_pairs.append(fully_crossed_possible_pairs[i])
    #print(filtered_pairs)
    if test_time:
        print('\t\t',time()-start)
        print('\tannotating source')
        start = time()
    final_output_list = []
    for i in range(0,len(filtered_pairs)):
        ## format of this will be cell_type_1:gene1;cell_type2:gene2,... for each interaction contained within the genes in this pathway
        temp_interaction = filtered_pairs[i]
        temp_interaction = temp_interaction.split(':')
        gene_source_1 = ''
        gene_source_2 = ''
        ## figure out which cell type is producing each within the pair 
        if key_in_dict(temp_interaction[0], cell_type_enriched_dict_1):
            #print(temp_interaction[0],"found in",cell_type_1,cell_type_enriched_ids_1)
            gene_source_1+=cell_type_1
        if key_in_dict(temp_interaction[0], cell_type_enriched_dict_2):
            #temp_interaction[0] in cell_type_enriched_ids_2:
            #print(temp_interaction[0],"found in",cell_type_2,cell_type_enriched_ids_2)
            if gene_source_1!='':
                gene_source_1+='&'
            gene_source_1+=cell_type_2
        #print(gene_source_1)
        if key_in_dict(temp_interaction[1], cell_type_enriched_dict_1):
        #if temp_interaction[1] in cell_type_enriched_ids_1:
            #print(temp_interaction[1],"found in",cell_type_1,cell_type_enriched_ids_1)
            gene_source_2+=cell_type_1
        if key_in_dict(temp_interaction[1], cell_type_enriched_dict_2):
        #if temp_interaction[1] in cell_type_enriched_ids_2:
            #print(temp_interaction[1],"found in",cell_type_2,cell_type_enriched_ids_2)
            if gene_source_2!='':
                gene_source_2+='&'
            gene_source_2+=cell_type_2
        ##print(gene_source_2)
        ## double check that there was a gene source found
        if gene_source_1 == '':
            print("couldn't find gene_source_1")
        if gene_source_2 == '':
            print("couldn't find gene_source_2")
        ## format the outputs for this line
        if paracrine:
            temp_full_interaction_description = gene_source_1+":"+temp_interaction[0]+";"+gene_source_2+":"+temp_interaction[1]
            #print(temp_full_interaction_description)
        else:
            temp_full_interaction_description = cell_type_1+":"+temp_interaction[0]+";"+cell_type_2+":"+temp_interaction[1]
        if paracrine and gene_source_1!=gene_source_2:
            final_output_list.append(temp_full_interaction_description)
        elif not paracrine:
            final_output_list.append(temp_full_interaction_description)
    if test_time:
        print('\t\t',time()-start)
    ## and return the final line
    if final_output_list == []:
        return('None')
    return(','.join(final_output_list))



def annotate_gprofiler_output(output_gprofiler):
    global cell_type_idx_dict
    print('\nannotating the gprofiler results\nThis might take a minute...')
    new_output_gprofiler = [output_gprofiler[0]+[output_gprofiler[0][-1]]]
    new_output_gprofiler[0][-2] = 'filtered_annotated_gene_list'
    first = True
    count=0
    total_length = len(output_gprofiler)
    for line in output_gprofiler:
        count+=1
        if count%500 == 0:
            print('\tline:',count,'\tpercent:',100*count/total_length,'%')
        if first:
            first = False
            pass
        else:
            ## put the cell types and annotations into the line, then append it to the new output
            ## but only add it for either all autocrine interactions, or for paracrine interactions
            ## only put it into the output if there are 
            temp_line = line[:]
            temp_line.append(temp_line[-1])
            temp_line[-2] = filter_and_annoatate_genes(temp_line[-1],temp_line[0],temp_line[1])
            if temp_line[-2] != "None":
                new_output_gprofiler.append(temp_line)
    return(new_output_gprofiler)


output_gprofiler = get_gprofiler_on_interaction_lists(interaction_lists, bg = all_included_bg)
output_gprofiler = annotate_gprofiler_output(output_gprofiler)
write_table(output_gprofiler,args.out_dir+'/all_cell_type_specific_interactions_gprofiler.txt')
##########################################################

def get_subset(out_file,term_a,term_b):
    global interaction_title_line
    temp_file_str = out_file
    cmd('rm '+temp_file_str)
    extra_cell_file = open(temp_file_str,'a')
    temp_title_line='\t'.join(interaction_title_line[0])
    extra_cell_file.write(temp_title_line+'\n')
    #extracellular_extracellular_interactions = interaction_title_line[:]
    for i in range(1,len(out_table)):
        if (out_table[i][4]  == term_a and out_table[i][8] == term_b) or (out_table[i][4]  == term_b and out_table[i][8] == term_a):
            temp_line = out_table[i][:]
            temp_line = '\t'.join(temp_line)
            if i!=len(out_table)-1:
                temp_line+='\n'
            extra_cell_file.write(temp_line)
    extra_cell_file.close()



##########################################################
## extracellular:extracellular interactions

#extracellular_extracellular_lists = get_empty_interaction_lists()
#receptor_gene_lists, secreted_gene_lists

# ## go through the out_table and filter it for extracellular:extracellular interactions
# temp_file_str = args.out_dir+'/extracellular_extracellular_cell_type_specific_interactions.txt'
# cmd('rm '+temp_file_str)
# extra_cell_file = open(temp_file_str,'a')
# extra_cell_file.write('\t'.join(interaction_title_line[:])+'\n')
# #extracellular_extracellular_interactions = interaction_title_line[:]
# for i in range(1,len(out_table)):
#     if out_table[i][4]  == 'extracellular' and out_table[i][8] == 'extracellular':
#         temp_line = out_table[i][:]
#         temp_line = '\t'.join(temp_line)
#         if i!=len(out_table)-1:
#             temp_line+='\n'
#         extra_cell_file.write(temp_line)
#         #extracellular_extracellular_interactions.append(out_table[i])
# # extracellular_extracellular_interactions_copy = extracellular_extracellular_interactions[:]
# # write_table(extracellular_extracellular_interactions_copy,args.out_dir+'/extracellular_extracellular_cell_type_specific_interactions.txt')

print('\n\nwriting output files\n')

print('extracellular','extracellular')
temp_file_str = args.out_dir+'/extracellular_extracellular_cell_type_specific_interactions.txt'
get_subset(temp_file_str,'extracellular','extracellular')
print('plasma_membrane','plasma_membrane')
temp_file_str = args.out_dir+'/plasma_membrane_plasma_membrane_cell_type_specific_interactions.txt'
get_subset(temp_file_str,'plasma_membrane','plasma_membrane')

##########################################################
## extracellular:plasma membrane interactions
print('extracellular','plasma_membrane')
def get_unique_ids(i):
    global out_table
    gene_1 = out_table[i][2]
    cell_type_1 = out_table[i][1]
    gene_2 = out_table[i][6]
    cell_type_1 = out_table[i][5]
    inuqe_id_1 = cell_type_1+"|"+gene_1+":"+cell_type_2+"|"+gene_2
    inuqe_id_2 = cell_type_2+"|"+gene_2+":"+cell_type_1+"|"+gene_1
    return(inuqe_id_1,inuqe_id_2)

prev_interact_dict = {}
extracellular_pm_interactions = interaction_title_line[:]
for i in range(1,len(out_table)):
    inuqe_id_1,inuqe_id_2 = get_unique_ids(i)
    if not key_in_dict(inuqe_id_1,prev_interact_dict) and not (key_in_dict(inuqe_id_2,prev_interact_dict)):# temp_line not in extracellular_pm_interactions:
        if out_table[i][4]  == 'extracellular' and out_table[i][8] == 'plasma_membrane':
            extracellular_pm_interactions.append(out_table[i])
            prev_interact_dict[inuqe_id_1]=True
            prev_interact_dict[inuqe_id_2]=True
        elif out_table[i][4]  == 'plasma_membrane' and out_table[i][8] == 'extracellular':
            ## make it a directional file so that things only flow from extracellular to plasma membrane
            temp_line = out_table[i][:]
            temp_cell_description = temp_line[1:5]
            temp_line[1:5] = temp_line[5:9]
            temp_line[5:9] = temp_cell_description
            #if not key_in_dict(inuqe_id_1,prev_interact_dict) and not (key_in_dict(inuqe_id_2,prev_interact_dict)):# temp_line not in extracellular_pm_interactions:
            extracellular_pm_interactions.append(temp_line)
            prev_interact_dict[inuqe_id_1]=True
            prev_interact_dict[inuqe_id_2]=True


extracellular_pm_interactions_copy = extracellular_pm_interactions[:]
write_table(extracellular_pm_interactions_copy,args.out_dir+'/extracellular_plasma_membrane_cell_type_specific_interactions.txt')





# ##########################################################
# ## plasma membrane:plasma membrane interactions

# pm_pm_interactions = interaction_title_line[:]
# for i in range(1,len(out_table)):
#     if out_table[i][4]  == 'plasma_membrane' and out_table[i][8] == 'plasma_membrane':
#         pm_pm_interactions.append(out_table[i])


# pm_pm_interactions_copy = pm_pm_interactions[:]
# write_table(pm_pm_interactions_copy,args.out_dir+'/plasma_membrane_plasma_membrane_cell_type_specific_interactions.txt')
