import cshogi
import random
import datetime
from evaluation_rule_mm import EvaluationRuleMm
from move import Move
from move_helper import MoveHelper


class Learn():
    """学習部"""


    @staticmethod
    def update_evaluation_table(
            mm_table_obj,
            canditates_memory,
            result_file,
            get_a_index_by_move,
            get_b_index_by_move):
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
                        mm_table_obj=mm_table_obj,
                        canditates_memory=canditates_memory,
                        turn=turn,
                        get_a_index_by_move=get_a_index_by_move,
                        get_b_index_by_move=get_b_index_by_move)
                print(f"[{datetime.datetime.now()}] {mm_table_obj._file_name} file updated", flush=True)


    @staticmethod
    def modify_mm_table(
            mm_table_obj,
            canditates_memory,
            turn,
            get_a_index_by_move,
            get_b_index_by_move):
        """指した手の評価値を適当に変更します

        Parameters
        ----------
        turn : int
            手番
        get_a_index_by_move : func
            指し手 a のテーブル番地を求める
        get_b_index_by_move : func
            指し手 b のテーブル番地を求める
        """

        for a_as_usi in canditates_memory.move_set:
            for b_as_usi in canditates_memory.move_set:

                a_obj = Move.from_usi(a_as_usi)
                b_obj = Move.from_usi(b_as_usi)

                # FIXME KK,KP,PP で分けたい
                mm_index = EvaluationRuleMm.get_mm_index_by_2_moves(
                        a_obj=a_obj,
                        b_obj=b_obj,
                        turn=turn,
                        b_index_size=mm_table_obj.list_of_move_size[1],
                        get_a_index_by_move=get_a_index_by_move,
                        get_b_index_by_move=get_b_index_by_move)

                if len(mm_table_obj.raw_mm_table) <= mm_index:
                    # 範囲外エラー
                    # 無視
                    pass
                else:
                    # 値は 0, 1 の２値。乱数で単純に上書き。つまり、変わらないこともある
                    mm_table_obj.raw_mm_table[mm_index] = random.randint(0,1)

                #
                # 盤を左右反転して、同じように学習したい
                #
                # reverse
                rev_a_obj = MoveHelper.flip_horizontal(a_obj)
                rev_b_obj = MoveHelper.flip_horizontal(b_obj)

                mm_index = EvaluationRuleMm.get_mm_index_by_2_moves(
                        a_obj=rev_a_obj,
                        b_obj=rev_b_obj,
                        turn=turn,
                        b_index_size=mm_table_obj.list_of_move_size[1],
                        get_a_index_by_move=get_a_index_by_move,
                        get_b_index_by_move=get_b_index_by_move)

                if len(mm_table_obj.raw_mm_table) <= mm_index:
                    # 範囲外エラー
                    # 無視
                    pass
                else:
                    # 値は 0, 1 の２値。乱数で単純に上書き。つまり、変わらないこともある
                    mm_table_obj.raw_mm_table[mm_index] = random.randint(0,1)


        mm_table_obj.is_file_modified = True
