from enum import Enum, unique

import streamlit as st

from src.epos import EposPointCalculator
from gui.utils import set_title_navi

def initialize(current_filename):
    set_title_navi(current_filename)
    if 'epos_problem' not in st.session_state:
        st.session_state.epos_problem = None
        st.session_state.epos_result = None


@unique
class Shipping(Enum):
    FREE =   ('無料',   0)
    CHARGE = ('有料', 210)

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def val(self) -> int:
        return self.value[1]

    def __str__(cls) -> str:
        return cls.label

def calculate(*args):
    msg = st.toast('入力データを読み込みます')
    problem = EposPointCalculator(*args)
    msg.toast('最適化モデルを定義します')
    problem.build_model()
    msg.toast('最適化計算を開始します')
    problem.solve()
    msg.toast('最適化計算を終了しました')

    st.session_state.epos_result = problem.result
