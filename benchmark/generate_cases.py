import json
from pathlib import Path


BENCHMARK_ROOT = Path(__file__).resolve().parent


def write_json(path: Path, data: dict):
    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def write_text(path: Path, text: str):
    path.write_text(
        text.strip() + "\n",
        encoding="utf-8"
    )


CASES = [

    # ========================================================
    # case_005
    # CPU OOM
    # ========================================================
    {
        "case_id": "case_005",

        "ground_truth": {
            "case_id": "case_005",
            "fault_type": "CPU_OUT_OF_MEMORY",
            "root_cause": "The job exhausted its requested system memory.",
            "difficulty": "medium",
            "required_evidence": [
                "scheduler_state",
                "resource_usage"
            ],
            "minimal_evidence": [
                "scheduler_state",
                "resource_usage"
            ],
            "expected_tools": [
                "get_job_accounting",
                "get_resource_usage"
            ]
        },

        "scheduler": {
            "job_id": "1005",
            "state": "OUT_OF_MEMORY",
            "exit_code": "0:125",
            "elapsed": "00:18:44"
        },

        "stdout": """
Reading genotype matrix...
Processing chromosome 1...
Processing chromosome 2...
""",

        "stderr": """
slurmstepd: error: Detected 1 oom_kill event in StepId=1005.batch
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=gwas
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=02:00:00

python gwas.py
""",

        "resource_usage": {
            "requested_memory_gb": 16,
            "max_rss_gb": 15.8,
            "cpu_efficiency": 76.1
        },

        "environment": {
            "python_version": "3.11",
            "conda_environment": "gwas",
            "packages": [
                "numpy",
                "pandas",
                "scipy"
            ]
        },

        "storage": {
            "disk_usage_percent": 54,
            "quota_exceeded": False
        }
    },

    # ========================================================
    # case_006
    # CUDA OOM
    # ========================================================
    {
        "case_id": "case_006",

        "ground_truth": {
            "case_id": "case_006",
            "fault_type": "CUDA_OUT_OF_MEMORY",
            "root_cause": "GPU memory was exhausted during model training.",
            "difficulty": "medium",
            "required_evidence": [
                "stderr",
                "resource_usage"
            ],
            "minimal_evidence": [
                "stderr",
                "resource_usage"
            ],
            "expected_tools": [
                "read_stderr",
                "get_resource_usage"
            ]
        },

        "scheduler": {
            "job_id": "1006",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:16:12"
        },

        "stdout": """
Loading model...
Training batch 1...
Training batch 2...
""",

        "stderr": """
RuntimeError: CUDA out of memory while attempting to allocate 1.50 GiB
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=dl_train
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --gres=gpu:1
#SBATCH --time=08:00:00

python train.py
""",

        "resource_usage": {
            "requested_memory_gb": 128,
            "max_rss_gb": 22.4,
            "gpu_memory_total_gb": 24,
            "gpu_memory_peak_gb": 23.9
        },

        "environment": {
            "python_version": "3.11",
            "conda_environment": "torch",
            "packages": [
                "torch",
                "numpy"
            ],
            "cuda_version": "12.1"
        },

        "storage": {
            "disk_usage_percent": 43,
            "quota_exceeded": False
        }
    },

    # ========================================================
    # case_007
    # TIMEOUT
    # ========================================================
    {
        "case_id": "case_007",

        "ground_truth": {
            "case_id": "case_007",
            "fault_type": "TIMEOUT",
            "root_cause": "The job exceeded the requested Slurm walltime.",
            "difficulty": "easy",
            "required_evidence": [
                "scheduler_state",
                "submit_script"
            ],
            "minimal_evidence": [
                "scheduler_state",
                "submit_script"
            ],
            "expected_tools": [
                "get_job_accounting",
                "read_submit_script"
            ]
        },

        "scheduler": {
            "job_id": "1007",
            "state": "TIMEOUT",
            "exit_code": "0:15",
            "elapsed": "00:30:04"
        },

        "stdout": """
Simulation step 7821...
Simulation step 7822...
""",

        "stderr": """
slurmstepd: error: JOB 1007 CANCELLED DUE TO TIME LIMIT
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=simulation
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=00:30:00

python simulation.py
""",

        "resource_usage": {
            "requested_memory_gb": 32,
            "max_rss_gb": 10.8,
            "cpu_efficiency": 91.3
        },

        "environment": {
            "python_version": "3.10",
            "conda_environment": "simulation",
            "packages": [
                "numpy"
            ]
        },

        "storage": {
            "disk_usage_percent": 61,
            "quota_exceeded": False
        }
    },

    # ========================================================
    # case_008
    # Missing Dependency
    # ========================================================
    {
        "case_id": "case_008",

        "ground_truth": {
            "case_id": "case_008",
            "fault_type": "MISSING_DEPENDENCY",
            "root_cause": "The runtime environment is missing the required cuDNN shared library.",
            "difficulty": "ambiguous",
            "required_evidence": [
                "stderr",
                "environment"
            ],
            "minimal_evidence": [
                "stderr",
                "environment"
            ],
            "expected_tools": [
                "read_stderr",
                "get_environment"
            ]
        },

        "scheduler": {
            "job_id": "1008",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:00:05"
        },

        "stdout": """
Initializing deep learning environment...
""",

        "stderr": """
ImportError: libcudnn.so.8: cannot open shared object file: No such file or directory
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=inference
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=01:00:00

python inference.py
""",

        "resource_usage": {
            "requested_memory_gb": 32,
            "max_rss_gb": 0.7,
            "gpu_memory_total_gb": 24,
            "gpu_memory_peak_gb": 0.2
        },

        "environment": {
            "python_version": "3.11",
            "conda_environment": "inference",
            "packages": [
                "torch",
                "numpy"
            ],
            "cuda_version": "12.1",
            "cudnn_available": False
        },

        "storage": {
            "disk_usage_percent": 50,
            "quota_exceeded": False
        }
    },

    # ========================================================
    # case_009
    # Wrong File Path
    # ========================================================
    {
        "case_id": "case_009",

        "ground_truth": {
            "case_id": "case_009",
            "fault_type": "WRONG_FILE_PATH",
            "root_cause": "The configured input file path does not exist.",
            "difficulty": "easy",
            "required_evidence": [
                "stderr",
                "storage_info"
            ],
            "minimal_evidence": [
                "stderr",
                "storage_info"
            ],
            "expected_tools": [
                "read_stderr",
                "check_storage"
            ]
        },

        "scheduler": {
            "job_id": "1009",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:00:02"
        },

        "stdout": """
Loading input dataset...
""",

        "stderr": """
FileNotFoundError: [Errno 2] No such file or directory: '/data/input.csv'
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=analysis
#SBATCH --mem=16G
#SBATCH --time=01:00:00

python analysis.py --input /data/input.csv
""",

        "resource_usage": {
            "requested_memory_gb": 16,
            "max_rss_gb": 0.2,
            "cpu_efficiency": 1.2
        },

        "environment": {
            "python_version": "3.11",
            "working_directory": "/home/user/project"
        },

        "storage": {
            "disk_usage_percent": 47,
            "quota_exceeded": False,
            "path_checked": "/data/input.csv",
            "path_exists": False
        }
    },

    # ========================================================
    # case_010
    # Wrong File Path - relative path
    # ========================================================
    {
        "case_id": "case_010",

        "ground_truth": {
            "case_id": "case_010",
            "fault_type": "WRONG_FILE_PATH",
            "root_cause": "A relative input path was resolved from the wrong working directory.",
            "difficulty": "ambiguous",
            "required_evidence": [
                "stderr",
                "submit_script",
                "environment",
                "storage_info"
            ],
            "minimal_evidence": [
                "stderr",
                "environment",
                "storage_info"
            ],
            "expected_tools": [
                "read_stderr",
                "read_submit_script",
                "get_environment",
                "check_storage"
            ]
        },

        "scheduler": {
            "job_id": "1010",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:00:04"
        },

        "stdout": """
Starting preprocessing...
""",

        "stderr": """
FileNotFoundError: data/train.csv
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=preprocess
#SBATCH --mem=8G
#SBATCH --time=01:00:00

python preprocess.py --input data/train.csv
""",

        "resource_usage": {
            "requested_memory_gb": 8,
            "max_rss_gb": 0.3,
            "cpu_efficiency": 2.1
        },

        "environment": {
            "python_version": "3.11",
            "working_directory": "/home/user/project/scripts"
        },

        "storage": {
            "disk_usage_percent": 38,
            "quota_exceeded": False,
            "requested_path": "/home/user/project/scripts/data/train.csv",
            "requested_path_exists": False,
            "actual_path": "/home/user/project/data/train.csv",
            "actual_path_exists": True
        }
    },

    # ========================================================
    # case_011
    # Disk Full
    # ========================================================
    {
        "case_id": "case_011",

        "ground_truth": {
            "case_id": "case_011",
            "fault_type": "DISK_FULL",
            "root_cause": "The target filesystem has no free space remaining.",
            "difficulty": "easy",
            "required_evidence": [
                "stderr",
                "storage_info"
            ],
            "minimal_evidence": [
                "stderr",
                "storage_info"
            ],
            "expected_tools": [
                "read_stderr",
                "check_storage"
            ]
        },

        "scheduler": {
            "job_id": "1011",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:42:11"
        },

        "stdout": """
Writing checkpoint...
""",

        "stderr": """
OSError: [Errno 28] No space left on device
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=checkpoint
#SBATCH --mem=16G
#SBATCH --time=02:00:00

python train.py
""",

        "resource_usage": {
            "requested_memory_gb": 16,
            "max_rss_gb": 7.8,
            "cpu_efficiency": 63.0
        },

        "environment": {
            "python_version": "3.11",
            "conda_environment": "train"
        },

        "storage": {
            "filesystem": "/scratch",
            "disk_usage_percent": 100,
            "free_space_gb": 0,
            "quota_exceeded": False
        }
    },

    # ========================================================
    # case_012
    # Disk Quota
    # ========================================================
    {
        "case_id": "case_012",

        "ground_truth": {
            "case_id": "case_012",
            "fault_type": "DISK_FULL",
            "root_cause": "The user exceeded their storage quota even though the filesystem still has free space.",
            "difficulty": "medium",
            "required_evidence": [
                "stderr",
                "storage_info"
            ],
            "minimal_evidence": [
                "stderr",
                "storage_info"
            ],
            "expected_tools": [
                "read_stderr",
                "check_storage"
            ]
        },

        "scheduler": {
            "job_id": "1012",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:19:17"
        },

        "stdout": """
Saving result matrix...
""",

        "stderr": """
OSError: Disk quota exceeded
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=result_save
#SBATCH --mem=8G
#SBATCH --time=01:00:00

python save_results.py
""",

        "resource_usage": {
            "requested_memory_gb": 8,
            "max_rss_gb": 2.1,
            "cpu_efficiency": 30.2
        },

        "environment": {
            "python_version": "3.11",
            "conda_environment": "analysis"
        },

        "storage": {
            "filesystem": "/home",
            "disk_usage_percent": 72,
            "free_space_gb": 640,
            "quota_limit_gb": 100,
            "user_usage_gb": 100,
            "quota_exceeded": True
        }
    },

    # ========================================================
    # case_013
    # Permission Denied
    # ========================================================
    {
        "case_id": "case_013",

        "ground_truth": {
            "case_id": "case_013",
            "fault_type": "PERMISSION_DENIED",
            "root_cause": "The current user does not have permission to read the required reference file.",
            "difficulty": "easy",
            "required_evidence": [
                "stderr",
                "storage_info"
            ],
            "minimal_evidence": [
                "stderr",
                "storage_info"
            ],
            "expected_tools": [
                "read_stderr",
                "check_storage"
            ]
        },

        "scheduler": {
            "job_id": "1013",
            "state": "FAILED",
            "exit_code": "1:0",
            "elapsed": "00:00:03"
        },

        "stdout": """
Opening reference genome...
""",

        "stderr": """
PermissionError: [Errno 13] Permission denied: '/shared/ref/genome.fa'
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=align
#SBATCH --mem=32G
#SBATCH --time=04:00:00

python align.py
""",

        "resource_usage": {
            "requested_memory_gb": 32,
            "max_rss_gb": 0.5,
            "cpu_efficiency": 2.2
        },

        "environment": {
            "python_version": "3.10",
            "user": "researcher"
        },

        "storage": {
            "path": "/shared/ref/genome.fa",
            "path_exists": True,
            "owner": "admin",
            "group": "bioinfo",
            "mode": "0640",
            "user_groups": [
                "users"
            ]
        }
    },

    # ========================================================
    # case_014
    # Permission Denied - execute bit
    # ========================================================
    {
        "case_id": "case_014",

        "ground_truth": {
            "case_id": "case_014",
            "fault_type": "PERMISSION_DENIED",
            "root_cause": "The submitted shell script is not executable because the execute permission is missing.",
            "difficulty": "ambiguous",
            "required_evidence": [
                "stderr",
                "submit_script",
                "storage_info"
            ],
            "minimal_evidence": [
                "stderr",
                "storage_info"
            ],
            "expected_tools": [
                "read_stderr",
                "read_submit_script",
                "check_storage"
            ]
        },

        "scheduler": {
            "job_id": "1014",
            "state": "FAILED",
            "exit_code": "126:0",
            "elapsed": "00:00:01"
        },

        "stdout": """
Launching analysis wrapper...
""",

        "stderr": """
bash: ./run_analysis.sh: Permission denied
""",

        "submit": """
#!/bin/bash
#SBATCH --job-name=wrapper
#SBATCH --mem=8G
#SBATCH --time=01:00:00

./run_analysis.sh
""",

        "resource_usage": {
            "requested_memory_gb": 8,
            "max_rss_gb": 0.1,
            "cpu_efficiency": 0.4
        },

        "environment": {
            "shell": "bash",
            "working_directory": "/home/user/project"
        },

        "storage": {
            "path": "/home/user/project/run_analysis.sh",
            "path_exists": True,
            "owner": "user",
            "mode": "0644",
            "executable": False
        }
    },

    # ========================================================
    # case_015
    # Pending Resources
    # ========================================================
    {
        "case_id": "case_015",

        "ground_truth": {
            "case_id": "case_015",
            "fault_type": "PENDING_RESOURCES",
            "root_cause": "The job is waiting because the requested GPU resources are currently unavailable.",
            "difficulty": "easy",
            "required_evidence": [
                "scheduler_state",
                "submit_script"
            ],
            "minimal_evidence": [
                "scheduler_state",
                "submit_script"
            ],
            "expected_tools": [
                "get_job_accounting",
                "read_submit_script"
            ]
        },

        "scheduler": {
            "job_id": "1015",
            "state": "PENDING",
            "reason": "Resources",
            "elapsed": "00:00:00"
        },

        "stdout": "",

        "stderr": "",

        "submit": """
#!/bin/bash
#SBATCH --job-name=gpu_train
#SBATCH --partition=gpu
#SBATCH --gres=gpu:4
#SBATCH --mem=128G
#SBATCH --time=12:00:00

python train.py
""",

        "resource_usage": {
            "allocated": False
        },

        "environment": {
            "python_version": "3.11",
            "conda_environment": "torch"
        },

        "storage": {
            "disk_usage_percent": 40,
            "quota_exceeded": False
        }
    },

    # ========================================================
    # case_016
    # Pending Resources
    # ========================================================
    {
        "case_id": "case_016",

        "ground_truth": {
            "case_id": "case_016",
            "fault_type": "PENDING_RESOURCES",
            "root_cause": "No currently available node satisfies the requested high-memory job configuration.",
            "difficulty": "medium",
            "required_evidence": [
                "scheduler_state",
                "submit_script"
            ],
            "minimal_evidence": [
                "scheduler_state",
                "submit_script"
            ],
            "expected_tools": [
                "get_job_accounting",
                "read_submit_script"
            ]
        },

        "scheduler": {
            "job_id": "1016",
            "state": "PENDING",
            "reason": "Resources",
            "elapsed": "00:00:00"
        },

        "stdout": "",

        "stderr": "",

        "submit": """
#!/bin/bash
#SBATCH --job-name=large_memory
#SBATCH --partition=highmem
#SBATCH --cpus-per-task=32
#SBATCH --mem=512G
#SBATCH --time=24:00:00

python large_analysis.py
""",

        "resource_usage": {
            "allocated": False
        },

        "environment": {
            "python_version": "3.11",
            "conda_environment": "analysis"
        },

        "storage": {
            "disk_usage_percent": 51,
            "quota_exceeded": False
        }
    }
]


def generate_case(case: dict):

    case_dir = (
        BENCHMARK_ROOT
        / case["case_id"]
    )

    case_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    write_json(
        case_dir / "ground_truth.json",
        case["ground_truth"]
    )

    write_json(
        case_dir / "scheduler.json",
        case["scheduler"]
    )

    write_text(
        case_dir / "stdout.log",
        case["stdout"]
    )

    write_text(
        case_dir / "stderr.log",
        case["stderr"]
    )

    write_text(
        case_dir / "submit.sh",
        case["submit"]
    )

    write_json(
        case_dir / "resource_usage.json",
        case["resource_usage"]
    )

    write_json(
        case_dir / "environment.json",
        case["environment"]
    )

    write_json(
        case_dir / "storage.json",
        case["storage"]
    )


def main():

    print(
        "\n================================"
    )

    print(
        "GENERATE BENCHMARK CASES"
    )

    print(
        "================================"
    )

    for case in CASES:

        generate_case(
            case
        )

        print(
            "Generated:",
            case["case_id"]
        )


    print(
        "\nGenerated cases:",
        len(CASES)
    )


if __name__ == "__main__":
    main()