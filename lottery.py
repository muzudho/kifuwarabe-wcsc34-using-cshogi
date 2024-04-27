import cshogi
import random
from move import Move
from move_list import create_move_lists


class Lottery():


    @staticmethod
    def choice_best(
            evaluation_facade_obj,
            legal_move_list,
            king_canditates_memory,
            pieces_canditates_memory,
            ko_memory,
            board):
        """くじを引く"""

        # 自玉の指し手の集合と、自玉を除く自軍の指し手の集合
        king_move_list_as_usi, pieces_move_list_as_usi = create_move_lists(
                legal_move_list,
                ko_memory,
                board)

        #
        # 相手が指せる手の集合
        # -----------------
        #
        #   ヌルムーブをしたいが、 `board.push_pass()` が機能しなかったので、合法手を全部指してみることにする
        #

        # 敵玉（Lord）の指し手の集合
        lord_move_set_as_usi = set()
        # 敵玉を除く敵軍の指し手の集合（Quaffer；ゴクゴク飲む人。Pの次の文字Qを頭文字にした単語）
        quaffers_move_set_as_usi = set()

        list_of_friend_move_list_as_usi = [
            king_move_list_as_usi,
            pieces_move_list_as_usi,
        ]

        for friend_move_list_as_usi in list_of_friend_move_list_as_usi:
            for friend_move_as_usi in friend_move_list_as_usi:
                board.push_usi(friend_move_as_usi)

                # 敵玉（L; Lord）の位置を調べる
                l_sq = board.king_square(board.turn)

                for opponent_move_id in board.legal_moves:
                    opponent_move_as_usi = cshogi.move_to_usi(opponent_move_id)

                    opponent_move_obj = Move(opponent_move_as_usi)
                    src_sq_or_none = opponent_move_obj.get_src_sq_or_none()

                    # 敵玉の指し手
                    if src_sq_or_none is not None and src_sq_or_none == l_sq:
                        lord_move_set_as_usi.add(opponent_move_as_usi)
                    # 敵玉を除く敵軍の指し手
                    else:
                        quaffers_move_set_as_usi.add(opponent_move_as_usi)

                board.pop()

        #
        # 候補手に評価値を付けた辞書を作成
        # ----------------------------
        #
        king_move_as_usi_and_policy_dictionary, pieces_move_as_usi_and_policy_dictionary = evaluation_facade_obj.make_move_as_usi_and_policy_dictionary(
                king_move_collection_as_usi=king_move_list_as_usi,
                pieces_move_collection_as_usi=pieces_move_list_as_usi,
                lord_move_collection_as_usi=lord_move_set_as_usi,
                quaffers_move_collection_as_usi=quaffers_move_set_as_usi,
                turn=board.turn)

        # 評価値算出のソースになった指し手は全て記憶しておく
        # 自玉の指し手
        king_canditates_memory.union_dictionary(king_move_as_usi_and_policy_dictionary)
        # 敵玉の指し手も、ポリシー値に加算されるから
        king_canditates_memory.union_set(lord_move_set_as_usi)
        # 自玉を除く自軍の指し手
        pieces_canditates_memory.union_dictionary(pieces_move_as_usi_and_policy_dictionary)
        # 敵玉を除く敵軍の指し手も、ポリシー値に加算されるから
        pieces_canditates_memory.union_set(quaffers_move_set_as_usi)

        list_of_friend_move_as_usi_and_policy_dictionary = [
            king_move_as_usi_and_policy_dictionary,
            pieces_move_as_usi_and_policy_dictionary,
        ]

        # 一番高い評価値を探す。評価値は（改造して範囲がよく変わるのではっきりしないが） ±１万もないだろう
        best_policy = -99999999
        best_move_list = []
        for friend_move_as_usi_and_policy_dictionary in list_of_friend_move_as_usi_and_policy_dictionary:
            for friend_move_as_usi, policy in friend_move_as_usi_and_policy_dictionary.items():
                if best_policy == policy:
                    best_move_list.append(friend_move_as_usi)
                elif best_policy < policy:
                    best_policy = policy
                    best_move_list = [friend_move_as_usi]

        return random.choice(best_move_list)
        """候補手の中からランダムに選ぶ。USIの指し手の記法で返却"""
