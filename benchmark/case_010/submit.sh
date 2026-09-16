#!/bin/bash
#SBATCH --job-name=preprocess
#SBATCH --mem=8G
#SBATCH --time=01:00:00

python preprocess.py --input data/train.csv
