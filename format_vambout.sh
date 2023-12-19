grep -v clustername $1 | \
gawk '{
      split($2, a, "_");
      print $1 "\t" a[1] a[2];  
     }' | \
sed 's/NODE//' > tmp;
python add_sample_vambout.py $2 tmp > $3
