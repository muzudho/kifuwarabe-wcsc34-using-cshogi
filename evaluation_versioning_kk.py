import os
import datetime
from evaluation_table_kk import EvaluationTableKk
from evaluation_versioning import EvaluationVersioning
from evaluation_table_property import EvaluationTableProperty
from evaluation_table_size_facade_kk import EvaluationTableSizeFacadeKk
from evaluation_load import EvaluationLoad


class EvaluationVersioningKk():


    @staticmethod
    def create_file_name(
            file_number,
            evaluation_kind):
        return f'n{file_number}_eval_{evaluation_kind}.bin'


    @staticmethod
    def load_from_file(
            file_number,
            evaluation_kind):
        """評価関数テーブルをファイルから読み込む

        Returns
        -------
        - mm_table
        """

        file_name = EvaluationVersioningKk.create_file_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_name} file exists check ...", flush=True)

        mm_table = EvaluationLoad.read_evaluation_file(
                file_name=file_name)

        return mm_table


    @staticmethod
    def load_on_usinewgame(
            file_number):
        """ＫＫポリシー読込

        Returns
        -------
        - テーブル
        - バージョンアップしたので保存要求の有無
        """
        shall_save_file = False
        evaluation_kind = "kk"

        file_name, is_file_exists = EvaluationVersioningKk.check_file_exists(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        # 読込
        tuple = EvaluationVersioningKk.load_from_file(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
            shall_save_file = True      # 保存しておかないと、毎回作成して時間がかかる
        else:
            mm_table, shall_save_file = tuple
            is_file_modified = mm_table is None


        evaluation_table_property = EvaluationTableProperty(
                is_king_size_of_a=True,             # 玉の指し手は評価値テーブル・サイズを縮めれる
                is_king_size_of_b=True)             # 玉の指し手は評価値テーブル・サイズを縮めれる

        # ファイルが存在しないとき
        if mm_table is None:
            new_table_size_obj = EvaluationTableSizeFacadeKk.create_it(
                    evaluation_table_property=evaluation_table_property)
            mm_table = EvaluationVersioning.create_random_table(
                    hint=f"n{file_number}  kind=kk)",
                    table_size_obj=new_table_size_obj)

            shall_save_file = True
            is_file_modified = True

        kk_table = EvaluationTableKk(
                file_number=file_number,
                file_name=file_name,
                evaluation_table_property=evaluation_table_property,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified)

        return (kk_table, shall_save_file)


    @staticmethod
    def check_file_exists(
            file_number,
            evaluation_kind):
        """ファイルの存在確認"""

        file_name = EvaluationVersioningKk.create_file_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_name} file exists check ...", flush=True)

        return (file_name, os.path.isfile(file_name))
