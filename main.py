import cshogi
import random
import datetime
from learn_candidates_king import LearnCandidatesKing
from learn_candidates_pieces import LearnCandidatesPieces
from evaluation_facade import EvaluationFacade
from lottery import Lottery
from ko_memory import KoMemory
from result_file import ResultFile
from move import Move
from move_list import create_move_lists_of_king_and_pieces
from evaluation_rule_facade import EvaluationRuleFacade
from evaluation_rule_k import EvaluationRuleK
from evaluation_rule_m import EvaluationRuleM
from evaluation_rule_p import EvaluationRuleP
from evaluation_save_kk import EvaluationSaveKk
from evaluation_save_kp import EvaluationSaveKp
from evaluation_save_pp import EvaluationSavePp


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

        # 評価の窓口
        self._evaluation_facade_obj = None

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

        # エンジン名は別ファイルから読込。pythonファイルはよく差し替えるのでデータは外に出したい
        try:
            file_name = "engine_name.txt"
            with open(file_name, 'r', encoding="utf-8") as f:
                engine_name = f.read().strip()

        except FileNotFoundError as ex:
            print(f"[usi protocol > usi] '{file_name}' file not found.  ex:{ex}")
            raise

        print(f'id name {engine_name}')
        print('usiok', flush=True)


    def isready(self):
        """対局準備"""
        print('readyok', flush=True)


    def usinewgame(self):
        """新しい対局"""

        # 内部的なプレイヤー数。多重人格みたいなもの。別ファイルから読込。pythonファイルはよく差し替えるのでデータは外に出したい。
        # 毎対局同じ指し手を繰り返すという千日手を回避するために多重人格にしている
        try:
            file_name = "player_size.txt"
            with open(file_name, 'r', encoding="utf-8") as f:
                player_size = int(f.read().strip())

        except FileNotFoundError as ex:
            print(f"[usi protocol > usinewgame] ignored. '{file_name}' file not found.  ex:{ex}")

            # 1 で続行
            player_size = 1

        self._player_file_number = random.randint(1,player_size)

        # 前回の対局の指し手の候補手の記憶
        self._king_canditates_memory = LearnCandidatesKing.from_file(
                self._player_file_number)
        self._pieces_canditates_memory = LearnCandidatesPieces.from_file(
                self._player_file_number)

        # コウの記録
        self._ko_memory = KoMemory()

        # 結果ファイル（デフォルト）
        self._result_file = ResultFile(self._player_file_number)

        # 評価の窓口を準備
        self._evaluation_facade_obj = EvaluationFacade(self._player_file_number)
        self._evaluation_facade_obj.usinewgame(
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
                evaluation_facade_obj=self._evaluation_facade_obj,
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

                # ［指した手］　勝っていないなら追加していく（旧称のファイルがあれば削除する）
                self._king_canditates_memory.save()
                self._king_canditates_memory.delete_old_version_file()

                self._pieces_canditates_memory.save()
                self._pieces_canditates_memory.delete_old_version_file()

            # 勝ち
            elif cmd[1] == 'win':
                # ［対局結果］　常に記憶する
                self._result_file.save_win(self._my_turn)

                # ［指した手］　勝ったら全部忘れる
                self._king_canditates_memory.delete_file()
                self._pieces_canditates_memory.delete_file()

                # ［評価値］　勝ったら記憶する
                EvaluationSaveKk.save_file_as_kk(
                        kk_table_obj=self._evaluation_facade_obj.kk_table_obj)
                EvaluationSaveKp.save_file_as_kp(
                        kp_table_obj=self._evaluation_facade_obj.kp_table_obj)
                EvaluationSavePp.save_file_as_pp(
                        pp_table_obj=self._evaluation_facade_obj.pp_table_obj)

            # 持将棋
            elif cmd[1] == 'draw':
                # ［対局結果］　常に記憶する
                self._result_file.save_draw(self._my_turn)

                # ［指した手］　勝っていないなら追加していく（旧称のファイルがあれば削除する）
                self._king_canditates_memory.save()
                self._king_canditates_memory.delete_old_version_file()

                self._pieces_canditates_memory.save()
                self._pieces_canditates_memory.delete_old_version_file()

            # その他
            else:
                # ［対局結果］　常に記憶する
                self._result_file.save_otherwise(cmd[1], self._my_turn)

                # ［指した手］　勝っていないなら追加していく（旧称のファイルがあれば削除する）
                self._king_canditates_memory.save()
                self._king_canditates_memory.delete_old_version_file()

                self._pieces_canditates_memory.save()
                self._pieces_canditates_memory.delete_old_version_file()


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

        #
        # USIプロトコルでの符号表記に変換
        # ---------------------------
        #
        # 自玉の指し手と、自玉を除く自軍の指し手を分けて取得
        #
        king_move_list_as_usi, pieces_move_list_as_usi = create_move_lists_of_king_and_pieces(
                legal_move_list=list(self._board.legal_moves),
                ko_memory=self._ko_memory,
                board=self._board)

        # 敵玉の指し手
        lord_move_set_as_usi = set()
        # 敵玉を除く敵軍の指し手
        quaffers_move_set_as_usi = set()

        #
        # 評価値テーブルのインデックスを一覧
        #

        number = 1
        print('自玉の合法手一覧：')

        # Ｋの指し手ということは分かるが、相手がＰなのかＬなのかＱなのか分からない
        for k_as_usi in king_move_list_as_usi:
            #
            # 指し手　ｋ
            # ---------
            #
            k_obj = Move.from_usi(k_as_usi)
            k_index = EvaluationRuleK.get_m_index_by_move(
                    move_obj=k_obj)

            #
            # 検算
            # ----
            #
            verify_usi = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=k_index,
                    is_king=True)

            #
            # 表示
            # ----
            #
            print(f'  ({number:3}) K:{k_as_usi:5} = {k_index:5}  検算 {verify_usi:5}')
            number += 1

        print('自玉以外の自軍の合法手一覧：')

        # Ｐの指し手ということは分かるが、相手がＫなのかＰなのかＬなのかＱなのか分からない
        for p_as_usi in pieces_move_list_as_usi:
            #
            # 指し手　p
            # ---------
            #
            p_obj = Move.from_usi(p_as_usi)
            p_index = EvaluationRuleP.get_m_index_by_move(
                    move_obj=p_obj)

            #
            # 検算
            # ----
            #
            verify_usi = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=p_index,
                    is_king=False)

            #
            # 表示
            # ----
            #
            print(f'  ({number:3}) P:{p_as_usi:5} = {p_index:5}  検算 {verify_usi:5}')
            number += 1

        #
        # 相手が指せる手の一覧
        #
        #   ヌルムーブをしたいが、 `self._board.push_pass()` が機能しなかったので、合法手を全部指してみることにする
        #
        list_of_friend_move_list_as_usi = [
            king_move_list_as_usi,
            pieces_move_list_as_usi,
        ]

        for friend_move_list_as_usi in list_of_friend_move_list_as_usi:
            for friend_move_as_usi in friend_move_list_as_usi:
                self._board.push_usi(friend_move_as_usi)

                # 敵玉（L; Lord）の位置を調べる
                l_sq = self._board.king_square(self._board.turn)

                for opponent_move_id in self._board.legal_moves:
                    opponent_move_as_usi = cshogi.move_to_usi(opponent_move_id)

                    opponent_move_obj = Move.from_usi(opponent_move_as_usi)
                    src_sq_or_none = opponent_move_obj.src_sq_or_none

                    # 敵玉の指し手
                    if src_sq_or_none is not None and src_sq_or_none == l_sq:
                        lord_move_set_as_usi.add(opponent_move_as_usi)
                    # 敵玉を除く敵軍の指し手
                    else:
                        quaffers_move_set_as_usi.add(opponent_move_as_usi)

                self._board.pop()

        #
        # 敵玉の応手の集合
        # --------------
        #

        print('敵玉の応手の集合：')
        number = 1

        # Ｌの指し手ということは分かるが、相手がＰなのかＬなのかＱなのか分からない
        # l は lord（敵玉）
        for l_as_usi in lord_move_set_as_usi:

            #
            # 指し手　l
            # ---------
            #
            l_obj = Move.from_usi(l_as_usi)
            l_index = EvaluationRuleK.get_m_index_by_move(
                    move_obj=l_obj)

            #
            # 検算
            # ----
            #
            verofy_usi = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=k_index_in_kk,
                    is_king=True)

            #
            # 表示
            # ----
            #
            print(f'  ({number:3}) L:{l_as_usi:5} = {l_index:5}  検算 {verofy_usi:5}')
            number += 1

        #
        # 敵玉以外の敵軍の応手の集合
        # -----------------------
        #

        print('敵玉以外の敵軍の応手の集合：')
        # Ｑの指し手ということは分かるが、相手がＫなのかＰなのかＬなのかＱなのか分からない
        # q は quaffer
        for q_as_usi in quaffers_move_set_as_usi:
            #
            # 指し手　q
            # ---------
            #
            q_obj = Move.from_usi(q_as_usi)
            q_index = EvaluationRuleFacade.get_m_index_by_move(
                    move_obj=q_obj)

            #
            # 検算
            # ----
            #
            verify_usi = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=q_index,
                    is_king=False)

            #
            # 表示
            # ----
            #
            print(f'  ({number:3}) Q:{q_as_usi:5} = {q_index:5}  検算 {verify_usi:5}')
            number += 1

        #
        # ポリシー値付きで候補手一覧
        # =======================
        #
        # 候補手に評価値を付けた辞書を作成
        king_move_as_usi_and_policy_dictionary, pieces_move_as_usi_and_score_dictionary = self._evaluation_facade_obj.make_move_as_usi_and_policy_dictionary(
                king_move_collection_as_usi=king_move_list_as_usi,
                pieces_move_collection_as_usi=pieces_move_list_as_usi,
                lord_move_collection_as_usi=lord_move_set_as_usi,
                quaffers_move_collection_as_usi=quaffers_move_set_as_usi,
                turn=self._board.turn)

        # 表示
        number = 1

        #
        # キングから
        # ---------
        #

        print('くじ一覧（自玉の合法手）：')
        for k_as_usi in king_move_list_as_usi:

            #
            # ＫＭポリシー
            # -----------
            #
            km_policy = king_move_as_usi_and_policy_dictionary[k_as_usi]

            #
            # ＫＫ表と、ＫＰ表
            # --------------
            #
            k_obj = Move.from_usi(k_as_usi)

            k_index_in_kk = EvaluationRuleFacade.get_m_index_by_move(   # FIXME KK
                    move_obj=k_obj,
                    is_king=self._evaluation_facade_obj.kk_table_obj.is_king_of_a)

            k_index_in_kp = EvaluationRuleFacade.get_m_index_by_move(   # FIXME KP
                    move_obj=k_obj,
                    is_king=self._evaluation_facade_obj.kp_table_obj.is_king_of_a)

            #
            # 検算
            # ----
            #
            verify_usi_in_kk = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=k_index_in_kk,
                    is_king=self._evaluation_facade_obj.kk_table_obj.is_king_of_a)

            verify_usi_in_kp = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=k_index_in_kp,
                    is_king=self._evaluation_facade_obj.kp_table_obj.is_king_of_a)

            #
            # 表示
            # ----
            #
            print(f'  ({number:3}) K:{k_as_usi:5} = KK{k_index_in_kk}  KP{k_index_in_kp:5}  policy:{km_policy:3}  検算 KK:{verify_usi_in_kk:5}  KP:{verify_usi_in_kp:5}')
            number += 1

        #
        # 次にピースズ
        # -----------
        #

        print('くじ一覧（自玉以外の自軍の合法手）：')
        for p_as_usi in pieces_move_list_as_usi:

            #
            # ＰＭポリシー
            # -----------
            #
            pm_policy = pieces_move_as_usi_and_score_dictionary[p_as_usi]

            #
            # ＫＰ表と、ＰＰ表
            # --------------
            #
            p_obj = Move.from_usi(p_as_usi)

            # TODO ＫＰを、ＰＫにひっくり返してみる必要がある？
            p_index_in_kp = EvaluationRuleFacade.get_m_index_by_move(
                    move_obj=p_obj,
                    is_king=self._evaluation_facade_obj.kp_table_obj.is_king_of_b)

            p_index_in_pp = EvaluationRuleFacade.get_m_index_by_move(
                    move_obj=p_obj,
                    is_king=self._evaluation_facade_obj.pp_table_obj.is_king_of_a)

            #
            # 検算
            # ----
            #
            # TODO ＫＰを、ＰＫにひっくり返してみる必要がある？
            verify_usi_in_kp = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=p_index_in_kp,
                    is_king=self._evaluation_facade_obj.kp_table_obj.is_king_of_b)

            verify_usi_in_pp = EvaluationRuleM.get_move_as_usi_by_m_index(
                    m_index=p_index_in_pp,
                    is_king=self._evaluation_facade_obj.pp_table_obj.is_king_of_a)

            #
            # 表示
            # ----
            #
            print(f'  ({number:3}) P:{p_as_usi:5} = PP{p_index_in_pp:5}  policy:{pm_policy:3}  検算 KP:{verify_usi_in_kp:5}  PP:{verify_usi_in_pp:5}')
            number += 1


if __name__ == '__main__':
    """コマンドから実行時"""
    try:
        kifuwarabe = Kifuwarabe()
        kifuwarabe.usi_loop()

    except Exception as err:
        print(f"[unexpected error] {err=}, {type(err)=}")
        raise

