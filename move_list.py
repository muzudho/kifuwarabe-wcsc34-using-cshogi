# 指し手のリスト・ヘルパー

import cshogi
from move import Move


def create_move_lists(
        legal_move_list,
        ko_memory,
        board):
    """自玉の合法手のリストと、自軍の玉以外の合法手のリストを作成"""

    # コウになる指し手の有無
    has_ko = False

    # 自玉のマス番号
    k_sq = board.king_square(board.turn)

    # USIプロトコルでの符号表記に変換
    sorted_friend_king_legal_move_list_as_usi = []
    sorted_friend_pieces_legal_move_list_as_usi = []
    ko_move_as_usi = ko_memory.get_head()

    for move in legal_move_list:
        move_as_usi = cshogi.move_to_usi(move)

        # 指し手の移動元を取得
        move_obj = Move(move_as_usi)
        src_sq_or_none = move_obj.src_sq_or_none

        # コウならスキップする
        if move_as_usi == ko_move_as_usi:
            has_ko = True
            ko_is_king = src_sq_or_none == k_sq
            continue

        # 自玉の指し手か？
        #print(f"［自玉の指し手か？］ move_as_usi: {move_as_usi}, src_sq_or_none: {src_sq_or_none}, k_sq: {k_sq}, board.turn: {board.turn}")
        if src_sq_or_none == k_sq:
            sorted_friend_king_legal_move_list_as_usi.append(move_as_usi)

        else:
            sorted_friend_pieces_legal_move_list_as_usi.append(move_as_usi)

    # コウを省いて投了になるぐらいなら、コウを指す
    if has_ko and len(sorted_friend_king_legal_move_list_as_usi) + len(sorted_friend_pieces_legal_move_list_as_usi) < 1:
        if ko_is_king:
            sorted_friend_king_legal_move_list_as_usi.append(ko_move_as_usi)
        else:
            sorted_friend_pieces_legal_move_list_as_usi.append(ko_move_as_usi)

    # ソート
    sorted_friend_king_legal_move_list_as_usi.sort()
    sorted_friend_pieces_legal_move_list_as_usi.sort()

    return (sorted_friend_king_legal_move_list_as_usi, sorted_friend_pieces_legal_move_list_as_usi)
