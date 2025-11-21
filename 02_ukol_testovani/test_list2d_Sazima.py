import unittest
from list_2D_manipulator import (
    two_columns_to_dict,
    replace_values_in_cols,
    indexes_of_values_as_dict,
    col_name_to_index
)

class TestTwoColumnsToDict(unittest.TestCase):
    def test_basic_conversion(self):
        data = [
            ["key1", "value1"],
            ["key2", "value2"],
            ["key3", "value3"]
        ]
        result = two_columns_to_dict(data, 0, 1)
        expected = {"key1": "value1", "key2": "value2", "key3": "value3"}
        self.assertEqual(result, expected)

    def test_non_first_columns(self):
        data = [
            ["id", "name", "city"],
            [1, "Alice", "Brno"],
            [2, "Bob", "Praha"],
            [3, "Charlie", "Ostrava"]
        ]
        result = two_columns_to_dict(data[1:], 1, 2)
        expected = {"Alice": "Brno", "Bob": "Praha", "Charlie": "Ostrava"}
        self.assertEqual(result, expected)

    def test_empty_list(self):
        result = two_columns_to_dict([], 0, 1)
        self.assertEqual(result, {})


class TestReplaceValuesInCols(unittest.TestCase):
    def test_basic_replacement(self):
        data = [
            ["Ahoj", "svete"],
            ["Python", "je super"]
        ]
        result = replace_values_in_cols(data, [0, 1], "e", "E")
        expected = [
            ["Ahoj", "svEtE"],
            ["Python", "jE supEr"]
        ]
        self.assertEqual(result, expected)

    def test_replace_all_columns(self):
        data = [["abc", "def"], ["ghi", "jkl"]]
        result = replace_values_in_cols(data, "ALL", "a", "A")
        expected = [["Abc", "def"], ["ghi", "jkl"]]
        self.assertEqual(result, expected)

    def test_skip_bad_length(self):
        data = [["A", "B"], ["C"]]  # druhý řádek má méně sloupců
        result = replace_values_in_cols(data, [1], "B", "Beta", skip_bad_length=True)
        expected = [["A", "Beta"], ["C"]]
        self.assertEqual(result, expected)


class TestIndexesOfValuesAsDict(unittest.TestCase):
    def test_valid_headers(self):
        data = [["Name", "Age", "City"], ["Alice", 25, "Brno"]]
        result = indexes_of_values_as_dict(data, 0, ["Name", "City"])
        expected = {"Name": 0, "City": 2}
        self.assertEqual(result, expected)

    def test_header_not_found_raises(self):
        data = [["A", "B", "C"], [1, 2, 3]]
        with self.assertRaises(ValueError):
            indexes_of_values_as_dict(data, 0, ["X", "B"])

    def test_no_raise_error_returns_partial(self):
        data = [["A", "B", "C"], [1, 2, 3]]
        result = indexes_of_values_as_dict(data, 0, ["A", "Z"], raise_error=False)
        expected = {"A": 0}
        self.assertEqual(result, expected)


class TestColNameToIndex(unittest.TestCase):
    def test_unique_header(self):
        headers = ["id", "name", "age"]
        result = col_name_to_index(headers, "name")
        self.assertEqual(result, 1)

    def test_header_not_found(self):
        headers = ["id", "name", "age"]
        result = col_name_to_index(headers, "city")
        self.assertIsNone(result)

    def test_duplicate_header_allowed(self):
        headers = ["id", "name", "name", "age"]
        result = col_name_to_index(headers, "name", allow_duplicities=True)
        self.assertEqual(result, 1)

    def test_duplicate_header_not_allowed(self):
        headers = ["id", "name", "name", "age"]
        result = col_name_to_index(headers, "name", allow_duplicities=False)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
