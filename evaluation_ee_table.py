import os
import datetime
import random


class EvaluationEeTable():


    def __init__(
            self,
            file_number,
            evaluation_kind,
            file_name,
            bin_file_name,
            bin_v2_file_name,
            move_size,
            table_size
    ):
        self._file_number = file_number
        self._evaluation_kind = evaluation_kind
        self._file_name = file_name                 # 旧
        self._bin_file_name = bin_file_name         # 旧
        self._bin_v2_file_name = bin_v2_file_name   # 新
        self._move_size = move_size
        self._table_size = table_size

        self._file_modified = False
        self._evaluation_ee_table = [0] * self._table_size


    def exists_text_file(self):
        """テキスト・ファイルは存在するか？"""
        return os.path.isfile(self._file_name)


    def exists_binary_file(self):
        """バイナリ・ファイルは存在するか？"""
        return os.path.isfile(self._bin_file_name)


    def exists_binary_v2_file(self):
        """バイナリV2ファイルは存在するか？"""
        return os.path.isfile(self._bin_v2_file_name)


    def reset_to_random_table(self):
        """ランダム値の入った評価値テーブルを新規作成する"""
        # ダミーデータを入れる。１分ほどかかる
        print(f"[{datetime.datetime.now()}] make random {self._evaluation_kind} evaluation table in memory ...", flush=True)

        for index in range(0, self._table_size):
            # 値は 0, 1 の２値
            self._evaluation_ee_table[index] = random.randint(0,1)

        print(f"[{datetime.datetime.now()}] {self._evaluation_kind} evaluation table maked in memory", flush=True)
        self._file_modified = True
