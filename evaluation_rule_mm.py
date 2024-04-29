from move import Move


class EvaluationRuleMm():


    @staticmethod
    def make_move_as_usi_and_policy_dictionary_2(
            mm_table_obj,
            a_move_collection_as_usi,
            b_move_collection_as_usi,
            turn,
            get_mm_index_by_2_moves):
        """指し手に評価値を付ける

        Parameters
        ----------
        a_move_set_as_usi : set
            指し手の収集（主体）
        b_move_set_as_usi : set
            指し手の収集（客体）
        turn : int
            手番
        get_mm_index_by_2_moves : func
            ２つの指し手を渡すと、MM関係のテーブル番地を返す関数
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
                mm_index = get_mm_index_by_2_moves(
                        a_obj=a_obj,
                        b_obj=b_obj,
                        turn=turn)

                # テーブルの番地を、ポリシー値に変換
                policy = mm_table_obj.get_policy_by_mm_index(mm_index)

                # 総和
                sum_policy += policy

            move_as_usi_and_policy_dictionary[a_as_usi] = sum_policy

        return move_as_usi_and_policy_dictionary
