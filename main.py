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


def usi_loop(kifuwarabe):
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
            position(kifuwarabe, cmd)

        elif cmd[0] == 'go':
            """思考開始～最善手返却"""
            go(kifuwarabe)

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
            do(kifuwarabe, cmd)

        elif cmd[0] == 'undo':
            """一手戻す
                code: undo
            """
            undo(kifuwarabe)

        elif cmd[0] == 'moveval':
            """１手読みでの指し手の評価値一覧"""
            moveval(kifuwarabe)


def usi():
    """USIエンジン握手"""
    print('id name KifuwarabeWCSC34')
    print('usiok', flush=True)


def isready():
    """対局準備"""
    print('readyok', flush=True)


def position(kifuwarabe, cmd):
    """局面データ解析"""
    pos = cmd[1].split('moves')
    kifuwarabe.position(pos[0].strip(), pos[1].split() if len(pos) > 1 else [])


def go(kifuwarabe):
    """思考開始～最善手返却"""
    (bestmove, beta) = kifuwarabe.colleague.thought.do_it()
    alpha = -beta
    print(f'info depth 1 seldepth 1 time 1 nodes 1 score cp {alpha} string x')
    print(f'bestmove {bestmove}', flush=True)


def stop():
    """中断"""
    print('bestmove resign' , flush=True)


def do(kifuwarabe, cmd):
    """一手指す
    example: ７六歩
        code: do 7g7f
    """
    kifuwarabe.subordinate.board.push_usi(cmd[1])


def undo(kifuwarabe):
    """一手戻す
        code: undo
    """
    kifuwarabe.subordinate.board.pop()

def moveval(kifuwarabe):
    """１手読みでの指し手の評価値一覧"""

    old_depth = kifuwarabe.colleague.thought.depth
    kifuwarabe.colleague.thought.depth = 1

    for move in kifuwarabe.subordinate.board.legal_moves:
        kifuwarabe.subordinate.board.push(move)
        # 一手指す

        # 局面評価値表示
        print('局面評価値内訳：')
        value_list = 0
        for index, value in enumerate(value_list):
            print(f'　　（{index:2}） {value:10}')
        print(f'　　（計） {sum(value_list):10}')

        kifuwarabe.subordinate.board.pop()
        # 一手戻す

    kifuwarabe.colleague.thought.depth = old_depth


class Kifuwarabe():
    """きふわらべ"""

    def __init__(self):
        """初期化"""

        self._board = cshogi.Board()
        """盤"""

        self._colleague = KifuwarabesColleague(board=self._board)
        """きふわらべの同僚"""


    @property
    def colleague(self):
        """きふわらべの同僚"""
        return self._colleague

    def position(self, sfen, usi_moves):
        """局面データ解析"""

        if sfen == 'startpos':
            """平手初期局面に変更"""
            self.board.reset()

        elif sfen[:5] == 'sfen ':
            """指定局面に変更"""
            self.board.set_sfen(sfen[5:])

        for usi_move in usi_moves:
            """棋譜再生"""
            self.board.push_usi(usi_move)

    @property
    def board(self):
        """盤"""
        return self._board


class KifuwarabesColleague():
    """きふわらべの同僚"""

    def __init__(self, board):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        """

        self._board = board
        """盤"""

        self._board_value = BoardValue(
            board=self._board)
        """盤の決まりきった価値"""

        self._thought = Thought(
            board=self._board)
        """思考"""

    @property
    def board(self):
        """盤"""
        return self._board

    @property
    def board_value(self):
        """盤の決まりきった価値"""
        return self._board_value

    @property
    def thought(self):
        """思考"""
        return self._thought


class BoardValue():
    """盤の決まりきった価値"""

    def __init__(self, board):
        """初期化

        Parameters
        ----------
        board
            盤
        """

        self._board = board
        """盤"""

    @property
    def board(self):
        """盤"""
        return self._board

    def eval(self):
        """評価"""

        if self.board.is_game_over():
            # 負け
            return -30000

        if self.board.is_nyugyoku():
            # 入玉宣言勝ち
            return 30000

        draw = self.board.is_draw(16)

        if draw == cshogi.REPETITION_DRAW:
            # 千日手
            return 0

        if draw == cshogi.REPETITION_WIN:
            # 千日手で勝ち
            return 30000

        if draw == cshogi.REPETITION_LOSE:
            # 千日手で負け
            return -30000

        if draw == cshogi.REPETITION_SUPERIOR:
            # 千日手の上限？？
            return 30000

        if draw == cshogi.REPETITION_INFERIOR:
            # 千日手の下限？？
            return -30000

        """別途、計算が必要"""
        return None


class Thought():
    """思考。
    主に、そのための設定"""

    def __init__(self, board):
        """初期化

        Parameters
        ----------
        board
            盤
        """

        self._board = board
        """盤"""

        self._depth = 3
        """読みの深さ"""

    @property
    def board(self):
        """盤"""
        return self._board

    @property
    def depth(self):
        """読みの深さ"""
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    def do_it(self):
        """それをする"""

        if self.board.is_game_over():
            """投了局面時"""

            return ('resign', 0)
            """投了"""

        if self.board.is_nyugyoku():
            """入玉宣言局面時"""

            return ('win', 0)
            """勝利宣言"""

        if not self.board.is_check():
            """自玉に王手がかかっていない時"""

            if (matemove:=self.board.mate_move_in_1ply()):
                """あれば、一手詰めの指し手を取得"""

                print('info score mate 1 pv {}'.format(cshogi.move_to_usi(matemove)))
                return (cshogi.move_to_usi(matemove), 0)

        bestmove_list = list(self.board.legal_moves)
        bestmove = random.choice(bestmove_list)
        """候補手の中からランダムに選ぶ"""

        # 未使用
        alpha = 0

        return (cshogi.move_to_usi(bestmove), alpha)
        """指し手の記法で返却"""


def main():
    kifuwarabe = Kifuwarabe()
    usi_loop(kifuwarabe)



if __name__ == '__main__':
    """コマンドから実行時"""
    main()

