from evaluation_configuration import EvaluationConfiguration
from evaluation_mm_table import EvaluationMmTable


class EvaluationKkTable(EvaluationMmTable):
    """評価値テーブル　ＫＫ"""

    def __init__(
            self,
            file_number,
            file_name,
            evaluation_mm_table,
            is_file_modified,
            is_symmetrical_connected):
        """初期化

        Parameters
        ----------
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        if is_symmetrical_connected:
            move_size = EvaluationConfiguration.get_symmetrical_connected_move_number()
            table_size = EvaluationConfiguration.get_symmetrical_connected_table_size()
        else:
            move_size = EvaluationConfiguration.get_fully_connected_move_number()
            table_size = EvaluationConfiguration.get_fully_connected_table_size()

        EvaluationMmTable.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                move_size=move_size,
                table_size=table_size,
                is_symmetrical_connected=is_symmetrical_connected,
                evaluation_mm_table=evaluation_mm_table,
                is_file_modified=is_file_modified)
