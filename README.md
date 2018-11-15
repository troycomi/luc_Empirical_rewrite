# merge_VCF
> Combining archaic and human vcf files in simplified output

Python script for combining two vcf files, one from stdin the other as a
command line argument.  A low-memory replacement for 01_GenotypeInputFromVCF.cpp
file as supplied.  Tested agreement using the files produced from merge1.sh with
no diff between outputs.

## Installation
On the Princeton University Della cluster, you must first create the conda
environment for package management.  After cloning to the source directory:

`module load anaconda3`
`conda env create --file environment.yml`

## Usage
Change the variables in `submit.sh` to the required input and output files.
Submit to the slurm job manager by calling `./submit.sh`
