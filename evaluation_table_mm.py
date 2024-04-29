class EvaluationTableMm():
    """評価値ＭＭテーブル

    USIプロトコルの指し手の符号を M (Move) と呼ぶとする
    M と M の関係を MM と呼ぶとする

    評価値テーブルは MM である

    自軍を F（Friend）、相手を O（Opponent） と呼ぶことがある

    自玉の合法手を K（King）、
    敵玉の合法手を L（Lord; next K） と呼ぶ
    自軍の玉以外の合法手を P (Piece) と呼ぶとする
    敵軍の玉以外の合法手を Q (Quaffers;next P) と呼ぶとする

    K と K の関係を KK、
    K と P の関係を KP、
    P と P の関係を PP、

    と呼ぶ
    """


    def __init__(
            self,
            file_number,
            file_name,
            table_size_obj,
            list_of_move_size,
            raw_mm_table,
            is_king_size_of_a,
            is_king_size_of_b,
            is_file_modified):
        """初期化

        Parameters
        ----------
        table_size_obj: EvaluationTableSize
            テーブル・サイズ。計算過程付き
        list_of_move_size : str[]
            指し手 a, b それぞれのサイズ
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真

        指し手は２種類
        ============

        (1) 駒を指す符号
        (2) resign （投了）や、 win （入玉勝ち宣言）などの文字列

        この評価関数は上記 (1) のみを取り扱う


        駒を指す符号の構造
        ================

        以下のもので構成される

        (1) src     移動元の８１マス または 打つ駒７種類
        (2) dst     移動先の８１マス
        (3) pro     成るか？

        上記(1),(2),(3) の組み合わせの数は、以下の通り

            (81 + 7) * 81 * 2 = 14_256       ... move 数

        実用上、駒はワープできるわけではないので本当はこの数より少なくできるはずですが、
        実装方法が思い浮かばないので、このまま全結合とします


        move 数を２つの組み合わせにすると、以下の通り

            (14256 - 1) * 14256 = 203_219_280       ... table_size 数

        ----------

        評価値テーブルのセル値は、 0,1 の２値とする

        (2024-04-12 fri)
            評価値テーブルは先手から見たものとし、後手番では
            （テーブルを１８０°回転させるのではなく）指し手を１８０°回転させて評価値テーブルを利用するものとする

        ----------
        """
        self._file_number = file_number
        self._file_name = file_name
        self._table_size_obj = table_size_obj
        self._list_of_move_size = list_of_move_size
        self._raw_mm_table = raw_mm_table
        self._is_king_of_a = is_king_size_of_a
        self._is_king_of_b = is_king_size_of_b
        self._is_file_modified = is_file_modified


    @property
    def file_number(self):
        return self._file_number


    @property
    def file_name(self):
        return self._file_name


    @property
    def list_of_move_size(self):
        return self._list_of_move_size


    @property
    def table_size_obj(self):
        """テーブル・サイズ。計算過程付き"""
        return self._table_size_obj


    @property
    def is_file_modified(self):
        return self._is_file_modified


    @is_file_modified.setter
    def is_file_modified(self, value):
        self._is_file_modified = value


    @property
    def is_king_of_a(self):
        return self._is_king_of_a


    @property
    def is_king_of_b(self):
        return self._is_king_of_b


    @property
    def raw_mm_table(self):
        return self._raw_mm_table
