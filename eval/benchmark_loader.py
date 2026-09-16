import json

from pathlib import Path


class BenchmarkLoader:

    def __init__(
        self,
        benchmark_root: Path
    ):
        self.benchmark_root = benchmark_root


    # ========================================================
    # List Cases
    # ========================================================

    def list_cases(
        self
    ) -> list[Path]:

        return sorted(

            self.benchmark_root.glob(
                "case_*"
            )
        )


    # ========================================================
    # Load Ground Truth
    #
    # 只允许 Eval 使用。
    # Agent Runtime 不应该调用它。
    # ========================================================

    def load_ground_truth(
        self,
        case_dir: Path
    ) -> dict:

        path = (
            case_dir
            / "ground_truth.json"
        )


        if not path.exists():

            raise FileNotFoundError(
                f"Missing ground truth: {path}"
            )


        return json.loads(

            path.read_text(
                encoding="utf-8"
            )
        )


    # ========================================================
    # Load All Ground Truth
    # ========================================================

    def load_all(
        self
    ) -> list[dict]:

        results = []


        for case_dir in (
            self.list_cases()
        ):

            results.append(

                self.load_ground_truth(
                    case_dir
                )
            )


        return results