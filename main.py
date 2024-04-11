import cshogi
import random
import datetime
from canditates_memory import CanditatesMemory
from evaluation_table import EvaluationTable
from feeling_luckey import choice_lottery
from result_file import ResultFile


class Kifuwarabe():
    """きふわらべ"""


    def __init__(self):
        """初期化"""

        # さいころに倣って６個
        self._player_file_number = None

        # 盤
        self._board = cshogi.Board()

        # 候補に挙がった手は全て覚えておく
        self._canditates_memory = None

        # 評価値テーブル
        self._evaluation_table = None

        # 結果ファイル（デフォルト）
        self._result_file = None


    def usi_loop(self):
        """USIループ"""

        while True:

            # 入力
            cmd = input().split(' ', 1)

            # USIエンジン握手
            if cmd[0] == 'usi':
                self.usi()

            # 対局準備
            elif cmd[0] == 'isready':
                self.isready()

            # 新しい対局
            elif cmd[0] == 'usinewgame':
                self.usinewgame()

            # 局面データ解析
            elif cmd[0] == 'position':
                self.position(cmd)

            # 思考開始～最善手返却
            elif cmd[0] == 'go':
                self.go()

            # 中断
            elif cmd[0] == 'stop':
                self.stop()

            # 対局終了
            elif cmd[0] == 'gameover':
                self.gameover(cmd)

            # アプリケーション終了
            elif cmd[0] == 'quit':
                break

            # 以下、独自拡張

            # 一手指す
            # example: ７六歩
            #       code: do 7g7f
            elif cmd[0] == 'do':
                self.do(cmd)

            # 一手戻す
            #       code: undo
            elif cmd[0] == 'undo':
                self.undo()

            # くじ一覧
            elif cmd[0] == 'lottery':
                self.lottery()


    def usi(self):
        """USIエンジン握手"""
        print('id name KifuwarabeWCSC34')
        print('usiok', flush=True)


    def isready(self):
        """対局準備"""
        print('readyok', flush=True)


    def usinewgame(self):
        """新しい対局"""

        # さいころに倣って６個
        self._player_file_number = random.randint(1,6)

        # 前回の対局の指し手の候補手の記憶
        self._canditates_memory = CanditatesMemory.load_from_file(self._player_file_number)

        # 結果ファイル（デフォルト）
        self._result_file = ResultFile(self._player_file_number)

        # 評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する
        self._evaluation_table = EvaluationTable(file_number=self._player_file_number)
        self._evaluation_table.load_from_file_or_random_table(self._result_file)
        self._evaluation_table.update_evaluation_table(self._canditates_memory, self._result_file)

        # 結果ファイルを削除
        if self._result_file.exists():
            self._result_file.delete()

        print(f"[{datetime.datetime.now()}] usinewgame end", flush=True)

    def position(self, cmd):
        """局面データ解析"""
        pos = cmd[1].split('moves')
        self.position_detail(pos[0].strip(), pos[1].split() if len(pos) > 1 else [])


    def position_detail(self, sfen, usi_moves):
        """局面データ解析"""

        if sfen == 'startpos':
            """平手初期局面に変更"""
            self._board.reset()

        elif sfen[:5] == 'sfen ':
            """指定局面に変更"""
            self._board.set_sfen(sfen[5:])

        for usi_move in usi_moves:
            """棋譜再生"""
            self._board.push_usi(usi_move)


    def go(self):
        """思考開始～最善手返却"""

        if self._board.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._board.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not self._board.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._board.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return

        # くじを引く
        best_move = choice_lottery(self._evaluation_table, list(self._board.legal_moves), self._canditates_memory)

        print(f"info depth 0 seldepth 0 time 1 nodes 0 score cp 0 string I'm feeling luckey")
        print(f'bestmove {best_move}', flush=True)


    def stop(self):
        """中断"""
        print('bestmove resign', flush=True)


    def gameover(self, cmd):
        """対局終了"""

        if 2 <= len(cmd):
            # 負け
            if cmd[1] == 'lose':
                self._result_file.save_lose()
                self._canditates_memory.save()

            # 勝ち
            elif cmd[1] == 'win':
                self._result_file.save_win()
                self._canditates_memory.save()
                self._evaluation_table.save_evaluation_to_file()

            # 持将棋
            elif cmd[1] == 'draw':
                self._result_file.save_draw()
                self._canditates_memory.save()

            # その他
            else:
                self._result_file.save_otherwise(cmd[1])
                self._canditates_memory.save()


    def do(self, cmd):
        """一手指す
        example: ７六歩
            code: do 7g7f
        """
        self._board.push_usi(cmd[1])


    def undo(self):
        """一手戻す
            code: undo
        """
        self._board.pop()


    def lottery(self):
        """くじ一覧"""

        print('くじ一覧：')

        # USIプロトコルでの符号表記に変換
        sorted_legal_move_list_as_usi = []

        for move in self._board.legal_moves:
            sorted_legal_move_list_as_usi.append(cshogi.move_to_usi(move))

        # ソート
        sorted_legal_move_list_as_usi.sort()

        # 候補手に評価値を付けた辞書を作成
        move_score_dictionary = self._evaluation_table.make_move_score_dictionary(sorted_legal_move_list_as_usi)

        # 表示
        number = 1

        for move_a_as_usi in sorted_legal_move_list_as_usi:

            # 指し手の評価値
            move_value = move_score_dictionary[move_a_as_usi]

            print(f'  ({number:3}) {move_a_as_usi:5} = {self._evaluation_table.get_evaluation_table_index_from_move_as_usi(move_a_as_usi):5} value:{move_value:3}')
            number += 1


if __name__ == '__main__':
    """コマンドから実行時"""
    try:
        kifuwarabe = Kifuwarabe()
        kifuwarabe.usi_loop()

    except Exception as err:
        print(f"[unexpected error] {err=}, {type(err)=}")
        raise

