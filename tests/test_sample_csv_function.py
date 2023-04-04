import unittest
from shared_code.sample_csv_helper_function import read_csv_str_to_dicts


class TestReadCsvStrToDicts(unittest.TestCase):
    def test_empty_str(self):
        self.assertEqual(read_csv_str_to_dicts(""), [])

    def test_header_only(self):
        self.assertEqual(read_csv_str_to_dicts("year,title,role,notes"), [])

    def test_normal(self):
        csv_str = """\
year,title,role,notes
1998,Lock Stock and Two Smoking Barrels,Bacon,
2004,Collateral,Frank Martin,Cameo credited as Airport Man
"""
        expected = [
            {
                "year": "1998",
                "title": "Lock Stock and Two Smoking Barrels",
                "role": "Bacon",
                "notes": ""
            },
            {
                "year": "2004",
                "title": "Collateral",
                "role": "Frank Martin",
                "notes": "Cameo credited as Airport Man"
            }
        ]
        self.assertEqual(read_csv_str_to_dicts(csv_str), expected)
