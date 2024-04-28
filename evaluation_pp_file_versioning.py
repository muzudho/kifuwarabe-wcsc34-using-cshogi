import os
import datetime
from evaluation_pp_table import EvaluationPpTable
from evaluation_file_versioning import FileVersioning
from evaluation_file_version_up import EvaluationFileVersionUp
from evaluation_table_size import EvaluationTableSize


class EvaluationPpFileVersioning():


    @staticmethod
    def load_pp_policy(
            file_number):
        """ＰＰポリシー読込

        Returns
        -------
        - テーブル
        - バージョンアップしたので保存要求の有無
        """
        shall_save_file = False
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
            shall_save_file = True      # 保存しておかないと、毎回作成して時間がかかる
        else:
            mm_table, file_version, shall_save_file = tuple
            is_file_modified = mm_table is None

        is_symmetrical_connected = True
        if file_version == "V3":
            is_symmetrical_connected = False

        if mm_table is None:
            # ファイルが存在しないとき
            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=False,     # P なんで
                    is_king_of_b=False,     # P なんで
                    is_symmetrical_connected=is_symmetrical_connected)

            mm_table = FileVersioning.create_random_table(
                    hint=f'n{file_number}  kind=pp  new_table_size_obj:({new_table_size_obj.to_debug_str()})',
                    table_size=new_table_size_obj.combination)

        pp_table = EvaluationPpTable(
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_mm_table=mm_table,
                is_king_of_a=False,     # P なんで
                is_king_of_b=False,     # P なんで
                is_symmetrical_connected=is_symmetrical_connected,
                is_file_modified=is_file_modified)

        return (pp_table, shall_save_file)


    @staticmethod
    def create_file_names_each_version(
            file_number,
            evaluation_kind):
        return [
            f'n{file_number}_eval_{evaluation_kind}.txt',       # 旧 V0
            f'n{file_number}_eval_{evaluation_kind}.bin',       # 旧 V1
            f'n{file_number}_eval_{evaluation_kind}_v2.bin',    # 旧 V2
            f'n{file_number}_eval_{evaluation_kind}_v3.bin',    # 現 V3
            f'n{file_number}_eval_{evaluation_kind}_v4.bin',    # 次期 V4
        ]


    @staticmethod
    def check_file_version_and_name(
            file_number,
            evaluation_kind):
        """ファイルのバージョンと、ファイル名のタプルを返す。無ければナン"""

        file_names_by_version = EvaluationPpFileVersioning.create_file_names_each_version(
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

        ファイルのバージョンがアップすることがある

        Returns
        -------
        - タプル
            - mm_table
            - バージョン番号
            - バージョンアップしたか？
        """

        file_names_by_version = EvaluationPpFileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリ・ファイル V4 に保存されているとき
        if file_version == "V4":
            # V4ファイル読込
            mm_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
                    file_name=file_names_by_version[4])
            pass

            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[3]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

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

            return (mm_table, "V4", False)

        # バイナリ・ファイル V3 に保存されているとき
        if file_version == "V3":
            #mm_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
            #        file_name=file_names_by_version[3])

            # バージョンアップする
            mm_table = EvaluationFileVersionUp.read_evaluation_v3_file_and_convert_to_v4(
                is_king_of_a=False, # PP だから
                is_king_of_b=False, # PP だから
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

            # バージョンアップ
            return (mm_table, "V4", True)

        # バイナリV2ファイルに保存されているとき
        if file_version == "V2":

            # バージョンアップする
            mm_table = EvaluationFileVersionUp.read_evaluation_v2_file_and_convert_to_v3(
                file_name=file_names_by_version[2])

            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[1]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            # 旧形式のテキスト・ファイルは削除
            old_file_name = file_names_by_version[0]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            # バージョンアップ
            return (mm_table, "V3", True)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if file_version == "V1":
            mm_table = FileVersioning.read_evaluation_from_binary_file(
                    file_name=file_names_by_version[1])

            # 旧形式のテキスト・ファイルは削除
            old_file_name = file_names_by_version[0]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

            return (mm_table, "V1", False)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if file_version == "V0":
            mm_table = FileVersioning.read_evaluation_from_text_file(
                    file_name=file_names_by_version[0])

            return (mm_table, "V0", False)

        # ファイルが存在しないとき
        return None
