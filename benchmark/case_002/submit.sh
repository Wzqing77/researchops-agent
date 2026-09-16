#!/bin/bash

#SBATCH --job-name=train_model
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --gres=gpu:1
#SBATCH --time=06:00:00

python train.py