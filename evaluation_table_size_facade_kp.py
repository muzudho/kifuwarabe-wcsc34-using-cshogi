from evaluation_rule_k import EvaluationRuleK
from evaluation_rule_p import EvaluationRuleP
from evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacadeKp():
    """生成

    組み合わせは n * (n - 1) だが、実装が難しいので関係 n * n にしている

    relation
    +---------------+------------------------+
    |   b           |      king        piece |
    | a             |       648       14_256 |
    |---------------+------------------------+
    | king      648 |   419_904    9_237_888 |
    | piece  14_256 | 9_237_888  203_233_536 |
    +---------------+------------------------+
    """


    @staticmethod
    def create_it():
        """生成"""
        return EvaluationTableSize(
                is_king_of_a=True,
                is_king_of_b=False,
                a_number=EvaluationRuleK.get_king_move_number(),
                b_number=EvaluationRuleP.get_piece_move_number())
