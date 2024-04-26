import cshogi
import os
import random
import datetime
from move import Move


class EvaluationEeTable():
    """評価値ＥＥテーブル

    合法手（つまり利き）を E （Effect）と呼ぶとし、

    現局面（自分の手番）の合法手を E1、
    E1 を指したときの局目（相手の手番）の合法手を E2 とする

    Eは e1, e2, ... en の集合とし、
    評価値テーブルは
    e1 e1
    e1 e2
    e1 e3
    ...
    en en
    の形を取る。これを EE と呼ぶとする

    さらに自軍を F（Friend）、相手を O（Opponent） と呼ぶとし、
    玉の合法手を K（King）、玉以外の合法手を M (Minions) と呼ぶとする。
    Fk（自玉の合法手）と F（自分の合法手）の関係を FkF、
    Fm（自軍の玉以外の合法手）と F（自分の合法手）の関係を FmF、
    Fk（自玉の合法手）と O（相手の合法手）の関係を FkO、
    Fm（自軍の玉以外の合法手）と O（相手の合法手）の関係を FmO、
    と呼ぶ
    """


    def __init__(
            self,
            file_number,
            evaluation_kind,
            file_name,
            bin_file_name,
            bin_v2_file_name,
            move_size,
            table_size,
            is_symmetrical_connected,
            evaluation_ee_table,
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

            (81 + 7) * 81 * 2 = 14256       ... fully_connected_move 数

        実用上、駒はワープできるわけではないので本当はこの数より少なくできるはずですが、
        実装方法が思い浮かばないので、このまま全結合とします


        fully_connected_move 数を２つの組み合わせにすると、以下の通り

            (14256 - 1) * 14256 = 203_219_280       ... fully_connected_table_size 数

        ----------

        しかし、家のＰＣでこのサイズの配列を２つ読み込んで２つのエンジンで対局させることはできなかったので、
        左右対称と仮定して、９筋ではなく、５筋にする。

            (5 * 9 + 7) * 81 * 2 = 8424     ... symmetrical_connected_move 数
            (8424 - 1) * 8424 = 70_955_352  ... symmetrical_connected_table_size 数

        ----------

        評価値テーブルのセル値は、 0,1 の２値とする

        (2024-04-12 fri)
            評価値テーブルは先手から見たものとし、後手番では
            （テーブルを１８０°回転させるのではなく）指し手を１８０°回転させて評価値テーブルを利用するものとする

        ----------
        """
        self._file_number = file_number
        self._evaluation_kind = evaluation_kind
        self._file_name = file_name                 # 旧
        self._bin_file_name = bin_file_name         # 旧
        self._bin_v2_file_name = bin_v2_file_name   # 新
        self._move_size = move_size
        self._table_size = table_size
        self._is_symmetrical_connected = is_symmetrical_connected
        self._evaluation_ee_table = evaluation_ee_table
        self._is_file_modified = is_file_modified


    @property
    def is_file_modified(self):
        return self._is_file_modified


    @property
    def evaluation_ee_table(self):
        return self._evaluation_ee_table


    def exists_text_file(self):
        """テキスト・ファイルは存在するか？"""
        return os.path.isfile(self._file_name)


    def exists_binary_file(self):
        """バイナリ・ファイルは存在するか？"""
        return os.path.isfile(self._bin_file_name)


    def exists_binary_v2_file(self):
        """バイナリV2ファイルは存在するか？"""
        return os.path.isfile(self._bin_v2_file_name)


    def get_table_index(self, move_a_as_usi, move_b_as_usi, turn):
        """指し手２つの組み合わせインデックス"""

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if move_a_as_usi == move_b_as_usi:
            return 0

        # 後手なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        if turn == cshogi.WHITE:
            move_a_as_usi = Move.flip_turn(move_a_as_usi)
            move_b_as_usi = Move.flip_turn(move_b_as_usi)

        index_a = Move(move_a_as_usi).get_table_index(
                is_symmetrical_board=True)
        index_b = Move(move_b_as_usi).get_table_index(
                is_symmetrical_board=True)

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


    def update_evaluation_table(self, canditates_memory, result_file):
        """結果ファイルを読み込んで、持将棋や、負けていれば、内容をランダムに変更してみる"""

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
                self.modify_table(result_text, canditates_memory, turn)
                print(f"[{datetime.datetime.now()}] {self._file_name} file updated", flush=True)


    def get_evaluation_value(self, move_a_as_usi, move_b_as_usi, turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        index = self.get_table_index(move_a_as_usi, move_b_as_usi, turn)
        #print(f"[DEBUG] 逆順 b:{index_b:3} a:{index_a:3} index:{index}", flush=True)

        # 古いデータには 2 が入っているので、 2 は　1 に変換する
        if self._evaluation_ee_table[index] == 2:
            self._evaluation_ee_table[index] = 1

        return self._evaluation_ee_table[index]


    def make_move_as_usi_and_policy_dictionary(
            self,
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_minions_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        sorted_friend_king_legal_move_list_as_usi : list
            USIプロトコルでの符号表記の指し手の配列。辞書順で昇順にソート済み
        sorted_friend_minions_legal_move_list_as_usi : list
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
            sorted_friend_minions_legal_move_list_as_usi,
        ]

        for sorted_friend_legal_move_list_as_usi in list_of_sorted_friend_legal_move_list_as_usi:
            for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
                # 総当たりで評価値を計算
                sum_value = 0

                # （ＦＦ）：　自軍の指し手Ａと、自軍の指し手Ｂ
                for sorted_king_legal_move_list_as_usi_2 in list_of_sorted_friend_legal_move_list_as_usi:
                    for move_b_as_usi in sorted_king_legal_move_list_as_usi_2:
                        sum_value += self.get_evaluation_value(move_a_as_usi, move_b_as_usi, turn)

                # （ＦＯ）：　自軍の指し手Ａと、相手の指し手Ｂ
                for move_b_as_usi in opponent_legal_move_set_as_usi:
                    sum_value += self.get_evaluation_value(move_a_as_usi, move_b_as_usi, turn)

                move_as_usi_and_score_dictionary[move_a_as_usi] = sum_value

        return move_as_usi_and_score_dictionary


    def modify_table(self, result_text, canditates_memory, turn):
        """指した手の評価値を適当に変更します。負けたときか、引き分けのときに限る"""

        if result_text in ('lose', 'draw'):
            for move_a_as_usi in canditates_memory.move_set:
                for move_b_as_usi in canditates_memory.move_set:
                    index = self.get_table_index(move_a_as_usi, move_b_as_usi, turn)

                    # 値は 0, 1 の２値。乱数で単純に上書き。つまり、変わらないこともある
                    self._evaluation_ee_table[index] = random.randint(0,1)

            self._is_file_modified = True
