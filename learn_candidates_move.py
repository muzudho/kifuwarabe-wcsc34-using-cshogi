import os
import datetime


class LearnCandidatesMove():
    """候補に挙がった手は全て覚えておく

    勝ったら、全部忘れる
    """


    def __init__(
            self):
        self._move_set = set()
        self._is_file_modified = False


    @property
    def file_name(self):
        """ファイル名"""
        return self._file_name


    @property
    def move_set(self):
        """指し手の集合"""
        return self._move_set


    def delete_file(self):
        """削除"""
        try:
            print(f"[{datetime.datetime.now()}] {self.file_name} file delete...", flush=True)
            os.remove(self.file_name)
            print(f"[{datetime.datetime.now()}] {self.file_name} file deleted", flush=True)

        except FileNotFoundError:
            # ファイルが無いのなら、削除に失敗しても問題ない
            pass
