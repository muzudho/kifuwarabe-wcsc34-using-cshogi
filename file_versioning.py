import os
import datetime
import random
from evaluation_configuration import EvaluationConfiguration
from move import Move


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
                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)
                    evaluation_mm_table.append(one_byte)

                    multiple_bytes = f.read(1)

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

                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)

                    evaluation_mm_table.append(one_byte//128 % 2)
                    evaluation_mm_table.append(one_byte// 64 % 2)
                    evaluation_mm_table.append(one_byte// 32 % 2)
                    evaluation_mm_table.append(one_byte// 16 % 2)
                    evaluation_mm_table.append(one_byte//  8 % 2)
                    evaluation_mm_table.append(one_byte//  4 % 2)
                    evaluation_mm_table.append(one_byte//  2 % 2)
                    evaluation_mm_table.append(one_byte//      2)

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] (v2,v3) '{file_name}' file loaded. evaluation table size: {len(evaluation_mm_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_mm_table


    @staticmethod
    def read_evaluation_v2_file_and_convert_to_v3(
            v2_file_name):
        """バイナリ・ファイル V2 を読込み、V3 にバージョンアップして使う
        ファイルの存在チェックを済ませておくこと"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {v2_file_name} file ...", flush=True)

        evaluation_mm_table = [0] * EvaluationConfiguration.get_fully_connected_table_size()

        try:

            table_index = 0

            with open(v2_file_name, 'rb') as f:

                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)

                    #
                    # V2 ---> V3 で、インデックスがずれる
                    #
                    two_powers = [128, 64, 32, 16, 8, 4, 2, 1]
                    for two_power in two_powers:

                        # ビットフィールドを全て使わず、途中で切れるケース
                        if EvaluationConfiguration.get_symmetrical_connected_table_size() <= table_index:
                            break

                        pair_of_list_of_move_as_usi = EvaluationConfiguration.get_pair_of_list_of_move_as_usi_by_mm_index(
                                mm_index=table_index,
                                # 左右対称の盤
                                is_symmetrical_connected=True)

                        for list_of_move_as_usi in pair_of_list_of_move_as_usi:
                            for move_as_usi in list_of_move_as_usi:
                                converted_m_index = EvaluationConfiguration.get_m_index_by_move(
                                        move=Move(move_as_usi),
                                        # 左右が異なる盤
                                        is_symmetrical_connected=False)

                                try:
                                    bit = one_byte//two_power % 2
                                    evaluation_mm_table[converted_m_index] = bit

                                    # TODO 共役の方にも反転して値を入れたい？

                                except IndexError as e:
                                    print(f"table length:{len(evaluation_mm_table)}  table_index:{table_index}  converted_m_index:{converted_m_index}  except:{e}")
                                    raise


                        table_index+=1

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] (v2 to v3) '{v2_file_name}' file loaded. evaluation table size: {len(evaluation_mm_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{v2_file_name}] file error. {ex}")
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


    @staticmethod
    def create_file_names_each_version(
            file_number,
            evaluation_kind):
        return [
            f'n{file_number}_eval_{evaluation_kind}.txt',       # 旧 V0
            f'n{file_number}_eval_{evaluation_kind}.bin',       # 旧 V1
            f'n{file_number}_eval_{evaluation_kind}_v2.bin',    # 新 V2
            f'n{file_number}_eval_{evaluation_kind}_v3.bin',    # 次期 V3
        ]


    @staticmethod
    def check_file_version_and_name(
            file_number,
            evaluation_kind):
        """ファイルのバージョンと、ファイル名のタプルを返す。無ければナン"""

        file_names_by_version = FileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリV3ファイルに保存されているとき
        file_name = file_names_by_version[3]
        if os.path.isfile(file_name):
            return ("V3", file_name)

        # バイナリV2ファイルに保存されているとき
        file_name = file_names_by_version[2]
        if os.path.isfile(file_name):
            return ("V2", file_name)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        file_name = file_names_by_version[1]
        if os.path.isfile(file_name):
            return ("V1", file_name)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        file_name = file_names_by_version[0]
        if os.path.isfile(file_name):
            return ("V0", file_name)

        # ファイルが存在しないとき
        return None


    @staticmethod
    def load_from_file_or_random_table(
            file_number,
            evaluation_kind,
            file_version):
        """評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する。

        ファイルのバージョンがアップすることがある"""

        file_names_by_version = FileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリ・ファイル V3 に保存されているとき
        if file_version == "V3":
            mm_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
                    file_name=file_names_by_version[3])

            # 旧形式のバイナリ・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[2])

            # 旧形式のバイナリ・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[0])

            return (mm_table, "V3")

        # バイナリV2ファイルに保存されているとき
        if file_version == "V2":

            # TODO バージョンアップしたい
            mm_table = FileVersioning.read_evaluation_v2_file_and_convert_to_v3(
                v2_file_name=file_names_by_version[2])

            # 旧形式のバイナリ・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[0])

            return (mm_table, "V3")

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if file_version == "V1":
            mm_table = FileVersioning.read_evaluation_from_binary_file(
                    file_name=file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[0])

            return (mm_table, "V1")

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if file_version == "V0":
            mm_table = FileVersioning.read_evaluation_from_text_file(
                    file_name=file_names_by_version[0])

            return (mm_table, "V0")

        # ファイルが存在しないとき
        return None


    def reset_to_random_table(
            hint,
            table_size):
        """ランダム値の入った評価値テーブルを新規作成する"""
        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random evaluation table in memory. hint: '{hint}' ...", flush=True)

        evaluation_mm_table = []

        for _index in range(0, table_size):
            # 値は 0, 1 の２値
            evaluation_mm_table.append(random.randint(0,1))

        print(f"[{datetime.datetime.now()}] random evaluation table maked in memory. hint: '{hint}'", flush=True)
        return evaluation_mm_table


    @staticmethod
    def save_evaluation_to_file(
            file_number,
            evaluation_kind,
            evaluation_mm_table):
        """最新のバージョンで保存する"""

        file_names_by_version = FileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        file_name = file_names_by_version[3]

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
