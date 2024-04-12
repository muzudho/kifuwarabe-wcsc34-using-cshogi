import cshogi
import random


def choice_lottery(evaluation_table, legal_move_list, canditates_memory, ko_memory, board):
    """くじを引く"""

    # USIプロトコルでの符号表記に変換
    sorted_friend_legal_move_list_as_usi = []
    opponent_legal_move_set_as_usi = set()
    ko_move_as_usi = ko_memory.get_head()

    for move in legal_move_list:
        move_as_usi = cshogi.move_to_usi(move)

        # コウならスキップする
        if move_as_usi == ko_move_as_usi:
            has_ko = True
            continue

        sorted_friend_legal_move_list_as_usi.append(move_as_usi)

    # コウを省いて投了になるぐらいなら、コウを指す
    if len(sorted_friend_legal_move_list_as_usi) < 1 and has_ko:
        sorted_friend_legal_move_list_as_usi.append(ko_move_as_usi)

    # ソート
    sorted_friend_legal_move_list_as_usi.sort()

    # 相手が指せる手の一覧
    #
    #   ヌルムーブをしたいが、 `board.push_pass()` が機能しなかったので、合法手を全部指してみることにする
    #
    for move_a_as_usi in sorted_friend_legal_move_list_as_usi:
        board.push_usi(move_a_as_usi)
        for opponent_move in board.legal_moves:
            opponent_legal_move_set_as_usi.add(cshogi.move_to_usi(opponent_move))

        board.pop()

    # 候補手に評価値を付けた辞書を作成
    move_score_dictionary = evaluation_table.make_move_score_dictionary(
            sorted_friend_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi)

    # 候補に挙がった指し手は全て記憶しておく
    canditates_memory.union_dictionary(move_score_dictionary)
    canditates_memory.union_set(opponent_legal_move_set_as_usi)

    # 一番高い評価値を探す。評価値は -593～593 程度を想定
    best_score = -1000
    best_move_list = []
    for move_as_usi, score in move_score_dictionary.items():
        if best_score == score:
            best_move_list.append(move_as_usi)
        elif best_score < score:
            best_score = score
            best_move_list = [move_as_usi]


    return random.choice(best_move_list)
    """候補手の中からランダムに選ぶ。USIの指し手の記法で返却"""
