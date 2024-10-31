import streamlit as st

from gui.kaonavi import show_page
from gui.utils import basic_auth, set_title_navi

# 初期化・サイドバー
st.set_page_config(layout='wide')
st.session_state.update(st.session_state)
set_title_navi(__file__)

# 枠組み・中身
if not st.session_state.logged_in:
    basic_auth()
else:
    show_page()
