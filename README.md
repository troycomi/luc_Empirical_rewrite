# merge_VCF
> Combining archaic and human vcf files in simplified output

Python script for combining two vcf files, one from stdin the other as a
command line argument.  A low-memory replacement for 01_GenotypeInputFromVCF.cpp
file as supplied.  Tested agreement using the files produced from merge1.sh with
no diff between outputs.

## Installation - Python
On the Princeton University Della cluster, you must first create the conda
environment for package management.  After cloning to the source directory:

```
module load anaconda3
conda create --name test_import --file environment.txt
```

## Installation - C++
Prior to running for the first time, the executable must be made manually with:

```
g++ -std=c++11 mergeVCF.cpp -o mergeVCF
```

## Usage
Change the variables for input and output files 
in `submit.sh` to the required input and output files.

The variable `SUPPRESS_LESS_THAN` is true if it is defined.  If all the rows
are required comment out the export statement.

Submit to the slurm job manager by calling `./submit.sh`

The choice of running the python or C++ version is made by 
selecting either the mergeVCF_py.slurm or mergeVCF_cpp.slurm script
in the sbatch command within submit.sh
