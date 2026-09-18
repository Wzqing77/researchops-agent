import json
from pathlib import Path


BENCHMARK_ROOT = (
    Path(__file__)
    .resolve()
    .parent
)


def write_json(
    path: Path,
    data: dict,
):
    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def write_text(
    path: Path,
    text: str,
):
    path.write_text(
        text,
        encoding="utf-8",
    )


def write_case(
    case_id: str,
    scheduler: dict,
    stderr: str,
    stdout: str,
    resource_usage: dict,
    submit_script: str,
    environment: dict,
    ground_truth: dict,
    storage: dict | None = None,
):

    case_dir = (
        BENCHMARK_ROOT
        / case_id
    )

    case_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_json(
        case_dir / "scheduler.json",
        scheduler,
    )

    write_text(
        case_dir / "stderr.log",
        stderr,
    )

    write_text(
        case_dir / "stdout.log",
        stdout,
    )

    write_json(
        case_dir / "resource_usage.json",
        resource_usage,
    )

    write_text(
        case_dir / "submit.sh",
        submit_script,
    )

    write_json(
        case_dir / "environment.json",
        environment,
    )

    write_json(
        case_dir / "ground_truth.json",
        ground_truth,
    )

    storage_path = (
        case_dir
        / "storage.json"
    )

    if storage is not None:

        write_json(
            storage_path,
            storage,
        )

    elif storage_path.exists():

        storage_path.unlink()


CASES = [

    # ========================================================
    # CPU OUT OF MEMORY
    # ========================================================

    {
        "case_id": "case_017",

        "scheduler": {
            "job_id": "1017",
            "state": "FAILED",
            "exit_code": "0:9",
            "elapsed": "00:27:43",
        },

        "stderr": (
            "slurmstepd: error: "
            "Detected 1 oom_kill event "
            "in StepId=1017.batch."
        ),

        "stdout": (
            "Loading dataset...\n"
            "Processing samples...\n"
        ),

        "resource_usage": {
            "requested_memory_gb": 48,
            "max_rss_gb": 47.8,
            "cpu_efficiency": 81.2,
        },

        "submit_script": """#!/bin/bash
#SBATCH --job-name=large_table
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=02:00:00

python large_table.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "data_env",
            "packages": [
                "numpy",
                "pandas",
                "pyarrow",
            ],
        },

        "ground_truth": {
            "case_id": "case_017",
            "fault_type": "CPU_OUT_OF_MEMORY",
            "root_cause": (
                "Job exceeded its allocated "
                "system memory."
            ),
            "difficulty": "ambiguous",
            "required_evidence": [
                "stderr",
                "resource_usage",
            ],
            "minimal_evidence": [
                "stderr",
                "resource_usage",
            ],
            "expected_tools": [
                "get_resource_usage",
            ],
        },
    },

    {
        "case_id": "case_018",

        "scheduler": {
            "job_id": "1018",
            "state": "OUT_OF_MEMORY",
            "exit_code": "0:9",
            "elapsed": "01:13:02",
        },

        "stderr": "Killed",

        "stdout": (
            "Starting matrix construction...\n"
        ),

        "resource_usage": {
            "requested_memory_gb": 64,
            "max_rss_gb": 63.6,
            "cpu_efficiency": 69.1,
        },

        "submit_script": """#!/bin/bash
#SBATCH --job-name=matrix_build
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=03:00:00

python build_matrix.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "matrix_env",
            "packages": [
                "numpy",
                "scipy",
            ],
        },

        "ground_truth": {
            "case_id": "case_018",
            "fault_type": "CPU_OUT_OF_MEMORY",
            "root_cause": (
                "Peak system RAM usage reached "
                "the allocated memory limit."
            ),
            "difficulty": "medium",
            "required_evidence": [
                "scheduler_state",
                "resource_usage",
            ],
            "minimal_evidence": [
                "scheduler_state",
                "resource_usage",
            ],
            "expected_tools": [
                "get_resource_usage",
            ],
        },
    },

    # ========================================================
    # CUDA OUT OF MEMORY
    # ========================================================

    {
        "case_id": "case_019",

        "scheduler": {
            "job_id": "1019",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:12:33",
        },

        "stderr": (
            "RuntimeError: CUDA error: "
            "out of memory"
        ),

        "stdout": (
            "Epoch 1 started...\n"
        ),

        "resource_usage": {
            "requested_memory_gb": 32,
            "max_rss_gb": 9.4,
            "gpu_memory_total_gb": 16,
            "gpu_memory_peak_gb": 15.9,
        },

        "submit_script": """#!/bin/bash
#SBATCH --job-name=gpu_train
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=04:00:00

python train_gpu.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "torch_env",
            "packages": [
                "torch",
                "numpy",
            ],
        },

        "ground_truth": {
            "case_id": "case_019",
            "fault_type": "CUDA_OUT_OF_MEMORY",
            "root_cause": (
                "GPU VRAM was exhausted "
                "during model execution."
            ),
            "difficulty": "medium",
            "required_evidence": [
                "stderr",
                "resource_usage",
            ],
            "minimal_evidence": [
                "stderr",
            ],
            "expected_tools": [
                "get_resource_usage",
            ],
        },
    },

    {
        "case_id": "case_020",

        "scheduler": {
            "job_id": "1020",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:48:15",
        },

        "stderr": (
            "torch.cuda.OutOfMemoryError: "
            "CUDA out of memory. "
            "Tried to allocate 3.00 GiB."
        ),

        "stdout": (
            "Training batch 842...\n"
        ),

        "resource_usage": {
            "requested_memory_gb": 96,
            "max_rss_gb": 21.7,
            "gpu_memory_total_gb": 48,
            "gpu_memory_peak_gb": 47.7,
        },

        "submit_script": """#!/bin/bash
#SBATCH --job-name=llm_train
#SBATCH --gres=gpu:1
#SBATCH --mem=96G
#SBATCH --time=08:00:00

python train_model.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "llm_env",
            "packages": [
                "torch",
                "transformers",
            ],
        },

        "ground_truth": {
            "case_id": "case_020",
            "fault_type": "CUDA_OUT_OF_MEMORY",
            "root_cause": (
                "Model exceeded available GPU VRAM."
            ),
            "difficulty": "easy",
            "required_evidence": [
                "stderr",
                "resource_usage",
            ],
            "minimal_evidence": [
                "stderr",
            ],
            "expected_tools": [
                "get_resource_usage",
            ],
        },
    },

    # ========================================================
    # TIMEOUT
    # ========================================================

    {
        "case_id": "case_021",

        "scheduler": {
            "job_id": "1021",
            "state": "TIMEOUT",
            "exit_code": "0:15",
            "elapsed": "02:00:03",
        },

        "stderr": "",

        "stdout": (
            "Simulation iteration 728...\n"
        ),

        "resource_usage": {
            "requested_memory_gb": 24,
            "max_rss_gb": 11.2,
        },

        "submit_script": """#!/bin/bash
#SBATCH --job-name=simulation
#SBATCH --mem=24G
#SBATCH --time=02:00:00

python simulate.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "sim_env",
            "packages": [
                "numpy",
                "scipy",
            ],
        },

        "ground_truth": {
            "case_id": "case_021",
            "fault_type": "TIMEOUT",
            "root_cause": (
                "Job reached the requested "
                "two-hour walltime."
            ),
            "difficulty": "ambiguous",
            "required_evidence": [
                "scheduler_state",
                "submit_script",
            ],
            "minimal_evidence": [
                "scheduler_state",
                "submit_script",
            ],
            "expected_tools": [
                "get_job_accounting",
                "read_submit_script",
            ],
        },
    },

    {
        "case_id": "case_022",

        "scheduler": {
            "job_id": "1022",
            "state": "TIMEOUT",
            "exit_code": "0:15",
            "elapsed": "00:45:03",
        },

        "stderr": (
            "slurmstepd: error: "
            "*** JOB 1022 CANCELLED "
            "DUE TO TIME LIMIT ***"
        ),

        "stdout": (
            "Processing chromosome 16...\n"
        ),

        "resource_usage": {
            "requested_memory_gb": 16,
            "max_rss_gb": 8.1,
        },

        "submit_script": """#!/bin/bash
#SBATCH --job-name=variant_scan
#SBATCH --mem=16G
#SBATCH --time=00:45:00

python scan.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "scan_env",
            "packages": [
                "numpy",
                "pandas",
            ],
        },

        "ground_truth": {
            "case_id": "case_022",
            "fault_type": "TIMEOUT",
            "root_cause": (
                "Job exceeded its configured walltime."
            ),
            "difficulty": "medium",
            "required_evidence": [
                "scheduler_state",
                "stderr",
                "submit_script",
            ],
            "minimal_evidence": [
                "scheduler_state",
                "stderr",
            ],
            "expected_tools": [
                "get_job_accounting",
                "read_submit_script",
            ],
        },
    },

    # ========================================================
    # MISSING DEPENDENCY
    # ========================================================

    {
        "case_id": "case_023",

        "scheduler": {
            "job_id": "1023",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:00:08",
        },

        "stderr": (
            "ImportError: libcudnn.so.9: "
            "cannot open shared object file: "
            "No such file or directory"
        ),

        "stdout": "",

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=cnn_train
#SBATCH --gres=gpu:1

python cnn_train.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "cnn_env",
            "packages": [
                "torch",
                "numpy",
            ],
            "loaded_modules": [
                "cuda/12.4",
            ],
        },

        "ground_truth": {
            "case_id": "case_023",
            "fault_type": "MISSING_DEPENDENCY",
            "root_cause": (
                "Required cuDNN shared library "
                "was unavailable."
            ),
            "difficulty": "ambiguous",
            "required_evidence": [
                "stderr",
                "environment",
            ],
            "minimal_evidence": [
                "stderr",
            ],
            "expected_tools": [
                "get_environment",
            ],
        },
    },

    {
        "case_id": "case_024",

        "scheduler": {
            "job_id": "1024",
            "state": "FAILED",
            "exit_code": "127:0",
            "elapsed": "00:00:01",
        },

        "stderr": (
            "/bin/bash: samtools: "
            "command not found"
        ),

        "stdout": "",

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=bam_index

samtools index sample.bam
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "bio_env",
            "packages": [
                "numpy",
                "pandas",
            ],
            "loaded_modules": [],
        },

        "ground_truth": {
            "case_id": "case_024",
            "fault_type": "MISSING_DEPENDENCY",
            "root_cause": (
                "samtools was unavailable "
                "in the runtime environment."
            ),
            "difficulty": "medium",
            "required_evidence": [
                "stderr",
                "environment",
            ],
            "minimal_evidence": [
                "stderr",
            ],
            "expected_tools": [
                "get_environment",
            ],
        },
    },

    # ========================================================
    # WRONG FILE PATH
    # ========================================================

    {
        "case_id": "case_025",

        "scheduler": {
            "job_id": "1025",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:00:03",
        },

        "stderr": (
            "FileNotFoundError: "
            "[Errno 2] No such file or directory: "
            "'configs/train.yaml'"
        ),

        "stdout": "",

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=config_train

cd /home/user/project/scripts
python train.py --config configs/train.yaml
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "train_env",
            "packages": [
                "torch",
                "pyyaml",
            ],
        },

        "ground_truth": {
            "case_id": "case_025",
            "fault_type": "WRONG_FILE_PATH",
            "root_cause": (
                "Relative configuration path was "
                "invalid from the working directory."
            ),
            "difficulty": "ambiguous",
            "required_evidence": [
                "stderr",
                "submit_script",
            ],
            "minimal_evidence": [
                "stderr",
                "submit_script",
            ],
            "expected_tools": [
                "read_submit_script",
            ],
        },
    },

    {
        "case_id": "case_026",

        "scheduler": {
            "job_id": "1026",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:00:05",
        },

        "stderr": (
            "FileNotFoundError: "
            "/scratch/project/reference.fa"
        ),

        "stdout": "",

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=align

python align.py --reference /scratch/project/reference.fa
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "align_env",
            "packages": [
                "pysam",
            ],
        },

        "ground_truth": {
            "case_id": "case_026",
            "fault_type": "WRONG_FILE_PATH",
            "root_cause": (
                "Configured reference file path "
                "did not exist."
            ),
            "difficulty": "easy",
            "required_evidence": [
                "stderr",
                "submit_script",
            ],
            "minimal_evidence": [
                "stderr",
            ],
            "expected_tools": [
                "read_submit_script",
            ],
        },
    },

    # ========================================================
    # DISK FULL
    # ========================================================

    {
        "case_id": "case_027",

        "scheduler": {
            "job_id": "1027",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:16:42",
        },

        "stderr": (
            "OSError: Disk quota exceeded"
        ),

        "stdout": (
            "Writing result files...\n"
        ),

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=result_export

python export_results.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "export_env",
            "packages": [
                "pandas",
            ],
        },

        "storage": {
            "disk_usage_percent": 62,
            "free_space_gb": 510,
            "quota_exceeded": True,
            "user_quota_gb": 100,
            "user_usage_gb": 100,
        },

        "ground_truth": {
            "case_id": "case_027",
            "fault_type": "DISK_FULL",
            "root_cause": (
                "User storage quota was exhausted "
                "despite free filesystem capacity."
            ),
            "difficulty": "medium",
            "required_evidence": [
                "stderr",
                "storage_info",
            ],
            "minimal_evidence": [
                "stderr",
                "storage_info",
            ],
            "expected_tools": [
                "check_storage",
            ],
        },
    },

    {
        "case_id": "case_028",

        "scheduler": {
            "job_id": "1028",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:08:14",
        },

        "stderr": (
            "OSError: [Errno 28] "
            "No space left on device"
        ),

        "stdout": (
            "Saving checkpoints...\n"
        ),

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=checkpoint

python save_checkpoints.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "model_env",
            "packages": [
                "torch",
            ],
        },

        "storage": {
            "disk_usage_percent": 100,
            "free_space_gb": 0,
            "quota_exceeded": False,
        },

        "ground_truth": {
            "case_id": "case_028",
            "fault_type": "DISK_FULL",
            "root_cause": (
                "Filesystem had no remaining capacity."
            ),
            "difficulty": "easy",
            "required_evidence": [
                "stderr",
                "storage_info",
            ],
            "minimal_evidence": [
                "stderr",
            ],
            "expected_tools": [
                "check_storage",
            ],
        },
    },

    # ========================================================
    # PERMISSION DENIED
    # ========================================================

    {
        "case_id": "case_029",

        "scheduler": {
            "job_id": "1029",
            "state": "FAILED",
            "exit_code": "126:0",
            "elapsed": "00:00:01",
        },

        "stderr": (
            "/bin/bash: ./run_pipeline.sh: "
            "Permission denied"
        ),

        "stdout": "",

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=pipeline

./run_pipeline.sh
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "base",
            "packages": [],
        },

        "ground_truth": {
            "case_id": "case_029",
            "fault_type": "PERMISSION_DENIED",
            "root_cause": (
                "Pipeline script could not be "
                "executed due to file permissions."
            ),
            "difficulty": "medium",
            "required_evidence": [
                "stderr",
                "submit_script",
            ],
            "minimal_evidence": [
                "stderr",
            ],
            "expected_tools": [
                "read_submit_script",
            ],
        },
    },

    # ========================================================
    # PENDING RESOURCES
    # ========================================================

    {
        "case_id": "case_030",

        "scheduler": {
            "job_id": "1030",
            "state": "PENDING",
            "reason": "Resources",
            "exit_code": "0:0",
            "elapsed": "00:00:00",
        },

        "stderr": "",

        "stdout": "",

        "resource_usage": {},

        "submit_script": """#!/bin/bash
#SBATCH --job-name=large_gpu_job
#SBATCH --partition=gpu
#SBATCH --gres=gpu:8
#SBATCH --mem=512G
#SBATCH --time=12:00:00

python train_large.py
""",

        "environment": {
            "python_version": "3.11",
            "conda_environment": "large_model_env",
            "packages": [
                "torch",
                "transformers",
            ],
        },

        "ground_truth": {
            "case_id": "case_030",
            "fault_type": "PENDING_RESOURCES",
            "root_cause": (
                "Job is waiting because requested "
                "resources are currently unavailable."
            ),
            "difficulty": "medium",
            "required_evidence": [
                "scheduler_state",
                "submit_script",
            ],
            "minimal_evidence": [
                "scheduler_state",
            ],
            "expected_tools": [
                "get_job_accounting",
                "read_submit_script",
            ],
        },
    },
]


def main():

    for case in CASES:

        write_case(
            **case
        )

        print(
            f"Generated "
            f"{case['case_id']}"
        )


    print()
    print(
        f"Generated: {len(CASES)} cases"
    )


if __name__ == "__main__":
    main()