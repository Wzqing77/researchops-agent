#!/bin/bash
#SBATCH --job-name=dl_train
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:1
#SBATCH --time=08:00:00

python train.py
