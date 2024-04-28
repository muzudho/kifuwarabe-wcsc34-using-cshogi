from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_facade import EvaluationRuleFacade
from evaluation_table_size_facade_kp import EvaluationTableSizeFacadeKp


class EvaluationTableFacadeKp():
    """評価値テーブル　ＫＰ"""


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
        table_size_obj = EvaluationTableSizeFacadeKp.create_it()

        k_size = EvaluationRuleFacade.get_move_number(
                is_king=True)
        p_size = EvaluationRuleFacade.get_move_number(
                is_king=False)

        return EvaluationTableMm(
                file_number=file_number,
                file_name=file_name,
                table_size_obj=table_size_obj,
                list_of_move_size=[k_size, p_size],
                evaluation_mm_table=evaluation_mm_table,
                is_king_size_of_a=True,
                is_king_size_of_b=False,
                is_file_modified=is_file_modified)
