class Move():
    """指し手"""


    _file_str_to_num = {
        '1':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
    }
    """列数字を数に変換"""


    _rank_str_to_num = {
        'a':1,
        'b':2,
        'c':3,
        'd':4,
        'e':5,
        'f':6,
        'g':7,
        'h':8,
        'i':9,
    }
    """段を数に変換"""


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


    _src_dst_str_1st_figure_to_index_on_fully_connected = {
        'R' : 45,   # 'R*' 移動元の打
        'B' : 46,   # 'B*'
        'G' : 47,   # 'G*'
        'S' : 48,   # 'S*'
        'N' : 49,   # 'N*'
        'L' : 50,   # 'L*'
        'P' : 51,   # 'P*'
        '1' : 0,
        '2' : 9,
        '3' : 18,
        '4' : 27,
        '5' : 36,
        '6' : 45,
        '7' : 54,
        '8' : 63,
        '9' : 72,
    }
    """移動元の１文字目をインデックスへ変換"""


    _src_dst_str_1st_figure_to_index_on_symmetrical_board = {
        'R' : 45,   # 'R*' 移動元の打
        'B' : 46,   # 'B*'
        'G' : 47,   # 'G*'
        'S' : 48,   # 'S*'
        'N' : 49,   # 'N*'
        'L' : 50,   # 'L*'
        'P' : 51,   # 'P*'
        '1' : 0,
        '2' : 9,
        '3' : 18,
        '4' : 27,
        '5' : 36,
        '6' : 27,   # 列は左右対称
        '7' : 18,
        '8' : 9,
        '9' : 0,
    }
    """移動元の１文字目をインデックスへ変換。盤は左右対称とします"""

    _src_dst_str_2nd_figure_to_index = {
        '*': 0,     # 移動元の打
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
        'i': 8,
    }
    """移動元、移動先の２文字目をインデックスへ変換"""


    _src_drops = ('R*', 'B*', 'G*', 'S*', 'N*', 'L*', 'P*')


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
        if src_str in Move._src_drops:
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
        """初期化

        Parameters
        ----------
        move_as_usi : str
            "7g7f" や "3d3c+"、 "R*5e" のような文字列を想定。 "resign" のような文字列は想定外
        """
        self._move_as_usi = move_as_usi


    def get_src_file_or_none(self):
        """移動元の列番号　＞　序数。打ではマス番号は取得できない"""

        # 移動元
        src_str = self._move_as_usi[0: 2]

        #print(f"[get_src_file_or_none] move_as_usi: {self._move_as_usi}, src_str: {src_str}")

        # ［打］は列番号を取得できない
        if src_str in Move._src_drops:
            return None

        file_str = src_str[0]

        #print(f"[get_src_file_or_none] move_as_usi: {self._move_as_usi}, file_str: {file_str}")

        try:
            return Move._file_str_to_num[file_str]
        except:
            raise Exception(f"src file error: '{file_str}' in '{self._move_as_usi}'")


    def get_src_rank_or_none(self):
        """移動元の段番号　＞　序数。打ではマス番号は取得できない"""

        # 移動元
        src_str = self._move_as_usi[0: 2]

        #print(f"[get_src_rank_or_none] move_as_usi: {self._move_as_usi}, src_str: {src_str}")

        # ［打］は列番号を取得できない
        if src_str in Move._src_drops:
            return None

        rank_str = src_str[1]

        #print(f"[get_src_rank_or_none] move_as_usi: {self._move_as_usi}, rank_str: {rank_str}")

        try:
            return Move._rank_str_to_num[rank_str]
        except:
            raise Exception(f"src rank error: '{rank_str}' in '{self._move_as_usi}'")


    def get_src_sq_or_none(self):
        """移動元のマス番号（Destination Square）。打ではマス番号は取得できない"""

        file_or_none = self.get_src_file_or_none()
        rank_or_none = self.get_src_rank_or_none()

        #print(f"[get_src_sq_or_none] move_as_usi: {self._move_as_usi}, file_or_none: {file_or_none}, rank_or_none: {rank_or_none}")

        if file_or_none is not None and rank_or_none is not None:
            return (file_or_none - 1) * 9 + (rank_or_none - 1)

        return None


    def get_dst_file(self):
        """移動先の列番号　＞　序数"""

        # 移動先
        dst_str = self._move_as_usi[2: 4]

        file_str = dst_str[0]

        try:
            Move._file_str_to_num[file_str]
        except:
            raise Exception(f"dst file error: '{file_str}' in '{self._move_as_usi}'")


    def get_dst_rank(self):
        """移動先の段番号　＞　序数"""

        # 移動先
        dst_str = self._move_as_usi[2: 4]

        rank_str = dst_str[1]

        try:
            Move._rank_str_to_num[rank_str]
        except:
            raise Exception(f"dst rank error: '{rank_str}' in '{self._move_as_usi}'")


    def get_dst_sq(self):
        """移動先のマス番号（Destination Square）"""
        return (self.get_dst_rank() - 1) * 9 + (self.get_dst_file() - 1)


    def is_promotion(self):
        """成りかそれ以外（５文字なら成りだろう）"""
        if 4 < len(self._move_as_usi):
            return True

        return False


    def get_table_index(
            self,
            is_symmetrical_board):
        """将棋盤の筋が左右対称のときの評価値テーブルのセルのインデックス

        Parameters
        ----------
        is_symmetrical_board : bool
            盤は左右対称か？
        """

        # 移動元
        src_str = self._move_as_usi[0: 2]

        # 移動先
        dst_str = self._move_as_usi[2: 4]

        try:
            if is_symmetrical_board:
                src_num = Move._src_dst_str_1st_figure_to_index_on_symmetrical_board[src_str[0]] + Move._src_dst_str_2nd_figure_to_index[src_str[1]]
                dst_num = Move._src_dst_str_1st_figure_to_index_on_symmetrical_board[dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[dst_str[1]]
            else:
                src_num = Move._src_dst_str_1st_figure_to_index_on_fully_connected[src_str[0]] + Move._src_dst_str_2nd_figure_to_index[src_str[1]]
                dst_num = Move._src_dst_str_1st_figure_to_index_on_fully_connected[dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[dst_str[1]]

        except:
            raise Exception(f"dst dst error in '{self._move_as_usi}'")

        # 成りか？
        if self.is_promotion():
            pro_num = 1
        else:
            pro_num = 0

        rank_size = 9
        pro_num_size = 2

        if is_symmetrical_board:
            file_size = 5
        else:
            file_size = 9

        return (src_num * file_size * rank_size * pro_num_size) + (dst_num * pro_num_size) + pro_num
