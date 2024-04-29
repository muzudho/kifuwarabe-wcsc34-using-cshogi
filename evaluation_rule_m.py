from evaluation_move_specification import EvaluationMoveSpecification
from move import Move


class EvaluationRuleM():


    @staticmethod
    def get_move_as_usi_by_m_index(
            m_index,
            is_king):
        """逆関数

        テーブルの番地を、指し手の USI 表記に変換

        Parameters
        ----------
        m_index : int
            指し手１つ分のインデックス
        is_king : bool
            玉の動きか？
        """

        m_spec = EvaluationMoveSpecification(
            # 玉は成らないから pro を削れる
            is_king=is_king)

        rest = m_index

        pro_value = None
        pro_str = ''
        if not is_king:
            pro_value = rest % m_spec.pro_patterns
            if pro_value == 1:
                # 成りだ
                pro_str = '+'

            rest //= m_spec.pro_patterns

        dst_value = rest % m_spec.dst_patterns
        rest //= m_spec.dst_patterns

        src_value = rest


        if 72 <= dst_value:
            dst_file = '9'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 72 + 1)
        elif 63 <= dst_value:
            dst_file = '8'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 63 + 1)
        elif 54 <= dst_value:
            dst_file = '7'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 54 + 1)
        elif 45 <= dst_value:
            dst_file = '6'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 45 + 1)
        elif 36 <= dst_value:
            dst_file = '5'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 36 + 1)
        elif 27 <= dst_value:
            dst_file = '4'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 27 + 1)
        elif 18 <= dst_value:
            dst_file = '3'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 18 + 1)
        elif 9 <= dst_value:
            dst_file = '2'
            dst_rank_str = Move.get_rank_num_to_str(dst_value - 9 + 1)
        else:
            dst_file = '1'
            dst_rank_str = Move.get_rank_num_to_str(dst_value + 1)

        # 81 以上は打
        if 81 <= src_value:
            src_file_str = EvaluationRuleFacade._src_num_to_file_str[src_value]
            src_rank_str = '*'

        # 盤上
        else:
            if 72 <= src_value:
                src_file_str = '9'
                src_rank_str = Move.get_rank_num_to_str(src_value - 72 + 1)
            elif 63 <= src_value:
                src_file_str = '8'
                src_rank_str = Move.get_rank_num_to_str(src_value - 63 + 1)
            elif 54 <= src_value:
                src_file_str = '7'
                src_rank_str = Move.get_rank_num_to_str(src_value - 54 + 1)
            elif 45 <= src_value:
                src_file_str = '6'
                src_rank_str = Move.get_rank_num_to_str(src_value - 45 + 1)
            elif 36 <= src_value:
                src_file_str = '5'
                src_rank_str = Move.get_rank_num_to_str(src_value - 36 + 1)
            elif 27 <= src_value:
                src_file_str = '4'
                src_rank_str = Move.get_rank_num_to_str(src_value - 27 + 1)
            elif 18 <= src_value:
                src_file_str = '3'
                src_rank_str = Move.get_rank_num_to_str(src_value - 18 + 1)
            elif 9 <= src_value:
                src_file_str = '2'
                src_rank_str = Move.get_rank_num_to_str(src_value - 9 + 1)
            else:
                src_file_str = '1'
                src_rank_str = Move.get_rank_num_to_str(src_value + 1)

        return f'{src_file_str}{src_rank_str}{dst_file}{dst_rank_str}{pro_str}'
