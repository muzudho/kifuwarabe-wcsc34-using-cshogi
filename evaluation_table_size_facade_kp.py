from evaluation_rule_facade import EvaluationRuleFacade
from evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacadeKp():


    @staticmethod
    def create_it(
            evaluation_table_property):
        """生成

        Parameters
        ----------
        evaluation_table_property : EvaluationTableProperty
            バージョン毎に異なる評価値テーブルの設定
        """

        return EvaluationTableSize(
                is_king_of_a=evaluation_table_property.is_king_size_of_a,
                is_king_of_b=evaluation_table_property.is_king_size_of_b,
                is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board,
                a_number=EvaluationRuleFacade.get_move_number(
                        is_king=evaluation_table_property.is_king_size_of_a,
                        is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board),
                b_number=EvaluationRuleFacade.get_move_number(
                        is_king=evaluation_table_property.is_king_size_of_b,
                        is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board))
