from display_helper import DisplayHelper


class EvaluationTableSizeKk():
    """ＫＫ関係のテーブル・サイズ

    玉は１マスしか動かないから、指し手は最大８手。
    成りもしないし、打もないし、ワープもしないから、
    １局面につき指し手は最大６４パターンしかないはず。

    相対SQは以下の通り

    +----+----+----+
    | +8 | -1 |-10 |
    |    |    |    |
    +----+----+----+
    | +9 | You| -9 |
    |    |    |    |
    +----+----+----+
    |+10 | +2 | -8 |
    |    |    |    |
    +----+----+----+

    指し手は例えば　5g5f　なら相対SQは -1 が該当する。
    以下の通りで充分だ

    81 *    8  *      8 =      5_184
    (file * rank) * around = k_patterns

    組み合わせだと n * (n-1) のようにしたいところだが実装が難しいので単に n * n にするとし、これを関係と呼ぶとき

    KL関係なら、以下で足りる

         5_184 *       5_184 =  26_873_856
    k_patterns * (k_patterns = kk_relation

    ※ PP関係が 203_219_280 あるので、１桁は少ない
    """


    def __init__(
            self):
        """初期化"""

        self._a_number = 8      # 玉の合法手は最大で８手
        self._b_number = 8      # 玉の合法手は最大で８手
        self._relation = self._a_number * self._b_number


    @property
    def is_king_of_a(self):
        """指し手 a は、玉の動きか？"""
        return True


    @property
    def is_king_of_b(self):
        """指し手 b は、玉の動きか？"""
        return True


    @property
    def is_symmetrical_half_board(self):
        """盤は左右対称にして半分だけ使っているか？"""

        # 非対応
        return False


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
        a = self.is_king_of_a   # bool
        b = self.is_king_of_b
        c = self._is_symmetrical_half_board
        d = DisplayHelper.with_underscore(self._a_number)
        e = DisplayHelper.with_underscore(self._b_number)
        f = DisplayHelper.with_underscore(self._relation)

        return f"is_king_of_a:{a}  is_king_of_b:{b}  is_symmetrical_half_board:{c}  a_number:{d}  b_number:{e}  relation:{f}"
