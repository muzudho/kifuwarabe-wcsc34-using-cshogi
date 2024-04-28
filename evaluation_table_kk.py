from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_kk import EvaluationRuleKk
from evaluation_table_size_facade_kk import EvaluationTableSizeFacadeKk


class EvaluationTableKk(EvaluationTableMm):
    """評価値テーブル　ＫＫ"""


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

        # テーブル・サイズ。計算過程付き
        table_size_obj = EvaluationTableSizeFacadeKk.create_it(
                evaluation_table_property=evaluation_table_property)

        # KKテーブルは左右対称に非対応
        k_size = EvaluationRuleKk.get_move_number()
        l_size = EvaluationRuleKk.get_move_number()

        EvaluationTableMm.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_table_property=evaluation_table_property,
                table_size_obj=table_size_obj,
                list_of_move_size=[k_size, l_size],
                evaluation_mm_table=evaluation_mm_table,
                is_file_modified=is_file_modified)
