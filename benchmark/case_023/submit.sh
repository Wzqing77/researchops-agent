#!/bin/bash
#SBATCH --job-name=cnn_train
#SBATCH --gres=gpu:1

python cnn_train.py
