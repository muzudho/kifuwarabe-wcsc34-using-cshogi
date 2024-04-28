import datetime
from evaluation_versioning_kp import EvaluationVersioningKp
from evaluation_versioning import EvaluationVersioning


class EvaluationSaveKp():


    @staticmethod
    def save_file_as_kp(
            kp_table_obj):
        """ＫＰ評価値ファイルの保存

        Parameters
        ----------
        kp_table_obj : EvaluationTableKp
            ポリシーのKP関係の評価値テーブル
        """

        # 保存するかどうかは先に判定しておくこと
        if kp_table_obj.is_file_modified:
            # ＫＰポリシー
            file_names_by_version = EvaluationVersioningKp.create_file_names_each_version(
                    file_number=kp_table_obj.file_number,
                    evaluation_kind="kp")    # V3 の途中からの新名を使っていく

            file_name = file_names_by_version[4]    # V4

            EvaluationVersioning.save_evaluation_to_file(
                    file_name=file_name,
                    evaluation_mm_table=kp_table_obj.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kp file not changed", flush=True)
