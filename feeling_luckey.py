import cshogi
import random


def choice_lottery(legal_move_list):
    """くじを引く"""

    bestmove = random.choice(legal_move_list)
    """候補手の中からランダムに選ぶ"""

    return cshogi.move_to_usi(bestmove)
    """指し手の記法で返却"""
