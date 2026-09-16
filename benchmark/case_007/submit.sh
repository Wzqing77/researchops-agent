#!/bin/bash
#SBATCH --job-name=simulation
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=00:30:00

python simulation.py
