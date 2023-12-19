# Filter contigs for 2000bp and rename them to conform with the multi-split workflow 
#delme
print('!'*100,contigs_list)
rule cat_contigs:
    input:
        contigs_list
    output:
        "contigs.flt.fna.gz"
    params:
        path=SCRIPTS + 'concatenate.py',
        walltime="864000",
        nodes="1",
        ppn="1",
    resources:
        mem="5GB"
    threads:
        1
    conda: 
        VAMBCONDAENV

    #log:
        #o = os.path.join(OUTDIR,"log/contigs/catcontigs.o"),
        #e = os.path.join(OUTDIR,"log/contigs/catcontigs.e")
    
    #envmodules:
    #    'tools',
    #    'vamb/4.1.3'     
    shell: 
        "python {params.path} {output} {input} -m {MIN_CONTIG_SIZE} --keepname"

