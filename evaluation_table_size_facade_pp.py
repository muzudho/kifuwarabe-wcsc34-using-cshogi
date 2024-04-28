from evaluation_rule_facade import EvaluationRuleFacade
from evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacadePp():


    @staticmethod
    def create_it(evaluation_table_property):
        """生成"""

        a_number = EvaluationRuleFacade.get_move_number(
                is_king=False)

        b_number = EvaluationRuleFacade.get_move_number(
                is_king=False)

        return EvaluationTableSize(
                is_king_of_a=False,
                is_king_of_b=False,
                a_number=a_number,
                b_number=b_number)
