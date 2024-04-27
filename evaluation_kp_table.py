from evaluation_configuration import EvaluationConfiguration
from evaluation_mm_table import EvaluationMmTable


class EvaluationKpTable(EvaluationMmTable):
    """評価値テーブル　ＫＰ"""


    def __init__(
            self,
            file_number,
            file_name,
            file_version,
            evaluation_mm_table,
            is_king_of_a,
            is_king_of_b,
            is_file_modified,
            is_symmetrical_connected):
        """初期化

        Parameters
        ----------
        file_version : str
            ファイルのバージョン
        is_king_of_a : bool
            指し手 a は玉か？
        is_king_of_b : bool
            指し手 b は玉か？
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        if file_version=="V4":
            is_king = True
        else:
            is_king = False

        if is_symmetrical_connected:
            k_size = EvaluationConfiguration.get_move_number(
                    is_king=is_king,
                    is_symmetrical_connected=True)
            p_size = EvaluationConfiguration.get_move_number(
                    is_king=False,  # P なんで
                    is_symmetrical_connected=True)
            table_size = EvaluationConfiguration.get_table_size(
                    is_symmetrical_connected=True)

        else:
            k_size = EvaluationConfiguration.get_move_number(
                    is_king=is_king,
                    is_symmetrical_connected=False)
            p_size = EvaluationConfiguration.get_move_number(
                    is_king=False,  # P なんで
                    is_symmetrical_connected=False)
            table_size = EvaluationConfiguration.get_table_size(
                    is_symmetrical_connected=False)

        EvaluationMmTable.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                list_of_move_size=[k_size, p_size],
                table_size=table_size,
                evaluation_mm_table=evaluation_mm_table,
                is_king_of_a=is_king_of_a,
                is_king_of_b=is_king_of_b,
                is_symmetrical_connected=is_symmetrical_connected,
                is_file_modified=is_file_modified)
