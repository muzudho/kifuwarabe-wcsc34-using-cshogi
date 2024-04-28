class EvaluationVersionRecord():


    def __init__(
            self,
            is_king_size_of_a,
            is_king_size_of_b):
        """初期化

        Parameters
        ----------
        is_king_size_of_a : bool
            KKテーブルの指し手 a は M サイズではなく K サイズか？
        is_king_size_of_b : bool
            KKテーブルの指し手 b は M サイズではなく K サイズか？
        """
        self._is_king_size_of_a = is_king_size_of_a
        self._is_king_size_of_b = is_king_size_of_b


    @property
    def is_king_size_of_a(self):
        return self._is_king_size_of_a


    @property
    def is_king_size_of_b(self):
        return self._is_king_size_of_b
