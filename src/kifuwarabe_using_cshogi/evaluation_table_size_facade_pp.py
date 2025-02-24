from .evaluation_rule_p import EvaluationRuleP
from .evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacadePp():


    @staticmethod
    def create_it():
        """生成"""
        return EvaluationTableSize(
                is_king_of_a=False,
                is_king_of_b=False,
                a_number=EvaluationRuleP.get_piece_move_number(),
                b_number=EvaluationRuleP.get_piece_move_number())
