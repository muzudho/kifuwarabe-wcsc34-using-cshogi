import datetime
from evaluation_versioning_kk import EvaluationVersioningKk
from evaluation_versioning import EvaluationVersioning


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
            file_names_by_version = EvaluationVersioningKk.create_file_names_each_version(
                    file_number=kk_table_obj.file_number,
                    evaluation_kind="kk")

            file_name = file_names_by_version[5]    # V5

            EvaluationVersioning.save_evaluation_to_file(
                    file_name=file_name,
                    evaluation_mm_table=kk_table_obj.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kk file not changed", flush=True)
