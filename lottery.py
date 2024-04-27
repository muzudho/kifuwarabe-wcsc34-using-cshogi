import cshogi
import random
from move_list import create_move_lists


class Lottery():


    @staticmethod
    def choice_best(
            evaluation_table,
            legal_move_list,
            king_canditates_memory,
            pieces_canditates_memory,
            ko_memory,
            board):
        """くじを引く"""

        sorted_friend_king_legal_move_list_as_usi, sorted_friend_pieces_legal_move_list_as_usi = create_move_lists(
                legal_move_list,
                ko_memory,
                board)
        opponent_legal_move_set_as_usi = set()

        # 相手が指せる手の一覧
        #
        #   ヌルムーブをしたいが、 `board.push_pass()` が機能しなかったので、合法手を全部指してみることにする
        #
        list_of_sorted_friend_legal_move_list_as_usi = [
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_pieces_legal_move_list_as_usi,
        ]

        for sorted_friend_legal_move_list_as_usi in list_of_sorted_friend_legal_move_list_as_usi:
            for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
                board.push_usi(move_a_as_usi)
                for opponent_move in board.legal_moves:
                    opponent_legal_move_set_as_usi.add(cshogi.move_to_usi(opponent_move))

                board.pop()

        # 候補手に評価値を付けた辞書を作成
        king_move_as_usi_and_score_dictionary, pieces_move_as_usi_and_score_dictionary = evaluation_table.make_move_as_usi_and_policy_dictionary(
                sorted_friend_king_legal_move_list_as_usi,
                n2nd_move_list_as_usi=sorted_friend_pieces_legal_move_list_as_usi,
                n3rd_move_set_as_usi=opponent_legal_move_set_as_usi,
                turn=board.turn)

        # 候補に挙がった指し手は全て記憶しておく
        king_canditates_memory.union_dictionary(king_move_as_usi_and_score_dictionary)
        king_canditates_memory.union_set(opponent_legal_move_set_as_usi)
        pieces_canditates_memory.union_dictionary(pieces_move_as_usi_and_score_dictionary)
        pieces_canditates_memory.union_set(opponent_legal_move_set_as_usi)

        all_move_as_usi_and_score_dictionary = [
            king_move_as_usi_and_score_dictionary,
            pieces_move_as_usi_and_score_dictionary,
        ]

        # 一番高い評価値を探す。評価値は -593～593 程度を想定
        best_score = -1000
        best_move_list = []
        for move_as_usi_and_score_dictionary in all_move_as_usi_and_score_dictionary:
            for move_as_usi, score in move_as_usi_and_score_dictionary.items():
                if best_score == score:
                    best_move_list.append(move_as_usi)
                elif best_score < score:
                    best_score = score
                    best_move_list = [move_as_usi]

        return random.choice(best_move_list)
        """候補手の中からランダムに選ぶ。USIの指し手の記法で返却"""
