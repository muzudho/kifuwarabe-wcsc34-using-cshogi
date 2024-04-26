import cshogi
import random
import datetime
from move import Move
from move_helper import MoveHelper


class Learn():
    """学習部"""


    @staticmethod
    def update_evaluation_table(
            evaluation_ee_table_obj,
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
                Learn.modify_table(
                        evaluation_ee_table_obj=evaluation_ee_table_obj,
                        canditates_memory=canditates_memory,
                        turn=turn)
                print(f"[{datetime.datetime.now()}] {evaluation_ee_table_obj._file_name} file updated", flush=True)


    @staticmethod
    def modify_table(evaluation_ee_table_obj, canditates_memory, turn):
        """指した手の評価値を適当に変更します"""

        for move_a_as_usi in canditates_memory.move_set:
            for move_b_as_usi in canditates_memory.move_set:

                move_a_obj = Move(move_a_as_usi)
                move_b_obj = Move(move_b_as_usi)

                index = evaluation_ee_table_obj.get_table_index_by_2_moves(
                        move_a_obj,
                        move_b_obj,
                        turn)

                # 値は 0, 1 の２値。乱数で単純に上書き。つまり、変わらないこともある
                evaluation_ee_table_obj.evaluation_ee_table[index] = random.randint(0,1)

                #
                # 左右反転して、同じようにしたい
                #
                reversed_move_a_obj = MoveHelper.flip_horizontal(move_a_obj)
                reversed_move_b_obj = MoveHelper.flip_horizontal(move_b_obj)

                index = evaluation_ee_table_obj.get_table_index_by_2_moves(
                        reversed_move_a_obj,
                        reversed_move_b_obj,
                        turn)

                # 値は 0, 1 の２値。乱数で単純に上書き。つまり、変わらないこともある
                evaluation_ee_table_obj.evaluation_ee_table[index] = random.randint(0,1)


        evaluation_ee_table_obj.is_file_modified = True
