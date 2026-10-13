import csv
import io


def read_csv_str_to_dicts(csv_str: str) -> list[dict[str, str]]:
    """CSV 文字列を、ヘッダ行をキーにした dict のリストにする。空行は飛ばす。

    ヘッダは最初の空でない行。ヘッダ名の重複と、列数がヘッダと合わない行は ValueError。
    """
    reader = csv.DictReader(io.StringIO(csv_str, newline=""))
    # DictReader は最初の行をそのままヘッダにするので、空行なら次の行を読む
    while reader.fieldnames == []:
        reader.fieldnames = next(reader.reader, None)
    # 重複したヘッダ名は後の列で上書きされて値が消えるので、エラーにする
    names = reader.fieldnames or []
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        # repr にして空の名前も見えるようにする
        shown = ", ".join(map(repr, duplicates))
        raise ValueError(f"line {reader.line_num}: duplicate header: {shown}")
    rows = []
    for row in reader:
        # 列が多いと余りがキー None に、少ないと足りない列の値が None になる
        if None in row or None in row.values():
            raise ValueError(
                f"line {reader.line_num}: column count does not match header"
            )
        rows.append(row)
    return rows
