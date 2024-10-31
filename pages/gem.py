import streamlit as st

from gui.gem import initialize, show_page
from gui.utils import basic_auth

# 初期化・サイドバー
st.set_page_config(layout='wide')
st.session_state.update(st.session_state)
initialize(__file__)

# 枠組み・中身
if not st.session_state.logged_in:
    basic_auth()
else:
    show_page()
