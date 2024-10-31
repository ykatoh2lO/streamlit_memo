import sys
from enum import Enum, unique
from hmac import compare_digest
from pathlib import Path

import pandas as pd
import streamlit as st

HOME_DIR = Path(sys.argv[0]).parent.absolute()


@unique
class Pages(Enum):
    # ファイルの相対パス，ラベル，アイコン
    HOME =     ('home.py',    'ホーム', '🏠')
    KAONAVI =  ('kaonavi.py', 'カオナビ', '🙃')
    EPOS =     ('epos.py',    'エポス調整', '👌')
    SUDOKU =   ('sudoku.py',  '数独', '9️⃣')
    GEM_EXAM = ('gem.py',     '地図表示', '💎')

    @property
    def filename(self) -> str:
        return self.value[0]

    @property
    def label(self) -> str:
        return self.value[1]

    @property
    def icon(self) -> str:
        return self.value[2]

    @classmethod
    @st.cache_data
    def get_by_filename(cls, filename):
        for page in cls:
            if Path(filename).name == page.filename:
                return cls[page.name]

    @classmethod
    @st.cache_data
    def show_sidebar(cls, current_page):
        for page in cls:
            if page == current_page:
                st.markdown(f'**{page.label}**')
            else:
                st.page_link(f'pages/{page.filename}' , label=page.label, icon=page.icon)


def set_title_navi(current_filename):
    current_page = Pages.get_by_filename(current_filename)
    st.title(current_page.label)
    with st.sidebar:
        Pages.show_sidebar(current_page)
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False


# https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso
@st.dialog('認証')
def basic_auth():
    username = st.text_input('ユーザー名', value='', type='default')
    password = st.text_input('パスワード', value='', type='password')

    if username == '' or password == '':
        return

    if username != st.secrets['username'] or not compare_digest(password, st.secrets['password']):
        st.session_state.logged_in = False
        st.error('ユーザー名またはパスワードが間違っています．')
    else:
        st.session_state.logged_in = True
        st.rerun()


def calc_height(df: pd.DataFrame) -> int:
    return (len(df) + 1) * 35 + 3

def calc_width(df: pd.DataFrame) -> int:
    return (len(df.columns) + 1) * 55 + 3
