import csv
import io


def read_csv_str_to_dicts(csv_str: str) -> list[dict[str, str]]:
    """CSV 文字列を、ヘッダ行をキーにした dict のリストにする。空行は飛ばす。

    ヘッダは最初の空でない行。ヘッダ名の重複と、列数がヘッダと合わない行は ValueError。
    """
    reader = csv.reader(io.StringIO(csv_str, newline=""))
    header = next((row for row in reader if row), [])
    # 重複したヘッダ名は dict にすると後の列で上書きされて値が消えるので、エラーにする
    duplicates = sorted({name for name in header if header.count(name) > 1})
    if duplicates:
        # repr にして空の名前も見えるようにする
        shown = ", ".join(map(repr, duplicates))
        raise ValueError(f"line {reader.line_num}: duplicate header: {shown}")
    rows = []
    for row in reader:
        if not row:
            continue
        if len(row) != len(header):
            raise ValueError(
                f"line {reader.line_num}: column count does not match header"
            )
        rows.append(dict(zip(header, row, strict=True)))
    return rows
