import pickle

import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium

from gui.utils import HOME_DIR, set_title_navi


def initialize(current_filename):
    set_title_navi(current_filename)
    if 'gem_data' not in st.session_state:
        # pickle をロード
        st.session_state.gem_data = load_pickle(HOME_DIR / 'src' / 'gem_data.pkl')
        st.session_state.df_mineral_info = st.session_state.gem_data['df_mineral_info']
        st.session_state.df_mineral_gem = st.session_state.gem_data['df_mineral_gem']
        st.session_state.df_country_gem = st.session_state.gem_data['df_country_gem']
        st.session_state.gdf_country_shape = st.session_state.gem_data['gdf_country_shape']
        # 初期化
        st.session_state.gems = st.session_state.df_country_gem['宝石名'].drop_duplicates().values.tolist()
        # st.session_state.target_gem = st.session_state.gems[0]


@st.cache_data
def load_pickle(pickle_path):
    with open(pickle_path, 'rb') as frb:
        return pickle.load(frb)

@st.cache_data
def read_fgb(flatgeobuf_path) -> pd.DataFrame:
    return gpd.read_file(flatgeobuf_path)


@st.cache_data
def read_csv(csv_path) -> pd.DataFrame:
    return pd.read_csv(csv_path, encoding='CP932')


@st.cache_data
def filter_df(df, col, target=None):
    if target is None:
        return df
    if col not in df.columns:
        print(f'column "{col}" not in df.columns')
        return df
    #
    return df[df[col] == target]

def show_page():
    # 枠組み
    col_select, col_map = st.columns([1, 3])

    # 中身
    with col_select:
        st.session_state.target_gem = st.selectbox('宝石を選んでください．', st.session_state.gems)
        target_mineral = filter_df(st.session_state.df_mineral_gem, '宝石名', st.session_state.target_gem)
        if len(target_mineral) > 0:
            st.dataframe(st.session_state.df_mineral_info.merge(target_mineral).T)

    with col_map:
        st.session_state.gdf = st.session_state.gdf_country_shape.merge(
            filter_df(st.session_state.df_country_gem, '宝石名', st.session_state.target_gem))
        st_folium(st.session_state.gdf.explore(column='国名'), use_container_width=True)
    col_map.write('境界データは https://gadm.org/download_country.html より取得．')
