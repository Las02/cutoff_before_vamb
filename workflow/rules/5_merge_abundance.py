# Merge the abundances to a single Abundance object and save it
print('IDS',IDS)
rule create_abundances:
    input:
        npzpaths=expand(os.path.join("abundances","{sample}.npz"), sample=IDS),
        mask_refhash=os.path.join("abundances","mask_refhash.npz")
    output:
        "abundance.npz"
    params:
        path = CUSTOM_SCRIPTS +  "create_abundances.py",
        abundance_dir = "abundances",
        walltime = "86400",
        nodes = "1",
        ppn = "4"
    resources:
        mem = "1GB"
    threads:
        4   
    conda:
        VAMBCONDAENV
    # envmodules:
        # 'gcc/12.2.0'
    log:
        create_abs = "log/abundance/create_abundances.log",
        o ="log/abundance/create_abundances.o",
        e = "log/abundance/create_abundances.e",

    shell:
        "python {params.path} --msk {input.mask_refhash} --ab {input.npzpaths} --min_id {MIN_IDENTITY} --out {output} 2> {log.create_abs} "
        # "rm -r {params.abundance_dir}"
