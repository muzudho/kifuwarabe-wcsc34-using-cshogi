from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_p import EvaluationRuleP
from evaluation_table_size_facade_pp import EvaluationTableSizeFacadePp


class EvaluationTableFacadePp():
    """評価値テーブル　ＰＰ"""


    @staticmethod
    def create_it(
            file_number,
            file_name,
            raw_mm_table,
            is_file_modified):
        """初期化

        Parameters
        ----------
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        # テーブル・サイズ。計算過程付き
        table_size_obj = EvaluationTableSizeFacadePp.create_it()

        a_size = EvaluationRuleP.get_piece_move_number()
        b_size = EvaluationRuleP.get_piece_move_number()

        return EvaluationTableMm(
                file_number=file_number,
                file_name=file_name,
                table_size_obj=table_size_obj,
                list_of_move_size=[a_size, b_size],
                raw_mm_table=raw_mm_table,
                is_king_size_of_a=False,
                is_king_size_of_b=False,
                is_file_modified=is_file_modified)
