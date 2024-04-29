import cshogi
from move import Move
from move_helper import MoveHelper


class EvaluationRuleMm():


    @staticmethod
    def get_mm_index_by_2_moves(
            a_obj,
            b_obj,
            turn,
            b_index_size,
            get_a_index_by_move,
            get_b_index_by_move):
        """指し手２つの関係インデックス

        Parameters
        ----------
        a_obj : Move
            指し手 a
        b_obj : Move
            指し手 b
        turn : int
            手番
        b_index_size : int
            指し手 b のパターン数
            例： EvaluationRuleK.get_king_move_number()
        get_a_index_by_move : func
            指し手 a のテーブル番地を求める
        get_b_index_by_move : func
            指し手 b のテーブル番地を求める
        """

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if a_obj.as_usi == b_obj.as_usi:
            return 0

        # 相手番なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        # 常に自分の盤から見た状態にする
        if turn == cshogi.WHITE:
            a_obj = MoveHelper.flip_turn(a_obj)
            b_obj = MoveHelper.flip_turn(b_obj)

        a_index = get_a_index_by_move(
                move_obj=a_obj)
        b_index = get_b_index_by_move(
                move_obj=b_obj)

        # ab関連。組み合わせは実装が難しいので廃止
        mm_index = a_index * b_index_size + b_index
        return mm_index


    @staticmethod
    def make_move_as_usi_and_policy_dictionary_2(
            mm_table_obj,
            a_move_collection_as_usi,
            b_move_collection_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        a_move_set_as_usi : set
            指し手の収集（主体）
        b_move_set_as_usi : set
            指し手の収集（客体）
        turn : int
            手番
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
                mm_index = EvaluationRuleMm.get_mm_index_by_2_moves(
                        a_obj=a_obj,
                        b_obj=b_obj,
                        turn=turn,
                        b_index_size=mm_table_obj.list_of_move_size[1])

                # テーブルの番地を、ポリシー値に変換
                policy = mm_table_obj.get_policy_by_mm_index(mm_index)

                # 総和
                sum_policy += policy

            move_as_usi_and_policy_dictionary[a_as_usi] = sum_policy

        return move_as_usi_and_policy_dictionary
