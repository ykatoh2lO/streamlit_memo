import streamlit as st

from src.sudoku import SudokuSolver
from gui.sudoku import initialize, load_csv, clicked, solve
from gui.utils import calc_width, calc_height

# タイトル
st.set_page_config(layout='wide')
st.session_state.update(st.session_state)
initialize(__file__)

# 枠組み・中身
col_input, col_table = st.columns([2, 4])

with col_input:
    sudoku_csv_file = st.file_uploader('問題 CSV のアップロード', type='csv', label_visibility='collapsed')
    if sudoku_csv_file:
        load_csv(sudoku_csv_file)

col_table.data_editor(
    st.session_state.sudoku_df,
    width=calc_width(st.session_state.sudoku_df), height=calc_height(st.session_state.sudoku_df),
    # https://github.com/streamlit/streamlit/issues/9570#issuecomment-2383654477
    column_config={'_index': st.column_config.Column(disabled=True)} | {
            col: st.column_config.NumberColumn(default=0, min_value=1, max_value=9, step=1)
            for col in st.session_state.sudoku_df})


# 青ボタン
if col_input.button('解く', type='primary', disabled=st.session_state.sudoku_invalid, on_click=clicked):
    solve()
    st.rerun()

if st.session_state.sudoku_result is not None:
    result = st.session_state.sudoku_result
    if result.status == 'Optimal':
        col_input.success(result.status, icon=':material/info:')
    else:
        col_input.error(str(result), icon=':material/error:')
