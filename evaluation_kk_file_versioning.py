import os
import datetime
from evaluation_configuration import EvaluationConfiguration
from evaluation_kk_table import EvaluationKkTable
from evaluation_file_versioning import FileVersioning


class EvaluationKkFileVersioning():


    @staticmethod
    def load_kk_policy(
            file_number):
        """ＫＫポリシー読込

        Returns
        -------
        - テーブル
        - バージョンアップしたので保存要求の有無
        """
        shall_save_file = False
        evaluation_kind = "kk"

        # ＫＫ評価値テーブルは V3 の途中から追加
        is_symmetrical_connected = False

        tuple = EvaluationKkFileVersioning.check_file_version_and_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            file_version = None
            file_name = None
        if tuple is not None:
            file_version, file_name = tuple

        # 読込
        tuple = EvaluationKkFileVersioning.load_from_file_or_random_table(
                file_number=file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version, shall_save_file = tuple
            is_file_modified = mm_table is None

        if file_version == "V4":
            is_king_of_a = True     # 玉の指し手は評価値テーブル・サイズを縮めれる
            is_king_of_b = True     # 玉の指し手は評価値テーブル・サイズを縮めれる
        else:
            is_king_of_a = False     # 過去バージョンではフラグ未対応
            is_king_of_b = False     # 過去バージョンではフラグ未対応

        # ファイルが存在しないとき
        if mm_table is None:
            mm_table = FileVersioning.reset_to_random_table(
                hint=f"n{file_number} kind=kk",
                table_size=EvaluationConfiguration.get_table_size(
                        is_king_of_a=is_king_of_a,
                        is_king_of_b=is_king_of_b,
                        is_symmetrical_connected=is_symmetrical_connected))

        kk_table = EvaluationKkTable(
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_mm_table=mm_table,
                is_king_of_a=is_king_of_a,
                is_king_of_b=is_king_of_b,
                is_symmetrical_connected=is_symmetrical_connected,
                is_file_modified=is_file_modified)

        return (kk_table, shall_save_file)


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

        file_names_by_version = EvaluationKkFileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリV3ファイルに保存されているとき
        file_name = file_names_by_version[3]
        if os.path.isfile(file_name):
            return ("V3", file_name)

        # ファイルが存在しないとき
        return None


    @staticmethod
    def load_from_file_or_random_table(
            file_number,
            evaluation_kind,
            file_version):
        """評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する。

        ファイルのバージョンがアップすることがある"""

        file_names_by_version = EvaluationKkFileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリ・ファイル V3 に保存されているとき
        if file_version == "V3":
            mm_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
                    file_name=file_names_by_version[3])

            return (mm_table, "V3")

        # ファイルが存在しないとき
        return None
