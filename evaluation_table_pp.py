from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_facade import EvaluationRuleFacade
from evaluation_table_size_facade_pp import EvaluationTableSizeFacadePp


class EvaluationTablePp(EvaluationTableMm):
    """評価値テーブル　ＰＰ"""


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
        table_size_obj = EvaluationTableSizeFacadePp.create_it(
                evaluation_table_property=evaluation_table_property)

        a_size = EvaluationRuleFacade.get_move_number(
                is_king=evaluation_table_property.is_king_size_of_a)
        b_size = EvaluationRuleFacade.get_move_number(
                is_king=evaluation_table_property.is_king_size_of_b)

        EvaluationTableMm.__init__(
                self,
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_table_property=evaluation_table_property,
                table_size_obj=table_size_obj,
                list_of_move_size=[a_size, b_size],
                evaluation_mm_table=evaluation_mm_table,
                is_file_modified=is_file_modified)
