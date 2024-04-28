from evaluation_rule_facade import EvaluationRuleFacade
from evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacade():


    @staticmethod
    def create_it(
            evaluation_table_property):
        """生成

        バージョン違いに対応する必要があって、ＫＫ型だからといって必ずしも玉の動きに対応しているとは限らない

        組み合わせは n * (n - 1) だが、実装が難しいので関係 n * n にしている

        symmetrical_half_board relation
        +--------------+------------------------+
        |   b          |       king       piece |
        | a            |      2_340       4_680 |
        +--------------+------------------------+
        | king   2_340 |  5_475_600  10_951_200 |
        | piece  4_680 | 10_951_200  21_902_400 |
        +--------------+------------------------+

        fully relation relation
        +---------------+--------------------------+
        |   b           |        king        piece |
        | a             |       7_128       14_256 |
        |---------------+--------------------------+
        | king    7_128 |  50_808_384  101_616_768 |
        | piece  14_256 | 101_616_768  203_233_536 |
        +---------------+--------------------------+

        Parameters
        ----------
        evaluation_table_property : EvaluationTableProperty
            バージョン毎に異なる評価値テーブルの設定
        """

        return EvaluationTableSize(
                is_king_of_a=evaluation_table_property.is_king_size_of_a,
                is_king_of_b=evaluation_table_property.is_king_size_of_b,
                is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board,
                a_number=EvaluationRuleFacade.get_move_number(
                        is_king=evaluation_table_property.is_king_size_of_a,
                        is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board),
                b_number=EvaluationRuleFacade.get_move_number(
                        is_king=evaluation_table_property.is_king_size_of_b,
                        is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board))
