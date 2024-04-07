import random
import datetime
import os
from result_file import exists_result_file, read_result_file


class EvaluationTable():
    """評価値テーブル"""

    def __init__(self):
        self._file_modified = False

        self._move_size = 8424
        self._table_size = 70_955_352
        self._evaluation_table = [0] * 70_955_352
        """評価値テーブル

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
        """


    def load_or_new_evaluation_table(self):
        """評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する"""

        print(f"[{datetime.datetime.now()}] eval.csv file exists check ...")

        # 評価関数テーブル・ファイルが存在しないとき
        if not os.path.isfile('eval.csv'):
            # ダミーデータを入れる。１分ほどかかる
            print(f"[{datetime.datetime.now()}] make random evaluation table in memory ...")

            for index in range(0, self._table_size):
                # -1,0,1 を保存するとマイナスの符号で文字数が多くなるので、+1 して 0,1,2 で保存する
                self._evaluation_table[index] = random.randint(0,2)

            print(f"[{datetime.datetime.now()}] evaluation table maked in memory")
            self._file_modified = True

        else:
            self.load_evaluation_from_file()

            # 結果を見る。持将棋や、負けていれば、内容をランダムに変更してみる
            if exists_result_file:
                result_text = read_result_file()

                # 前回の対局で、負けるか、引き分けなら、内容を変えます
                if result_text in ('lose', 'draw'):
                    self.modify_table(result_text)

            print(f"[{datetime.datetime.now()}] eval.csv file loaded")


    def get_evaluation_table_index_from_move_as_usi(self, move_as_usi):
        """USIの指し手の符号を、評価値テーブルのインデックスへ変換します

        Parameters
        ----------
        move_as_usi : str
            "7g7f" や "3d3c+"、 "R*5e" のような文字列を想定。 "resign" のような文字列は想定外
        """

        # 移動元
        src_str = move_as_usi[0: 2]

        # 移動先
        dst_str = move_as_usi[2: 4]

        # 移動元
        if src_str == 'R*':
            src_num = 45
        elif src_str == 'B*':
            src_num = 46
        elif src_str == 'G*':
            src_num = 47
        elif src_str == 'S*':
            src_num = 48
        elif src_str == 'N*':
            src_num = 49
        elif src_str == 'L*':
            src_num = 50
        elif src_str == 'P*':
            src_num = 51
        else:

            file_str = src_str[0]
            if file_str in ('1', '9'):
                src_num = 0
            elif file_str in ('2', '8'):
                src_num = 9
            elif file_str in ('3', '7'):
                src_num = 18
            elif file_str in ('4', '6'):
                src_num = 27
            elif file_str == "5":
                src_num = 36
            else:
                raise Exception(f"src file error: '{file_str}' in '{move_as_usi}'")

            rank_str = src_str[1]
            if rank_str == 'a':
                src_num += 0
            elif rank_str == 'b':
                src_num += 1
            elif rank_str == 'c':
                src_num += 2
            elif rank_str == 'd':
                src_num += 3
            elif rank_str == 'e':
                src_num += 4
            elif rank_str == 'f':
                src_num += 5
            elif rank_str == 'g':
                src_num += 6
            elif rank_str == 'h':
                src_num += 7
            elif rank_str == 'i':
                src_num += 8
            else:
                raise Exception(f"src rank error: '{rank_str}' in '{move_as_usi}'")

        # 移動先
        file_str = dst_str[0]

        if file_str in ('1', '9'):
            dst_num = 0
        elif file_str in ('2', '8'):
            dst_num = 9
        elif file_str in ('3', '7'):
            dst_num = 18
        elif file_str in ('4', '6'):
            dst_num = 27
        elif file_str == '5':
            dst_num = 36
        else:
            raise Exception(f"dst file error: '{file_str}' in '{move_as_usi}'")

        rank_str = dst_str[1]
        if rank_str == "a":
            dst_num += 0
        elif rank_str == "b":
            dst_num += 1
        elif rank_str == "c":
            dst_num += 2
        elif rank_str == "d":
            dst_num += 3
        elif rank_str == "e":
            dst_num += 4
        elif rank_str == "f":
            dst_num += 5
        elif rank_str == "g":
            dst_num += 6
        elif rank_str == "h":
            dst_num += 7
        elif rank_str == "i":
            dst_num += 8
        else:
            raise Exception(f"dst rank error: '{rank_str}' in '{move_as_usi}'")

        # 成りかそれ以外（５文字なら成りだろう）
        if 4 < len(move_as_usi):
            pro_num = 1
        else:
            pro_num = 0

        return (2 * 5 * 9 * src_num) + (2 * dst_num) + pro_num


    def get_evaluation_value(self, move_a_as_usi, move_b_as_usi):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if move_a_as_usi == move_b_as_usi:
            return 0

        index_a = self.get_evaluation_table_index_from_move_as_usi(move_a_as_usi)
        index_b = self.get_evaluation_table_index_from_move_as_usi(move_b_as_usi)

        move_indexes = [index_a, index_b]
        move_indexes.sort()

        # 昇順
        if index_a <= index_b:
            index = index_a * self._move_size + index_b
            #print(f"[DEBUG] 昇順 a:{index_a:3} b:{index_b:3} index:{index}")

        # 降順
        else:
            index = index_b * self._move_size + index_a

        #print(f"[DEBUG] 逆順 b:{index_b:3} a:{index_a:3} index:{index}")
        # 0,1,2 が保存されているので、 -1 すると、 -1,0,1 になる。マイナスの符号が付くと文字数が多くなるのでこうしている
        return self._evaluation_table[index] - 1


    def make_move_score_dictionary(self, sorted_legal_move_list_as_usi):
        """指し手に評価値を付ける

        Parameters
        ----------
        sorted_legal_move_list_as_usi : list
            USIプロトコルでの符号表記の指し手の配列。辞書順で昇順にソート済み
        """

        # 指し手に評価値を付ける
        move_score_dictionary = {}

        for move_a_as_usi in sorted_legal_move_list_as_usi:

            # 総当たりで評価値を計算
            sum_value = 0

            for move_b_as_usi in sorted_legal_move_list_as_usi:
                sum_value += self.get_evaluation_value(move_a_as_usi, move_b_as_usi)

            move_score_dictionary[move_a_as_usi] = sum_value

        return move_score_dictionary


    def modify_table(self, result_text):
        """評価値テーブルの内容を適当に変更します"""

        if result_text == 'lose':
            count = self._table_size//1000
        elif result_text == 'draw':
            count = self._table_size//10000
        else:
            count = 0

        for _i in range(0, count):
            n = random.randint(0, self._table_size)
            # -1,0,1 を保存するとマイナスの符号で文字数が多くなるので、+1 して 0,1,2 で保存する
            self._evaluation_table[n] = random.randint(0,2)

        self._file_modified = True


    def save_evaluation_to_file(self):
        """保存する"""

        if self._file_modified:
            print(f"[{datetime.datetime.now()}] save eval.csv file ...")

            # ファイルに出力する
            with open('eval.csv', 'w', encoding="utf-8") as f:
                # 配列の要素の整数型を文字列型に変換して隙間を空けずに連結
                text = ''.join(map(str,self._evaluation_table))
                print(f"[{datetime.datetime.now()}] text created ...")

                f.write(text)

            self._file_modified = False

            print(f"[{datetime.datetime.now()}] eval.csv file saved")

        else:
            print(f"[{datetime.datetime.now()}] eval.csv file not changed")

    def load_evaluation_from_file(self):
        """読込む"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] load eval.csv file ...")

        with open('eval.csv', 'r', encoding="utf-8") as f:
            text = f.read()
            print(f"[{datetime.datetime.now()}] eval.csv read ...")

            # 隙間のないテキストを１文字ずつ分解
            tokens = list(text)
            # 整数型へ変換したあと、またリストに入れる
            self._evaluation_table = list(map(int,tokens))
