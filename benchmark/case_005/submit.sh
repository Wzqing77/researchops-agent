#!/bin/bash
#SBATCH --job-name=gwas
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=02:00:00

python gwas.py
