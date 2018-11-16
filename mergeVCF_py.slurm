#!/bin/bash

#SBATCH --time 8:00:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1

set -euox pipefail
date +%F" "%T

module load samtools
module load anaconda3

# extra variables so conda is happy
PS1=""

conda activate merge_VCF

time tabix -h $INPUT_GZ_FILE $TABIX_RANGE |\
    python mergeVCF.py \
        -a $ARCHAIC_VCF \
        -o $OUTPUT_FILE

date +%F" "%T
echo done
