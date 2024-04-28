import datetime
from evaluation_file_pp import EvaluationFilePp
from evaluation_save import EvaluationSave


class EvaluationSavePp():


    @staticmethod
    def save_file_as_pp(
            pp_table_obj):
        """ＰＰ評価値ファイルの保存

        Parameters
        ----------
        pp_table_obj : EvaluationTableFacadePp
            ポリシーのPP関係の評価値テーブル
        """

        # 保存するかどうかは先に判定しておくこと
        if pp_table_obj.is_file_modified:
            # ＰＰポリシー
            file_name = EvaluationFilePp.create_file_name(
                    file_number=pp_table_obj.file_number)

            EvaluationSave.save_evaluation_file(
                    file_name=file_name,
                    raw_mm_table=pp_table_obj.raw_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] pp file not changed", flush=True)
