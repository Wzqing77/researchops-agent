#!/bin/bash
#SBATCH --job-name=large_gpu_job
#SBATCH --partition=gpu
#SBATCH --gres=gpu:8
#SBATCH --mem=512G
#SBATCH --time=12:00:00

python train_large.py
