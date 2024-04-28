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

        is_king = evaluation_version_record.is_king_size_of_kk

        if file_version in ("V4", "V5"):
            is_king = True
        else:
            is_king = False

        if is_symmetrical_half_board:
            k_size = EvaluationRuleKk.get_move_number(
                    is_king=is_king,
                    is_symmetrical_half_board=True)

            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=is_king,
                    is_king_of_b=is_king,
                    is_symmetrical_half_board=True)

        else:
            k_size = EvaluationRuleKk.get_move_number(
                    is_king=is_king,
                    is_symmetrical_half_board=False)

            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=is_king,
                    is_king_of_b=is_king,
                    is_symmetrical_half_board=False)

        EvaluationTableMm.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                list_of_move_size=[k_size, k_size],
                table_size_obj=new_table_size_obj,
                evaluation_mm_table=evaluation_mm_table,
                is_king_of_a=is_king_of_a,
                is_king_of_b=is_king_of_b,
                is_symmetrical_half_board=is_symmetrical_half_board,
                is_file_modified=is_file_modified)
