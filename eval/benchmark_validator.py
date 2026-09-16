from pathlib import Path

from eval.benchmark_loader import (
    BenchmarkLoader
)


# ============================================================
# Allowed Values
# ============================================================

VALID_FAULT_TYPES = {

    "CPU_OUT_OF_MEMORY",
    "CUDA_OUT_OF_MEMORY",
    "TIMEOUT",
    "MISSING_DEPENDENCY",
    "WRONG_FILE_PATH",
    "DISK_FULL",
    "PERMISSION_DENIED",
    "PENDING_RESOURCES",
}


VALID_DIFFICULTIES = {

    "easy",
    "medium",
    "ambiguous",
}


VALID_EVIDENCE_TYPES = {

    "scheduler_state",
    "stdout",
    "stderr",
    "resource_usage",
    "submit_script",
    "environment",
    "storage_info",
    "cluster_documentation",
}


VALID_TOOLS = {

    "get_job_status",
    "get_job_accounting",
    "read_stdout",
    "read_stderr",
    "get_resource_usage",
    "read_submit_script",
    "get_environment",
    "check_storage",
}


REQUIRED_GROUND_TRUTH_FIELDS = {

    "case_id",
    "fault_type",
    "root_cause",
    "difficulty",
    "required_evidence",
    "minimal_evidence",
    "expected_tools",
}


# ============================================================
# Benchmark Validator
# ============================================================

class BenchmarkValidator:

    def __init__(
        self,
        benchmark_root: Path
    ):

        self.benchmark_root = (
            benchmark_root
        )


        self.loader = BenchmarkLoader(

            benchmark_root=(
                benchmark_root
            )
        )


    # ========================================================
    # Validate One Case
    # ========================================================

    def validate_case(
        self,
        case_dir: Path
    ) -> list[str]:

        errors = []


        # ----------------------------------------------------
        # Ground Truth
        # ----------------------------------------------------

        try:

            truth = (
                self.loader
                .load_ground_truth(
                    case_dir
                )
            )

        except Exception as exc:

            return [

                (
                    f"{case_dir.name}: "
                    f"cannot load ground truth: "
                    f"{exc}"
                )
            ]


        # ----------------------------------------------------
        # Required Fields
        # ----------------------------------------------------

        missing_fields = (

            REQUIRED_GROUND_TRUTH_FIELDS
            -
            set(
                truth.keys()
            )
        )


        if missing_fields:

            errors.append(

                (
                    f"{case_dir.name}: "
                    f"missing fields: "
                    f"{sorted(missing_fields)}"
                )
            )


            # 后面的验证依赖这些字段，
            # 缺失时直接返回。
            return errors


        # ----------------------------------------------------
        # Case ID
        # ----------------------------------------------------

        if (
            truth["case_id"]
            !=
            case_dir.name
        ):

            errors.append(

                (
                    f"{case_dir.name}: "
                    f"case_id mismatch: "
                    f"{truth['case_id']}"
                )
            )


        # ----------------------------------------------------
        # Fault Type
        # ----------------------------------------------------

        if (
            truth["fault_type"]
            not in
            VALID_FAULT_TYPES
        ):

            errors.append(

                (
                    f"{case_dir.name}: "
                    f"invalid fault_type: "
                    f"{truth['fault_type']}"
                )
            )


        # ----------------------------------------------------
        # Difficulty
        # ----------------------------------------------------

        if (
            truth["difficulty"]
            not in
            VALID_DIFFICULTIES
        ):

            errors.append(

                (
                    f"{case_dir.name}: "
                    f"invalid difficulty: "
                    f"{truth['difficulty']}"
                )
            )


        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        for field_name in [

            "required_evidence",
            "minimal_evidence",
        ]:

            values = truth[
                field_name
            ]


            if not isinstance(
                values,
                list
            ):

                errors.append(

                    (
                        f"{case_dir.name}: "
                        f"{field_name} must be a list"
                    )
                )

                continue


            invalid_values = (

                set(values)
                -
                VALID_EVIDENCE_TYPES
            )


            if invalid_values:

                errors.append(

                    (
                        f"{case_dir.name}: "
                        f"invalid {field_name}: "
                        f"{sorted(invalid_values)}"
                    )
                )


        # ----------------------------------------------------
        # minimal_evidence
        # 应该是 required_evidence 的子集
        # ----------------------------------------------------

        if (

            isinstance(
                truth["minimal_evidence"],
                list
            )

            and

            isinstance(
                truth["required_evidence"],
                list
            )
        ):

            extra_minimal = (

                set(
                    truth[
                        "minimal_evidence"
                    ]
                )

                -

                set(
                    truth[
                        "required_evidence"
                    ]
                )
            )


            if extra_minimal:

                errors.append(

                    (
                        f"{case_dir.name}: "
                        f"minimal_evidence is not "
                        f"a subset of required_evidence: "
                        f"{sorted(extra_minimal)}"
                    )
                )


        # ----------------------------------------------------
        # Expected Tools
        # ----------------------------------------------------

        expected_tools = (
            truth[
                "expected_tools"
            ]
        )


        if not isinstance(
            expected_tools,
            list
        ):

            errors.append(

                (
                    f"{case_dir.name}: "
                    f"expected_tools must be a list"
                )
            )


        else:

            invalid_tools = (

                set(
                    expected_tools
                )

                -
                VALID_TOOLS
            )


            if invalid_tools:

                errors.append(

                    (
                        f"{case_dir.name}: "
                        f"invalid expected_tools: "
                        f"{sorted(invalid_tools)}"
                    )
                )


        # ----------------------------------------------------
        # Scheduler File
        # ----------------------------------------------------

        scheduler_file = (

            case_dir
            / "scheduler.json"
        )


        if not scheduler_file.exists():

            errors.append(

                (
                    f"{case_dir.name}: "
                    f"missing scheduler.json"
                )
            )


        return errors


    # ========================================================
    # Validate Whole Benchmark
    # ========================================================

    def validate_all(
        self
    ) -> list[str]:

        errors = []


        case_dirs = (
            self.loader
            .list_cases()
        )


        case_ids = set()

        job_ids = set()


        for case_dir in case_dirs:

            case_errors = (
                self.validate_case(
                    case_dir
                )
            )


            errors.extend(
                case_errors
            )


            # ------------------------------------------------
            # Global uniqueness checks
            # ------------------------------------------------

            try:

                truth = (
                    self.loader
                    .load_ground_truth(
                        case_dir
                    )
                )


                case_id = truth.get(
                    "case_id"
                )


                if case_id in case_ids:

                    errors.append(

                        (
                            f"duplicate case_id: "
                            f"{case_id}"
                        )
                    )


                case_ids.add(
                    case_id
                )


            except Exception:

                pass


            scheduler_file = (

                case_dir
                / "scheduler.json"
            )


            if scheduler_file.exists():

                try:

                    import json


                    scheduler = json.loads(

                        scheduler_file
                        .read_text(
                            encoding="utf-8"
                        )
                    )


                    job_id = str(
                        scheduler[
                            "job_id"
                        ]
                    )


                    if job_id in job_ids:

                        errors.append(

                            (
                                f"duplicate job_id: "
                                f"{job_id}"
                            )
                        )


                    job_ids.add(
                        job_id
                    )


                except Exception as exc:

                    errors.append(

                        (
                            f"{case_dir.name}: "
                            f"invalid scheduler.json: "
                            f"{exc}"
                        )
                    )


        return errors