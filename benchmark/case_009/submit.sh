#!/bin/bash
#SBATCH --job-name=analysis
#SBATCH --mem=16G
#SBATCH --time=01:00:00

python analysis.py --input /data/input.csv
