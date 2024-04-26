from move import Move


class MoveHelper():


    _flip_turn_files = {
        '1':'9',
        '2':'8',
        '3':'7',
        '4':'6',
        '5':'5',
        '6':'4',
        '7':'3',
        '8':'2',
        '9':'1',
    }
    """先後逆さの筋番号"""


    _flip_turn_ranks = {
        'a':'i',
        'b':'h',
        'c':'g',
        'd':'f',
        'e':'e',
        'f':'d',
        'g':'c',
        'h':'b',
        'i':'a',
    }
    """先後逆さの段符号"""


    @staticmethod
    def flip_horizontal(move):
        """左右反転した盤上の指し手を返します

        Parameters
        ----------
        move : Move
            指し手
        """
        # 移動元
        #
        # ［打］は先後で表記は同じ
        if move.src_str in Move._src_drops:
            reversed_src_str = move.src_str

        else:

            reversed_file_str = MoveHelper._flip_turn_files[move.src_str[0]]

            rank_str = move.src_str[1]

            reversed_src_str = f"{reversed_file_str}{rank_str}"

        # 移動先
        reversed_file_str = MoveHelper._flip_turn_files[move.dst_str[0]]

        rank_str = move.dst_str[1]

        reversed_dst_str = f"{reversed_file_str}{rank_str}"

        # 成りかそれ以外（５文字なら成りだろう）
        if 4 < len(move.as_usi):
            pro = "+"
        else:
            pro = ""

        return Move(f"{reversed_src_str}{reversed_dst_str}{pro}")


    @staticmethod
    def flip_turn(move):
        """先後をひっくり返します

        Parameters
        ----------
        move : Move
            指し手
        """

        # 移動元
        #
        # ［打］は先後で表記は同じ
        if move.src_str in Move._src_drops:
            reversed_src_str = move.src_str

        else:

            reversed_file_str = MoveHelper._flip_turn_files[move.src_str[0]]

            reversed_rank_str = MoveHelper._flip_turn_ranks[move.src_str[1]]

            reversed_src_str = f"{reversed_file_str}{reversed_rank_str}"

        # 移動先
        reversed_file_str = MoveHelper._flip_turn_files[move.dst_str[0]]

        reversed_rank_str = MoveHelper._flip_turn_ranks[move.dst_str[1]]

        reversed_dst_str = f"{reversed_file_str}{reversed_rank_str}"

        # 成りかそれ以外（５文字なら成りだろう）
        if 4 < len(move.as_usi):
            pro = "+"
        else:
            pro = ""

        return Move(f"{reversed_src_str}{reversed_dst_str}{pro}")
