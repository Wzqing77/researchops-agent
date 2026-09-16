#!/bin/bash
#SBATCH --job-name=align
#SBATCH --mem=32G
#SBATCH --time=04:00:00

python align.py
