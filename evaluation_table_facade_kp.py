from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_k import EvaluationRuleK
from evaluation_rule_p import EvaluationRuleP
from evaluation_rule_kp import EvaluationRuleKp
from evaluation_table_size_facade_kp import EvaluationTableSizeFacadeKp
from move import Move


class EvaluationTableFacadeKp():
    """評価値テーブル　ＫＰ"""


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
        table_size_obj = EvaluationTableSizeFacadeKp.create_it()

        k_size = EvaluationRuleK.get_king_move_number()
        p_size = EvaluationRuleP.get_piece_move_number()

        return EvaluationTableMm(
                file_number=file_number,
                file_name=file_name,
                table_size_obj=table_size_obj,
                list_of_move_size=[k_size, p_size],
                raw_mm_table=raw_mm_table,
                is_king_size_of_a=True,
                is_king_size_of_b=False,
                is_file_modified=is_file_modified)


    @staticmethod
    def get_kp_policy(
            kp_table_obj,
            k_obj,
            p_obj,
            turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        kp_index = EvaluationRuleKp.get_kp_index_by_2_moves(
                k_obj=k_obj,
                p_obj=p_obj,
                turn=turn)

        return kp_table_obj.get_policy_by_mm_index(kp_index)


    @staticmethod
    def make_move_as_usi_and_policy_dictionary_2(
            kp_table_obj,
            k_move_collection_as_usi,
            p_move_collection_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        a_move_set_as_usi : set
            指し手の収集（主体）
        b_move_set_as_usi : set
            指し手の収集（客体）
        turn
            手番
        """

        # 指し手に評価値を付ける
        move_as_usi_and_policy_dictionary = {}

        # 主体
        for k_as_usi in k_move_collection_as_usi:
            k_obj = Move.from_usi(k_as_usi)
            sum_policy = 0

            # 客体と総当たり
            for p_as_usi in p_move_collection_as_usi:
                p_obj = Move.from_usi(p_as_usi)
                sum_policy += EvaluationTableFacadeKp.get_kp_policy(
                        kp_table_obj=kp_table_obj,
                        k_obj=k_obj,
                        p_obj=p_obj,
                        turn=turn)

            move_as_usi_and_policy_dictionary[k_as_usi] = sum_policy

        return move_as_usi_and_policy_dictionary
