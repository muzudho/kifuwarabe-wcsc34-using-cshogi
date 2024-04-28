from evaluation_rule_k import EvaluationRuleK
from evaluation_table_size import EvaluationTableSize


class EvaluationTableSizeFacadeKk():


    @staticmethod
    def create_it():
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

        (file * rank) * around = k_patterns
        (   9 *    9) *      8 =        648

        組み合わせだと n * (n-1) のようにしたいところだが実装が難しいので単に n * n にするとし、これを関係と呼ぶとき

        KL関係なら、以下で足りる

        k_patterns * k_patterns = kk_relation
               648 *        648 =      419904
        """

        return EvaluationTableSize(
                is_king_of_a=True,
                is_king_of_b=True,
                a_number=EvaluationRuleK.get_king_move_number(),
                b_number=EvaluationRuleK.get_king_move_number())
