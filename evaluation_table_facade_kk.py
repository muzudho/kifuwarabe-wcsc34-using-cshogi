from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_k import EvaluationRuleK
from evaluation_table_size_facade_kk import EvaluationTableSizeFacadeKk


class EvaluationTableKk():
    """評価値テーブル　ＫＫ"""


    @staticmethod
    def create_it(
            file_number,
            file_name,
            evaluation_mm_table,
            is_file_modified):
        """初期化

        Parameters
        ----------
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        # テーブル・サイズ。計算過程付き
        table_size_obj = EvaluationTableSizeFacadeKk.create_it()

        k_size = EvaluationRuleK.get_king_move_number()
        l_size = EvaluationRuleK.get_king_move_number()

        return EvaluationTableMm(
                file_number=file_number,
                file_name=file_name,
                table_size_obj=table_size_obj,
                list_of_move_size=[k_size, l_size],
                evaluation_mm_table=evaluation_mm_table,
                is_king_size_of_a=True,
                is_king_size_of_b=True,
                is_file_modified=is_file_modified)
