#!/bin/bash

#SBATCH --time 8:00:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1

set -euo pipefail
date +%F" "%T

module load samtools

time \
    tabix -h $INPUT_GZ_FILE2 $TABIX_RANGE |\
        ./mergeVCF2 \
            -s three \
            -o $OUTPUT_FILE \
            -a <(\
                tabix -h $INPUT_GZ_FILE1 $TABIX_RANGE |\
                    ./mergeVCF2 \
                        -s yes \
                        -a $ARCHAIC_VCF \
                        )

date +%F" "%T
echo done
