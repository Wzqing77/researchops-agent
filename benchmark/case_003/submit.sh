#!/bin/bash

#SBATCH --job-name=long_analysis
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00

python long_analysis.py