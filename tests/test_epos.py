import unittest

from src.epos import EposPointCalculator

class TestEpos(unittest.TestCase):
    """ 正しい数値になっているか確認 """

    # (商品金額, クーポン割引額, 目標金額), (ポイント利用額, カード割引額, 割引対象額, 支払金額)
    patterns = [
        ((10373,  500,  8800), (   94,  979,  9779,  8800)),  # Failed
        ((14960,  300, 13000), (  215, 1445, 14445, 13000)),
        ((39216,  500, 30000), ( 5382, 3334, 33334, 30000)),
        ((41960, 1500, 36000), (  458, 4002, 40002, 36000)),  # Failed
        ((46829,    0, 42000), (  162, 4667, 46667, 42000)),
        ((72523, 1000, 54000), (11522, 6001, 60001, 54000)),
    ]

    def test_with_params(self):
        for param_in, param_out in self.patterns:
            with self.subTest(param_in=param_in, param_out=param_out):
                epos_point_calculator = EposPointCalculator(param_in[0] - param_in[1], param_in[2])
                epos_point_calculator.build_model()
                epos_point_calculator.solve()

                self.assertEqual(epos_point_calculator.result.x_point_usage,     param_out[0])
                self.assertEqual(epos_point_calculator.result.x_epos_discount,   param_out[1])
                self.assertEqual(epos_point_calculator.result.applicable_amount, param_out[2])
                self.assertEqual(epos_point_calculator.result.payment,           param_out[3])
