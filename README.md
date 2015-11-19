# Convert ClinVar flat file to VCF

The MacArthur lab has made a great effort make ClinVar data more available to the bioinformatics community. This script converts their flat file to a VCF file. 
 
##Usage

~~~bash

python macarthur-clinvar-to-vcf.py --clinvar path/to/clinvar.tsv -V output.vcf

~~~

If you want to compress the output on the fly, you can:

~~~bash

python macarthur-clinvar-to-vcf.py --clinvar path/to/clinvar.tsv -V /dev/stdout |bgzip > output.vcf.gz
tabix -p vcf output.vcf.gz
~~~