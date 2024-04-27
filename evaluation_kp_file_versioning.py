import os
import datetime
from evaluation_configuration import EvaluationConfiguration
from evaluation_kp_table import EvaluationKpTable
from file_versioning import FileVersioning


class EvaluationKpFileVersioning():


    @staticmethod
    def load_kp_policy(
            file_number):
        """ＫＰポリシー読込"""
        evaluation_kind = "kp"

        tuple = EvaluationKpFileVersioning.check_file_version_and_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            file_version = None
            file_name = None
        if tuple is not None:
            file_version, file_name = tuple

        if file_version == None:
            evaluation_kind = "kp_ko" # V3の途中までの旧名その２

            tuple = EvaluationKpFileVersioning.check_file_version_and_name(
                    file_number=file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        if file_version == None:
            evaluation_kind = "fkf_fko" # V3の途中までの旧名

            tuple = EvaluationKpFileVersioning.check_file_version_and_name(
                    file_number=file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        # 読込
        tuple = EvaluationKpFileVersioning.load_from_file_or_random_table(
                file_number=file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version = tuple
            is_file_modified = mm_table is None

        is_symmetrical_connected = True
        if file_version == "V3":
            # V3 から盤面を左右対称ではなく、全体を使うよう変更
            is_symmetrical_connected = False

        # ファイルが存在しないとき
        if mm_table is None:
            mm_table = FileVersioning.reset_to_random_table(
                hint=f"n{file_number} kind=kp",
                table_size=EvaluationConfiguration.get_table_size(
                        is_symmetrical_connected=is_symmetrical_connected))

        if file_version == "V4":
            is_king_of_a = True     # 玉の指し手は評価値テーブル・サイズを縮めれる
            is_king_of_b = False    # P なんで
        else:
            is_king_of_a = False    # 過去バージョンではフラグ未対応
            is_king_of_b = False    # 過去バージョンではフラグ未対応

        return EvaluationKpTable(
                file_number=file_number,
                file_name=file_name,
                evaluation_mm_table=mm_table,
                is_king_of_a=is_king_of_a,
                is_king_of_b=is_king_of_b,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=is_symmetrical_connected)


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

        file_names_by_version = EvaluationKpFileVersioning.create_file_names_each_version(
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

        file_names_by_version = EvaluationKpFileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリ・ファイル V3 に保存されているとき
        if file_version == "V3":
            mm_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
                    file_name=file_names_by_version[3])

            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[2]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[1]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            # 旧形式のテキスト・ファイルは削除
            old_file_name = file_names_by_version[0]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            return (mm_table, "V3")

        # バイナリV2ファイルに保存されているとき
        if file_version == "V2":

            # TODO バージョンアップしたい
            mm_table = FileVersioning.read_evaluation_v2_file_and_convert_to_v3(
                v2_file_name=file_names_by_version[2])

            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[1]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            # 旧形式のテキスト・ファイルは削除
            old_file_name = file_names_by_version[0]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            return (mm_table, "V3")

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if file_version == "V1":
            mm_table = FileVersioning.read_evaluation_from_binary_file(
                    file_name=file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            old_file_name = file_names_by_version[0]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            return (mm_table, "V1")

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if file_version == "V0":
            mm_table = FileVersioning.read_evaluation_from_text_file(
                    file_name=file_names_by_version[0])

            return (mm_table, "V0")

        # ファイルが存在しないとき
        return None
