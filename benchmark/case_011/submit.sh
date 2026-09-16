#!/bin/bash
#SBATCH --job-name=checkpoint
#SBATCH --mem=16G
#SBATCH --time=02:00:00

python train.py
