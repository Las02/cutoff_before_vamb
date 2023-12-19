import sys
# SAMPLE FROM

sample = sys.argv[1]
refpath = f"/home/people/lasdan/contig_cutoff/vamb_ptracker_done/sample_data/{sample}/samples2data.tsv"
# path =  "/home/people/lasdan/contig_cutoff/vamb_ptracker_done/Airways/para_1000/1_vamb/"
cluster_path = sys.argv[2] # path + "formatted_vae_cluster_split.tsv"

enum2sample = {}

# Make dict of enum -> sample
with open(refpath, 'r') as f:
    i = 0
    for line in f:
        line = line.strip()
        if len(line.split()) == 1:
            continue
        i +=1
        sample = line.strip().split()[0]
        enum2sample['S'+str(i)] = sample.strip()


with open(cluster_path, 'r') as f:
    for line in f:

        line_split = line.split()
        bin = line_split[0]
        ref = line_split[1]
        enum = ref.split('C')[0]
        id = ref.split('C')[1]
        bin_sample = bin.split('C')[0]
        bin_id = bin.split('C')[1]
        #print(enum2sample[enum],enum)
        print('S' + enum2sample[bin_sample] + "C"+bin_id + '\tS' + enum2sample[enum] + "C" + id)


# Apply dict to vamb output
# cluster_path 
# with open(cluster_path, 'r') as f:
#     for line in f:
#
#         line_split = line.split()
#         ref = line_split[1]
#         enum = ref.split('C')[0]
#         id = ref.split('C')[1]
#         #print(enum2sample[enum],enum)
#         bin = line_split[0]
        # bin1 = bin.split('C')[0]
        # bin2 = bin.split('C')[1]

        # print(bin + '\tS' + enum2sample[enum] + "C" + id)
        # print(bin1 + "C" + bin2 + '\tS' + enum2sample[enum] + "C" + id)
        # print("S" + enum2sample[bin1] + "C" + bin2 + '\tS' + enum2sample[enum] + "C" + id)
