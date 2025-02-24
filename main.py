import cshogi
import random
import datetime

from src.kifuwarabe_using_cshogi.shogi_engine_with_usi import Kifuwarabe


if __name__ == '__main__':
    """コマンドから実行時"""
    try:
        kifuwarabe = Kifuwarabe()
        kifuwarabe.usi_loop()

    except Exception as err:
        print(f"[unexpected error] {err=}, {type(err)=}")
        raise

