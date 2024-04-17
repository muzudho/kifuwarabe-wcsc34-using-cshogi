import cshogi
import random
import datetime
from canditates_memory import CanditatesMemory
from evaluation_table import EvaluationTable
from feeling_luckey import choice_lottery
from ko_memory import KoMemory
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

        # コウの記憶
        self._ko_memory = None

        # 結果ファイル（デフォルト）
        self._result_file = None

        # 自分の手番（初期値はダミー値）
        self._my_turn = cshogi.BLACK


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

        # コウの記録
        self._ko_memory = KoMemory()

        # 結果ファイル（デフォルト）
        self._result_file = ResultFile(self._player_file_number)

        # 評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する
        self._evaluation_table = EvaluationTable(file_number=self._player_file_number)
        self._evaluation_table.load_from_file_or_random_table()
        self._evaluation_table.update_evaluation_table(self._canditates_memory, self._result_file)

        ## 結果ファイルを削除
        #if self._result_file.exists():
        #    self._result_file.delete()

        print(f"[{datetime.datetime.now()}] usinewgame end", flush=True)


    def position(self, cmd):
        """局面データ解析"""
        pos = cmd[1].split('moves')
        sfen_text = pos[0].strip()
        # 区切りは半角空白１文字とします
        moves_text = (pos[1].split(' ') if len(pos) > 1 else [])
        self.position_detail(sfen_text, moves_text)


    def position_detail(self, sfen_text, moves_text_as_usi):
        """局面データ解析"""

        # 平手初期局面に変更
        if sfen_text == 'startpos':
            self._board.reset()

        # 指定局面に変更
        elif sfen_text[:5] == 'sfen ':
            self._board.set_sfen(sfen_text[5:])

        # 棋譜再生
        for move_as_usi in moves_text_as_usi:
            self._board.push_usi(move_as_usi)

        # 局面の手番を、自分の手番とする
        self._my_turn = self._board.turn

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
        best_move = choice_lottery(
                self._evaluation_table,
                list(self._board.legal_moves),
                self._canditates_memory,
                self._ko_memory,
                self._board)

        # コウを更新
        self._ko_memory.enqueue(best_move)

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
                # ［対局結果］　常に記憶する
                self._result_file.save_lose(self._my_turn)

                # ［指した手］　勝っていないなら追加していく
                self._canditates_memory.save()

            # 勝ち
            elif cmd[1] == 'win':
                # ［対局結果］　常に記憶する
                self._result_file.save_win(self._my_turn)

                # ［指した手］　勝ったら全部忘れる
                self._canditates_memory.delete()

                # ［評価値］　勝ったら記憶する
                self._evaluation_table.save_evaluation_to_file()

            # 持将棋
            elif cmd[1] == 'draw':
                # ［対局結果］　常に記憶する
                self._result_file.save_draw(self._my_turn)

                # ［指した手］　勝っていないなら追加していく
                self._canditates_memory.save()

            # その他
            else:
                # ［対局結果］　常に記憶する
                self._result_file.save_otherwise(cmd[1], self._my_turn)

                # ［指した手］　勝っていないなら追加していく
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

        # USIプロトコルでの符号表記に変換
        sorted_friend_legal_move_list_as_usi = []
        opponent_legal_move_set_as_usi = set()

        for move in self._board.legal_moves:
            sorted_friend_legal_move_list_as_usi.append(cshogi.move_to_usi(move))

        # ソート
        sorted_friend_legal_move_list_as_usi.sort()

        print('自分の合法手一覧：')
        number = 1
        for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
            evaluation_table_index = self._evaluation_table.get_evaluation_table_index_from_move_as_usi(move_a_as_usi, self._board.turn)
            print(f'  ({number:3}) {move_a_as_usi:5} = {evaluation_table_index:5}')
            number += 1


        # 相手が指せる手の一覧
        #
        #   ヌルムーブをしたいが、 `self._board.push_pass()` が機能しなかったので、合法手を全部指してみることにする
        #
        for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
            self._board.push_usi(move_a_as_usi)
            for opponent_move in self._board.legal_moves:
                opponent_legal_move_set_as_usi.add(cshogi.move_to_usi(opponent_move))

            self._board.pop()

        print('次のいくつもの局面の相手の合法手の集合：')
        number = 1
        for move_a_as_usi in opponent_legal_move_set_as_usi:
            evaluation_table_index = self._evaluation_table.get_evaluation_table_index_from_move_as_usi(move_a_as_usi, self._board.turn)
            print(f'  ({number:3}) {move_a_as_usi:5} = {evaluation_table_index:5}')
            number += 1


        # 候補手に評価値を付けた辞書を作成
        move_score_dictionary = self._evaluation_table.make_move_score_dictionary(
                sorted_friend_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                self._board.turn)

        # 表示
        print('くじ一覧：')
        number = 1

        for move_a_as_usi in sorted_friend_legal_move_list_as_usi:

            # 指し手の評価値
            move_value = move_score_dictionary[move_a_as_usi]

            evaluation_table_index = self._evaluation_table.get_evaluation_table_index_from_move_as_usi(move_a_as_usi, self._board.turn)
            print(f'  ({number:3}) {move_a_as_usi:5} = {evaluation_table_index:5} value:{move_value:3}')
            number += 1


if __name__ == '__main__':
    """コマンドから実行時"""
    try:
        kifuwarabe = Kifuwarabe()
        kifuwarabe.usi_loop()

    except Exception as err:
        print(f"[unexpected error] {err=}, {type(err)=}")
        raise

