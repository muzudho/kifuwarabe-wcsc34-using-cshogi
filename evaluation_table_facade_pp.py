from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_p import EvaluationRuleP
from evaluation_rule_pp import EvaluationRulePp
from evaluation_table_size_facade_pp import EvaluationTableSizeFacadePp
from move import Move


class EvaluationTableFacadePp():
    """評価値テーブル　ＰＰ"""


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
        table_size_obj = EvaluationTableSizeFacadePp.create_it()

        a_size = EvaluationRuleP.get_piece_move_number()
        b_size = EvaluationRuleP.get_piece_move_number()

        return EvaluationTableMm(
                file_number=file_number,
                file_name=file_name,
                table_size_obj=table_size_obj,
                list_of_move_size=[a_size, b_size],
                raw_mm_table=raw_mm_table,
                is_king_size_of_a=False,
                is_king_size_of_b=False,
                is_file_modified=is_file_modified)


    @staticmethod
    def get_pq_policy(
            pq_table_obj,
            p_obj,
            q_obj,
            turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        pq_index = EvaluationRulePp.get_pq_index_by_2_moves(
                p_obj=p_obj,
                q_obj=q_obj,
                turn=turn)

        return pq_table_obj.get_policy_by_mm_index(pq_index)


    @staticmethod
    def make_move_as_usi_and_policy_dictionary_2(
            pq_table_obj,
            p_move_collection_as_usi,
            q_move_collection_as_usi,
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
        for p_as_usi in p_move_collection_as_usi:
            p_obj = Move.from_usi(p_as_usi)
            sum_policy = 0

            # 客体と総当たり
            for q_as_usi in q_move_collection_as_usi:
                q_obj = Move.from_usi(q_as_usi)
                sum_policy += EvaluationTableFacadePp.get_pq_policy(
                        pq_table_obj=pq_table_obj,
                        a_move_obj=p_obj,
                        b_move_obj=q_obj,
                        turn=turn)

            move_as_usi_and_policy_dictionary[p_as_usi] = sum_policy

        return move_as_usi_and_policy_dictionary
