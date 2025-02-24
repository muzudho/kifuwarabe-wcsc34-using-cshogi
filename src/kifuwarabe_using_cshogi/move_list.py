# 指し手のリスト・ヘルパー

import cshogi

from .move import Move


def create_move_lists_of_king_and_pieces(
        legal_move_list,
        ko_memory,
        board):
    """自玉の合法手のリストと、自軍の玉以外の合法手のリストを作成"""

    # コウになる指し手の有無
    has_ko = False

    # 自玉のマス番号
    k_sq = board.king_square(board.turn)

    # USIプロトコルでの符号表記に変換
    king_move_list_as_usi = []
    pieces_move_list_as_usi = []
    ko_move_as_usi = ko_memory.get_head()

    for move in legal_move_list:
        move_as_usi = cshogi.move_to_usi(move)

        # 指し手の移動元を取得
        move_obj = Move.from_usi(move_as_usi)
        src_sq_or_none = move_obj.src_sq_or_none

        # コウならスキップする
        if move_as_usi == ko_move_as_usi:
            has_ko = True
            ko_is_king = src_sq_or_none == k_sq
            continue

        # 自玉の指し手か？
        #print(f"［自玉の指し手か？］ move_as_usi: {move_as_usi}, src_sq_or_none: {src_sq_or_none}, k_sq: {k_sq}, board.turn: {board.turn}")
        if src_sq_or_none == k_sq:
            king_move_list_as_usi.append(move_as_usi)

        else:
            pieces_move_list_as_usi.append(move_as_usi)

    # コウを省いて投了になるぐらいなら、コウを指す
    if has_ko and len(king_move_list_as_usi) + len(pieces_move_list_as_usi) < 1:
        if ko_is_king:
            king_move_list_as_usi.append(ko_move_as_usi)
        else:
            pieces_move_list_as_usi.append(ko_move_as_usi)

    return (king_move_list_as_usi, pieces_move_list_as_usi)
