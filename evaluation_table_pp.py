from evaluation_table_mm import EvaluationTableMm
from evaluation_table_size import EvaluationTableSize
from evaluation_rule_mm import EvaluationRuleMm


class EvaluationTablePp(EvaluationTableMm):
    """評価値テーブル　ＰＰ"""


    def __init__(
            self,
            file_number,
            file_name,
            file_version,
            evaluation_version_record,
            evaluation_mm_table,
            is_king_of_a,
            is_king_of_b,
            is_file_modified,
            is_symmetrical_half_board):
        """初期化

        Parameters
        ----------
        file_version : str
            ファイルのバージョン
        evaluation_version_record : EvaluationVersionRecord
            バージョン別の仕様の情報
        is_king_of_a : bool
            指し手 a は玉か？
        is_king_of_b : bool
            指し手 b は玉か？
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        if is_symmetrical_half_board:
            p_size = EvaluationRuleMm.get_move_number(
                    is_king=False,          # P なんで
                    is_symmetrical_half_board=True)
            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=False,     # P なんで
                    is_king_of_b=False,     # P なんで
                    is_symmetrical_half_board=True)

        else:
            p_size = EvaluationRuleMm.get_move_number(
                    is_king=False,          # P なんで
                    is_symmetrical_half_board=False)
            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=False,     # P なんで
                    is_king_of_b=False,     # P なんで
                    is_symmetrical_half_board=False)

        EvaluationTableMm.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_version_record=evaluation_version_record,
                list_of_move_size=[p_size, p_size],
                table_size_obj=new_table_size_obj,
                evaluation_mm_table=evaluation_mm_table,
                is_king_of_a=is_king_of_a,
                is_king_of_b=is_king_of_b,
                is_symmetrical_half_board=is_symmetrical_half_board,
                is_file_modified=is_file_modified)
