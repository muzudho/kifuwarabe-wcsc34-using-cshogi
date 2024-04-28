from evaluation_table_mm import EvaluationTableMm
from evaluation_table_size import EvaluationTableSize
from evaluation_rule_mm import EvaluationRuleMm


class EvaluationTableKp(EvaluationTableMm):
    """評価値テーブル　ＫＰ"""


    def __init__(
            self,
            file_number,
            file_name,
            file_version,
            evaluation_table_property,
            evaluation_mm_table,
            is_file_modified):
        """初期化

        Parameters
        ----------
        file_version : str
            ファイルのバージョン
        evaluation_table_property : EvaluationTableProperty
            バージョン別の仕様の情報
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        k_size = EvaluationRuleMm.get_move_number(
                is_king=evaluation_table_property.is_king_size_of_a,
                is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board)
        p_size = EvaluationRuleMm.get_move_number(
                is_king=evaluation_table_property.is_king_size_of_b,
                is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board)

        new_table_size_obj = EvaluationTableSize(
                evaluation_table_property=evaluation_table_property)

        EvaluationTableMm.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_table_property=evaluation_table_property,
                list_of_move_size=[k_size, p_size],
                table_size_obj=new_table_size_obj,
                evaluation_mm_table=evaluation_mm_table,
                is_file_modified=is_file_modified)
