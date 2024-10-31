import streamlit as st

from src.kaonavi import read_md_file, dump_md_file
from src.utils import get_fiscal_year, get_yyyymmdd


def show_page():
    # 枠組み，読込ボタン
    col_input_button, col_output_button = st.columns([5, 5], vertical_alignment='center')
    kaonavi_md_file = col_input_button.file_uploader(
        '過去に記入したファイルを読み込む', type=['md'], label_visibility='collapsed')

    # メイン: 編集
    lst_section = read_md_file(kaonavi_md_file)
    # print(lst_section)
    tabs = st.tabs([section.caption for section in lst_section])

    for i, section in enumerate(lst_section):
        section_name = f'section{i}'
        if section_name not in st.session_state:
            st.session_state[section_name] = section.answer_before

        with tabs[i]:
            st.info(section.info)
            height = 150

            col_before, col_after = st.empty(), st.empty()
            with col_before:
                st.text_area(
                    f'{section_name}_before', value=section.answer_before,
                    height=height, max_chars=section.maxchar,
                    disabled=True, label_visibility='collapsed')
            with col_after:
                st.text_area(
                    section_name,
                    height=height, max_chars=section.maxchar,
                    key=section_name, label_visibility='collapsed')
                section.answer_after = st.session_state[section_name]

    # 保存ボタン
    col_output_button.download_button(
        '今回記入したファイルを書き出す',
        dump_md_file(f'{get_fiscal_year()} 年度キャリア面談シート', lst_section),
        f'{get_yyyymmdd()}.md',
        'text/markdown')
