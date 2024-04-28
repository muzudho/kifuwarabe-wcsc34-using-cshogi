import os
import datetime
from evaluation_kp_table import EvaluationKpTable
from evaluation_file_versioning import FileVersioning
from evaluation_file_version_up import EvaluationFileVersionUp
from evaluation_table_size import EvaluationTableSize


class EvaluationKpFileVersioning():


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
            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[3]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

        if 2 < current_number:
            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[2]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

        if 1 < current_number:
            # 旧形式のバイナリ・ファイルは削除
            old_file_name = file_names_by_version[1]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)

        if 0 < current_number:
            # 旧形式のテキスト・ファイルは削除
            old_file_name = file_names_by_version[0]
            if os.path.isfile(old_file_name):
                FileVersioning.delete_file(old_file_name)


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

        file_names_by_version = EvaluationKpFileVersioning.create_file_names_each_version(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[2]} file exists check ...", flush=True)

        # バイナリ・ファイル V4 に保存されているとき
        if file_version == "V4":
            # V4ファイル読込
            mm_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
                    file_name=file_names_by_version[4])

            # 旧形式ファイル削除
            EvaluationKpFileVersioning.delete_old_files_cascade(
                    current_number=4,
                    file_names_by_version=file_names_by_version)

            return (mm_table, "V4", False)

        # バイナリ・ファイル V3 に保存されているとき
        if file_version == "V3":

            ## V3ファイル読込
            #mm_table = FileVersioning.read_evaluation_from_binary_v2_v3_file(
            #        file_name=file_names_by_version[3])

            # バージョンアップする
            mm_table = EvaluationFileVersionUp.update_v3_to_v4(
                is_king_of_a=True,  # KP だから
                is_king_of_b=False, # KP だから
                file_name=file_names_by_version[3])

            # 旧形式ファイル削除
            EvaluationKpFileVersioning.delete_old_files_cascade(
                    current_number=3,
                    file_names_by_version=file_names_by_version)

            # バージョンアップ
            return (mm_table, "V4", True)

        # バイナリV2ファイルに保存されているとき
        if file_version == "V2":

            # バージョンアップする
            mm_table = EvaluationFileVersionUp.update_v2_to_v3(
                file_name=file_names_by_version[2])

            # 旧形式ファイル削除
            EvaluationKpFileVersioning.delete_old_files_cascade(
                    current_number=2,
                    file_names_by_version=file_names_by_version)

            # バージョンアップ
            return (mm_table, "V3", True)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[1]} file exists check ...", flush=True)

        # バイナリ・ファイルに保存されているとき
        if file_version == "V1":
            mm_table = FileVersioning.read_evaluation_from_binary_file(
                    file_name=file_names_by_version[1])

            # 旧形式ファイル削除
            EvaluationKpFileVersioning.delete_old_files_cascade(
                    current_number=1,
                    file_names_by_version=file_names_by_version)

            return (mm_table, "V1", False)

        print(f"[{datetime.datetime.now()}] {file_names_by_version[0]} file exists check ...", flush=True)

        # テキスト・ファイルに保存されているとき
        if file_version == "V0":
            mm_table = FileVersioning.read_evaluation_from_text_file(
                    file_name=file_names_by_version[0])

            return (mm_table, "V0", False)

        # ファイルが存在しないとき
        return None


    @staticmethod
    def load_on_usinewgame(
            file_number):
        """ＫＰポリシー読込

        Returns
        -------
        - テーブル
        - バージョンアップしたので保存要求の有無
        """
        shall_save_file = False
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
        tuple = EvaluationKpFileVersioning.load_from_file(
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
            # V3 から盤面を左右対称ではなく、全体を使うよう変更
            is_symmetrical_half_board = False

        if file_version == "V4":
            is_king_of_a = True     # 玉の指し手は評価値テーブル・サイズを縮めれる
            is_king_of_b = False    # P なんで
        else:
            is_king_of_a = False    # 過去バージョンではフラグ未対応
            is_king_of_b = False    # 過去バージョンではフラグ未対応

        # ファイルが存在しないとき
        if mm_table is None:
            new_table_size_obj = EvaluationTableSize(
                    is_king_of_a=is_king_of_a,
                    is_king_of_b=is_king_of_b,
                    is_symmetrical_half_board=is_symmetrical_half_board)

            mm_table = FileVersioning.create_random_table(
                    hint=f"n{file_number}  kind=kp)",
                    table_size_obj=new_table_size_obj)

        kp_table = EvaluationKpTable(
                file_number=file_number,
                file_name=file_name,
                file_version=file_version,
                evaluation_mm_table=mm_table,
                is_king_of_a=is_king_of_a,
                is_king_of_b=is_king_of_b,
                is_symmetrical_half_board=is_symmetrical_half_board,
                is_file_modified=is_file_modified)

        return (kp_table, shall_save_file)


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
