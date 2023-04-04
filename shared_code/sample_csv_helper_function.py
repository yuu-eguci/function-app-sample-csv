import csv
from typing import List, Dict


def read_csv_str_to_dicts(csv_str: str) -> List[Dict[str, str]]:
    if not csv_str:
        return []
    rows = csv.reader(csv_str.splitlines())
    header, *data = rows
    if not data:
        return []
    return [
        {header[i]: value for i, value in enumerate(row)}
        for row in data
    ]
