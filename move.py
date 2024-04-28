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


    _src_dst_str_1st_figure_to_sq_on_fully_connected = {
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
    """移動元の１文字目をマス番号へ変換"""


    _src_dst_str_1st_figure_to_sq_on_symmetrical_board = {
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
    """移動元の１文字目をマス番号、または打番号へ変換。盤は左右対称とします"""

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

        # 移動元
        self._src_str = self._move_as_usi[0: 2]

        # 移動先
        self._dst_str = self._move_as_usi[2: 4]

        #
        # 移動元の列番号を序数で。打にはマス番号は無い
        #
        if self.src_str in Move._src_drops:
            self._src_file_or_none = None

        else:
            file_str = self.src_str[0]

            try:
                self._src_file_or_none = Move._file_str_to_num[file_str]
            except:
                raise Exception(f"src file error: '{file_str}' in '{self._move_as_usi}'")

        #
        # 移動元の段番号を序数で。打は無い
        #
        if self.src_str in Move._src_drops:
            self._src_rank_or_none = None

        else:
            rank_str = self.src_str[1]

            try:
                self._src_rank_or_none = Move._rank_str_to_num[rank_str]
            except:
                raise Exception(f"src rank error: '{rank_str}' in '{self._move_as_usi}'")

        #
        # 移動元のマス番号を基数で。打にはマス番号は無い
        #
        if self.src_file_or_none is not None and self.src_rank_or_none is not None:
            self._src_sq_or_none = (self.src_file_or_none - 1) * 9 + (self.src_rank_or_none - 1)
        else:
            self._src_sq_or_none = None

        #
        # 移動先の列番号を序数で
        #
        file_str = self.dst_str[0]

        try:
            self._dst_file = Move._file_str_to_num[file_str]
        except:
            raise Exception(f"dst file error: '{file_str}' in '{self._move_as_usi}'")


        #
        # 移動先の段番号を序数で
        #
        rank_str = self.dst_str[1]

        try:
            self._dst_rank = Move._rank_str_to_num[rank_str]
        except:
            raise Exception(f"dst rank error: '{rank_str}' in '{self._move_as_usi}'")

        #
        # 移動先のマス番号を序数で
        #
        self._dst_sq = (self.dst_rank - 1) * 9 + (self.dst_file - 1)

        #
        # 成ったか？
        #
        #   - ５文字なら成りだろう
        #
        self._promoted = 4 < len(self._move_as_usi)


    @property
    def as_usi(self):
        return self._move_as_usi


    @property
    def src_str(self):
        """移動元"""
        return self._src_str


    @property
    def dst_str(self):
        """移動先"""
        return self._dst_str


    @property
    def src_file_or_none(self):
        """移動元の列番号を序数で。打にはマス番号は無い"""
        return self._src_file_or_none


    @property
    def src_rank_or_none(self):
        """移動元の段番号を序数で。打にはマス番号は無い"""
        return self._src_rank_or_none


    @property
    def src_sq_or_none(self):
        """移動元のマス番号を基数で。打にはマス番号は無い"""
        return self._src_sq_or_none


    @property
    def dst_file(self):
        """移動先の列番号を序数で"""
        return self._dst_file


    @property
    def dst_rank(self):
        """移動先の段番号を序数で"""
        return self._dst_rank


    @property
    def dst_sq(self):
        """移動先のマス番号を序数で"""
        return self._dst_sq


    @property
    def promoted(self):
        """成ったか？"""
        return self._promoted
