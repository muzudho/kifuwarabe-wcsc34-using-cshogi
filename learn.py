import cshogi
import random
import datetime
from move import Move
from move_helper import MoveHelper


class Learn():
    """学習部"""


    @staticmethod
    def update_evaluation_table(
            evaluation_mm_table_obj,
            canditates_memory,
            result_file):
        """結果ファイルを読み込んで、持将棋や、負けかどうか判定する。
        そうなら、評価値テーブルのうち、指した手（CanditatesMemory）に関連する箇所をランダムに変更してみる"""

        if result_file.exists():
            # 結果ファイルを読込
            tokens = result_file.read().split(' ')
            result_text = tokens[0]
            turn_text = tokens[1]

            if turn_text == 'black':
                turn = cshogi.BLACK
            elif turn_text == 'white':
                turn = cshogi.WHITE
            else:
                raise ValueError(f"failed to turn: '{turn_text}'")

            # 前回の対局で、負けるか、引き分けなら、内容を変えます
            if result_text in ('lose', 'draw'):
                Learn.modify_mm_table(
                        evaluation_mm_table_obj=evaluation_mm_table_obj,
                        a_is_king=False,    # TODO
                        b_is_king=False,    # TODO
                        canditates_memory=canditates_memory,
                        turn=turn)
                print(f"[{datetime.datetime.now()}] {evaluation_mm_table_obj._file_name} file updated", flush=True)


    @staticmethod
    def modify_mm_table(
            evaluation_mm_table_obj,
            a_is_king,
            b_is_king,
            canditates_memory,
            turn):
        """指した手の評価値を適当に変更します"""

        for move_a_as_usi in canditates_memory.move_set:
            for move_b_as_usi in canditates_memory.move_set:

                a_move_obj = Move(move_a_as_usi)
                b_move_obj = Move(move_b_as_usi)

                mm_index = evaluation_mm_table_obj.get_mm_index_by_2_moves(
                        a_move_obj=a_move_obj,
                        a_is_king=a_is_king,
                        b_move_obj=b_move_obj,
                        b_is_kind=b_is_king,
                        turn=turn)

                # 値は 0, 1 の２値。乱数で単純に上書き。つまり、変わらないこともある
                evaluation_mm_table_obj.evaluation_mm_table[mm_index] = random.randint(0,1)

                #
                # 左右反転して、同じようにしたい
                #
                reversed_a_move_obj = MoveHelper.flip_horizontal(a_move_obj)
                reversed_b_move_obj = MoveHelper.flip_horizontal(b_move_obj)

                mm_index = evaluation_mm_table_obj.get_mm_index_by_2_moves(
                        a_move_obj=reversed_a_move_obj,
                        a_is_king=False,    # TODO
                        b_move_obj=reversed_b_move_obj,
                        b_is_kind=False,    # TODO
                        turn=turn)

                # 値は 0, 1 の２値。乱数で単純に上書き。つまり、変わらないこともある
                evaluation_mm_table_obj.evaluation_mm_table[mm_index] = random.randint(0,1)


        evaluation_mm_table_obj.is_file_modified = True
