import os
import datetime


def exists_result_file():
    """ファイルの存在確認"""
    return os.path.isfile('result.txt')


def delete_result_file():
    """ファイルの削除"""
    os.remove('result.txt')


def read_result_file():
    """結果の読込"""
    with open('result.txt', 'r', encoding="utf-8") as f:
        text = f.read()
        print(f"[{datetime.datetime.now()}] result.txt read ...")

    return text.strip()


def save_lose():
    """負け"""
    print("あ～あ、負けたぜ（＞＿＜）", flush=True)

    # ファイルに出力する
    with open('result.txt', 'w', encoding="utf-8") as f:
        f.write("lose")

def save_win():
    """勝ち"""
    print("やったぜ　勝ったぜ（＾ｑ＾）", flush=True)

    # ファイルに出力する
    with open('result.txt', 'w', encoding="utf-8") as f:
        f.write("win")

def save_draw():
    """持将棋"""
    print("持将棋か～（ー＿ー）", flush=True)

    # ファイルに出力する
    with open('result.txt', 'w', encoding="utf-8") as f:
        f.write("draw")

def save_otherwise(result_text):
    print(f"なんだろな（・＿・）？　{result_text}", flush=True)

    # ファイルに出力する
    with open('result.txt', 'w', encoding="utf-8") as f:
        f.write(result_text)
