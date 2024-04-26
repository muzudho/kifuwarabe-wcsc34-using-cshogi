import cshogi
import os
from evaluation_configuration import EvaluationConfiguration
from move import Move
from move_helper import MoveHelper

class EvaluationMmTable():
    """評価値ＭＭテーブル

    USIプロトコルの指し手の符号を M (Move) と呼ぶとする
    M と M の関係を MM と呼ぶとする

    評価値テーブルは MM である

    旧：　さらに自軍を F（Friend）、相手を O（Opponent） と呼ぶとし、

    旧：　玉の合法手を K（King）、
    新：　自玉の合法手を K（King）、敵玉の合法手を L（next K） と呼ぶ

    旧：　玉以外の合法手を M (Minions) と呼ぶとする。
    新：　自軍の玉以外の合法手を P (Piece) と呼ぶとする
    新：　敵軍の玉以外の合法手を Q (next P) と呼ぶとする

    新：　K と P の関係を KP、
    新：　P と P の関係を PP、
    新：　K と O の関係を KO、
    新：　P と O の関係を PO

    と呼ぶ
    """


    def __init__(
            self,
            file_number,
            move_size,
            table_size,
            is_symmetrical_connected,
            evaluation_mm_table,
            is_file_modified):
        """初期化

        Parameters
        ----------
        is_symmetrical_connected : bool
            左右対称の盤か？
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真

        指し手は２種類
        ============

        (1) 駒を指す符号
        (2) resign （投了）や、 win （入玉勝ち宣言）などの文字列

        この評価関数は上記 (1) のみを取り扱う


        駒を指す符号の構造
        ================

        以下のもので構成される

        (1) src     移動元の８１マス または 打つ駒７種類
        (2) dst     移動先の８１マス
        (3) pro     成るか？

        上記(1),(2),(3) の組み合わせの数は、以下の通り

            (81 + 7) * 81 * 2 = 14_256       ... fully_connected_move 数

        実用上、駒はワープできるわけではないので本当はこの数より少なくできるはずですが、
        実装方法が思い浮かばないので、このまま全結合とします


        fully_connected_move 数を２つの組み合わせにすると、以下の通り

            (14256 - 1) * 14256 = 203_219_280       ... fully_connected_table_size 数

        ----------

        しかし、家のＰＣでこのサイズの配列を２つ読み込んで２つのエンジンで対局させることはできなかったので、
        左右対称と仮定して、９筋ではなく、５筋にする。

            (5 * 9 + 7) * (5 * 9) * 2 = 4_680     ... symmetrical_connected_move 数


            (4_680 - 1) * 4_680 = 21_897_720    ... symmetrical_connected_table_size 数

        ----------

        評価値テーブルのセル値は、 0,1 の２値とする

        (2024-04-12 fri)
            評価値テーブルは先手から見たものとし、後手番では
            （テーブルを１８０°回転させるのではなく）指し手を１８０°回転させて評価値テーブルを利用するものとする

        ----------
        """
        self._file_number = file_number
        self._move_size = move_size
        self._table_size = table_size
        self._is_symmetrical_connected = is_symmetrical_connected
        self._evaluation_mm_table = evaluation_mm_table
        self._is_file_modified = is_file_modified


    @property
    def is_file_modified(self):
        return self._is_file_modified


    @is_file_modified.setter
    def is_file_modified(self, value):
        self._is_file_modified = value


    @property
    def is_symmetrical_connected(self):
        return self._is_symmetrical_connected


    @property
    def evaluation_mm_table(self):
        return self._evaluation_mm_table


    def get_table_index_by_2_moves(
            self,
            move_a_obj,
            move_b_obj,
            turn):
        """指し手２つの組み合わせインデックス"""

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if move_a_obj.as_usi == move_b_obj.as_usi:
            return 0

        # 後手なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        if turn == cshogi.WHITE:
            move_a_obj = MoveHelper.flip_turn(move_a_obj)
            move_b_obj = MoveHelper.flip_turn(move_b_obj)

        index_a = EvaluationConfiguration.get_table_index_by_move(
                move=move_a_obj,
                is_symmetrical_connected=self._is_symmetrical_connected)
        index_b = EvaluationConfiguration.get_table_index_by_move(
                move=move_b_obj,
                is_symmetrical_connected=self._is_symmetrical_connected)

        move_indexes = [index_a, index_b]
        move_indexes.sort()

        # 昇順
        if index_a <= index_b:
            index = index_a * self._move_size + index_b
            #print(f"[DEBUG] 昇順 a:{index_a:3} b:{index_b:3} index:{index}", flush=True)

        # 降順
        else:
            index = index_b * self._move_size + index_a

        return index


    def get_evaluation_value(self, move_a_obj, move_b_obj, turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        index = self.get_table_index_by_2_moves(
                move_a_obj,
                move_b_obj,
                turn)
        #print(f"[DEBUG] 逆順 b:{index_b:3} a:{index_a:3} index:{index}", flush=True)

        try:
            # 古いデータには 2 が入っているので、 2 は　1 に変換する
            if self._evaluation_mm_table[index] == 2:
                self._evaluation_mm_table[index] = 1

        except IndexError as e:
            # 例： table length: 70955352  index: 102593390  except: list index out of range
            print(f"table length: {len(self._evaluation_mm_table)}  index: {index}  except: {e}")
            raise

        return self._evaluation_mm_table[index]


    def make_move_as_usi_and_policy_dictionary(
            self,
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_pieces_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        sorted_friend_king_legal_move_list_as_usi : list
            USIプロトコルでの符号表記の指し手の配列。辞書順で昇順にソート済み
        sorted_friend_pieces_legal_move_list_as_usi : list
            USIプロトコルでの符号表記の指し手の配列。辞書順で昇順にソート済み
        sorted_opponent_legal_move_set_as_usi : set
            相手の指し手
        turn
            手番
        """

        # 指し手に評価値を付ける
        move_as_usi_and_score_dictionary = {}

        list_of_sorted_friend_legal_move_list_as_usi = [
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_pieces_legal_move_list_as_usi,
        ]

        for sorted_friend_legal_move_list_as_usi in list_of_sorted_friend_legal_move_list_as_usi:
            for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
                move_a_obj = Move(move_a_as_usi)
                # 総当たりで評価値を計算
                sum_value = 0

                # （ＦＦ）：　自軍の指し手Ａと、自軍の指し手Ｂ
                for sorted_king_legal_move_list_as_usi_2 in list_of_sorted_friend_legal_move_list_as_usi:
                    for move_b_as_usi in sorted_king_legal_move_list_as_usi_2:
                        move_b_obj = Move(move_b_as_usi)
                        sum_value += self.get_evaluation_value(move_a_obj, move_b_obj, turn)

                # （ＦＯ）：　自軍の指し手Ａと、相手の指し手Ｂ
                for move_b_as_usi in opponent_legal_move_set_as_usi:
                    move_b_obj = Move(move_b_as_usi)
                    sum_value += self.get_evaluation_value(move_a_obj, move_b_obj, turn)

                move_as_usi_and_score_dictionary[move_a_as_usi] = sum_value

        return move_as_usi_and_score_dictionary
