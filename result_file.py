import os
import datetime
from turn import Turn


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

        try:
            print(f"[{datetime.datetime.now()}] {self.file_name} file delete...", flush=True)
            os.remove(self.file_name)
            print(f"[{datetime.datetime.now()}] {self.file_name} file deleted", flush=True)

        except FileNotFoundError:
            # ファイルが無いのなら、削除に失敗しても問題ない
            pass


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


    def save_lose(self, my_turn):
        """負け"""

        turn_text = Turn.to_string(my_turn)
        print(f"あ～あ、 {turn_text} 番で負けたぜ（＞＿＜）", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write(f"lose {turn_text}")

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)

    def save_win(self, my_turn):
        """勝ち"""

        turn_text = Turn.to_string(my_turn)
        print(f"やったぜ {turn_text} 番で勝ったぜ（＾ｑ＾）", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write(f"win {turn_text}")

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)

    def save_draw(self, my_turn):
        """持将棋"""

        turn_text = Turn.to_string(my_turn)
        print(f"持将棋か～（ー＿ー） turn: {turn_text}", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write(f"draw {turn_text}")

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)

    def save_otherwise(self, result_text, my_turn):
        """予期しない結果"""

        turn_text = Turn.to_string(my_turn)
        print(f"なんだろな（・＿・）？　'{result_text}', turn: '{turn_text}'", flush=True)

        # ファイルに出力する
        print(f"[{datetime.datetime.now()}] {self.file_name} file save ...", flush=True)
        with open(self.file_name, 'w', encoding="utf-8") as f:
            f.write(f"{result_text} {turn_text}")

        print(f"[{datetime.datetime.now()}] {self.file_name} file saved", flush=True)
