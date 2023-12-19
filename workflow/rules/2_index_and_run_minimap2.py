
# Index resulting contig-file with minimap2
rule index:
    input:
        contigs = "contigs.flt.fna.gz"
    output:
        mmi = "contigs.flt.mmi"
    params:
        walltime="864000",
        nodes="1",
        ppn="1"
    resources:
        mem="90GB"
    threads:
        1
    group:
        '2_index_and_run_minimap2'
    log:
        out_ind ="log/contigs/index.log",
        o = "log/contigs/index.o",
        e = "log/contigs/index.e",
 
    envmodules:
        'tools',
        config['moduleenvs']['minimap2']
    #conda: 
    #    "envs/minimap2.yaml"
    shell:
        "minimap2 -I {INDEX_SIZE} -d {output} {input} 2> {log.out_ind}"

# This rule creates a SAM header from a FASTA file.
# We need it because minimap2 for truly unknowable reasons will write
# SAM headers INTERSPERSED in the output SAM file, making it unparseable.
# To work around this mind-boggling bug, we remove all header lines from
# minimap2's SAM output by grepping, then re-add the header created in this
# rule.
rule dict:
    input:
        contigs = "contigs.flt.fna.gz",
    output:
        dict = "contigs.flt.dict"
    params:
        walltime="864000",
        nodes="1",
        ppn="1"
    resources:
        mem="10GB"
    threads:
        1
    log:
        out_dict= "log/contigs/dict.log",
        o = "log/contigs/dict.o",
        e = "log/contigs/dict.e"
    envmodules:
        'tools',
        config['moduleenvs']['samtools']
    group:
        '2_index_and_run_minimap2'

    shell:
        "samtools dict {input} | cut -f1-3 > {output} 2> {log.out_dict}"

print(sample2path)
# Generate bam files 
rule minimap:
    input:
        fq = lambda wildcards: sample2path[wildcards.sample],
        mmi ="contigs.flt.mmi",
        dict = "contigs.flt.dict"
    output:
        bam = temp("mapped/{sample}.bam")
    params:
        walltime="864000",
        nodes="1",
        ppn=MM_PPN,
        long_or_short_read = 'map-pb -L' if LONG_READS else 'sr',
        
        
    resources:
        mem=MM_MEM
    threads:
        int(MM_PPN)
    log:
        out_minimap = "log/map/{sample}.minimap.log",
        o = "log/map/{sample}.minimap.o",
        e = "log/map/{sample}.minimap.e",
    envmodules:
        'tools',
        config['moduleenvs']['minimap2'],
        config['moduleenvs']['samtools']
    group:
        '2_index_and_run_minimap2'

    shell:
        # See comment over rule "dict" to understand what happens here
        "minimap2 -t {threads} -ax {params.long_or_short_read} {input.mmi} {input.fq} -N 5"
        " | grep -v '^@'"
        " | cat {input.dict} - "
        " | samtools view -F 3584 -b - " # supplementary, duplicate read, fail QC check
        " > {output.bam} 2> {log.out_minimap}"
