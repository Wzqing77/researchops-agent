#!/bin/bash
#SBATCH --job-name=large_memory
#SBATCH --partition=highmem
#SBATCH --cpus-per-task=32
#SBATCH --mem=512G
#SBATCH --time=24:00:00

python large_analysis.py
