from display_helper import DisplayHelper


class EvaluationTableSize():
    """テーブル・サイズ。その計算方法含む"""


    def __init__(
            self,
            is_king_of_a,
            is_king_of_b,
            is_symmetrical_half_board,
            a_number,
            b_number):
        """初期化

        バージョン違いに対応する必要もあって、固定にできない"""
        self._is_king_of_a = is_king_of_a
        self._is_king_of_b = is_king_of_b
        self._is_symmetrical_half_board = is_symmetrical_half_board
        self._a_number = a_number
        self._b_number = b_number
        self._relation = a_number * b_number


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
    def relation(self):
        """指し手 a, b の関係の数"""
        return self._relation


    def to_debug_str(self):
        """デバッグ用"""
        a = self._is_king_of_a   # bool
        b = self._is_king_of_b
        c = self._is_symmetrical_half_board
        d = DisplayHelper.with_underscore(self._a_number)
        e = DisplayHelper.with_underscore(self._b_number)
        f = DisplayHelper.with_underscore(self._relation)

        return f"is_king_of_a:{a}  is_king_of_b:{b}  is_symmetrical_half_board:{c}  a_number:{d}  b_number:{e}  relation:{f}"
