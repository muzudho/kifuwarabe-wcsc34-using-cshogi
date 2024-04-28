class EvaluationRuleKK():


    _relative_sq_to_move_index = {
        -10: 0,
        -9: 1,
        -8: 2,
        -1: 3,
        2: 4,
        8: 5,
        9: 6,
        10: 7,
    }
    """相対SQを、玉の指し手のインデックスへ変換"""


    _k_index_to_relative_sq = {
        0: -10,
        1: -9,
        2: -8,
        3: -1,
        4: 2,
        5: 8,
        6: 9,
        7: 10,
    }
    """玉の指し手のインデックスを、相対SQへ復元"""


    @staticmethod
    def get_k_index_by_move(
            move_obj):
        """指し手を指定すると、指し手のインデックスを返す。
        ＫＫ関係用

        指し手から、以下の相対SQを算出します

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

        例えば　5g5f　なら相対SQは -1 が該当する

        相対SQを、以下の 指し手のindex に変換します

        +----+----+----+
        |  5 |  3 |  0 |
        |    |    |    |
        +----+----+----+
        |  6 | You|  1 |
        |    |    |    |
        +----+----+----+
        |  7 |  4 |  2 |
        |    |    |    |
        +----+----+----+


        Parameters
        ----------
        move_obj : Move
            指し手

        Returns
        -------
            - 指し手のインデックス
        """

        # 移動元マス番号
        #
        #   - 打はありません。したがって None にはなりません
        #
        src_sq = move_obj.get_src_sq_or_none()

        # 移動先マス番号
        dst_sq = move_obj.get_dst_sq()

        # 玉は成らない

        # 相対SQ
        relative_sq = dst_sq - src_sq

        return EvaluationRuleKK._relative_sq_to_move_index[relative_sq]


    def get_k_move_by_k_index_and_src_sq(
            k_index,
            src_sq):
        """玉の指し手のインデックスと、玉の移動元マスから、指し手を復元します

        Parameters
        ----------
        k_index : int
            玉の指し手のインデックス
        src_sq : int
            玉の移動元マス

        Returns
        -------
        指し手
        """

        relative_sq = EvaluationRuleKK._k_index_to_relative_sq[k_index]
        dst_sq = src_sq + relative_sq

        pass
