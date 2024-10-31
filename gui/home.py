import streamlit as st

from gui.utils import set_title_navi

CODE_FRAME = """
import streamlit as st
# その他モジュール読み込み

# 初期化
st.set_page_config(layout='wide')

# 枠組み
if not st.session_state.logged_in:
    basic_auth()
else:
    show_page()
"""


CODE_FUNC = """
import streamlit as st
# その他モジュール読み込み

# 処理の中身
def show_page():
    pass
"""


def initialize(current_filename):
    set_title_navi(current_filename)


def show_contents():
    st.write('  \n'.join([
        '## Excel を使わずにデモアプリを作成する際の覚え書き',
        'Streamlit は GUI の入力に変更があるたびにスクリプトを先頭から再実行する (ボタン押下も含まれる) ため，',
        '- 固定表示: 枠組み',
        '- 可変表示: 処理の内容など\n',
        'のようにスクリプトを分けておくことが大事．']))

    col_app, col_func, _ = st.columns([3, 3, 3])
    with col_app:
        st.header('固定表示')
        st.code(CODE_FRAME, language='python')
    with col_func:
        st.header('可変表示')
        st.code(CODE_FUNC, language='python')

    st.divider()
    st.header('各ページの概要')
    col_left, col_right = st.columns(2)
    with col_left.container():
        st.subheader('1. カオナビ (要認証)')
        st.write('  \n'.join([
            '各項目に集中しつつ過去の記入内容と比較して書きたかったので作成．',
            'markdown の内容に合わせてタブを作成できるが別になくてもよい．']))
        st.subheader('2. エポス調整')
        st.write('  \n'.join([
            'Google スプレッドシートの OpenSolver アドオンで作っていたものを移植．',
            'Streamlit Cloud のおかげで iPhone からも使えるようになった．']))
    with col_right.container():
        st.subheader('3. 数独')
        st.write('  \n'.join([
            '解く前に違反がないかチェックしてから解かせている．',
            'ボタンを押したあと複数段階に分けて実行したいときのサンプル．']))
        st.subheader('4. 地図表示 (要認証)')
        st.write('  \n'.join([
            'folium と組み合わせて地図表示など．',
            'データ容量の割に処理が重く，Jupyter や HTML 出力のほうが便利そう．',]))
