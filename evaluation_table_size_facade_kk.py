from evaluation_rule_kk import EvaluationRuleKk
from evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacadeKk():


    @staticmethod
    def create_it(
            evaluation_table_property):
        """ＫＫ関係のテーブル・サイズ

        玉は１マスしか動かないから、指し手は最大８手。
        成りもしないし、打もないし、ワープもしないから、
        １局面につき指し手は最大６４パターンしかないはず。

        相対SQは以下の通り

        +----+----+----+
        | +8 | -1 |-10 |
        |    |    |    |
        +----+----+----+
        | +9 | You| -9 |
        |    |    |    |
        +----+----+----+
        |+10 | +2 | -8 |
        |    |    |    |
        +----+----+----+

        指し手は例えば　5g5f　なら相対SQは -1 が該当する。
        以下の通りで充分だ

        81 *    8  *      8 =      5_184
        (file * rank) * around = k_patterns

        組み合わせだと n * (n-1) のようにしたいところだが実装が難しいので単に n * n にするとし、これを関係と呼ぶとき

        KL関係なら、以下で足りる

            5_184 *       5_184 =  26_873_856
        k_patterns * (k_patterns = kk_relation

        ※ PP関係が 203_219_280 あるので、１桁は少ない
        """

        # FIXME バージョン対応したい
        return EvaluationTableSize(
                is_king_of_a=evaluation_table_property.is_king_size_of_a,
                is_king_of_b=evaluation_table_property.is_king_size_of_b,
                is_symmetrical_half_board=evaluation_table_property.is_symmetrical_half_board,
                a_number=EvaluationRuleKk.get_move_number(),
                b_number=EvaluationRuleKk.get_move_number())
