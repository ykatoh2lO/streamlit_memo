import sys
import unittest
from pathlib import Path

from src.sudoku import SudokuSolver


class TestSudoku(unittest.TestCase):
    """ 正しい数値になっているか確認 """
    home_dir = Path(sys.argv[0]).parent.absolute()

    def test_ok(self):
        sudoku_solver = SudokuSolver(self.home_dir / 'sample_data' / 'sudoku_ok.csv')
        self.assertTrue(sudoku_solver.check_duplicates()[0])

        sudoku_solver.build_model()
        sudoku_solver.solve()

        ans_df = SudokuSolver.read_problem(self.home_dir / 'sample_data' / 'sudoku_ans.csv')
        self.assertTrue(ans_df.equals(sudoku_solver.result.df))

    def test_ng(self):
        sudoku_solver = SudokuSolver(self.home_dir / 'sample_data' / 'sudoku_ng.csv')
        self.assertFalse(sudoku_solver.check_duplicates()[0])
