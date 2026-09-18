#!/bin/bash
#SBATCH --job-name=gpu_train
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=04:00:00

python train_gpu.py
