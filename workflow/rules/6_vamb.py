

rule run_avamb:
    input:
        contigs="contigs.flt.fna.gz",
        abundance="abundance.npz",
    output:
        outdir_avamb=directory('{vamb_runs}_vamb'),
        # file = '{vamb_runs}_vamb/vae_clusters.tsv',
    params:
        # walltime="86400",
        # nodes="1",
        # ppn=AVAMB_PPN,
        # cuda="--cuda" if CUDA else ""
    resources:
        mem=AVAMB_MEM
    threads:
        int(8)
    conda:
        VAMBCONDAENV
    benchmark: 'benchmark/{vamb_runs}_vamb'
    log:
        vamb_out="tmp/{vamb_runs}_vamb_finished.log",
        o=os.path.join('log','{vamb_runs}_vamb.out'),
        e=os.path.join('log','{vamb_runs}_vamb.err')
    shell:
        "module unload snakemake/7.28.2;"
        "rm -rf {output.outdir_avamb};"
        # "vamb bin default --outdir 1_vamb --fasta {input.contigs} "
        "vamb bin default --outdir {output.outdir_avamb} --fasta {input.contigs} "
        "--rpkm {input.abundance} -m {MIN_CONTIG_SIZE} " # -o er seperatoren
        #  {params.cuda}  {AVAMB_PARAMS}-p {threads}  --minfasta {MIN_BIN_SIZE} 
        # Removes dir before because vamb doesnt work in directory allready made, which snakemake does automaticall :
