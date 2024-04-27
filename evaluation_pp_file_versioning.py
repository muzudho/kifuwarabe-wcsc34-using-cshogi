import os
import datetime
from evaluation_configuration import EvaluationConfiguration
from evaluation_pp_table import EvaluationPpTable
from file_versioning import FileVersioning


class EvaluationPpFileVersioning():


    @staticmethod
    def load_pp_policy(
            file_number):
        """ＰＰポリシー読込"""
        evaluation_kind = "pp"

        tuple = EvaluationPpFileVersioning.check_file_version_and_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            file_version = None
            file_name = None
        if tuple is not None:
            file_version, file_name = tuple

        if file_version is None:
            evaluation_kind = "pp_po"   # V3の途中までの旧称その２

            tuple = EvaluationPpFileVersioning.check_file_version_and_name(
                    file_number=file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        if file_version is None:
            evaluation_kind = "fmf_fmo"     # V3の途中までの旧称
            tuple = EvaluationPpFileVersioning.check_file_version_and_name(
                    file_number=file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        # 読込
        tuple = EvaluationPpFileVersioning.load_from_file_or_random_table(
                file_number=file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version = tuple
            is_file_modified = mm_table is None

        is_symmetrical_connected_of_pp = True
        if file_version == "V3":
            # TODO 予定
            is_symmetrical_connected_of_pp = False

        if mm_table is None:
            # ファイルが存在しないとき
            mm_table = FileVersioning.reset_to_random_table(
                hint=f'n{file_number} kind=pp',
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        return EvaluationPpTable(
                file_number=file_number,
                file_name=file_name,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=is_symmetrical_connected_of_pp)


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

        file_names_by_version = EvaluationPpFileVersioning.create_file_names_each_version(
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
