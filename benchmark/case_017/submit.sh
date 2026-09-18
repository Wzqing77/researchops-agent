#!/bin/bash
#SBATCH --job-name=large_table
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=02:00:00

python large_table.py
