configfile:  '../../config/config.yaml'  #'/home/people/lasdan/lasdan/benchmark_workflow/config/config.yaml'
SCRIPTS = '/home/people/lasdan/lasdan/vamb_versions/vamb/src/'
CUSTOM_SCRIPTS =  '../../workflow/scripts/' #'/home/people/lasdan/lasdan/benchmark_workflow/workflow/scripts/'    

VAMBCONDAENV = 'vamb' 
SAMTOOLSENV = "samtools/1.17"
MINIMAP2ENV = "minimap2/2.6"

import re
import os
import sys
import numpy as np
SNAKEDIR = os.path.dirname(workflow.snakefile)



sys.path.append(os.path.join(SNAKEDIR, 'scripts'))


def get_config(name, default, regex):
    res = config.get(name, default).strip()
    m = re.match(regex, res) 
    if m is None:
        raise ValueError(
            f"Config option \"{name}\" is \"{res}\", but must conform to regex \"{regex}\"")
    return res

# set configurationsi
CONFIG_PATH = config['config_path']
SAMPLE = config['sample']
CONTIGS = get_config("contigs", CONFIG_PATH + SAMPLE + "/contigs.txt", r".*") # each line is a contigs path from a given sample
TIMES_RUN_VAMB = config['times_run_vamb']

#
# print('CONTIGS:',CONTIGS)
# print('SAMPLE:', SAMPLE)
#
#
# print()
SAMPLE_DATA =  CONFIG_PATH + SAMPLE + "/samples2data.tsv"
# TODO remove 
config['contigs'] = CONTIGS
# print('SAMPLE_DATA:', SAMPLE_DATA)

INDEX_SIZE = config['index_size'] 
MIN_BIN_SIZE = config['min_bin_size']
MIN_CONTIG_SIZE = config['min_contig_size'] 
MIN_IDENTITY = config['min_identity'] 
MM_MEM = config['minimap']['minimap_mem']
MM_PPN = config['minimap']['minimap_ppn']
AVAMB_MEM = config['vamb']['avamb_mem']
AVAMB_PPN = config['vamb']['avamb_ppn']

# AVAMB_PARAMS = get_config("avamb_params"," -o C --minfasta 200000  ", r".*")
# AVAMB_PRELOAD = get_config("avamb_preload", "", r".*")

MIN_COMP = config['min_comp']#get_config("min_comp", "0.9", r".*")
MAX_CONT = config['max_cont']#get_config("max_cont", "0.05", r".*")

# config['outdir']= get_config("outdir", "outdir_avamb", r".*")

#try:
#    os.makedirs(os.path.join(config['outdir'],"log"), exist_ok=True)
#except FileExistsError:
#    pass


# parse if GPUs is needed #
AVAMB_PPN = AVAMB_PPN 
AVAMB_GPUS = config['vamb']['avamb_gpus']
CUDA = AVAMB_GPUS > 0

## read in sample information ##

print('-'*20, 'SAMPLE:',SAMPLE,'| MIN_CONTIG_SIZE:',MIN_CONTIG_SIZE, '-'*20)
# read in sample2path
IDS = []
sample2path = {}
fh_in = open(SAMPLE_DATA, 'r')
LONG_READS = None
one_samples = False
two_samples = False
head_path = False
path = ''
for line in fh_in:
    line = line.rstrip()
    fields = line.split()

    ### Basic Reading of file
    # Checking for mistakes in the files
    if two_samples and len(fields) == 2:
        raise Exception('both 1 and 2 samples')
    if one_samples and len(fields) == 3:
        raise Exception('both 1 and 2 samples')
#    if head_path and len(fields) == 1:
#        raise Exception('1 sample line after header')  

    # Adding the data for entries with 1
    if len(fields) == 3:
        sample2path[fields[0]] = [path + fields[1], path + fields[2]]
        two_samples = True
        # print('Assuming paired reads, since given 2 fastq sequences per sample:')
        LONG_READS = False
        # print('LONG_READS=',LONG_READS)

        IDS.append(fields[0])

    
    elif len(fields) == 2:
        sample2path[fields[0]] = [path + fields[1]]
        one_samples = True
        # print('Assuming long-reads, since given 1 fastq sequence per sample')
        LONG_READS = True
        # print('LONG_READS=',LONG_READS)

        IDS.append(fields[0])



    elif len(fields) == 1:
        path = fields[0]
        head_path = True

# for line in fh_in:
#     line = line.rstrip()
#     fields = line.split()
#     IDS.append(fields[0])
#     if len(fields) == 3:
#         sample2path[fields[0]] = [fields[1], fields[2]]
#         print('Assuming paired reads, since given 2 fastq sequences per sample:')
#         LONG_READS = False
#         print('LONG_READS=',LONG_READS)
#     elif len(fields) == 2:
#         sample2path[fields[0]] = [fields[1]]
#         print('Assuming long-reads, since given 1 fastq sequence per sample')
#         LONG_READS = True
#         print('LONG_READS=',LONG_READS)
# for line in fh_in:
#     line = line.rstrip()
#     fields = line.split('\t')
#     IDS.append(fields[0])
#     sample2path[fields[0]] = [fields[1], fields[2]]



#
# read in list of per-sample assemblies
CONTIGS = CONFIG_PATH + SAMPLE + "/contigs.txt"
contigs_list = []
fh_in = open(CONTIGS, 'r')
for line in fh_in:
    line = line.rstrip()
    contigs_list.append(line)

# target rule
#rule all       :
#    input:
#        contigs=os.path.join(config['outdir'],"contigs.flt.fna.gz"),
#        abundance=os.path.join(config['outdir'],"abundance.npz") 
rule all:
    input:
        # outdir_avamb=expand('{vamb_runs}_vamb/vae_clusters.tsv', vamb_runs = list(range(1, TIMES_RUN_VAMB + 1)))
        outdir_avamb=directory(expand('{vamb_runs}_vamb', vamb_runs = list(range(1, TIMES_RUN_VAMB + 1))))

# print('SAMPLE_DATA:',SAMPLE_DATA)
# print('IDS:', IDS)
# print('sample2path:',sample2path)
print('contigs_list:', contigs_list)
# print('-'*40)
#
#rulepath = '/home/people/lasdan/lasdan/benchmark_workflow/workflow/rules/'

include:'workflow/rules/1_filter_rename_cat.py'
include:'workflow/rules/2_index_and_run_minimap2.py'
include:'workflow/rules/3_sort_bam.py'
include:'workflow/rules/4_calculate_abundance.py'
include:'workflow/rules/5_merge_abundance.py'
include:'workflow/rules/6_vamb.py'


