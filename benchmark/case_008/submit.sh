#!/bin/bash
#SBATCH --job-name=inference
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=01:00:00

python inference.py
