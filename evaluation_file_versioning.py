import os
import datetime
import random


class FileVersioning():
    """評価値ファイル等の読込や、バージョン更新などを担当"""


    @staticmethod
    def read_evaluation_from_text_file(
            file_name):
        """テキスト・ファイル V0 を読込む"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {file_name} file ...", flush=True)

        # ファイルの存在チェックを済ませておくこと

        # テキスト・ファイル
        try:
            with open(file_name, 'r', encoding="utf-8") as f:
                text = f.read()
                print(f"[{datetime.datetime.now()}] {file_name} read", flush=True)

            # 隙間のないテキストを１文字ずつ分解
            tokens = list(text)

            # 整数型へ変換したあと、またリストに入れる
            evaluation_mm_table = list(map(int,tokens))

            print(f"[{datetime.datetime.now()}] (v0) '{file_name}' file loaded. evaluation table size: {len(evaluation_mm_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_mm_table


    @staticmethod
    def read_evaluation_from_binary_file(
            file_name):
        """バイナリ・ファイル V1 を読込む"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {file_name} file ...", flush=True)

        # ファイルの存在チェックを済ませておくこと

        # バイナリを数値型へ変換してリストに入れていく
        evaluation_mm_table = list()

        # バイナリ・ファイル
        try:
            with open(file_name, 'rb') as f:
                one_byte_binary = f.read(1)

                while one_byte_binary:
                    one_byte_num = int.from_bytes(one_byte_binary, signed=False)
                    evaluation_mm_table.append(one_byte_num)

                    one_byte_binary = f.read(1)

            print(f"[{datetime.datetime.now()}] (v1) '{file_name}' file loaded. evaluation table size: {len(evaluation_mm_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_mm_table


    @staticmethod
    def read_evaluation_from_binary_v2_v3_file(
            file_name):
        """バイナリ・ファイル V2, V3 を読込む
        ファイルの存在チェックを済ませておくこと"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {file_name} file ...", flush=True)

        evaluation_mm_table = []

        try:

            with open(file_name, 'rb') as f:

                one_byte_binary = f.read(1)

                while one_byte_binary:
                    one_byte_num = int.from_bytes(one_byte_binary, signed=False)

                    evaluation_mm_table.append(one_byte_num//128 % 2)
                    evaluation_mm_table.append(one_byte_num// 64 % 2)
                    evaluation_mm_table.append(one_byte_num// 32 % 2)
                    evaluation_mm_table.append(one_byte_num// 16 % 2)
                    evaluation_mm_table.append(one_byte_num//  8 % 2)
                    evaluation_mm_table.append(one_byte_num//  4 % 2)
                    evaluation_mm_table.append(one_byte_num//  2 % 2)
                    evaluation_mm_table.append(one_byte_num//      2)

                    one_byte_binary = f.read(1)

            print(f"[{datetime.datetime.now()}] (v2,v3) '{file_name}' file loaded. evaluation table size: {len(evaluation_mm_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_mm_table


    @staticmethod
    def delete_file(file_name):
        """ファイル削除"""
        try:
            print(f"[{datetime.datetime.now()}] try {file_name} file delete...", flush=True)
            os.remove(file_name)
            print(f"[{datetime.datetime.now()}] {file_name} file deleted", flush=True)

        except FileNotFoundError:
            # ファイルが無いのなら、削除に失敗しても問題ない
            pass


    def create_random_table(
            hint,
            table_size):
        """ランダム値の入った評価値テーブルを新規作成する"""

        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random evaluation table in memory. hint: '{hint}' ...", flush=True)

        new_mm_table = []

        for _index in range(0, table_size):
            # 値は 0, 1 の２値
            new_mm_table.append(random.randint(0,1))

        print(f"[{datetime.datetime.now()}] random evaluation table maked in memory. hint: '{hint}'", flush=True)
        return new_mm_table


    @staticmethod
    def save_evaluation_to_file(
            file_name,
            evaluation_mm_table):
        """最新のバージョンで保存する"""

        print(f"[{datetime.datetime.now()}] save {file_name} file ...", flush=True)

        # バイナリ・ファイルに出力する
        with open(file_name, 'wb') as f:

            length = 0
            sum = 0

            for value in evaluation_mm_table:
                if value==0:
                    # byte型配列に変換して書き込む
                    # 1 byte の数 0
                    sum *= 2
                    sum += 0
                    length += 1
                else:
                    # 1 byte の数 1
                    sum *= 2
                    sum += 1
                    length += 1

                if 8 <= length:
                    # 整数型を、１バイトのバイナリーに変更
                    f.write(sum.to_bytes(1))
                    sum = 0
                    length = 0

            # 末端にはみ出た１バイト
            if 0 < length and length < 8:
                while length < 8:
                    sum *= 2
                    length += 1

                f.write(sum.to_bytes(1))

        print(f"[{datetime.datetime.now()}] {file_name} file saved", flush=True)
