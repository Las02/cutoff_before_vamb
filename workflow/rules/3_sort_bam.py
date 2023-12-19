# Sort bam files
rule sort:
    input:
        "mapped/{sample}.bam",
    output:
        "mapped/{sample}.sort.bam",
    params:
        walltime="864000",
        nodes="1",
        ppn="2",
        prefix="mapped/tmp.{sample}"
    resources:
        mem="15GB"
    threads:
        2
    log:
        out_sort = "log/map/{sample}.sort.log",
        o = "log/map/{sample}.sort.o",
        e = "log/map/{sample}.sort.e",
    envmodules:
       'tools',
        config['moduleenvs']['samtools']
        #conda:
    #    '/mnt/c/Users/Admin/Desktop/benchmark_workflow/workflow/envs/samtools.yaml'
    shell:
        "samtools sort {input} -T {params.prefix} --threads 1 -m 3G -o {output} 2> {log.out_sort}"
