import os
import datetime
from evaluation_table_kk import EvaluationTableKk
from evaluation_file import EvaluationFile
from evaluation_table_property import EvaluationTableProperty
from evaluation_table_size_facade_kk import EvaluationTableSizeFacadeKk
from evaluation_load import EvaluationLoad


class EvaluationFileKk():


    @staticmethod
    def create_file_name(
            file_number,
            evaluation_kind):
        return f'n{file_number}_eval_{evaluation_kind}.bin'


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

        file_name = EvaluationFileKk.create_file_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_name} file exists check ...", flush=True)
        is_file_exists = os.path.isfile(file_name)

        if is_file_exists:
            # 読込
            mm_table = EvaluationLoad.read_evaluation_file(
                    file_name=file_name)
        else:
            mm_table = None

        if mm_table is None:
            is_file_modified = True     # 新規作成だから
            shall_save_file = True      # 保存しておかないと、毎回作成して時間がかかる
        else:
            is_file_modified = False
            shall_save_file = False


        evaluation_table_property = EvaluationTableProperty(
                is_king_size_of_a=True,             # 玉の指し手は評価値テーブル・サイズを縮めれる
                is_king_size_of_b=True)             # 玉の指し手は評価値テーブル・サイズを縮めれる

        # ファイルが存在しないとき
        if mm_table is None:
            new_table_size_obj = EvaluationTableSizeFacadeKk.create_it(
                    evaluation_table_property=evaluation_table_property)
            mm_table = EvaluationFile.create_random_table(
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
