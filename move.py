class Move():
    """指し手"""


    _flip_files = {
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
    """逆さの筋番号"""


    _flip_ranks = {
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
    """逆さの段符号"""


    @classmethod
    def flip_turn(clazz, move_as_usi):
        """先後をひっくり返します"""

        # 移動元
        src_str = move_as_usi[0: 2]

        # 移動先
        dst_str = move_as_usi[2: 4]

        # 移動元
        #
        # ［打］は先後で表記は同じ
        if src_str in ('R*', 'B*', 'G*', 'S*', 'N*', 'L*', 'P*'):
            pass

        else:

            file_str = Move._flip_files[src_str[0]]

            rank_str = Move._flip_ranks[src_str[1]]

            src_str = f"{file_str}{rank_str}"

        # 移動先
        file_str = Move._flip_files[dst_str[0]]

        rank_str = Move._flip_ranks[dst_str[1]]

        dst_str = f"{file_str}{rank_str}"

        # 成りかそれ以外（５文字なら成りだろう）
        if 4 < len(move_as_usi):
            pro = "+"
        else:
            pro = ""

        return f"{src_str}{dst_str}{pro}"


    def __init__(self, move_as_usi):
        """初期化"""
        self._move_as_usi = move_as_usi

        # 移動元
        src_str = move_as_usi[0: 2]

        # 移動先
        dst_str = move_as_usi[2: 4]

        # 移動元
        if src_str == 'R*':
            src_num = 45
        elif src_str == 'B*':
            src_num = 46
        elif src_str == 'G*':
            src_num = 47
        elif src_str == 'S*':
            src_num = 48
        elif src_str == 'N*':
            src_num = 49
        elif src_str == 'L*':
            src_num = 50
        elif src_str == 'P*':
            src_num = 51
        else:

            file_str = src_str[0]
            if file_str in ('1', '9'):
                src_num = 0
            elif file_str in ('2', '8'):
                src_num = 9
            elif file_str in ('3', '7'):
                src_num = 18
            elif file_str in ('4', '6'):
                src_num = 27
            elif file_str == "5":
                src_num = 36
            else:
                raise Exception(f"src file error: '{file_str}' in '{move_as_usi}'")

            rank_str = src_str[1]
            if rank_str == 'a':
                src_num += 0
            elif rank_str == 'b':
                src_num += 1
            elif rank_str == 'c':
                src_num += 2
            elif rank_str == 'd':
                src_num += 3
            elif rank_str == 'e':
                src_num += 4
            elif rank_str == 'f':
                src_num += 5
            elif rank_str == 'g':
                src_num += 6
            elif rank_str == 'h':
                src_num += 7
            elif rank_str == 'i':
                src_num += 8
            else:
                raise Exception(f"src rank error: '{rank_str}' in '{move_as_usi}'")

        # 移動先
        file_str = dst_str[0]

        if file_str in ('1', '9'):
            dst_num = 0
        elif file_str in ('2', '8'):
            dst_num = 9
        elif file_str in ('3', '7'):
            dst_num = 18
        elif file_str in ('4', '6'):
            dst_num = 27
        elif file_str == '5':
            dst_num = 36
        else:
            raise Exception(f"dst file error: '{file_str}' in '{move_as_usi}'")

        rank_str = dst_str[1]
        if rank_str == "a":
            dst_num += 0
        elif rank_str == "b":
            dst_num += 1
        elif rank_str == "c":
            dst_num += 2
        elif rank_str == "d":
            dst_num += 3
        elif rank_str == "e":
            dst_num += 4
        elif rank_str == "f":
            dst_num += 5
        elif rank_str == "g":
            dst_num += 6
        elif rank_str == "h":
            dst_num += 7
        elif rank_str == "i":
            dst_num += 8
        else:
            raise Exception(f"dst rank error: '{rank_str}' in '{move_as_usi}'")

        # 成りかそれ以外（５文字なら成りだろう）
        if 4 < len(move_as_usi):
            pro_num = 1
        else:
            pro_num = 0

        self._evaluation_table_index = (2 * 5 * 9 * src_num) + (2 * dst_num) + pro_num


    @property
    def evaluation_table_index(self):
        """評価値テーブルのセルのインデックス"""
        return self._evaluation_table_index
