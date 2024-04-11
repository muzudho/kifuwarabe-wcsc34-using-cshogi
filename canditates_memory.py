import os
import datetime


class CanditatesMemory():
    """候補に挙がった手は全て覚えておく"""


    @classmethod
    def load_from_file(clazz, file_number):
        """読込"""
        candidates_memory = CanditatesMemory(file_number)

        # ファイルが存在するとき
        if os.path.isfile(candidates_memory.file_name):
            print(f"[{datetime.datetime.now()}] read {candidates_memory.file_name} file ...", flush=True)

            with open(candidates_memory.file_name, 'r', encoding="utf-8") as f:
                text = f.read()
                print(f"[{datetime.datetime.now()}] {candidates_memory.file_name} read", flush=True)

            candidates_memory._move_set = set(text.split(' '))

        return candidates_memory


    def __init__(self, file_number):
        """初期化"""
        self._file_number = file_number
        self._file_name = f'n{self._file_number}_canditates_memory.txt'

        self._move_set = set()
        self._file_modified = False


    @property
    def file_name(self):
        """ファイル名"""
        return self._file_name


    def save(self):
        """保存"""
        print(f"[{datetime.datetime.now()}] save {self.file_name} file ...", flush=True)

        # ファイルに出力する
        with open(self.file_name, 'w', encoding="utf-8") as f:
            # 配列の要素の整数型を文字列型に変換して隙間を空けずに連結
            text = ''.join(map(str,self._move_set))
            print(f"[{datetime.datetime.now()}] text created ...", flush=True)

            f.write(text)

        self._file_modified = False

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)


    def union_dictionary(self, move_score_dictionary):
        # 和集合
        self._move_set.union(move_score_dictionary.keys())

        # 変わってないかも知らんけど
        self._file_modified = True
