import cshogi
import random
import datetime
from learn_candidates_memory import CandidatesMemory
from evaluation_configuration import EvaluationConfiguration
from evaluation_table import EvaluationTable
from lottery import Lottery
from ko_memory import KoMemory
from result_file import ResultFile
from move import Move
from move_list import create_move_lists


class Kifuwarabe():
    """きふわらべ"""


    def __init__(self):
        """初期化"""

        # さいころに倣って６個
        self._player_file_number = None

        # 盤
        self._board = cshogi.Board()

        # 候補に挙がった手は全て覚えておく
        self._king_canditates_memory = None
        self._pieces_canditates_memory = None

        # 評価値テーブル・オブジェクト
        self._evaluation_table_obj = None

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
        self._king_canditates_memory = CandidatesMemory.load_from_file(self._player_file_number, is_king=True)
        self._pieces_canditates_memory = CandidatesMemory.load_from_file(self._player_file_number, is_king=False)

        # コウの記録
        self._ko_memory = KoMemory()

        # 結果ファイル（デフォルト）
        self._result_file = ResultFile(self._player_file_number)

        # 評価関数テーブルをファイルから読み込む。無ければランダム値の入った物を新規作成する
        self._evaluation_table_obj = EvaluationTable(self._player_file_number)
        self._evaluation_table_obj.usinewgame(
                self._king_canditates_memory,
                self._pieces_canditates_memory,
                self._result_file)

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
        best_move = Lottery.choice_best(
                evaluation_table=self._evaluation_table_obj,
                legal_move_list=list(self._board.legal_moves),
                king_canditates_memory=self._king_canditates_memory,
                pieces_canditates_memory=self._pieces_canditates_memory,
                ko_memory=self._ko_memory,
                board=self._board)

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
                self._king_canditates_memory.save()
                self._pieces_canditates_memory.save()

            # 勝ち
            elif cmd[1] == 'win':
                # ［対局結果］　常に記憶する
                self._result_file.save_win(self._my_turn)

                # ［指した手］　勝ったら全部忘れる
                self._king_canditates_memory.delete()
                self._pieces_canditates_memory.delete()

                # ［評価値］　勝ったら記憶する
                self._evaluation_table_obj.save_file_as_kp_ko()
                self._evaluation_table_obj.save_file_as_pp_po()

            # 持将棋
            elif cmd[1] == 'draw':
                # ［対局結果］　常に記憶する
                self._result_file.save_draw(self._my_turn)

                # ［指した手］　勝っていないなら追加していく
                self._king_canditates_memory.save()
                self._pieces_canditates_memory.save()

            # その他
            else:
                # ［対局結果］　常に記憶する
                self._result_file.save_otherwise(cmd[1], self._my_turn)

                # ［指した手］　勝っていないなら追加していく
                self._king_canditates_memory.save()
                self._pieces_canditates_memory.save()


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

        print(f"""\
先手玉の位置：　{self._board.king_square(cshogi.BLACK)}
後手玉の位置：　{self._board.king_square(cshogi.WHITE)}
""")

        if self._my_turn == cshogi.BLACK:
            sq_of_friend_king = self._board.king_square(cshogi.BLACK)
            sq_of_opponent_king = self._board.king_square(cshogi.WHITE)
            print(f"""\
自分の手番：　先手
自玉の位置：　{sq_of_friend_king}
敵玉の位置：　{sq_of_opponent_king}
""")
        else:
            sq_of_friend_king = self._board.king_square(cshogi.WHITE)
            sq_of_opponent_king = self._board.king_square(cshogi.BLACK)
            print(f"""\
自分の手番：　後手
自玉の位置：　{sq_of_friend_king}
敵玉の位置：　{sq_of_opponent_king}
""")


        # USIプロトコルでの符号表記に変換
        #
        #
        # ＦｋＦ＋ＦｋＯポリシー と ＦｍＦ＋ＦｍＯポリシー を分けて取得
        #
        sorted_friend_king_legal_move_list_as_usi, sorted_friend_pieces_legal_move_list_as_usi = create_move_lists(
                legal_move_list=list(self._board.legal_moves),
                ko_memory=self._ko_memory,
                board=self._board)



        opponent_legal_move_set_as_usi = set()

        #
        # 評価値テーブルのインデックスを一覧
        #

        number = 1
        print('自玉の合法手一覧：')
        for move_a_as_usi in sorted_friend_king_legal_move_list_as_usi:
            k_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            k_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=k_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            m_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            m_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=m_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            print(f'  ({number:3}) {move_a_as_usi:5} = K{k_table_index:5} M{m_table_index:5}  検算 Ka:{",".join(k_moves_pair_as_usi[0]):11}  b:{",".join(k_moves_pair_as_usi[1]):11}  Ma:{",".join(m_moves_pair_as_usi[0]):11}  b:{",".join(m_moves_pair_as_usi[1]):11}')
            number += 1

        print('自軍の玉以外の合法手一覧：')
        for move_a_as_usi in sorted_friend_pieces_legal_move_list_as_usi:
            k_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            k_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=k_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            m_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            m_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=m_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            print(f'  ({number:3}) {move_a_as_usi:5} = K{k_table_index:5} M{m_table_index:5}  検算 Ka:{",".join(k_moves_pair_as_usi[0]):11}  b:{",".join(k_moves_pair_as_usi[1]):11}  Ma:{",".join(m_moves_pair_as_usi[0]):11}  b:{",".join(m_moves_pair_as_usi[1]):11}')
            number += 1

        #
        # 相手が指せる手の一覧
        #
        #   ヌルムーブをしたいが、 `self._board.push_pass()` が機能しなかったので、合法手を全部指してみることにする
        #
        list_of_sorted_friend_legal_move_list_as_usi = [
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_pieces_legal_move_list_as_usi,
        ]

        for sorted_friend_legal_move_list_as_usi in list_of_sorted_friend_legal_move_list_as_usi:
            for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
                self._board.push_usi(move_a_as_usi)
                for opponent_move in self._board.legal_moves:
                    opponent_legal_move_set_as_usi.add(cshogi.move_to_usi(opponent_move))

                self._board.pop()

        print('次のいくつもの局面の相手の合法手の集合：')
        number = 1
        for move_a_as_usi in opponent_legal_move_set_as_usi:
            k_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            k_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=k_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            m_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            m_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=m_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            print(f'  ({number:3}) {move_a_as_usi:5} = K{k_table_index:5} M{m_table_index:5}  検算 Ka:{",".join(k_moves_pair_as_usi[0]):11}  b:{",".join(k_moves_pair_as_usi[1]):11}  Ma:{",".join(m_moves_pair_as_usi[0]):11}  b:{",".join(m_moves_pair_as_usi[1]):11}')
            number += 1

        #
        # ポリシー値付きで候補手一覧
        # =======================
        #
        # 候補手に評価値を付けた辞書を作成
        king_move_as_usi_and_score_dictionary, pieces_move_as_usi_and_score_dictionary = self._evaluation_table_obj.make_move_as_usi_and_policy_dictionary(
                sorted_friend_king_legal_move_list_as_usi,
                sorted_friend_pieces_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                self._board.turn)

        # 表示
        number = 1

        #
        # キングから
        # ---------
        #

        print('くじ一覧（自玉の合法手）：')
        for move_a_as_usi in sorted_friend_king_legal_move_list_as_usi:

            # 指し手の評価値
            k_move_value = king_move_as_usi_and_score_dictionary[move_a_as_usi]

            k_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            k_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=k_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.kp_plus_ko_policy_table.is_symmetrical_connected)

            print(f'  ({number:3}) {move_a_as_usi:5} = K{k_table_index:5} value:{k_move_value:3}  検算 Ka:{",".join(k_moves_pair_as_usi[0]):11}  b:{",".join(k_moves_pair_as_usi[1]):11}')
            number += 1

        #
        # 次にミニオンズ
        # ------------
        #

        print('くじ一覧（自軍の玉以外の合法手）：')
        for move_a_as_usi in sorted_friend_pieces_legal_move_list_as_usi:

            # 指し手の評価値
            m_move_value = pieces_move_as_usi_and_score_dictionary[move_a_as_usi]

            m_table_index = EvaluationConfiguration.get_table_index_by_move(
                    move=Move(move_a_as_usi),
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            m_moves_pair_as_usi = EvaluationConfiguration.get_moves_pair_as_usi_by_table_index(
                    table_index=m_table_index,
                    is_symmetrical_connected=self._evaluation_table_obj.pp_plus_po_policy_table.is_symmetrical_connected)

            print(f'  ({number:3}) {move_a_as_usi:5} = M{m_table_index:5} value:{m_move_value:3}  検算 Ma:{",".join(m_moves_pair_as_usi[0]):11}  b:{",".join(m_moves_pair_as_usi[1]):11}')
            number += 1


if __name__ == '__main__':
    """コマンドから実行時"""
    try:
        kifuwarabe = Kifuwarabe()
        kifuwarabe.usi_loop()

    except Exception as err:
        print(f"[unexpected error] {err=}, {type(err)=}")
        raise

