import datetime
import random


class EvaluationTableRawRandom():


    def create_random_table(
            hint,
            table_size_obj):
        """ランダム値の入った評価値テーブルを新規作成する

        Parameters
        ----------
        table_size_obj : EvaluationTableSize
            テーブル・サイズ。計算過程付き
        """

        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random evaluation table in memory. hint: '{hint}' ... table_size_obj:({table_size_obj.to_debug_str()})", flush=True)

        new_mm_table = []

        for _index in range(0, table_size_obj.relation):
            # 値は 0, 1 の２値
            new_mm_table.append(random.randint(0,1))

        print(f"[{datetime.datetime.now()}] random evaluation table maked in memory.", flush=True)
        return new_mm_table
