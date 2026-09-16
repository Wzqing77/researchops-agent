#!/bin/bash
#SBATCH --job-name=result_save
#SBATCH --mem=8G
#SBATCH --time=01:00:00

python save_results.py
