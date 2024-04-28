class EvaluationVersionRecord():


    def __init__(
            self,
            is_king_size_of_kk):
        """初期化

        Parameters
        ----------
        is_king_size_of_kk : bool
            KKテーブルの指し手は M サイズではなく K サイズか？
        """
        self._is_king_size_of_kk = is_king_size_of_kk


    @property
    def is_king_size_of_kk(self):
        return self._is_king_size_of_kk
