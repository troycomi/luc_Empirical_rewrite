#!/bin/bash

#SBATCH --time 24:00:00       # wall time
#SBATCH --mem=50G

cd /tigress/AKEY/akey_vol1/home/luchenuw/WenqingEmpiricaltest_chr22/
module load samtools
tabix -h ./ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 1:1-250000000 | ./mergeVCF -a Altai_chr1_new.recode.vcf -l 217844600 -d 1 -n 2504 -o Altainew_1KGP3_chr1.txt
