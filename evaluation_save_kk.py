import datetime
from evaluation_file_kk import EvaluationFileKk
from evaluation_file import EvaluationFile


class EvaluationSaveKk():


    @staticmethod
    def save_file_as_kk(
            kk_table_obj):
        """ＫＫ評価値ファイルの保存

        Parameters
        ----------
        kk_table_obj : EvaluationTableKk
            ポリシーのKK関係の評価値テーブル
        """

        # 保存するかどうかは先に判定しておくこと
        if kk_table_obj.is_file_modified:
            file_name = EvaluationFileKk.create_file_name(
                    file_number=kk_table_obj.file_number,
                    evaluation_kind="kk")

            EvaluationFile.save_evaluation_to_file(
                    file_name=file_name,
                    evaluation_mm_table=kk_table_obj.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kk file not changed", flush=True)
