import cshogi
import os
import random
import datetime
from move import Move


class EvaluationKfPlusKoTable():
    """自玉×自軍の合法手＋相手玉×自軍の合法手の関係

    玉の位置を K （King）と呼ぶとし、要素は k1, k2, ... k81 まである。
    合法手（つまり利き）を E （Effect）と呼ぶとする。

    E はさらに自軍と相手とに分け、
    自軍を Friend、相手を Opponent と呼ぶとし、
    自玉と自軍の合法手の関係を KF、
    相手玉と自軍の合法手との関係を KO と呼ぶ

    評価値テーブルは
    k1 e1
    k1 e2
    k1 e3
    ...
    k81 en
    の形を取る。これを KE と呼ぶ


    この KE テーブルを使って KF + KO の評価値を返す
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


    def get_table_index(self, move_as_usi, sq_of_friend_king, sq_of_opponent_king, turn):
        """指し手２つの組み合わせインデックス
    
        Parameters
        ----------
        move_as_usi : str
            指し手の符号。USI表記
        sq_of_friend_king : int
            自玉の位置
        sq_of_opponent_king : int
            敵玉の位置
        turn : int
            手番の指定
        """

        # 後手なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        if turn == cshogi.WHITE:
            move_as_usi = Move.flip_turn(move_as_usi)

        return self.get_table_index_from_move_as_usi(move_as_usi)


    def make_move_and_policy_dictionary(
            self,
            sorted_friend_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        sorted_friend_legal_move_list_as_usi : list
            USIプロトコルでの符号表記の指し手の配列。辞書順で昇順にソート済み
        sorted_opponent_legal_move_set_as_usi : set
            相手の指し手
        turn
            手番
        """
        return {} # TODO
