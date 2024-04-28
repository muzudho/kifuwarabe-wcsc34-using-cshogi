import datetime
from evaluation_versioning_pp import EvaluationVersioningPp
from evaluation_versioning import EvaluationVersioning


class EvaluationSavePp():


    @staticmethod
    def save_file_as_pp(
            pp_table_obj):
        """ＰＰ評価値ファイルの保存

        Parameters
        ----------
        pp_table_obj : EvaluationTablePp
            ポリシーのPP関係の評価値テーブル
        """

        # 保存するかどうかは先に判定しておくこと
        if pp_table_obj.is_file_modified:
            # ＰＰポリシー
            file_name = EvaluationVersioningPp.create_file_name(
                    file_number=pp_table_obj.file_number,
                    evaluation_kind="pp")   # V3 の途中からの新名を使っていく

            EvaluationVersioning.save_evaluation_to_file(
                    file_name=file_name,
                    evaluation_mm_table=pp_table_obj.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] pp file not changed", flush=True)
