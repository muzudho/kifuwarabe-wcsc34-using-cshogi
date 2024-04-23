import cshogi
import os
import random
import datetime
from move import Move


class EvaluationFkfPlusFkoTable():
    """評価値ＦｋＦ＋ＦｋＯテーブル

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
    と呼ぶとき、

    このテーブルを使って FkF + FkO の評価値を返す
    """

    def __init__(self, file_number):
        self._file_number = file_number
        self._file_name = f'n{file_number}_eval_ke.txt'
        self._file_modified = False

        self._move_size = 14256
        self._table_size = 1_154_736
        self._evaluation_ke_table = [0] * self._table_size
        """評価値KEテーブル

            玉（K）は８１マスのいずれかを指す。
            file を筋 0～8、
            rank を段 0～8 として、
            k = rank * 9 + file
            となる

            指し手（E）の種類は、 src, dst, pro で構成されるものの他、 resign 等の文字列がいくつかある。
            src は盤上の 81マスと、駒台の７種類の駒。

                (81 + 7)

            dst は盤上の 81マス。

                81

            pro は成りとそれ以外の２種類。

                2

            この数を配列のインデックスにしたときの範囲は、

                (81 + 7) * 81 * 2 = 14256

            K と E の組み合わせの数は

                81 * 14256 = 1_154_736

            ----------

            値は、 -1,0,1 を入れる代わりに、+1 して 0,1,2 を入れてある。保存時にマイナスの符号で１文字使うのを省くため

            ----------

            TODO 駒は任意の点ＡからＢへ移動できるわけではないので、本来はもっと圧縮できるはず

            ----------

        """


    def exists_file(self):
        """ファイルは存在するか？"""
        return os.path.isfile(self._file_name)


    def reset_to_random_table(self):
        """ランダム値の入った評価値テーブルを新規作成する"""
        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random ke evaluation table in memory ...", flush=True)

        for index in range(0, self._table_size):
            # -1,0,1 を保存するとマイナスの符号で文字数が多くなるので、+1 して 0,1,2 で保存する
            self._evaluation_ee_table[index] = random.randint(0,2)

        print(f"[{datetime.datetime.now()}] evaluation table maked in memory", flush=True)
        self._file_modified = True


    def load_evaluation_from_file(self):
        """ファイルを読込む"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {self._file_name} file ...", flush=True)

        try:
            # ファイルの存在チェックを済ませておくこと
            with open(self._file_name, 'r', encoding="utf-8") as f:
                text = f.read()
                print(f"[{datetime.datetime.now()}] {self._file_name} read", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{self._file_name}] file error. {ex}")
            raise

        # 隙間のないテキストを１文字ずつ分解
        tokens = list(text)
        # 整数型へ変換したあと、またリストに入れる
        self._evaluation_ee_table = list(map(int,tokens))
        self._file_modified = False
        print(f"[{datetime.datetime.now()}] {self._file_name} file loaded", flush=True)


    def load_from_file_or_random_table(self):
        """評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する"""

        print(f"[{datetime.datetime.now()}] {self._file_name} file exists check ...", flush=True)

        # 評価関数テーブル・ファイルが存在しないとき
        if not self.exists_file():
            self.reset_to_random_table()

        else:
            self.load_evaluation_from_file()


    def get_table_index(self, move_as_usi, sq_of_king, turn):
        """ＫＥテーブルのインデックス

        Parameters
        ----------
        move_as_usi : str
            指し手の符号。USI表記
        sq_of_king : int
            指定の玉のいるマス
        turn : int
            手番の指定
        """

        # 後手なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        if turn == cshogi.WHITE:
            move_as_usi = Move.flip_turn(move_as_usi)
            sq_of_king = 81 - sq_of_king

        return sq_of_king * self._move_size + Move(move_as_usi).get_table_index(
                is_symmetrical_board=False)


    def get_evaluation_value(self, move_as_usi, turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        index = self.get_table_index(move_as_usi, turn)

        # 0,1,2 が保存されているので、 -1 すると、 -1,0,1 になる。マイナスの符号が付くと文字数が多くなるのでこうしている
        return self._evaluation_ke_table[index] - 1


    def make_move_as_usi_and_policy_dictionary(
            self,
            friend_king_sq,
            opponent_king_sq,
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_others_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        friend_king_sq : int
            自玉のマス
        opponent_king_sq : int
            敵玉のマス
        sorted_friend_king_legal_move_list_as_usi : list
            USIプロトコルでの符号表記の指し手の配列。辞書順で昇順にソート済み。自玉の合法手
        sorted_friend_others_legal_move_list_as_usi : list
            USIプロトコルでの符号表記の指し手の配列。辞書順で昇順にソート済み。自軍の自玉以外の合法手
        sorted_opponent_legal_move_set_as_usi : set
            相手の指し手
        turn
            手番
        """
        #return {} # TODO

        # 指し手に評価値を付ける
        move_as_usi_and_score_dictionary = {}

        for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
            # 総当たりで評価値を計算
            sum_value = 0

            # （ＦＦ）：　自軍の玉のいるマスと、自軍の指し手Ａ
            for move_b_as_usi in sorted_friend_legal_move_list_as_usi:
                sum_value += self.get_evaluation_value(move_a_as_usi, move_b_as_usi, turn)

            # （ＦＯ）：　敵軍の玉のいるマスと、敵軍の指し手Ｂ
            for move_b_as_usi in opponent_legal_move_set_as_usi:
                sum_value += self.get_evaluation_value(move_a_as_usi, move_b_as_usi, turn)

            move_as_usi_and_score_dictionary[move_a_as_usi] = sum_value

        return move_as_usi_and_score_dictionary
