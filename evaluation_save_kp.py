import datetime
from evaluation_file_kp import EvaluationFileKp
from evaluation_save import EvaluationSave


class EvaluationSaveKp():


    @staticmethod
    def save_file_as_kp(
            kp_table_obj):
        """ＫＰ評価値ファイルの保存

        Parameters
        ----------
        kp_table_obj : EvaluationTableMm
            ポリシーのKP関係の評価値テーブル
        """

        # 保存するかどうかは先に判定しておくこと
        if kp_table_obj.is_file_modified:
            # ＫＰポリシー
            file_name = EvaluationFileKp.create_file_name(
                    file_number=kp_table_obj.file_number)

            EvaluationSave.save_evaluation_file(
                    file_name=file_name,
                    raw_mm_table=kp_table_obj.raw_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kp file not changed", flush=True)
