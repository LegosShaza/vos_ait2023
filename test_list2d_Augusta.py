import unittest
from list_2D_manipulator import (
    sort_by_col,
    col_names_from_firts_row,
    deflatten_list_2D,
    replace_values_in_col_by_dict
)

# ============================================
#  TESTY FUNKCÍ ZE SOUBORU list_2D_manipulator.py
#  Autor: Daniel Augusta
#  VOŠ AIT 2023 – druhá lekce programování
# ============================================


# -------------------------------------------------
# Testy pro funkci sort_by_col
# -------------------------------------------------
# Funkce třídí dvourozměrný seznam podle zvoleného sloupce (indexem, ne názvem).
# Testy ověřují správné seřazení číselných i textových dat.
class TestSortByCol(unittest.TestCase):
    def test_sort_numeric_column(self):
        # Data s hlavičkou a čísly ve 2. sloupci
        data = [
            ["jméno", "věk"],
            ["Petr", 25],
            ["Jana", 19],
            ["Karel", 30]
        ]
        # Třídíme podle indexu 1 (věk)
        result = sort_by_col(data[1:], 1)
        expected = [
            ["Jana", 19],
            ["Petr", 25],
            ["Karel", 30]
        ]
        self.assertEqual(result, expected)

    def test_sort_text_column(self):
        # Test třídění podle textu v prvním sloupci
        data = [
            ["jméno", "věk"],
            ["Karel", 30],
            ["Jana", 19],
            ["Petr", 25]
        ]
        result = sort_by_col(data[1:], 0)
        expected = [
            ["Jana", 19],
            ["Karel", 30],
            ["Petr", 25]
        ]
        self.assertEqual(result, expected)


# -------------------------------------------------
# Testy pro funkci col_names_from_firts_row
# -------------------------------------------------
# Funkce bere první řádek jako hlavičku,
# ověřuje jeho správnost a odstraňuje ho z dat.
class TestColNamesFromFirstRow(unittest.TestCase):
    def test_extract_headers(self):
        # Vstupní data s hlavičkou
        data = [
            ["jméno", "věk", "město"],
            ["Petr", 25, "Praha"],
            ["Jana", 30, "Brno"]
        ]
        # Funkce vrací trojici (data_bez_hlavičky, hlavička, počet_smazaných_řádků)
        new_data, headers, count = col_names_from_firts_row(data)
        self.assertEqual(headers, ["jméno", "věk", "město"])
        self.assertEqual(count, 1)
        # Ověření, že hlavička byla odstraněna
        self.assertEqual(new_data, [["Petr", 25, "Praha"], ["Jana", 30, "Brno"]])

    def test_empty_input_raises(self):
        # Při prázdném vstupu má být vyhozena chyba
        with self.assertRaises(ValueError):
            col_names_from_firts_row([])


# -------------------------------------------------
# Testy pro funkci deflatten_list_2D
# -------------------------------------------------
# Funkce převádí jednorozměrný seznam na 2D seznam,
# kde každý prvek je samostatný vnořený list.
class TestDeflattenList2D(unittest.TestCase):
    def test_basic_deflatten(self):
        flat = ["a", "b", "c"]
        result = deflatten_list_2D(flat)
        expected = [["a"], ["b"], ["c"]]
        self.assertEqual(result, expected)

    def test_empty_input(self):
        # Při prázdném vstupu očekáváme prázdný seznam
        result = deflatten_list_2D([])
        self.assertEqual(result, [])


# -------------------------------------------------
# Testy pro funkci replace_values_in_col_by_dict
# -------------------------------------------------
# Funkce nahrazuje hodnoty ve vybraném sloupci
# podle předaného slovníku (replikačního mapování).
class TestReplaceValuesInColByDict(unittest.TestCase):
    def test_replace_values(self):
        # Vstupní data, kde sloupec 1 obsahuje zkratky pohlaví
        data = [
            ["Petr", "M"],
            ["Jana", "F"],
            ["Karel", "M"]
        ]
        repl = {"M": "muž", "F": "žena"}
        result = replace_values_in_col_by_dict(data, 1, repl)
        expected = [
            ["Petr", "muž"],
            ["Jana", "žena"],
            ["Karel", "muž"]
        ]
        self.assertEqual(result, expected)

    def test_unknown_value_unchanged(self):
        # Hodnoty, které nejsou ve slovníku, zůstanou beze změny
        data = [
            ["Petr", "A"],
            ["Jana", "B"]
        ]
        repl = {"B": "aktivní"}
        result = replace_values_in_col_by_dict(data, 1, repl)
        expected = [
            ["Petr", "A"],
            ["Jana", "aktivní"]
        ]
        self.assertEqual(result, expected)


# Spuštění všech testů
if __name__ == "__main__":
    unittest.main()
