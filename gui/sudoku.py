from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from src.sudoku import SudokuSolver
from gui.utils import set_title_navi


def initialize(current_filename):
    set_title_navi(current_filename)
    if 'sudoku_problem' not in st.session_state:
        st.session_state.sudoku_invalid = True
        st.session_state.sudoku_result = None
        st.session_state.sudoku_df = SudokuSolver.read_problem()

def clicked():
    st.session_state.sudoku_invalid = True

def solve():
    sudoku_solver = SudokuSolver(st.session_state.sudoku_df)
    sudoku_solver.build_model()
    sudoku_solver.solve()
    st.session_state.sudoku_result = sudoku_solver.result
    st.session_state.sudoku_df = sudoku_solver.result.df
    st.session_state.sudoku_invalid = False


def load_csv(sudoku_csv_file):
    with NamedTemporaryFile(delete=False) as tmp_file:
        fp = Path(tmp_file.name)
        fp.write_bytes(sudoku_csv_file.getvalue())
        st.session_state.sudoku_df = SudokuSolver.read_problem(tmp_file.name)

    ok_flg, error_sudoku_df = SudokuSolver.check_duplicates(st.session_state.sudoku_df)
    if ok_flg:
        st.session_state.sudoku_invalid = False
    else:
        st.session_state.sudoku_invalid = True
        st.error('次の値が重複しています．', icon=':material/error:')
        st.dataframe(error_sudoku_df, hide_index=True)
