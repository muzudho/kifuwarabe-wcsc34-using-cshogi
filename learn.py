import random
from move import Move
from move_helper import MoveHelper


class Learn():
    """学習部"""


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
