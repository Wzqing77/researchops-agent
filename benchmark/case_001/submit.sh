#!/bin/bash

#SBATCH --job-name=analysis
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00

python analysis.py