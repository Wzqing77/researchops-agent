#!/bin/bash
#SBATCH --job-name=align

python align.py --reference /scratch/project/reference.fa
