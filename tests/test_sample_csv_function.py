import logging
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from sample_csv_function import main
from sample_csv_function.example import read_csv_to_dicts
from shared_code.sample_csv_helper_function import read_csv_str_to_dicts

BUNDLED_CSV = Path(__file__).parents[1] / "sample_csv_function" / "jason_statham.csv"


def test_bundled_csv():
    rows = read_csv_to_dicts(BUNDLED_CSV)
    assert len(rows) == 3
    assert all(list(row) == ["year", "title", "role", "notes"] for row in rows)
    assert rows[1]["title"] == "The Transporter"


def test_quoted_newline_is_kept():
    assert read_csv_str_to_dicts('a,b\n"x\ny",z\n') == [{"a": "x\ny", "b": "z"}]


@pytest.mark.parametrize(
    ("csv_str", "expected"),
    [
        ("a,b\n\n1,2\n\n", [{"a": "1", "b": "2"}]),  # 空行は飛ばす
        ("a,b\r1,2\r", [{"a": "1", "b": "2"}]),  # CR だけの改行
        ("a,b,c\n1,2,\n", [{"a": "1", "b": "2", "c": ""}]),  # 末尾の空の列
        ("\n\na,b\n1,2\n", [{"a": "1", "b": "2"}]),  # ヘッダの前の空行
    ],
)
def test_parse(csv_str, expected):
    assert read_csv_str_to_dicts(csv_str) == expected


@pytest.mark.parametrize("csv_str", ["a,b\n1,2,3\n", "a,b\n1\n"])
def test_column_count_mismatch(csv_str):
    with pytest.raises(ValueError, match="line 2"):
        read_csv_str_to_dicts(csv_str)


@pytest.mark.parametrize(
    ("csv_str", "message"),
    [
        ("a,a\n1,2\n", "line 1: duplicate header: 'a'"),
        ("a,b,a\n", "line 1: duplicate header: 'a'"),
        ("a,,\n1,2,3\n", "line 1: duplicate header: ''"),  # 空の名前も見えるように
        ("\na,a\n", "line 2: duplicate header: 'a'"),  # 空行を数えた行番号
    ],
)
def test_duplicate_header(csv_str, message):
    with pytest.raises(ValueError, match=f"^{re.escape(message)}$"):
        read_csv_str_to_dicts(csv_str)


@pytest.mark.parametrize("csv_str", ["", "\n\n", "a,b\n"])
def test_no_data_rows(csv_str):
    assert read_csv_str_to_dicts(csv_str) == []


def test_bom_is_stripped(tmp_path):
    path = tmp_path / "bom.csv"
    path.write_text("\ufeffa,b\r\n1,2\r\n", encoding="utf-8", newline="")
    assert read_csv_to_dicts(path) == [{"a": "1", "b": "2"}]


def test_main_logs_rows_from_any_cwd(tmp_path, monkeypatch, caplog):
    monkeypatch.chdir(tmp_path)
    caplog.set_level(logging.INFO)
    main(SimpleNamespace(past_due=False))
    assert "Loaded 3 rows" in caplog.text
    assert "The Transporter" in caplog.text
