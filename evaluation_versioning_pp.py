import os
import datetime
from evaluation_table_pp import EvaluationTablePp
from evaluation_versioning import EvaluationVersioning
from evaluation_version_up_mm import EvaluationVersionUpMm
from evaluation_table_size import EvaluationTableSize
from evaluation_table_property import EvaluationTableProperty


class EvaluationVersioningPp():


    @staticmethod
    def create_file_names_each_version(
            file_number,
            evaluation_kind):
        return [
            # ↑ 旧い
            f'n{file_number}_eval_{evaluation_kind}.txt',       # 0
            f'n{file_number}_eval_{evaluation_kind}.bin',       # 1
            f'n{file_number}_eval_{evaluation_kind}_v2.bin',    # 2
            f'n{file_number}_eval_{evaluation_kind}_v3.bin',    # 3
            f'n{file_number}_eval_{evaluation_kind}_v4.bin',    # 4
            f'n{file_number}_eval_{evaluation_kind}_v5.bin',    # 5
            # ↓ 新しい
        ]


    @staticmethod
    def delete_old_files_cascade(
            current_number,
            file_names_by_version):
        """旧形式のファイルを削除します"""

        if 3 < current_number:
            # 旧形式のバイナリ・ファイル V3 は削除
            old_file_name = file_names_by_version[3]
            if os.path.isfile(old_file_name):
                EvaluationVersioning.delete_file(old_file_name)

        if 2 < current_number:
            # 旧形式のバイナリ・ファイル V2 は削除
            old_file_name = file_names_by_version[2]
            if os.path.isfile(old_file_name):
                EvaluationVersioning.delete_file(old_file_name)

        if 1 < current_number:
            # 旧形式のバイナリ・ファイル V1 は削除
            old_file_name = file_names_by_version[1]
            if os.path.isfile(old_file_name):
                EvaluationVersioning.delete_file(old_file_name)

        if 0 < current_number:
            # 旧形式のテキスト・ファイル V0 は削除
            old_file_name = file_names_by_version[0]
            if os.path.isfile(old_file_name):
                EvaluationVersioning.delete_file(old_file_name)


    @staticmethod
    def load_from_file(
            file_number,
            evaluation_kind,
            file_version):
        """評価関数テーブルをファイルから読み込む

        ファイルのバージョンがアップすることがある

        Returns
        -------
        - タプル
            - mm_table
            - バージョン番号
            - バージョンアップしたか？
        """

        file_names_by_version = EvaluationVersioningPp.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリ・ファイル V4 に保存されているとき
        if file_version == "V4":
            # V4ファイル読込
            mm_table = EvaluationVersioning.read_evaluation_from_binary_v2_v3_file(
                    file_name=file_names_by_version[4])

            # 旧形式ファイル削除
            EvaluationVersioningPp.delete_old_files_cascade(
                    current_number=4,
                    file_names_by_version=file_names_by_version)

            return (mm_table, "V4", False)

        # バイナリ・ファイル V3 に保存されているとき
        if file_version == "V3":
            #mm_table = EvaluationVersioning.read_evaluation_from_binary_v2_v3_file(
            #        file_name=file_names_by_version[3])

            # バージョンアップする
            mm_table = EvaluationVersionUpMm.update_v3_to_v4(
                is_king_of_a=False, # PP だから
                is_king_of_b=False, # PP だから
                file_name=file_names_by_version[3])

            # 旧形式ファイル削除
            EvaluationVersioningPp.delete_old_files_cascade(
                    current_number=3,
                    file_names_by_version=file_names_by_version)

            # バージョンアップ
            return (mm_table, "V4", True)

        # バイナリV2ファイルに保存されているとき
        if file_version == "V2":

            # バージョンアップする
            mm_table = EvaluationVersionUpMm.update_v2_to_v3(
                file_name=file_names_by_version[2])

            # 旧形式ファイル削除
            EvaluationVersioningPp.delete_old_files_cascade(
                    current_number=2,
                    file_names_by_version=file_names_by_version)

            # バージョンアップ
            return (mm_table, "V3", True)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if file_version == "V1":
            mm_table = EvaluationVersioning.read_evaluation_from_binary_file(
                    file_name=file_names_by_version[1])

            # 旧形式ファイル削除
            EvaluationVersioningPp.delete_old_files_cascade(
                    current_number=1,
                    file_names_by_version=file_names_by_version)

            return (mm_table, "V1", False)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if file_version == "V0":
            mm_table = EvaluationVersioning.read_evaluation_from_text_file(
                    file_name=file_names_by_version[0])

            return (mm_table, "V0", False)

        # ファイルが存在しないとき
        return None


    @staticmethod
    def load_on_usinewgame(
            file_number):
        """ＰＰポリシー読込

        Returns
        -------
        - テーブル
        - バージョンアップしたので保存要求の有無
        """
        shall_save_file = False
        evaluation_kind = "pp"

        tuple = EvaluationVersioningPp.check_file_version_and_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            file_version = None
            file_name = None
        if tuple is not None:
            file_version, file_name = tuple

        if file_version is None:
            evaluation_kind = "pp_po"   # V3の途中までの旧称その２

            tuple = EvaluationVersioningPp.check_file_version_and_name(
                    file_number=file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        if file_version is None:
            evaluation_kind = "fmf_fmo"     # V3の途中までの旧称
            tuple = EvaluationVersioningPp.check_file_version_and_name(
                    file_number=file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        # 読込
        tuple = EvaluationVersioningPp.load_from_file(
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

        is_symmetrical_half_board = True

        if file_version == "V3":
            is_symmetrical_half_board = False

        evaluation_table_property = EvaluationTableProperty(
                is_king_size_of_a=False,    # P なんで
                is_king_size_of_b=False)    # P なんで


        if mm_table is None:
            # ファイルが存在しないとき
            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=evaluation_table_property.is_king_size_of_a,
                    is_king_of_b=evaluation_table_property.is_king_size_of_b,
                    is_symmetrical_half_board=is_symmetrical_half_board)

            mm_table = EvaluationVersioning.create_random_table(
                    hint=f'n{file_number}  kind=pp)',
                    table_size_obj=new_table_size_obj)

        pp_table = EvaluationTablePp(
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_table_property=evaluation_table_property,
                evaluation_mm_table=mm_table,
                is_symmetrical_half_board=is_symmetrical_half_board,
                is_file_modified=is_file_modified)

        return (pp_table, shall_save_file)


    @staticmethod
    def check_file_version_and_name(
            file_number,
            evaluation_kind):
        """ファイルのバージョンと、ファイル名のタプルを返す。無ければナン"""

        file_names_by_version = EvaluationVersioningPp.create_file_names_each_version(
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
