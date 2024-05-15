import cshogi
from move import Move
from move_helper import MoveHelper
from evaluation_rule_k import EvaluationRuleK


class EvaluationRuleKk():


    _relative_sq_to_move_index = {
        -10: 0,
        -9: 1,
        -8: 2,
        -1: 3,
        1: 4,
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

        相対SQを、以下の 指し手の相対index に変換します

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
        src_sq = move_obj.src_sq_or_none

        # 玉は成らない

        # 相対SQ    =  移動先マス番号    - 移動元マス番号
        relative_sq = move_obj.dst_sq - src_sq
        relative_index = EvaluationRuleKk._relative_sq_to_move_index[relative_sq]


        #      0～80  *                                  8 +           0～7
        return src_sq * EvaluationRuleK.get_king_direction_max_number() + relative_index


    @staticmethod
    def destructure_k_index(
            k_index):
        """インデックス分解"""
        rest = k_index

        move_number = EvaluationRuleK.get_king_move_number()

        relative_index = rest % move_number
        rest //= move_number

        src_sq = rest

        return (src_sq, relative_index)


    @staticmethod
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

        relative_sq = EvaluationRuleKk._k_index_to_relative_sq[k_index]
        dst_sq = src_sq + relative_sq

        return Move.from_src_dst_pro(
            src_sq=src_sq,
            dst_sq=dst_sq,
            promoted=False)


    @staticmethod
    def get_move_by_index(
            kl_index):
        """逆関数

        指し手２つ分返す

        Parameters
        ----------
        kl_index : int
            指し手 k, l のペアの通しインデックス

        Returns
        -------
        - タプル
            - 指し手 k
            - 指し手 l
        """

        #
        # 下位の b から
        # ------------
        #

        l_size = EvaluationRuleK.get_king_move_number()

        rest = kl_index

        l_index = rest % l_size
        rest //= l_size

        k_index = rest

        try:
            src_sq, relative_index = EvaluationRuleKk.destructure_k_index(
                    k_index=l_index)

            dst_sq = src_sq + relative_index

            l_move = Move.from_src_dst_pro(
                    src_sq=src_sq,
                    dst_sq=dst_sq,
                    promoted=False)

        except Exception as e:
            print(f"list_of_b_move error.  k_index:{k_index}  l_index:{l_index}  kl_index:{kl_index}  e:{e}")
            raise

        try:
            src_sq, relative_index = EvaluationRuleKk.destructure_k_index(
                    k_index=k_index)

            dst_sq = src_sq + relative_index

            k_move = Move.from_src_dst_pro(
                    src_sq=src_sq,
                    dst_sq=dst_sq,
                    promoted=False)

        except Exception as e:
            print(f"list_of_b_move error.  k_index:{k_index}  l_index:{l_index}  kl_index:{kl_index}  e:{e}")
            raise

        return [k_move, l_move]
