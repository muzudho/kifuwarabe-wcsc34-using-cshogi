from move import Move
from evaluation_rule_mm import EvaluationRuleMm


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
            file_version,
            list_of_move_size,
            table_size_obj,
            evaluation_mm_table,
            is_king_of_a,
            is_king_of_b,
            is_symmetrical_half_board,
            is_file_modified):
        """初期化

        Parameters
        ----------
        file_version : str
            ファイルのバージョン
        list_of_move_size : str[]
            指し手 a, b それぞれのサイズ
        table_size_obj: EvaluationTableSize
            テーブル・サイズ。計算過程付き
        is_king_of_a : bool
            指し手 a は玉か？
        is_king_of_b : bool
            指し手 b は玉か？
        is_symmetrical_half_board : bool
            左右対称の盤か？
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

            (81 + 7) * 81 * 2 = 14_256       ... fully_connected_move 数

        実用上、駒はワープできるわけではないので本当はこの数より少なくできるはずですが、
        実装方法が思い浮かばないので、このまま全結合とします


        fully_connected_move 数を２つの組み合わせにすると、以下の通り

            (14256 - 1) * 14256 = 203_219_280       ... fully_connected_table_size 数

        ----------

        しかし、家のＰＣでこのサイズの配列を２つ読み込んで２つのエンジンで対局させることはできなかったので、
        左右対称と仮定して、９筋ではなく、５筋にする。

            (5 * 9 + 7) * (5 * 9) * 2 = 4_680     ... symmetrical_half_board_move 数


            (4_680 - 1) * 4_680 = 21_897_720    ... symmetrical_half_board_table_size 数

        ----------

        評価値テーブルのセル値は、 0,1 の２値とする

        (2024-04-12 fri)
            評価値テーブルは先手から見たものとし、後手番では
            （テーブルを１８０°回転させるのではなく）指し手を１８０°回転させて評価値テーブルを利用するものとする

        ----------
        """
        self._file_number = file_number
        self._file_name = file_name
        self._file_version = file_version
        self._list_of_move_size = list_of_move_size
        self._table_size_obj = table_size_obj
        self._evaluation_mm_table = evaluation_mm_table
        self._is_king_of_a = is_king_of_a
        self._is_king_of_b = is_king_of_b
        self._is_symmetrical_half_board = is_symmetrical_half_board
        self._is_file_modified = is_file_modified


    @property
    def file_number(self):
        return self._file_number


    @property
    def file_name(self):
        return self._file_name


    @property
    def file_version(self):
        return self._file_version


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
    def is_symmetrical_half_board(self):
        return self._is_symmetrical_half_board


    @property
    def evaluation_mm_table(self):
        return self._evaluation_mm_table


    def get_evaluation_value(
            self,
            a_move_obj,
            b_move_obj,
            turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        mm_index = EvaluationRuleMm.get_mm_index_by_2_moves(
                a_move_obj=a_move_obj,
                a_is_king=self._is_king_of_a,
                b_move_obj=b_move_obj,
                b_is_king=self._is_king_of_b,
                turn=turn,
                list_of_move_size=self.list_of_move_size,
                is_symmetrical_half_board=self.is_symmetrical_half_board)
        #print(f"[DEBUG] 逆順 b:{index_b:3} a:{index_a:3} mm_index:{mm_index}", flush=True)

        try:
            # 古いデータには 2 が入っているので、 2 は　1 に変換する
            if self._evaluation_mm_table[mm_index] == 2:
                self._evaluation_mm_table[mm_index] = 1

        except IndexError as e:
            # 例： table length: 70955352  mm_index: 102593390  except: list index out of range
            print(f"table length:{len(self._evaluation_mm_table)}  mm_index:{mm_index}  a_move_obj.as_usi:{a_move_obj.as_usi}  b_move_obj.as_usi:{b_move_obj.as_usi}  turn:{turn}  except: {e}")
            raise

        return self._evaluation_mm_table[mm_index]


    def make_move_as_usi_and_policy_dictionary_2(
            self,
            a_move_collection_as_usi,
            b_move_collection_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        a_move_set_as_usi : set
            指し手の収集（主体）
        b_move_set_as_usi : set
            指し手の収集（客体）
        turn
            手番
        """

        # 指し手に評価値を付ける
        move_as_usi_and_policy_dictionary = {}

        # 主体
        for a_move_as_usi in a_move_collection_as_usi:
            a_move_obj = Move.from_usi(a_move_as_usi)
            sum_value = 0

            # 客体と総当たり
            for b_move_as_usi in b_move_collection_as_usi:
                b_move_obj = Move.from_usi(b_move_as_usi)
                sum_value += self.get_evaluation_value(
                        a_move_obj=a_move_obj,
                        b_move_obj=b_move_obj,
                        turn=turn)

            move_as_usi_and_policy_dictionary[a_move_as_usi] = sum_value

        return move_as_usi_and_policy_dictionary