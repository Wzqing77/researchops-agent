#!/bin/bash
#SBATCH --job-name=wrapper
#SBATCH --mem=8G
#SBATCH --time=01:00:00

./run_analysis.sh
