#!/bin/bash

#SBATCH --time 8:00:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1

set -euo pipefail
date +%F" "%T

module load samtools

time tabix -h $INPUT_GZ_FILE $TABIX_RANGE |\
    ./mergeVCF \
        ${SUPPRESS_LESS_THAN:+-s yes} \
        -a $ARCHAIC_VCF \
        -o $OUTPUT_FILE

date +%F" "%T
echo done
