import os
import datetime


class ResultFile():
    """結果ファイル"""


    def __init__(self, file_number):
        """初期化

        Parameters
        ----------
        file_number : int
            ファイル番号
        """
        self._file_number = file_number
        self._file_name = f'n{file_number}_result.txt'


    @property
    def file_name(self):
        """ファイル名"""
        return self._file_name


    def exists(self):
        """ファイルの存在確認"""
        return os.path.isfile(self.file_name)


    def delete(self):
        """ファイルの削除"""
        print(f"[{datetime.datetime.now()}] {self.file_name} file delete...", flush=True)
        os.remove(self.file_name)
        print(f"[{datetime.datetime.now()}] {self.file_name} file deleted", flush=True)


    def read(self):
        try:
            """結果の読込"""
            print(f"[{datetime.datetime.now()}] {self.file_name} file read ...", flush=True)

            with open(self.file_name, 'r', encoding="utf-8") as f:
                text = f.read()

            text = text.strip()
            print(f"[{datetime.datetime.now()}] {self.file_name} file read", flush=True)

            return text

        # ファイルの読込に失敗したら、空文字を返す
        except:
            return ""


    def save_lose(self):
        """負け"""
        print("あ～あ、負けたぜ（＞＿＜）", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write("lose")

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)

    def save_win(self):
        """勝ち"""
        print("やったぜ　勝ったぜ（＾ｑ＾）", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write("win")

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)

    def save_draw(self):
        """持将棋"""
        print("持将棋か～（ー＿ー）", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write("draw")

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)

    def save_otherwise(self, result_text):
        """予期しない結果"""
        print(f"なんだろな（・＿・）？　{result_text}", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write(result_text)

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)
