#!/bin/bash
#SBATCH --job-name=llm_train
#SBATCH --gres=gpu:1
#SBATCH --mem=96G
#SBATCH --time=08:00:00

python train_model.py
