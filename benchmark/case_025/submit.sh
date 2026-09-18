#!/bin/bash
#SBATCH --job-name=config_train

cd /home/user/project/scripts
python train.py --config configs/train.yaml
