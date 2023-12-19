# Extract header lengths from a BAM file in order to determine which headers
# to filter from the abundance (i.e. get the mask)
rule get_headers:
    input:
        os.path.join( "mapped", f"{IDS[-1]}.sort.bam")
    output:
        "abundances/headers.txt"
    params:
        walltime = "86400",
        nodes = "1",
        ppn = "1"
    resources:
        mem = "4GB"
    threads:
        1
    envmodules:
        'tools',
        config['moduleenvs']['samtools']
    group:
        '4_calculate_abundance.py'
    log:
        head = "log/abundance/headers.log",
        o = "log/abundance/get_headers.o",
        e = "log/abundance/get_headers.e",

    shell:
        "samtools view -H {input}"
        " | grep '^@SQ'"
        " | cut -f 2,3"
        " > {output} 2> {log.head} "
 
# Using the headers above, compute the mask and the refhash
rule abundance_mask:
    input:
        "abundances/headers.txt"
    output:
        "abundances/mask_refhash.npz"
    log:
        mask = "log/abundance/mask.log",
        o = "log/abundance/mask.o",
        e = "log/abundance/mask.e",
    params:
        path = CUSTOM_SCRIPTS + "abundances_mask.py",
        walltime = "86400",
        nodes = "1",
        ppn = "4"
    resources:
        mem = "1GB"
    threads:
        4
    conda:
        VAMBCONDAENV
    group:
        '4_calculate_abundance.py'

    shell:
        """
        python {params.path} --h {input} --msk {output} --minsize {MIN_CONTIG_SIZE} 2> {log.mask}
        """


# For every sample, compute the abundances given the mask and refhash above
rule bam_abundance:
    input:
        bampath="mapped/{sample}.sort.bam",
         mask_refhash="abundances/mask_refhash.npz",
    output:
        "abundances/{sample}.npz",
    params:
        path = CUSTOM_SCRIPTS +"write_abundances.py",
        walltime = "86400",
        nodes = "1",
        ppn = "4"
    resources:
        mem = "1GB"
    threads:
        4
    conda:
        VAMBCONDAENV
    log:
        bam = "log/abundance/bam_abundance_{sample}.log",
        o = "log/abundance/{sample}.bam_abundance.o",
        e = "log/abundance/{sample}.bam_abundance.e",
    group:
        '4_calculate_abundance.py'
    shell:
        """
        python {params.path} --msk {input.mask_refhash} --b {input.bampath} --min_id {MIN_IDENTITY} --out {output} 2> {log.bam}
        """
