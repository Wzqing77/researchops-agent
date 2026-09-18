#!/bin/bash
#SBATCH --job-name=matrix_build
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=03:00:00

python build_matrix.py
