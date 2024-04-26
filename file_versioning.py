import os
import datetime
import random
from evaluation_configuration import EvaluationConfiguration
from move import Move


class FileVersioning():


    @staticmethod
    def read_evaluation_from_text_file(
            file_name):
        """テキスト・ファイルを読込む"""

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
            evaluation_ee_table = list(map(int,tokens))

            print(f"[{datetime.datetime.now()}] {file_name} file loaded. evaluation table size: {len(evaluation_ee_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_ee_table


    @staticmethod
    def read_evaluation_from_binary_file(
            file_name):
        """バイナリ・ファイルを読込む"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {file_name} file ...", flush=True)

        # ファイルの存在チェックを済ませておくこと

        # バイナリを数値型へ変換してリストに入れていく
        evaluation_ee_table = list()

        # バイナリ・ファイル
        try:
            with open(file_name, 'rb') as f:
                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)
                    evaluation_ee_table.append(one_byte)

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] {file_name} file loaded. evaluation table size: {len(evaluation_ee_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_ee_table


    @staticmethod
    def read_evaluation_from_binary_v2_v3_file(
            file_name):
        """バイナリ・ファイルを読込む
        V2, V3 用
        ファイルの存在チェックを済ませておくこと"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {file_name} file ...", flush=True)

        evaluation_ee_table = []

        try:

            with open(file_name, 'rb') as f:

                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)

                    evaluation_ee_table.append(one_byte//128 % 2)
                    evaluation_ee_table.append(one_byte// 64 % 2)
                    evaluation_ee_table.append(one_byte// 32 % 2)
                    evaluation_ee_table.append(one_byte// 16 % 2)
                    evaluation_ee_table.append(one_byte//  8 % 2)
                    evaluation_ee_table.append(one_byte//  4 % 2)
                    evaluation_ee_table.append(one_byte//  2 % 2)
                    evaluation_ee_table.append(one_byte//      2)

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] {file_name} file loaded. evaluation table size: {len(evaluation_ee_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_ee_table


    @staticmethod
    def read_evaluation_v2_file_and_convert_to_v3(
            v2_file_name):
        """TODO バイナリ・ファイル V2 を読込み、V3 にバージョンアップして使う
        ファイルの存在チェックを済ませておくこと"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {v2_file_name} file ...", flush=True)

        evaluation_ee_table = [0] * EvaluationConfiguration.get_fully_connected_table_size()

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
                        bit = one_byte//two_power % 2

                        moves_as_usi_pair = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                                table_index=table_index,
                                # 左右対称の盤
                                is_symmetrical_connected=True)

                        for moves_as_usi in moves_as_usi_pair:
                            for move_as_usi in moves_as_usi:
                                converted_table_index = EvaluationConfiguration.get_table_index_by_move(
                                        move=Move(move_as_usi),
                                        # 左右が異なる盤
                                        is_symmetrical_connected=False)

                                try:
                                    evaluation_ee_table[converted_table_index] = bit

                                except IndexError as e:
                                    print(f"table length: {len(evaluation_ee_table)}  index: {converted_table_index}  except: {e}")
                                    raise


                        table_index+=1

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] {v2_file_name} file loaded. evaluation table size: {len(evaluation_ee_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{v2_file_name}] file error. {ex}")
            raise

        return evaluation_ee_table


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
    def check_file_version(
            file_number,
            evaluation_kind):
        """評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する"""

        file_names_by_version = FileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリV3ファイルに保存されているとき
        if os.path.isfile(file_names_by_version[3]):
            return "V3"

        # バイナリV2ファイルに保存されているとき
        if os.path.isfile(file_names_by_version[2]):
            return "V2"

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if os.path.isfile(file_names_by_version[1]):
            return "V1"

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if os.path.isfile(file_names_by_version[0]):
            return "V0"

        # ファイルが存在しないとき
        return None


    @staticmethod
    def load_from_file_or_random_table(
            file_number,
            evaluation_kind,
            file_version):
        """評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する"""

        file_names_by_version = FileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリ・ファイル V3 に保存されているとき
        if file_version == "V3":
            ee_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
                    file_name=file_names_by_version[3])

            # 旧形式のバイナリ・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[2])

            # 旧形式のバイナリ・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[0])

            return ee_table

        # バイナリV2ファイルに保存されているとき
        if file_version == "V2":

            # TODO バージョンアップしたい
            ee_table = FileVersioning.read_evaluation_v2_file_and_convert_to_v3(
                v2_file_name=file_names_by_version[2])
            #ee_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
            #        file_name=file_names_by_version[2])

            # 旧形式のバイナリ・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[0])

            return ee_table

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if file_version == "V1":
            ee_table = FileVersioning.read_evaluation_from_binary_file(
                    file_name=file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            FileVersioning.delete_file(file_names_by_version[0])

            return ee_table

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if file_version == "V0":
            ee_table = FileVersioning.read_evaluation_from_text_file(
                    file_name=file_names_by_version[0])

            return ee_table

        # ファイルが存在しないとき
        return None


    def reset_to_random_table(
            file_number,
            evaluation_kind,
            table_size):
        """ランダム値の入った評価値テーブルを新規作成する"""
        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random {evaluation_kind} evaluation table in memory ...", flush=True)

        evaluation_ee_table = []

        for index in range(0, table_size):
            # 値は 0, 1 の２値
            evaluation_ee_table.append(random.randint(0,1))

        print(f"[{datetime.datetime.now()}] {evaluation_kind} evaluation table maked in memory", flush=True)
        return evaluation_ee_table


    @staticmethod
    def save_evaluation_to_file(
            file_number,
            evaluation_kind,
            evaluation_ee_table):
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

            for value in evaluation_ee_table:
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
