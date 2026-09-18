#!/bin/bash
#SBATCH --job-name=simulation
#SBATCH --mem=24G
#SBATCH --time=02:00:00

python simulate.py
