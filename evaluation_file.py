import os
import datetime
import random


class EvaluationFile():
    """評価値ファイル等の読込や、バージョン更新などを担当"""


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
            table_size_obj):
        """ランダム値の入った評価値テーブルを新規作成する

        Parameters
        ----------
        table_size_obj : EvaluationTableSize
            テーブル・サイズ。計算過程付き
        """

        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random evaluation table in memory. hint: '{hint}' ... table_size_obj:({table_size_obj.to_debug_str()})", flush=True)

        new_mm_table = []

        for _index in range(0, table_size_obj.relation):
            # 値は 0, 1 の２値
            new_mm_table.append(random.randint(0,1))

        print(f"[{datetime.datetime.now()}] random evaluation table maked in memory.", flush=True)
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
