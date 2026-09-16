import json

from pathlib import Path


class MockCluster:

    def __init__(
        self,
        benchmark_root: Path
    ):
        self.benchmark_root = benchmark_root


    # ========================================================
    # Internal:
    # Find Benchmark Case
    # ========================================================

    def _find_case_by_job_id(
        self,
        job_id: str
    ) -> Path:

        for case_dir in self.benchmark_root.glob(
            "case_*"
        ):

            scheduler_file = (
                case_dir
                / "scheduler.json"
            )


            if not scheduler_file.exists():
                continue


            data = self._read_json(
                scheduler_file
            )


            if str(
                data["job_id"]
            ) == str(
                job_id
            ):
                return case_dir


        raise ValueError(
            f"Job not found: {job_id}"
        )


    # ========================================================
    # Internal:
    # JSON Reader
    # ========================================================

    def _read_json(
        self,
        path: Path
    ) -> dict:

        if not path.exists():

            raise FileNotFoundError(
                f"Evidence file not found: {path.name}"
            )


        return json.loads(

            path.read_text(
                encoding="utf-8"
            )
        )


    # ========================================================
    # Internal:
    # Text Reader
    # ========================================================

    def _read_text(
        self,
        path: Path
    ) -> str:

        if not path.exists():

            raise FileNotFoundError(
                f"Evidence file not found: {path.name}"
            )


        return path.read_text(
            encoding="utf-8"
        )


    # ========================================================
    # Tool 1:
    # Current Job Status
    # ========================================================

    def get_job_status(
        self,
        job_id: str
    ) -> dict:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        data = self._read_json(

            case_dir
            / "scheduler.json"
        )


        return {

            "job_id":
                data["job_id"],

            "state":
                data["state"]
        }


    # ========================================================
    # Tool 2:
    # Job Accounting
    #
    # 模拟 sacct
    # ========================================================

    def get_job_accounting(
        self,
        job_id: str
    ) -> dict:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        return self._read_json(

            case_dir
            / "scheduler.json"
        )


    # ========================================================
    # Tool 3:
    # stdout
    # ========================================================

    def read_stdout(
        self,
        job_id: str
    ) -> str:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        return self._read_text(

            case_dir
            / "stdout.log"
        )


    # ========================================================
    # Tool 4:
    # stderr
    # ========================================================

    def read_stderr(
        self,
        job_id: str
    ) -> str:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        return self._read_text(

            case_dir
            / "stderr.log"
        )


    # ========================================================
    # Tool 5:
    # Resource Usage
    # ========================================================

    def get_resource_usage(
        self,
        job_id: str
    ) -> dict:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        return self._read_json(

            case_dir
            / "resource_usage.json"
        )


    # ========================================================
    # Tool 6:
    # Submission Script
    # ========================================================

    def read_submit_script(
        self,
        job_id: str
    ) -> str:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        return self._read_text(

            case_dir
            / "submit.sh"
        )


    # ========================================================
    # Tool 7:
    # Environment
    # ========================================================

    def get_environment(
        self,
        job_id: str
    ) -> dict:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        return self._read_json(

            case_dir
            / "environment.json"
        )


    # ========================================================
    # Tool 8:
    # Storage
    # ========================================================

    def check_storage(
        self,
        job_id: str
    ) -> dict:

        case_dir = (
            self._find_case_by_job_id(
                job_id
            )
        )


        storage_file = (
            case_dir
            / "storage.json"
        )


        # ----------------------------------------------------
        # 某个 Benchmark Case 可以没有 storage Evidence。
        # ----------------------------------------------------

        if not storage_file.exists():

            return {

                "available":
                    False,

                "message":
                    "Storage evidence is not available "
                    "for this case."
            }


        data = self._read_json(
            storage_file
        )


        return {

            "available":
                True,

            **data
        }