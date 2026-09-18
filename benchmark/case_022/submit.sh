#!/bin/bash
#SBATCH --job-name=variant_scan
#SBATCH --mem=16G
#SBATCH --time=00:45:00

python scan.py
