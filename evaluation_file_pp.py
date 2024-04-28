import os
import datetime
from evaluation_table_pp import EvaluationTablePp
from evaluation_file import EvaluationFile
from evaluation_table_property import EvaluationTableProperty
from evaluation_table_size_facade_pp import EvaluationTableSizeFacadePp
from evaluation_load import EvaluationLoad


class EvaluationFilePp():


    @staticmethod
    def create_file_name(
            file_number,
            evaluation_kind):
        return f'n{file_number}_eval_{evaluation_kind}.bin'


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

        file_name = EvaluationFilePp.create_file_name(
                file_number=file_number,
                evaluation_kind=evaluation_kind)

        print(f"[{datetime.datetime.now()}] {file_name} file exists check ...", flush=True)
        is_file_exists = os.path.isfile(file_name)


        # 読込
        if is_file_exists:
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
                is_king_size_of_a=False,            # P なんで
                is_king_size_of_b=False)            # P なんで

        if mm_table is None:
            # ファイルが存在しないとき
            new_table_size_obj = EvaluationTableSizeFacadePp.create_it(
                    evaluation_table_property=evaluation_table_property)

            mm_table = EvaluationFile.create_random_table(
                    hint=f'n{file_number}  kind=pp)',
                    table_size_obj=new_table_size_obj)

            shall_save_file = True
            is_file_modified = True

        pp_table = EvaluationTablePp(
                file_number=file_number,
                file_name=file_name,
                evaluation_table_property=evaluation_table_property,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified)

        return (pp_table, shall_save_file)
