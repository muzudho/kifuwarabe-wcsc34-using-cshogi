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

        self._file_name = f'n{file_number}_eval_fkf_fko.txt'            # 旧
        self._bin_file_name = f'n{file_number}_eval_fkf_fko.bin'        # 旧
        self._bin_v2_file_name = f'n{file_number}_eval_fkf_fko_v2.bin'  # 新

        self._file_modified = False

        self._move_size = 8424
        self._table_size = 70_955_352
        self._evaluation_ee_table = [0] * self._table_size
        """評価値EEテーブル

            指し手の種類は、 src, dst, pro で構成されるものの他、 resign 等の文字列がいくつかある。
            src は盤上の 81マスと、駒台の７種類の駒。

                (81 + 7)

            dst は盤上の 81マス。

                81

            pro は成りとそれ以外の２種類。

                2

            この数を配列のインデックスにしたときの範囲は、

                (81 + 7) * 81 * 2 = 14256

            この数を２つの組み合わせにすると

                (14256 - 1) * 14256 = 203_219_280

            ２億超えの組み合わせがある。

            ----------

            しかし、家のＰＣでこのサイズの配列を２つ読み込んで対局させることはできないようだ。
            左右対称と仮定して、９筋ではなく、５筋にする。

                (5 * 9 + 7) * 81 * 2 = 8424
                (8424 - 1) * 8424 = 70_955_352

            ----------

            値は、 -1,0,1 を入れる代わりに、+1 して 0,1,2 を入れてある。保存時にマイナスの符号で１文字使うのを省くため

            ----------

            TODO 駒は任意の点ＡからＢへ移動できるわけではないので、本来はもっと圧縮できるはず

            (2024-04-12 fri) 敵の指し手も利用するように変更

            ----------

        """


    def exists_text_file(self):
        """テキスト・ファイルは存在するか？"""
        return os.path.isfile(self._file_name)


    def exists_binary_file(self):
        """バイナリ・ファイルは存在するか？"""
        return os.path.isfile(self._bin_file_name)


    def exists_v2_binary_file(self):
        """バイナリV2ファイルは存在するか？"""
        return os.path.isfile(self._bin_v2_file_name)


    def reset_to_random_table(self):
        """ランダム値の入った評価値テーブルを新規作成する"""
        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random fkf_plus_fko evaluation table in memory ...", flush=True)

        for index in range(0, self._table_size):
            # 値は 0, 1 の２値
            self._evaluation_ee_table[index] = random.randint(0,1)

        print(f"[{datetime.datetime.now()}] evaluation table maked in memory", flush=True)
        self._file_modified = True


    def read_evaluation_from_text_file(self):
        """テキスト・ファイルを読込む"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {self._file_name} file ...", flush=True)

        # ファイルの存在チェックを済ませておくこと

        # テキスト・ファイル
        try:
            with open(self._file_name, 'r', encoding="utf-8") as f:
                text = f.read()
                print(f"[{datetime.datetime.now()}] {self._file_name} read", flush=True)

            # 隙間のないテキストを１文字ずつ分解
            tokens = list(text)
            # 整数型へ変換したあと、またリストに入れる
            self._evaluation_ee_table = list(map(int,tokens))

            print(f"[{datetime.datetime.now()}] {self._file_name} file loaded. evaluation table size: {len(self._evaluation_ee_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{self._file_name}] file error. {ex}")
            raise

        self._file_modified = False


    def read_evaluation_from_binary_file(self):
        """バイナリ・ファイルを読込む"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {self._bin_file_name} file ...", flush=True)

        # ファイルの存在チェックを済ませておくこと

        # バイナリ・ファイル
        try:
            self._evaluation_ee_table = []

            with open(self._bin_file_name, 'rb') as f:

                multiple_bytes = f.read(1)

                while multiple_bytes:
                    number = int.from_bytes(multiple_bytes, signed=False)
                    self._evaluation_ee_table.append(number)

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] {self._bin_file_name} file loaded. evaluation table size: {len(self._evaluation_ee_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{self._bin_file_name}] file error. {ex}")
            raise

        self._file_modified = False


    def read_evaluation_from_binary_v2_file(self):
        """バイナリV2ファイルを読込む
        ファイルの存在チェックを済ませておくこと"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {self._bin_v2_file_name} file ...", flush=True)

        try:
            self._evaluation_ee_table = []

            with open(self._bin_v2_file_name, 'rb') as f:

                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)

                    self._evaluation_ee_table.append(one_byte//128 % 2)
                    self._evaluation_ee_table.append(one_byte// 64 % 2)
                    self._evaluation_ee_table.append(one_byte// 32 % 2)
                    self._evaluation_ee_table.append(one_byte// 16 % 2)
                    self._evaluation_ee_table.append(one_byte//  8 % 2)
                    self._evaluation_ee_table.append(one_byte//  4 % 2)
                    self._evaluation_ee_table.append(one_byte//  2 % 2)
                    self._evaluation_ee_table.append(one_byte//      2)

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] {self._bin_v2_file_name} file loaded. evaluation table size: {len(self._evaluation_ee_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{self._bin_v2_file_name}] file error. {ex}")
            raise

        self._file_modified = False


    def save_evaluation_to_file(self):
        """保存する"""

        if self._file_modified:
            print(f"[{datetime.datetime.now()}] save {self._bin_v2_file_name} file ...", flush=True)

            # バイナリ・ファイルに出力する
            with open(self._bin_v2_file_name, 'wb') as f:

                length = 0
                sum = 0

                for value in self._evaluation_ee_table:
                    if value==0:
                        # byte型配列に変換して書き込む
                        # 1 byte の数 0
                        sum *= 2
                        sum += 0x0.to_bytes(1)
                        length += 1
                    else:
                        # 1 byte の数 1
                        sum *= 2
                        sum += 0x1.to_bytes(1)
                        length += 1

                    if 8 <= length:
                        f.write(sum)
                        length = 0

                # 末端にはみ出た１バイト
                if length < 8:
                    while length < 8:
                        sum *= 2
                        length += 1

                    f.write(sum)

            self._file_modified = False

            print(f"[{datetime.datetime.now()}] {self._bin_v2_file_name} file saved", flush=True)

        else:
            print(f"[{datetime.datetime.now()}] {self._bin_v2_file_name} file not changed", flush=True)


    def load_from_file_or_random_table(self):
        """評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する"""

        print(f"[{datetime.datetime.now()}] {self._bin_v2_file_name} file exists check ...", flush=True)

        # バイナリV2ファイルに保存されているとき
        if self.exists_binary_v2_file():
            self.read_evaluation_from_binary_v2_file()

            # 旧形式のバイナリ・ファイルは削除
            try:
                print(f"[{datetime.datetime.now()}] try {self._bin_file_name} file delete...", flush=True)
                os.remove(self._bin_file_name)
                print(f"[{datetime.datetime.now()}] {self._bin_file_name} file deleted", flush=True)

            except FileNotFoundError:
                # ファイルが無いのなら、削除に失敗しても問題ない
                pass

            # 旧形式のテキスト・ファイルは削除
            try:
                print(f"[{datetime.datetime.now()}] try {self._file_name} file delete...", flush=True)
                os.remove(self._file_name)
                print(f"[{datetime.datetime.now()}] {self._file_name} file deleted", flush=True)

            except FileNotFoundError:
                # ファイルが無いのなら、削除に失敗しても問題ない
                pass

            return

        print(f"[{datetime.datetime.now()}] {self._bin_file_name} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if self.exists_binary_file():
            self.read_evaluation_from_binary_file()

            # 旧形式のテキスト・ファイルは削除
            try:
                print(f"[{datetime.datetime.now()}] try {self._file_name} file delete...", flush=True)
                os.remove(self._file_name)
                print(f"[{datetime.datetime.now()}] {self._file_name} file deleted", flush=True)

            except FileNotFoundError:
                # ファイルが無いのなら、削除に失敗しても問題ない
                pass

            return

        print(f"[{datetime.datetime.now()}] {self._file_name} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if self.exists_text_file():
            self.read_evaluation_from_text_file()
            return

        # ファイルが存在しないとき
        self.reset_to_random_table()


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

            self._file_modified = True
