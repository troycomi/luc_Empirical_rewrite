#!/bin/bash

set -euo pipefail

# variables used throughout
# slurm output directory
SLURM_OUT=slurm_out

# arguments for commands, export so the slurm file sees them
export INPUT_GZ_FILE=ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz
export TABIX_RANGE=1:1-250000000
export ARCHAIC_VCF=Altai_chr1_new.recode.vcf
export OUTPUT_FILE=Altainew_1KGP3_chr1_cpp.txt

[[ -d $SLURM_OUT ]] || mkdir -p $SLURM_OUT

JOB_ID_COMBINE=$(sbatch \
    --output=${SLURM_OUT}/%x_%A.out \
    --error=${SLURM_OUT}/%x_%A.out \
    --job-name=${USER}-vcf-comb \
    --parsable \
    mergeVCF_cpp.slurm)

echo $JOB_ID_COMBINE submitted merging VCFs
