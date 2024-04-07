import cshogi
from feeling_luckey import choice_lottery
from evaluation_table import EvaluationTable


board = cshogi.Board()
"""盤"""

evaluation_table = EvaluationTable()
"""評価値テーブル"""


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

        elif cmd[0] == 'gameover':
            """対局終了"""
            gameover(cmd)

        elif cmd[0] == 'quit':
            """アプリケーション終了"""
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

    # 評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する
    evaluation_table.load_or_new_evaluation_table()

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

    if board.is_game_over():
        """投了局面時"""

        # 投了
        print(f'resign', flush=True)
        return

    if board.is_nyugyoku():
        """入玉宣言局面時"""

        # 勝利宣言
        print(f'win', flush=True)
        return

    # 一手詰めを詰める
    if not board.is_check():
        """自玉に王手がかかっていない時で"""

        if (matemove := board.mate_move_in_1ply()):
            """一手詰めの指し手があれば、それを取得"""

            print('info score mate 1 pv {}'.format(cshogi.move_to_usi(matemove)), flush=True)
            return

    # くじを引く
    bestmove = choice_lottery(evaluation_table, list(board.legal_moves))

    print(f"info depth 0 seldepth 0 time 1 nodes 0 score cp 0 string I'm feeling luckey")
    print(f'bestmove {bestmove}', flush=True)


def stop():
    """中断"""
    print('bestmove resign', flush=True)


def gameover(cmd):
    """対局終了"""

    if 2 <= len(cmd):
        if cmd[1] == 'lose':
            print("あ～あ、負けたぜ（ー＿ー）", flush=True)
        elif cmd[1] == 'win':
            print("やったぜ　勝ったぜ（＾ｑ＾）", flush=True)
        else:
            print(f"なんだろな（・＿・）？　{cmd[1]}", flush=True)


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
    sorted_legal_move_list_as_usi = []

    for move in board.legal_moves:
        sorted_legal_move_list_as_usi.append(cshogi.move_to_usi(move))

    # ソート
    sorted_legal_move_list_as_usi.sort()

    # 候補手に評価値を付けた辞書を作成
    move_score_dictionary = evaluation_table.make_move_score_dictionary(sorted_legal_move_list_as_usi)

    # 表示
    number = 1

    for move_a_as_usi in sorted_legal_move_list_as_usi:

        # 指し手の評価値
        move_value = move_score_dictionary[move_a_as_usi]

        print(f'  ({number:3}) {move_a_as_usi:5} = {evaluation_table.get_evaluation_table_index_from_move_as_usi(move_a_as_usi):5} value:{move_value:3}')
        number += 1


if __name__ == '__main__':
    """コマンドから実行時"""
    usi_loop()

