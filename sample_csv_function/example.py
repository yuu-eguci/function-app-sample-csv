from typing import List, Dict
from shared_code.sample_csv_helper_function import read_csv_str_to_dicts


def read_csv_to_dicts(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, 'r') as f:
        csv_str = f.read()
    return read_csv_str_to_dicts(csv_str)
