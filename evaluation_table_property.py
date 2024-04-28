class EvaluationTableProperty():


    def __init__(
            self,
            is_king_size_of_a,
            is_king_size_of_b,
            is_symmetrical_half_board):
        """初期化

        Parameters
        ----------
        is_king_size_of_a : bool
            KKテーブルの指し手 a は M サイズではなく K サイズか？
        is_king_size_of_b : bool
            KKテーブルの指し手 b は M サイズではなく K サイズか？
        is_symmetrical_half_board : bool
            盤は左右対称とみなして半分だけを使っているか？
        """
        self._is_king_size_of_a = is_king_size_of_a
        self._is_king_size_of_b = is_king_size_of_b
        self._is_symmetrical_half_board = is_symmetrical_half_board


    @property
    def is_king_size_of_a(self):
        """KKテーブルの指し手 a は M サイズではなく K サイズか？"""
        return self._is_king_size_of_a


    @property
    def is_king_size_of_b(self):
        """KKテーブルの指し手 b は M サイズではなく K サイズか？"""
        return self._is_king_size_of_b


    @property
    def is_symmetrical_half_board(self):
        """盤は左右対称とみなして半分だけを使っているか？"""
        return self._is_symmetrical_half_board
