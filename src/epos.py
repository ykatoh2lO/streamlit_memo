import math

from dataclasses import dataclass

import pulp


@dataclass
class EposPointResult:
    status: str
    objective: float
    x_point_usage: int
    applicable_amount: int
    x_epos_discount: int
    payment: int

    def __init__(self, status, objective, x_point_usage, applicable_amount, x_epos_discount, payment):
        self.status = str(status)
        self.objective = objective
        self.x_point_usage = int(x_point_usage.value())
        self.applicable_amount = int(applicable_amount.value())
        self.x_epos_discount = int(x_epos_discount.value())
        self.payment = int(payment.value())


class EposPointCalculator:
    ''' ポイント使用額調整 '''
    def __init__(self, default_amount, target_amount, max_point=None, discount_rate=0.1):
        assert 0 <= discount_rate <= 1, f'カード割引率 {discount_rate} は 0 以上 1 以下にしてください'

        # 定数
        self.default_amount = default_amount  # 商品金額 + 配送料 - クーポン割引額
        self.target_amount = target_amount  # 目標金額
        self.max_point = default_amount if max_point is None else max_point  # ポイント上限
        self.discount_rate = discount_rate  # カード割引率

        # 変数・中間式
        self.x_point_usage = {}  # ポイント利用額
        self.x_epos_discount = {}  # カード割引額
        self.applicable_amount = {}  # 割引対象額
        self.payment = {}  # 支払金額

        # 数理モデル・計算ステータス・結果
        self.model = None
        self.status = -1
        self.result = None


    def show_input(self):
        ''' 入力データの表示 '''
        print('=' * 50)
        print(f'商品金額 + 配送料 + クーポン割引額: {self.default_amount} 円')
        print(f'目標金額: {self.target_amount} 円')
        print(f'最大ポイント: {self.max_point} 円')
        print(f'カード割引率: {self.discount_rate}')
        print('=' * 50)


    def build_model(self, epsilon=1e-5):
        ''' 数理モデルの定義 '''
        self.model = pulp.LpProblem('EposPointCalculator', pulp.LpMinimize)

        ### 変数 (引数は name, lowBound, upBound, cat の順) ###
        # ポイント利用額
        self.x_point_usage = pulp.LpVariable(
            'x_point_usage', 0, self.max_point, 'Integer')
        # カード割引額
        self.x_epos_discount = pulp.LpVariable(
            'x_epos_discount', 0, math.ceil(self.discount_rate * self.default_amount), 'Integer')
        # 支払金額
        self.payment = pulp.LpVariable(
            'payment', 0, self.default_amount, 'Integer')
        # 割引対象額
        self.applicable_amount = pulp.LpVariable(
            'applicable_amount', 0, self.default_amount, 'Integer')

        ### 中間式 ###
        # 割引対象額 = (商品金額 + 配送料 - クーポン割引額) - ポイント利用額
        self.model += (
            self.applicable_amount == self.default_amount - self.x_point_usage
        )
        # 支払金額 = 割引対象額 - カード割引額
        self.model += (
            self.payment == self.applicable_amount - self.x_epos_discount
        )

        ### 制約式 ###
        # カード割引額は ceil(カード割引率 * 割引対象額)
        self.model += (
            self.x_epos_discount - 1 + epsilon <= self.discount_rate * self.applicable_amount
            # 10 * self.x_epos_discount - 9 <= self.default_amount
        )
        self.model += (
            self.discount_rate * self.applicable_amount <= self.x_epos_discount
            # self.default_amount <= 10 * (self.x_epos_discount + 1)
        )

        # 支払金額は目標金額以上
        self.model += (
            self.payment >= self.target_amount
        )

        ### 目的関数 ###
        # 支払金額を最小化する
        self.model += self.payment + epsilon * self.x_point_usage


    def solve(self):
        ''' 求解 '''
        self.status = self.model.solve(pulp.PULP_CBC_CMD(msg=0))
        self.result = EposPointResult(
            pulp.LpStatus[self.status], self.model.objective.value(),
            self.x_point_usage, self.applicable_amount,
            self.x_epos_discount, self.payment)
        print(f'status: {self.result.status}, objective: {self.result.objective}')


if __name__ == '__main__':
    pass
