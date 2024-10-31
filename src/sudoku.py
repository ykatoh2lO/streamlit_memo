from dataclasses import dataclass
from itertools import product
from math import sqrt

from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, PULP_CBC_CMD, lpSum
import pandas as pd


@dataclass
class SudokuResult:
    status: str
    objective: float
    df: int

    def __init__(self, status, objective, df):
        self.status = str(status)
        self.objective = objective
        self.df = df


class SudokuSolver:
    ''' 数独ソルバー '''
    def __init__(self, df):
        # 問題 (行名・列名を Excel 形式に，空白は一旦ゼロに)
        self.init_df = df

        # 変数・中間式
        self.x = pd.DataFrame()

        # 数理モデル・計算ステータス・結果
        self.model = None
        self.status = -1
        self.result = None

    def show(self, is_init=False):
        """ 数独の表示 """
        df = self.result.df if is_init else self.init_df
        for row in df.itertuples(name=None):
            i, *val = row
            if i % 3 == 1:
                print('+-------+-------+-------+')
            for j, v in enumerate(val):
                if j % 3 == 0:
                    print('| ', end='')
                print(f'{" " if v is None else v} ', end='')
                if j == 8:
                    print('|')
        print("+-------+-------+-------+")

    @classmethod
    def read_problem(cls, csv_path=None):
        if csv_path is None:
            return pd.DataFrame('', index=[i+1 for i in range(9)], columns=[chr(j+65) for j in range(9)])
        #
        df = pd.read_csv(csv_path, header=None)
        df.index = df.index + 1
        return df.rename(columns={j: chr(65+j) for j in df.columns}).replace({' ': '0'}).astype(int).replace({0: None})


    @classmethod
    def _get_partial_values(cls, partial_df, label):
        df = partial_df.copy()
        df = df.reset_index().melt(id_vars='index', value_vars=list(df.columns), var_name='column')
        df = df[['column', 'index', 'value']]
        df['type'] = label
        return df

    @classmethod
    def _get_row(cls, df):
        return [
            cls._get_partial_values(df.iloc[[i], :], f'row_{i+1}')
            for i in range(len(df))]

    @classmethod
    def _get_col(cls, df):
        return [
            cls._get_partial_values(df.iloc[:, [j]], f'col_{chr(j+65)}')
            for j in range(len(df))]

    @classmethod
    def _get_block(cls, df):
        size = int(sqrt(len(df)))
        lst = [[bi * size + di for di in range(size)] for bi in range(size)]
        return [
            cls._get_partial_values(df.iloc[lst[i], lst[j]], f'blk_{chr(i*size + j + 97)}')
            for i, j in product(range(size), repeat=2)]

    def get_init_values(self):
        df = pd.concat(self._get_block(self.init_df)).reset_index(drop=True)
        df['init'] = df['value'] > 0
        return df

    @classmethod
    def check_duplicates(cls, df):
        df = pd.concat(cls._get_row(df) + cls._get_col(df) + cls._get_block(df))
        df = df.dropna(subset='value')
        df = df[df.duplicated(keep=False, subset=['type', 'value'])].reset_index(drop=True)
        return len(df) == 0, df

    def build_model(self):
        ''' 数理モデルの定義 '''
        self.model = LpProblem('SudokuSolver', LpMinimize)

        # self.x は col, idx, blk, val, fixed, BinaryVariable の順
        df = self.get_init_values()
        self.x = pd.DataFrame([[
            row.column, row.index, row.type[4], val+1, row.init and row.value == val+1,
            LpVariable(f'x_{row.column}{row.index}_{val+1}', cat='Binary')]
            for row, val in product(df.itertuples(index=False), range(len(self.init_df)))],
            columns=['column', 'index', 'block', 'value', 'fixed', 'BinaryVariable'])

        # pandasを使った数理モデルの参考: https://qiita.com/SaitoTsutomu/items/070ca9cb37c6b2b492f0
        # 初期値固定
        df_fixed = self.x[self.x['fixed']]
        self.model += lpSum(df_fixed.BinaryVariable) == len(df_fixed)
        # (col, index) は 1 つの val
        for _, df_cell in self.x.groupby(by=['column', 'index']):
            self.model += lpSum(df_cell.BinaryVariable) == 1
        # 行で 1 つの val
        for _, df_row in self.x.groupby(by=['index', 'value']):
            self.model += lpSum(df_row.BinaryVariable) == 1
        # 列で 1 つの val
        for _, df_col in self.x.groupby(by=['column', 'value']):
            self.model += lpSum(df_col.BinaryVariable) == 1
        # ブロックで 1 つの val
        for _, df_blk in self.x.groupby(by=['block', 'value']):
            self.model += lpSum(df_blk.BinaryVariable) == 1

    def solve(self):
        ''' 求解 '''
        self.status = self.model.solve(PULP_CBC_CMD(msg=0))
        df_result = self.x[[x.value() > 0 for x in self.x.BinaryVariable]]
        self.result = SudokuResult(
            LpStatus[self.status], self.model.objective,  #.value(),
            df_result.pivot(index='index', columns='column', values='value'))


if __name__ == '__main__':
    pass
