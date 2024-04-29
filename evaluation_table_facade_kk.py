from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_k import EvaluationRuleK
from evaluation_rule_kk import EvaluationRuleKk
from evaluation_table_size_facade_kk import EvaluationTableSizeFacadeKk
from move import Move


class EvaluationTableFacadeKk():
    """評価値テーブル　ＫＫ"""


    @staticmethod
    def create_it(
            file_number,
            file_name,
            raw_mm_table,
            is_file_modified):
        """初期化

        Parameters
        ----------
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        # テーブル・サイズ。計算過程付き
        table_size_obj = EvaluationTableSizeFacadeKk.create_it()

        k_size = EvaluationRuleK.get_king_move_number()
        l_size = EvaluationRuleK.get_king_move_number()

        return EvaluationTableMm(
                file_number=file_number,
                file_name=file_name,
                table_size_obj=table_size_obj,
                list_of_move_size=[k_size, l_size],
                raw_mm_table=raw_mm_table,
                is_king_size_of_a=True,
                is_king_size_of_b=True,
                is_file_modified=is_file_modified)


    @staticmethod
    def make_move_as_usi_and_policy_dictionary_2(
            mm_table_obj,
            a_move_collection_as_usi,
            b_move_collection_as_usi,
            turn,
            get_kl_index_by_2_moves):
        """指し手に評価値を付ける

        Parameters
        ----------
        a_move_set_as_usi : set
            指し手の収集（主体）
        b_move_set_as_usi : set
            指し手の収集（客体）
        turn : int
            手番
        get_kl_index_by_2_moves : func
            ２つの指し手を渡すと、KL関係のテーブル番地を返す関数
        """

        # 指し手に評価値を付ける
        move_as_usi_and_policy_dictionary = {}

        # 主体
        for a_as_usi in a_move_collection_as_usi:
            a_obj = Move.from_usi(a_as_usi)
            sum_policy = 0

            # 客体と総当たり
            for b_as_usi in b_move_collection_as_usi:
                b_obj = Move.from_usi(b_as_usi)

                # ２つの指し手を、テーブルの番地に変換
                kl_index = get_kl_index_by_2_moves(
                        k_obj=a_obj,
                        l_obj=b_obj,
                        turn=turn)

                # テーブルの番地を、ポリシー値に変換
                policy = mm_table_obj.get_policy_by_mm_index(kl_index)

                # 総和
                sum_policy += policy

            move_as_usi_and_policy_dictionary[a_as_usi] = sum_policy

        return move_as_usi_and_policy_dictionary
