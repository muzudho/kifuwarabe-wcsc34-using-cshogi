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


    _file_num_to_str = {
        1:'1',
        2:'2',
        3:'3',
        4:'4',
        5:'5',
        6:'6',
        7:'7',
        8:'8',
        9:'9',
    }
    """列数を文字に変換"""


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
    """段英字を数に変換"""


    _rank_num_to_str = {
        1:'a',
        2:'b',
        3:'c',
        4:'d',
        5:'e',
        6:'f',
        7:'g',
        8:'h',
        9:'i',
    }
    """段数を英字に変換"""


    _src_dst_str_1st_figure_to_index_on_fully_connected = {
        'R' : 81,   # 'R*' 移動元の打 72+9=81
        'B' : 82,   # 'B*'
        'G' : 83,   # 'G*'
        'S' : 84,   # 'S*'
        'N' : 85,   # 'N*'
        'L' : 86,   # 'L*'
        'P' : 87,   # 'P*'
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
        'R' : 45,   # 'R*' 移動元の打 36+9=45
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
    _src_drop_files = ('R', 'B', 'G', 'S', 'N', 'L', 'P')


    @staticmethod
    def get_rank_num_to_str(rank_num):
        return Move._rank_num_to_str[rank_num]


    def __init__(self, move_as_usi):
        """初期化

        Parameters
        ----------
        move_as_usi : str
            "7g7f" や "3d3c+"、 "R*5e" のような文字列を想定。 "resign" のような文字列は想定外
        """
        self._move_as_usi = move_as_usi


    @property
    def as_usi(self):
        return self._move_as_usi


    @property
    def src_str(self):
        # 移動元
        return self._move_as_usi[0: 2]


    @property
    def dst_str(self):
        # 移動先
        return self._move_as_usi[2: 4]


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
