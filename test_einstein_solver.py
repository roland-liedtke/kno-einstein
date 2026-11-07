"""Testy solvera Zagadki Einsteina (uruchomienie: python -m unittest)."""

import unittest

from einstein_solver import CATEGORIES, HOUSES, build_problem, invert, terminal_table


class SolverTest(unittest.TestCase):
    def setUp(self):
        self.solutions = build_problem().getSolutions()

    def test_unique_solution(self):
        self.assertEqual(len(self.solutions), 1)

    def test_german_keeps_fish(self):
        matrix = invert(self.solutions[0])
        self.assertEqual(matrix[4]["Narodowość"], "Niemiec")
        self.assertEqual(matrix[4]["Zwierzę"], "Rybki")


class TerminalTableTest(unittest.TestCase):
    def setUp(self):
        self.lines = terminal_table(invert(build_problem().getSolutions()[0])).splitlines()

    def test_layout(self):
        # ramka górna, nagłówek, separator, 5 wierszy domów, ramka dolna
        self.assertEqual(len(self.lines), 3 + len(HOUSES) + 1)
        self.assertTrue(self.lines[0].startswith("┌"))
        self.assertTrue(self.lines[2].startswith("├"))
        self.assertTrue(self.lines[-1].startswith("└"))

    def test_all_lines_have_equal_width(self):
        self.assertEqual(len({len(line) for line in self.lines}), 1)

    def test_column_separators_aligned(self):
        # pozycje znaków │ w każdym wierszu treści są takie same jak ┬ w ramce
        top = [i for i, ch in enumerate(self.lines[0]) if ch == "┬"]
        for line in self.lines[3:-1]:
            inner = [i for i, ch in enumerate(line) if ch == "│"][1:-1]
            self.assertEqual(inner, top)

    def test_header_and_values_present(self):
        self.assertIn("Dom", self.lines[1])
        for category in CATEGORIES:
            self.assertIn(category, self.lines[1])
        self.assertIn("Philip Morris", "\n".join(self.lines))


if __name__ == "__main__":
    unittest.main()
