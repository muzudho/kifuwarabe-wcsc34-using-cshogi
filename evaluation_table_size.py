from display_helper import DisplayHelper
from evaluation_rule_mm import EvaluationRuleMm


class EvaluationTableSize():
    """テーブル・サイズ。その計算方法含む"""


    def __init__(
            self,
            is_king_of_a,
            is_king_of_b,
            is_symmetrical_half_board):
        """初期化

        symmetrical_half_board
        +--------------+------------------------+
        |   b          |       king       piece |
        | a            |    2_340-1     4_680-1 |
        +--------------+------------------------+
        | king   2_340 |  5_473_260  10_948_860 |
        | piece  4_680 | 10_946_520  21_897_720 |
        +--------------+------------------------+

        fully
        +---------------+--------------------------+
        |   b           |        king        piece |
        | a             |     7_128-1     14_256-1 |
        |---------------+--------------------------+
        | king    7_128 |  50_801_256  101_609_640 |
        | piece  14_256 | 101_602_512  203_219_280 |
        +---------------+--------------------------+

        Parameters
        ----------
        is_king_of_a : bool
            指し手 a は、玉の動きか？
        is_king_of_b : bool
            指し手 b は、玉の動きか？
        is_symmetrical_half_board : bool
            盤は左右対称にして半分だけ使っているか？
        """
        self._is_king_of_a = is_king_of_a
        self._is_king_of_b = is_king_of_b
        self._is_symmetrical_half_board = is_symmetrical_half_board

        self._a_number = EvaluationRuleMm.get_move_number(
                is_king=is_king_of_a,
                is_symmetrical_half_board=is_symmetrical_half_board)

        self._b_number = EvaluationRuleMm.get_move_number(
                is_king=is_king_of_b,
                is_symmetrical_half_board=is_symmetrical_half_board)

        # a と b のどちらを -1 するかで計算結果に違いが出てくるが、難しいところだ
        self._combination = self._a_number * (self._b_number - 1)
        #self._combination = (self._a_number - 1) * self._b_number


    @property
    def is_king_of_a(self):
        """指し手 a は、玉の動きか？"""
        return self._is_king_of_a


    @property
    def is_king_of_b(self):
        """指し手 b は、玉の動きか？"""
        return self._is_king_of_b


    @property
    def is_symmetrical_half_board(self):
        """盤は左右対称にして半分だけ使っているか？"""
        return self._is_symmetrical_half_board


    @property
    def a_number(self):
        """指し手 a のパターン数"""
        return self._a_number


    @property
    def b_number(self):
        """指し手 b のパターン数"""
        return self._b_number


    @property
    def combination(self):
        """指し手 a, b の組み合わせの数"""
        return self._combination


    def to_debug_str(self):
        """デバッグ用"""
        a = self._is_king_of_a   # bool
        b = self._is_king_of_b
        c = self._is_symmetrical_half_board
        d = DisplayHelper.with_underscore(self._a_number)
        e = DisplayHelper.with_underscore(self._b_number)
        f = DisplayHelper.with_underscore(self._combination)

        return f"is_king_of_a:{a}  is_king_of_b:{b}  is_symmetrical_half_board:{c}  a_number:{d}  b_number:{e}  combination:{f}"
