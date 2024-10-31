import streamlit as st

from gui.epos import Shipping, initialize, calculate

# 初期化・サイドバー
st.set_page_config(layout='wide')
st.session_state.update(st.session_state)
initialize(__file__)


# 枠組み
col_input, col_result = st.columns([5, 5])
col_input.subheader('入力データ')
col_result.subheader('結果')

# 中身
with col_input:
    product_amount = st.number_input(
        '商品金額', value=0, min_value=0,
        format='%d', placeholder='商品金額を入力してください')
    shipping_fee = st.selectbox(
        '配送料', Shipping)
    coupon_discount = st.number_input(
        'クーポン割引額', value=0, min_value=0, max_value=product_amount,
        format='%d', placeholder='クーポン割引額を入力してください')

    # ポイント・エポスの割引適用前の金額
    default_amount = product_amount + shipping_fee.val - coupon_discount
    default_target = 200 * (int(0.9*default_amount)//200)
    # ポイント・エポスの割引適用後の金額
    target_amount = st.number_input(
        '目標金額', value=default_target, min_value=0, max_value=default_amount, step=200,
        format='%d', placeholder='目標金額を入力してください')
    max_point = st.number_input(
        '最大ポイント', value=default_target, min_value=0, max_value=default_target,
        format='%d', placeholder='使用するポイントの最大値を入力してください')

with col_result:
    button = st.button('計算実行')
    if button:
        calculate(default_amount, target_amount, max_point)

    if st.session_state.epos_result is not None:
        result = st.session_state.epos_result
        if result.status == 'Optimal':
            st.success('  \n'.join([
                result.status,
                f'ポイントを {result.x_point_usage} 円分使うと，',
                f'割引対象額 {result.applicable_amount} 円，割引額 {result.x_epos_discount} 円で',
                f'支払金額は {result.payment} 円です．']), icon=':material/info:')
        else:
            st.error(str(result), icon=':material/error:')
