from pathlib import Path

from shared_code.sample_csv_helper_function import read_csv_str_to_dicts

# cwd に依存しないよう、このファイルの隣を指す
CSV_PATH = Path(__file__).with_name("jason_statham.csv")


def read_csv_to_dicts(csv_path: str | Path) -> list[dict[str, str]]:
    # utf-8-sig: BOM があれば取る。newline="": クォート内の改行をそのまま csv に渡す
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        return read_csv_str_to_dicts(f.read())
