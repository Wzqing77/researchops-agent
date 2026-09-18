#!/bin/bash
#SBATCH --job-name=bam_index

samtools index sample.bam
