import csv
import io


def read_csv_str_to_dicts(csv_str: str) -> list[dict[str, str]]:
    """CSV 文字列を、ヘッダ行をキーにした dict のリストにする。空行は飛ばす。"""
    reader = csv.DictReader(io.StringIO(csv_str, newline=""))
    rows = []
    for row in reader:
        # 列が多いと余りがキー None に、少ないと足りない列の値が None になる
        if None in row or None in row.values():
            raise ValueError(
                f"line {reader.line_num}: column count does not match header"
            )
        rows.append(row)
    return rows
