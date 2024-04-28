import os
import datetime
from evaluation_table_facade_kk import EvaluationTableKk
from evaluation_table_size_facade_kk import EvaluationTableSizeFacadeKk
from evaluation_load import EvaluationLoad
from evaluation_table_raw_random import EvaluationTableRawRandom


class EvaluationFileKk():


    @staticmethod
    def create_file_name(
            file_number):
        return f'n{file_number}_eval_kk.bin'


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

        file_name = EvaluationFileKk.create_file_name(
                file_number=file_number)

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


        # ファイルが存在しないとき
        if mm_table is None:
            new_table_size_obj = EvaluationTableSizeFacadeKk.create_it()
            mm_table = EvaluationTableRawRandom.create_random_table(
                    hint=f"n{file_number}  kind=kk)",
                    table_size_obj=new_table_size_obj)

            shall_save_file = True
            is_file_modified = True

        kk_table = EvaluationTableKk.create_it(
                file_number=file_number,
                file_name=file_name,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified)

        return (kk_table, shall_save_file)
