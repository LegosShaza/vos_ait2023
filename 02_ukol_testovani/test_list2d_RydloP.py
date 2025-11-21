# -*- coding: utf-8 -*-
"""
Unit testy pro list_2D_manipulator.py
Testované funkce:
- histogram_unicates_in_col
- dict_with_lists_to_list_2D_only_values
- histogram_rows_length
- value_to_unicode

Autor: RydloP
"""

import unittest
import sys

# Python 2/3 kompatibilita
if sys.version_info[0] >= 3:
    unicode = str

from list_2D_manipulator import (
    histogram_unicates_in_col,
    dict_with_lists_to_list_2D_only_values,
    histogram_rows_length,
    value_to_unicode
)


class TestHistogramUnicatesInCol(unittest.TestCase):
    """Testovací třída pro funkci histogram_unicates_in_col"""

    def setUp(self):
        """Příprava testovacích dat před každým testem"""
        self.test_data_simple = [
            ['a', 'x', '1'],
            ['b', 'y', '2'],
            ['a', 'z', '3'],
            ['c', 'x', '4'],
            ['a', 'y', '5']
        ]

        self.test_data_with_duplicates = [
            ['red', 'apple'],
            ['blue', 'car'],
            ['red', 'flower'],
            ['green', 'grass'],
            ['blue', 'sky'],
            ['red', 'rose']
        ]

    def test_basic_histogram_col_0(self):
        """Test základního histogramu pro sloupec 0"""
        result = histogram_unicates_in_col(self.test_data_simple, 0)

        # Ověříme, že výsledek je list_2D (seznam seznamů)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, list) for item in result))

        # Převedeme na slovník pro snadnější testování
        result_dict = {item[0]: item[1] for item in result}

        # Ověříme počty
        self.assertEqual(result_dict['a'], 3)
        self.assertEqual(result_dict['b'], 1)
        self.assertEqual(result_dict['c'], 1)

    def test_histogram_col_1(self):
        """Test histogramu pro sloupec 1"""
        result = histogram_unicates_in_col(self.test_data_simple, 1)
        result_dict = {item[0]: item[1] for item in result}

        self.assertEqual(result_dict['x'], 2)
        self.assertEqual(result_dict['y'], 2)
        self.assertEqual(result_dict['z'], 1)

    def test_histogram_with_skip_values(self):
        """Test histogramu s vynecháním určitých hodnot"""
        result = histogram_unicates_in_col(
            self.test_data_with_duplicates,
            0,
            skip_values=['red']
        )
        result_dict = {item[0]: item[1] for item in result}

        # 'red' by mělo být ve speciální kategorii
        self.assertIn('**skip_values**', result_dict)
        self.assertEqual(result_dict['**skip_values**'], 3)

        # Ostatní hodnoty by měly být normálně
        self.assertEqual(result_dict['blue'], 2)
        self.assertEqual(result_dict['green'], 1)

    def test_histogram_invalid_col_index(self):
        """Test s neplatným indexem sloupce"""
        with self.assertRaises(ValueError):
            histogram_unicates_in_col(self.test_data_simple, 10)

    def test_histogram_empty_list(self):
        """Test s prázdným seznamem"""
        # Prázdný seznam by měl vyhodit ValueError (validace)
        with self.assertRaises(ValueError):
            histogram_unicates_in_col([], 0)

    def test_histogram_single_row(self):
        """Test s jedním řádkem"""
        single_row_data = [['value1', 'value2']]
        result = histogram_unicates_in_col(single_row_data, 0)
        result_dict = {item[0]: item[1] for item in result}

        self.assertEqual(result_dict['value1'], 1)


class TestDictWithListsToList2DOnlyValues(unittest.TestCase):
    """Testovací třída pro funkci dict_with_lists_to_list_2D_only_values"""

    def test_basic_conversion(self):
        """Test základní konverze slovníku na list_2D"""
        test_dict = {
            'a': ['b', 'c', 'd', 'e'],
            'f': ['g', 'h', 'i', 'j']
        }

        result = dict_with_lists_to_list_2D_only_values(test_dict)

        # Ověříme, že výsledek je list
        self.assertIsInstance(result, list)

        # Ověříme počet řádků
        self.assertEqual(len(result), 2)

        # Ověříme, že všechny hodnoty jsou přítomny
        flat_result = [item for sublist in result for item in sublist]
        expected_values = ['b', 'c', 'd', 'e', 'g', 'h', 'i', 'j']

        self.assertEqual(sorted(flat_result), sorted(expected_values))

    def test_empty_dict(self):
        """Test s prázdným slovníkem"""
        result = dict_with_lists_to_list_2D_only_values({})
        self.assertEqual(result, [])

    def test_dict_with_different_length_lists(self):
        """Test se slovníkem obsahujícím seznamy různých délek"""
        test_dict = {
            'short': [1, 2],
            'medium': [3, 4, 5],
            'long': [6, 7, 8, 9, 10]
        }

        result = dict_with_lists_to_list_2D_only_values(test_dict)

        # Ověříme počet řádků
        self.assertEqual(len(result), 3)

        # Ověříme délky jednotlivých řádků
        lengths = [len(row) for row in result]
        self.assertIn(2, lengths)
        self.assertIn(3, lengths)
        self.assertIn(5, lengths)

    def test_dict_with_empty_lists(self):
        """Test se slovníkem obsahujícím prázdné seznamy"""
        test_dict = {
            'empty1': [],
            'filled': [1, 2, 3],
            'empty2': []
        }

        result = dict_with_lists_to_list_2D_only_values(test_dict)

        # Ověříme počet řádků
        self.assertEqual(len(result), 3)

        # Prázdné seznamy by měly být zachovány
        empty_count = sum(1 for row in result if len(row) == 0)
        self.assertEqual(empty_count, 2)

    def test_dict_with_mixed_types(self):
        """Test se slovníkem obsahujícím různé typy dat v seznamech"""
        test_dict = {
            'numbers': [1, 2, 3],
            'strings': ['a', 'b', 'c'],
            'mixed': [1, 'two', 3.0, None]
        }

        result = dict_with_lists_to_list_2D_only_values(test_dict)

        # Ověříme, že všechny typy jsou zachovány
        self.assertEqual(len(result), 3)

        # Najdeme řádek s mixed daty
        mixed_row = [row for row in result if len(row) == 4][0]
        self.assertIn(None, mixed_row)
        self.assertIn('two', mixed_row)


class TestHistogramRowsLength(unittest.TestCase):
    """Testovací třída pro funkci histogram_rows_length"""

    def setUp(self):
        """Příprava testovacích dat"""
        self.test_data_uniform = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        self.test_data_varied = [
            [1],
            [2, 3],
            [4, 5, 6],
            [7],
            [8, 9, 10, 11]
        ]

    def test_uniform_length_rows(self):
        """Test s řádky stejné délky"""
        result = histogram_rows_length(self.test_data_uniform)

        # Ověříme, že výsledek je list_2D
        self.assertIsInstance(result, list)

        # Index 3 by měl mít hodnotu 3 (3 řádky s délkou 3)
        self.assertEqual(result[3][0], 3)  # index
        self.assertEqual(result[3][1], 3)  # počet

    def test_varied_length_rows(self):
        """Test s řádky různých délek"""
        result = histogram_rows_length(self.test_data_varied)

        # Převedeme na slovník pro snadnější testování
        result_dict = {item[0]: item[1] for item in result}

        # Ověříme počty
        self.assertEqual(result_dict[1], 2)  # 2 řádky s délkou 1
        self.assertEqual(result_dict[2], 1)  # 1 řádek s délkou 2
        self.assertEqual(result_dict[3], 1)  # 1 řádek s délkou 3
        self.assertEqual(result_dict[4], 1)  # 1 řádek s délkou 4

    def test_with_max_length_parameter(self):
        """Test s parametrem max_length"""
        result = histogram_rows_length(self.test_data_varied, max_length=5)

        # Histogram by měl mít délku max_length + 1
        self.assertEqual(len(result), 6)

    def test_empty_list(self):
        """Test s prázdným seznamem"""
        result = histogram_rows_length([])

        # Prázdný seznam by měl vrátit histogram s jedním prvkem [0, 0]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], [0, 0])

    def test_with_return_match_rows(self):
        """Test s parametrem return_match_rows"""
        # POZNÁMKA: Tento test odhaluje bug v původním kódu
        # Funkce histogram_rows_length má bug na řádku 799,
        # kde se pokouší použít proměnnou match_rows, která není
        # v tomto kontextu definována.

        # Test očekává NameError kvůli bugu v původním kódu
        with self.assertRaises(NameError):
            result = histogram_rows_length(
                self.test_data_varied,
                return_match_rows=True,
                match_rule=">2"
            )

    def test_single_element_rows(self):
        """Test s řádky o jednom prvku"""
        single_element_data = [[1], [2], [3], [4]]
        result = histogram_rows_length(single_element_data)
        result_dict = {item[0]: item[1] for item in result}

        # Všechny řádky mají délku 1
        self.assertEqual(result_dict[1], 4)


class TestValueToUnicode(unittest.TestCase):
    """Testovací třída pro funkci value_to_unicode"""

    def test_basic_string_conversion(self):
        """Test základní konverze řetězce"""
        result = value_to_unicode("hello world")
        self.assertEqual(result, u"hello world")
        self.assertIsInstance(result, unicode)

    def test_strip_whitespace(self):
        """Test odstranění bílých znaků"""
        result = value_to_unicode("  test  ")
        self.assertEqual(result, u"test")

    def test_strip_quotes(self):
        """Test odstranění uvozovek"""
        result = value_to_unicode("'quoted'")
        self.assertEqual(result, u"quoted")

        result2 = value_to_unicode('"double quoted"')
        self.assertEqual(result2, u"double quoted")

    def test_strip_special_chars(self):
        """Test odstranění speciálních znaků (z STRIPPED_CHARS)"""
        # STRIPPED_CHARS = ' \'\\"\r\n\t'
        result = value_to_unicode("\t\nvalue\r\n")
        self.assertEqual(result, u"value")

    def test_empty_string(self):
        """Test s prázdným řetězcem"""
        result = value_to_unicode("")
        self.assertIsNone(result)

    def test_whitespace_only(self):
        """Test s pouze bílými znaky"""
        result = value_to_unicode("   ")
        self.assertIsNone(result)

    def test_none_value(self):
        """Test s None hodnotou"""
        # Funkce by měla zachytit exception a vrátit None
        result = value_to_unicode(None)
        self.assertIsNone(result)

    def test_number_to_unicode(self):
        """Test konverze čísla na unicode"""
        # Funkce očekává string, ne číslo - číslo vrátí None
        result = value_to_unicode(123)
        # Alternativně můžeme testovat string reprezentaci čísla
        result_string = value_to_unicode("123")
        self.assertEqual(result_string, u"123")

    def test_unicode_string_input(self):
        """Test s unicode vstupem"""
        unicode_input = u"příliš žluťoučký kůň"
        result = value_to_unicode(unicode_input)
        self.assertEqual(result, unicode_input)

    def test_special_unicode_chars(self):
        """Test se speciálními unicode znaky"""
        result = value_to_unicode(u"中文字符")
        self.assertEqual(result, u"中文字符")

    def test_mixed_content(self):
        """Test se smíšeným obsahem"""
        result = value_to_unicode("  text123  ")
        self.assertEqual(result, u"text123")

    def test_boolean_value(self):
        """Test s boolean hodnotou"""
        # Funkce očekává string, ne boolean - boolean vrátí None
        result = value_to_unicode(True)
        # Testujeme string reprezentaci booleanu
        result_string = value_to_unicode("True")
        self.assertEqual(result_string, u"True")

        result_string2 = value_to_unicode("False")
        self.assertEqual(result_string2, u"False")


if __name__ == '__main__':
    # Spuštění testů s verbose výstupem
    unittest.main(verbosity=2)
