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
            file_name,
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
        self._file_name = file_name
        self._move_size = move_size
        self._table_size = table_size
        self._is_symmetrical_connected = is_symmetrical_connected
        self._evaluation_mm_table = evaluation_mm_table
        self._is_file_modified = is_file_modified


    @property
    def file_name(self):
        return self._file_name


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
            a_move_obj,
            b_move_obj,
            turn):
        """指し手２つの組み合わせインデックス"""

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if a_move_obj.as_usi == b_move_obj.as_usi:
            return 0

        # 後手なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        if turn == cshogi.WHITE:
            a_move_obj = MoveHelper.flip_turn(a_move_obj)
            b_move_obj = MoveHelper.flip_turn(b_move_obj)

        a_index = EvaluationConfiguration.get_m_index_by_move(
                move=a_move_obj,
                is_symmetrical_connected=self._is_symmetrical_connected)
        b_index = EvaluationConfiguration.get_m_index_by_move(
                move=b_move_obj,
                is_symmetrical_connected=self._is_symmetrical_connected)

        move_indexes = [a_index, b_index]
        move_indexes.sort()

        # 昇順
        if a_index <= b_index:
            index = a_index * self._move_size + b_index
            #print(f"[DEBUG] 昇順 a:{a_index:3} b:{b_index:3} index:{index}", flush=True)

        # 降順
        else:
            index = b_index * self._move_size + a_index

        return index


    def get_evaluation_value(self, a_move_obj, b_move_obj, turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        index = self.get_table_index_by_2_moves(
                a_move_obj,
                b_move_obj,
                turn)
        #print(f"[DEBUG] 逆順 b:{index_b:3} a:{index_a:3} index:{index}", flush=True)

        try:
            # 古いデータには 2 が入っているので、 2 は　1 に変換する
            if self._evaluation_mm_table[index] == 2:
                self._evaluation_mm_table[index] = 1

        except IndexError as e:
            # 例： table length: 70955352  index: 102593390  except: list index out of range
            print(f"table length:{len(self._evaluation_mm_table)}  index:{index}  a_move_obj.as_usi:{a_move_obj.as_usi}  b_move_obj.as_usi:{b_move_obj.as_usi}  turn:{turn}  except: {e}")
            raise

        return self._evaluation_mm_table[index]


    def make_move_as_usi_and_policy_dictionary_2(
            self,
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
        turn
            手番
        """

        # 指し手に評価値を付ける
        move_as_usi_and_policy_dictionary = {}

        # 主体
        for a_move_as_usi in a_move_collection_as_usi:
            a_move_obj = Move(a_move_as_usi)
            sum_value = 0

            # 客体と総当たり
            for b_move_as_usi in b_move_collection_as_usi:
                b_move_obj = Move(b_move_as_usi)
                sum_value += self.get_evaluation_value(a_move_obj, b_move_obj, turn)

            move_as_usi_and_policy_dictionary[a_move_as_usi] = sum_value

        return move_as_usi_and_policy_dictionary
