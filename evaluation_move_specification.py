class EvaluationMoveSpecification():
    """指し手の仕様"""


    def __init__(
            self,
            is_king,
            is_symmetrical_connected):
        """初期化

        Parameters
        ----------
        m_index : int
            指し手１つ分のインデックス
        is_king : bool
            玉の動きか？
        is_symmetrical_connected : bool
            盤は左右対称か？
        """
        self._is_king = is_king
        self._is_symmetrical_connected = is_symmetrical_connected

        if is_king:
            # 玉は成らずの１パターン
            self._pro_patterns = 1
        else:
            # 成り、成らずで２パターン
            self._pro_patterns = 2

        # 段数
        self._rank_size = 9

        # 筋数
        if is_symmetrical_connected:
            # 盤が左右対称
            self._file_size = 5
        else:
            self._file_size = 9

        # 移動先パターン数
        self._dst_patterns = self._file_size * self._rank_size

        # 打の種類数
        self._drop_patterns = 7

        # 移動元のパターン数
        self._src_patterns = self._drop_patterns + self._file_size * self._rank_size

        # 移動のパターン数
        self._move_patterns = self._src_patterns * self._drop_patterns * self._pro_patterns


    @property
    def is_king(self):
        """玉の動きか？"""
        return self._is_king


    @property
    def is_symmetrical_connected(self):
        """盤は左右対称か？"""
        return self._is_symmetrical_connected


    @property
    def pro_patterns(self):
        """成り、成らずで２パターン"""
        return self._pro_patterns


    @property
    def rank_size(self):
        """段数"""
        return self._rank_size


    @property
    def file_size(self):
        """筋数"""
        return self._file_size


    @property
    def dst_patterns(self):
        """移動先パターン数"""
        return self._dst_patterns


    @property
    def drop_patterns(self):
        """打の種類数"""
        return self._drop_patterns


    @property
    def src_patterns(self):
        """移動元のパターン数"""
        return self._src_patterns


    @property
    def move_patterns(self):
        """移動のパターン数"""
        return self._move_patterns


    def to_debug_str(self):
        """デバッグ用文字列"""
        return f"is_king:{self._is_king}  is_symmetrical_connected:{self._is_symmetrical_connected}  pro_patterns:{self._pro_patterns}  rank_size:{self._rank_size}  file_size:{self._file_size}  dst_patterns:{self._dst_patterns}  drop_patterns:{self._drop_patterns}  src_patterns:{self._src_patterns}  move_patterns:{self._move_patterns}"
