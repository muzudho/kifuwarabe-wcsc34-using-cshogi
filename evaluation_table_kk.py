from evaluation_table_mm import EvaluationTableMm
from evaluation_table_size import EvaluationTableSize
from evaluation_rule_kk import EvaluationRuleKk


class EvaluationTableKk(EvaluationTableMm):
    """評価値テーブル　ＫＫ"""


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
            # KKテーブルは左右対称に非対応
            k_size = EvaluationRuleKk.get_move_number()
            l_size = EvaluationRuleKk.get_move_number()

            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=evaluation_table_property.is_king_size_of_a,
                    is_king_of_b=evaluation_table_property.is_king_size_of_b,
                    is_symmetrical_half_board=True)

        else:
            k_size = EvaluationRuleKk.get_move_number()
            l_size = EvaluationRuleKk.get_move_number()

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
                list_of_move_size=[k_size, l_size],
                table_size_obj=new_table_size_obj,
                evaluation_mm_table=evaluation_mm_table,
                is_symmetrical_half_board=is_symmetrical_half_board,
                is_file_modified=is_file_modified)
