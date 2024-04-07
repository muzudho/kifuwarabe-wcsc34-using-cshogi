import cshogi
# import numpy as np
import random

# テストケース

test_case_1 = "position sfen 4r4/4l4/3nlnb2/3kps3/3g1G3/3SPK3/2BNLN3/4L4/4R4 b GS8Pgs8p 1"
"""Ｎｏ．１　駒の取り合い。次の一手は５五銀 S*5e """

test_case_1_1 = "position sfen 4r4/4l4/3nlnb2/3kps3/3g1G3/3SPK3/2BNLN3/4L4/4R4 b GS8Pgs8p 1 moves 4e3e"
"""Ｎｏ．１．１　変形。３五金。posval 35 で局面評価値確認"""

test_case_2 = "position sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B1R5/LNSGKGSNL b - 1"
"""Ｎｏ．２　初手、四間飛車。振り飛車しているかどうかの確認"""

test_case_3 = "position sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B7/LNSGKGSNL b R 1"
"""Ｎｏ．３　平手初期局面から、先手が飛車を駒台に乗せた局面"""

# 📖 [_cshogi.pyx](https://github.com/TadaoYamaoka/cshogi/blob/master/cshogi/_cshogi.pyx)


board = cshogi.Board()
"""盤"""


def usi_loop():
    """USIループ"""
    while True:

        cmd = input().split(' ', 1)
        """入力"""

        if cmd[0] == 'usi':
            """USIエンジン握手"""
            usi()

        elif cmd[0] == 'isready':
            """対局準備"""
            isready()

        elif cmd[0] == 'position':
            """局面データ解析"""
            position(cmd)

        elif cmd[0] == 'go':
            """思考開始～最善手返却"""
            go()

        elif cmd[0] == 'stop':
            """中断"""
            stop()

        elif cmd[0] == 'quit':
            """終了"""
            break

        # 以下、独自拡張

        elif cmd[0] == 'do':
            """一手指す
            example: ７六歩
                code: do 7g7f
            """
            do(cmd)

        elif cmd[0] == 'undo':
            """一手戻す
                code: undo
            """
            undo()

        elif cmd[0] == 'lottery':
            """くじ一覧"""
            lottery()


def usi():
    """USIエンジン握手"""
    print('id name KifuwarabeWCSC34')
    print('usiok', flush=True)


def isready():
    """対局準備"""
    print('readyok', flush=True)


def position(cmd):
    """局面データ解析"""
    pos = cmd[1].split('moves')
    position_detail(pos[0].strip(), pos[1].split() if len(pos) > 1 else [])


def position_detail(sfen, usi_moves):
    """局面データ解析"""

    if sfen == 'startpos':
        """平手初期局面に変更"""
        board.reset()

    elif sfen[:5] == 'sfen ':
        """指定局面に変更"""
        board.set_sfen(sfen[5:])

    for usi_move in usi_moves:
        """棋譜再生"""
        board.push_usi(usi_move)


def go():
    """思考開始～最善手返却"""
    (bestmove, beta) = think(board)
    alpha = -beta
    print(f'info depth 0 seldepth 1 time 1 nodes 1 score cp {alpha} string x')
    print(f'bestmove {bestmove}', flush=True)


def stop():
    """中断"""
    print('bestmove resign' , flush=True)


def do(cmd):
    """一手指す
    example: ７六歩
        code: do 7g7f
    """
    board.push_usi(cmd[1])


def undo():
    """一手戻す
        code: undo
    """
    board.pop()


def lottery():
    """くじ一覧"""

    print('くじ一覧：')

    # USIプロトコルでの符号表記に変換
    move_list_as_usi = []

    for move in board.legal_moves:
        move_list_as_usi.append(cshogi.move_to_usi(move))

    # ソート
    move_list_as_usi.sort()

    # 表示
    number = 1

    for move_as_usi in move_list_as_usi:
        print(f'  ({number:3}) {move_as_usi}')
        number += 1


def think():
    """それをする"""

    if board.is_game_over():
        """投了局面時"""

        return ('resign', 0)
        """投了"""

    if board.is_nyugyoku():
        """入玉宣言局面時"""

        return ('win', 0)
        """勝利宣言"""

    if not board.is_check():
        """自玉に王手がかかっていない時"""

        if (matemove:=board.mate_move_in_1ply()):
            """あれば、一手詰めの指し手を取得"""

            print('info score mate 1 pv {}'.format(cshogi.move_to_usi(matemove)))
            return (cshogi.move_to_usi(matemove), 0)

    bestmove_list = list(board.legal_moves)
    bestmove = random.choice(bestmove_list)
    """候補手の中からランダムに選ぶ"""

    # 未使用
    alpha = 0

    return (cshogi.move_to_usi(bestmove), alpha)
    """指し手の記法で返却"""


if __name__ == '__main__':
    """コマンドから実行時"""
    usi_loop()

