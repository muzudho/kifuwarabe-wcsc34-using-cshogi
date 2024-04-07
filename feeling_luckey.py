import cshogi
import random


def choice_lottery(evaluation_table, legal_move_list):
    """くじを引く"""

    # USIプロトコルでの符号表記に変換
    sorted_legal_move_list_as_usi = []

    for move in legal_move_list:
        sorted_legal_move_list_as_usi.append(cshogi.move_to_usi(move))

    # ソート
    sorted_legal_move_list_as_usi.sort()

    # 候補手に評価値を付けた辞書を作成
    move_score_dictionary = evaluation_table.make_move_score_dictionary(sorted_legal_move_list_as_usi)

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
