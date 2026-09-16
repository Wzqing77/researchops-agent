#!/bin/bash
#SBATCH --job-name=gpu_train
#SBATCH --partition=gpu
#SBATCH --gres=gpu:4
#SBATCH --mem=128G
#SBATCH --time=12:00:00

python train.py
