# test_list2d_Smid.py
# Autor: Tomáš Šmíd
# Testy pro funkce z list_2D_manipulator.py

import unittest
from list_2D_manipulator import (
    replace_values_in_col_by_dict_values_in_other_col,
    value_to_int,
    dict_with_lists_to_list_2D,
    two_columns_to_dict_of_list
)


# ------------------------------------------------------
class TestReplaceValuesInColByDictValuesInOtherCol(unittest.TestCase):
    """Testy pro funkci replace_values_in_col_by_dict_values_in_other_col"""

    def test_basic_replacement(self):
        data = [
            ["A", "x"],
            ["B", "y"],
            ["C", "z"]
        ]
        repl = {"x": "X1", "y": "Y1"}
        result = replace_values_in_col_by_dict_values_in_other_col(
            data, col_set=0, col_test=1, repl_dict=repl
        )
        self.assertEqual(result, [["X1", "x"], ["Y1", "y"], ["C", "z"]])

    def test_expression_evaluation(self):
        data = [["num", "calc"], ["a", "math"]]
        repl = {"calc": "=str(5 + 5)", "math": "=str(len('abc'))"}
        result = replace_values_in_col_by_dict_values_in_other_col(
            data, col_set=0, col_test=1, repl_dict=repl
        )
        self.assertEqual(result, [["10", "calc"], ["3", "math"]])

    def test_skip_missing_keys(self):
        data = [["v1", "ok"], ["v2", "nope"]]
        repl = {"ok": "OK"}
        result = replace_values_in_col_by_dict_values_in_other_col(data, 0, 1, repl)
        self.assertEqual(result, [["OK", "ok"], ["v2", "nope"]])


# ------------------------------------------------------
class TestValueToInt(unittest.TestCase):
    """Testy pro value_to_int"""

    def test_valid_integers(self):
        self.assertEqual(value_to_int("42"), 42)
        self.assertEqual(value_to_int(10), 10)

    def test_invalid_values(self):
        self.assertIsNone(value_to_int("abc"))
        self.assertIsNone(value_to_int(None))
        self.assertIsNone(value_to_int(""))

    def test_negative_numbers(self):
        self.assertEqual(value_to_int("-5"), -5)


# ------------------------------------------------------
class TestDictWithListsToList2D(unittest.TestCase):
    """Testy pro dict_with_lists_to_list_2D"""

    def test_basic_conversion(self):
        data = {"a": [1, 2], "b": [3]}
        expected = [["a", 1], ["a", 2], ["b", 3]]
        self.assertEqual(dict_with_lists_to_list_2D(data), expected)

    def test_empty_dict(self):
        self.assertEqual(dict_with_lists_to_list_2D({}), [])


# ------------------------------------------------------
class TestTwoColumnsToDictOfList(unittest.TestCase):
    """Testy pro two_columns_to_dict_of_list"""

    def test_basic(self):
        data = [
            ["a", 1],
            ["a", 2],
            ["b", 3]
        ]
        expected = {"a": [1, 2], "b": [3]}
        self.assertEqual(two_columns_to_dict_of_list(data, 0, 1), expected)

    def test_single_row(self):
        data = [["key", "val"]]
        self.assertEqual(two_columns_to_dict_of_list(data, 0, 1), {"key": ["val"]})

    def test_empty_input(self):
        self.assertEqual(two_columns_to_dict_of_list([], 0, 1), {})


# ------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
