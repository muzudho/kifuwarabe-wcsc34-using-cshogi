from evaluation_rule_facade import EvaluationRuleFacade
from evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacadePp():


    @staticmethod
    def create_it():
        """生成"""
        return EvaluationTableSize(
                is_king_of_a=False,
                is_king_of_b=False,
                a_number=EvaluationRuleFacade.get_move_number(
                        is_king=False),
                b_number=EvaluationRuleFacade.get_move_number(
                        is_king=False))
