import streamlit as st

from gui.home import show_contents
from gui.utils import set_title_navi

# 初期化
st.set_page_config(layout='wide')
st.session_state.update(st.session_state)
set_title_navi(__file__)

# 枠組み
show_contents()
