#!/bin/bash

#SBATCH --time 1:00:00
#SBATCH --mem=4G

set -euox pipefail
date +%F" "%T

module load samtools
module load anaconda3

# extra variables so conda is happy
PS1=""

conda activate merge_VCF

pwd

time tabix -h $INPUT_GZ_FILE $TABIX_RANGE |\
    python mergeVCF.py \
        -a $ARCHAIC_VCF \
        -o $OUTPUT_FILE
