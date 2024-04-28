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
            is_file_modified,
            is_symmetrical_half_board):
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

        if is_symmetrical_half_board:
            k_size = EvaluationRuleMm.get_move_number(
                    is_king=evaluation_table_property.is_king_size_of_a,
                    is_symmetrical_half_board=True)
            p_size = EvaluationRuleMm.get_move_number(
                    is_king=evaluation_table_property.is_king_size_of_b,
                    is_symmetrical_half_board=True)

            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=evaluation_table_property.is_king_size_of_a,
                    is_king_of_b=evaluation_table_property.is_king_size_of_b,
                    is_symmetrical_half_board=True)

        else:
            k_size = EvaluationRuleMm.get_move_number(
                    is_king=evaluation_table_property.is_king_size_of_a,
                    is_symmetrical_half_board=False)
            p_size = EvaluationRuleMm.get_move_number(
                    is_king=evaluation_table_property.is_king_size_of_b,
                    is_symmetrical_half_board=False)

            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=evaluation_table_property.is_king_size_of_a,
                    is_king_of_b=evaluation_table_property.is_king_size_of_b,
                    is_symmetrical_half_board=False)

        EvaluationTableMm.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_table_property=evaluation_table_property,
                list_of_move_size=[k_size, p_size],
                table_size_obj=new_table_size_obj,
                evaluation_mm_table=evaluation_mm_table,
                is_symmetrical_half_board=is_symmetrical_half_board,
                is_file_modified=is_file_modified)
