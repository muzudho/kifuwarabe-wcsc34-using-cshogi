from evaluation_rule_k import EvaluationRuleK
from evaluation_rule_m import EvaluationRuleM
from evaluation_rule_p import EvaluationRuleP


class EvaluationRuleFacade():


    _src_num_to_file_str = {
        81:'R',   # 'R*' 移動元の打 72+9=81
        82:'B',   # 'B*'
        83:'G',   # 'G*'
        84:'S',   # 'S*'
        85:'N',   # 'N*'
        86:'L',   # 'L*'
        87:'P',   # 'P*'
    }


    @staticmethod
    def get_move_number(
            is_king):
        """指し手の数

        Parameters
        ----------
        is_king : bool
            玉の動きか？

        Returns
        -------
        - int
        """

        if is_king:
            return EvaluationRuleK.get_king_move_number()
        else:
            #  sq   drop    sq   pro
            # (81 +    7) * 81 *   2 = 14_256
            return EvaluationRuleP.get_piece_move_number()


    # FIXME 使っていない？
    @staticmethod
    def get_pair_of_move_as_usi_by_mm_index(
            mm_index,
            is_king_of_b):
        """逆関数

        指し手２つ分返す

        Parameters
        ----------
        mm_index : int
            指し手 a, b のペアの通しインデックス
        is_king_of_b : bool
            指し手 b は、玉の動きか？
        """

        #
        # 下位の b から
        # ------------
        #

        b_size = EvaluationRuleFacade.get_move_number(
            is_king=is_king_of_b)

        rest = mm_index

        b_index = rest % b_size
        rest //= b_size

        a_index = rest

        try:
            b_move = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=b_index,
                    is_king=is_king_of_b)
        except Exception as e:
            # 例： list_of_b_move error.  a_index:0  b_index:4680  mm_index:21902400  e:52
            print(f"list_of_b_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  e:{e}")
            raise

        try:
            a_move = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=a_index,
                    is_king=is_king_of_b)
        except Exception as e:
            # mm_index がでかすぎる？
            # 例： list_of_a_move error.  a_index:4680  b_index:0  e:52
            # 例： list_of_a_move error.  a_index:4680  b_index:0  mm_index:21902400  e:52
            print(f"list_of_a_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  is_king_of_b:{is_king_of_b}  e:{e}")
            raise

        return [a_move, b_move]
