import datetime
from evaluation_kk_file_versioning import EvaluationKkFileVersioning
from evaluation_kp_file_versioning import EvaluationKpFileVersioning
from evaluation_pp_file_versioning import EvaluationPpFileVersioning
from evaluation_file_versioning import FileVersioning
from learn import Learn


class EvaluationFacade():
    """評価の窓口"""


    def __init__(self, file_number):
        self._file_number = file_number

        # 評価値テーブル：　ＫＫポリシー
        self._kk_policy_table = None

        # 評価値テーブル：　ＫＰポリシー
        self._kp_policy_table = None

        # 評価値テーブル：　ＰＰポリシー
        self._pp_policy_table = None


    @property
    def kk_policy_table(self):
        return self._kk_policy_table


    @property
    def kp_policy_table(self):
        return self._kp_policy_table


    @property
    def pp_policy_table(self):
        return self._pp_policy_table


    def usinewgame(
            self,
            king_canditates_memory,
            pieces_canditates_memory,
            result_file):
        """新規対局の準備

        Parameters
        ----------
        king_canditates_memory : CanditatesMemory
            自玉の指し手
        pieces_canditates_memory : CanditatesMemory
            自軍の玉以外の指し手
        result_file : ResultFile
            結果
        """

        #
        # ＫＫポリシー
        #
        self._kk_policy_table, shall_save_file = EvaluationKkFileVersioning.load_kk_policy(
                file_number=self._file_number)

        if shall_save_file:
            self.save_file_as_kk()

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._kk_policy_table,
                canditates_memory=king_canditates_memory, # キング
                result_file=result_file)

        #
        # ＫＰポリシー
        #
        self._kp_policy_table, shall_save_file = EvaluationKpFileVersioning.load_kp_policy(
                file_number=self._file_number)

        if shall_save_file:
            self.save_file_as_kp()

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._kp_policy_table,
                canditates_memory=king_canditates_memory, # キング
                result_file=result_file)

        #
        # ＰＰポリシー
        #
        self._pp_policy_table, shall_save_file = EvaluationPpFileVersioning.load_pp_policy(
                file_number=self._file_number)

        if shall_save_file:
            self.save_file_as_pp()

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._pp_policy_table,
                canditates_memory=pieces_canditates_memory,  # 自軍の玉以外の合法手
                result_file=result_file)


    def save_file_as_kk(self):
        """ＫＫ評価値ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._kk_policy_table.is_file_modified:
            # ＫＫポリシー
            file_names_by_version = EvaluationKkFileVersioning.create_file_names_each_version(
                    file_number=self._kk_policy_table.file_number,
                    evaluation_kind="kk")

            file_name = file_names_by_version[3]

            FileVersioning.save_evaluation_to_file(
                    file_name=file_name,
                    evaluation_mm_table=self._kk_policy_table.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kk file not changed", flush=True)


    def save_file_as_kp(self):
        """ＫＰ評価値ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._kp_policy_table.is_file_modified:
            # ＫＰポリシー
            file_names_by_version = EvaluationKpFileVersioning.create_file_names_each_version(
                    file_number=self._file_number,
                    evaluation_kind="kp")    # V3 の途中からの新名を使っていく

            file_name = file_names_by_version[3]

            FileVersioning.save_evaluation_to_file(
                    file_name=file_name,
                    evaluation_mm_table=self._kp_policy_table.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kp file not changed", flush=True)


    def save_file_as_pp(self):
        """ＰＰ評価値ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._pp_policy_table.is_file_modified:
            # ＰＰポリシー
            file_names_by_version = EvaluationPpFileVersioning.create_file_names_each_version(
                    file_number=self._file_number,
                    evaluation_kind="pp")   # V3 の途中からの新名を使っていく

            file_name = file_names_by_version[3]

            FileVersioning.save_evaluation_to_file(
                    file_name=file_name,
                    evaluation_mm_table=self._pp_policy_table.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] pp file not changed", flush=True)


    def make_move_as_usi_and_policy_dictionary(
            self,
            king_move_collection_as_usi,
            pieces_move_collection_as_usi,
            lord_move_collection_as_usi,
            quaffers_move_collection_as_usi,
            turn):
        """指し手にスコアが紐づく辞書を作成

        Parameters
        ----------
        king_move_collection_as_usi : iterable
            例えば自玉の指し手の収集
        pieces_move_collection_as_usi : iterable
            自玉を除く自軍の指し手の収集
        lord_move_collection_as_usi : iterable
            敵玉の指し手の収集
        quaffers_move_collection_as_usi : iterable
            敵玉を除く敵軍の指し手の収集

        Returns
        -------
            - 自玉の指し手のポリシー値付き辞書
            - 自玉を除く自軍のポリシー値付き辞書
        """

        # 指し手に評価値を付ける
        king_move_as_usi_and_policy_dictionary = {}
        pieces_move_as_usi_and_policy_dictionary = {}

        # ＫＰポリシー　ｉｎ　ＫＰテーブル
        kp_policy_dictionary = self._kp_policy_table.make_move_as_usi_and_policy_dictionary_2(
                a_move_collection_as_usi=king_move_collection_as_usi,
                b_move_collection_as_usi=pieces_move_collection_as_usi,
                turn=turn)

        # 評価値をマージ
        for king_move_as_usi, policy in kp_policy_dictionary.items():
            if king_move_as_usi in king_move_as_usi_and_policy_dictionary:
                king_move_as_usi_and_policy_dictionary[king_move_as_usi] += policy
            else:
                king_move_as_usi_and_policy_dictionary[king_move_as_usi] = policy

        # ＫＬポリシー　ｉｎ　ＫＫテーブル
        kl_policy_dictionary = self._kk_policy_table.make_move_as_usi_and_policy_dictionary_2(
                a_move_collection_as_usi=king_move_collection_as_usi,
                b_move_collection_as_usi=lord_move_collection_as_usi,
                turn=turn)

        # 評価値をマージ
        for king_move_as_usi, policy in kl_policy_dictionary.items():
            if king_move_as_usi in king_move_as_usi_and_policy_dictionary:
                king_move_as_usi_and_policy_dictionary[king_move_as_usi] += policy
            else:
                king_move_as_usi_and_policy_dictionary[king_move_as_usi] = policy

        # ＫＱポリシー　ｉｎ　ＫＰテーブル
        kq_policy_dictionary = self._kp_policy_table.make_move_as_usi_and_policy_dictionary_2(
                a_move_collection_as_usi=king_move_collection_as_usi,
                b_move_collection_as_usi=quaffers_move_collection_as_usi,
                turn=turn)

        # 評価値をマージ
        for king_move_as_usi, policy in kq_policy_dictionary.items():
            if king_move_as_usi in king_move_as_usi_and_policy_dictionary:
                king_move_as_usi_and_policy_dictionary[king_move_as_usi] += policy
            else:
                king_move_as_usi_and_policy_dictionary[king_move_as_usi] = policy

        # ＰＰポリシー　ｉｎ　ＰＰテーブル
        pp_policy_dictionary = self._pp_policy_table.make_move_as_usi_and_policy_dictionary_2(
                a_move_collection_as_usi=pieces_move_collection_as_usi,
                b_move_collection_as_usi=pieces_move_collection_as_usi,
                turn=turn)

        # 評価値をマージ
        for piece_move_as_usi, policy in pp_policy_dictionary.items():
            if piece_move_as_usi in pieces_move_as_usi_and_policy_dictionary:
                pieces_move_as_usi_and_policy_dictionary[piece_move_as_usi] += policy
            else:
                pieces_move_as_usi_and_policy_dictionary[piece_move_as_usi] = policy

        # ＰＬポリシー　ｉｎ　ＫＰテーブル
        # TODO 盤の先後をひっくり返さないといけないか？
        pl_policy_dictionary = self._kp_policy_table.make_move_as_usi_and_policy_dictionary_2(
                a_move_collection_as_usi=pieces_move_collection_as_usi,
                b_move_collection_as_usi=lord_move_collection_as_usi,
                turn=turn)

        # 評価値をマージ
        for piece_move_as_usi, policy in pl_policy_dictionary.items():
            if piece_move_as_usi in pieces_move_as_usi_and_policy_dictionary:
                pieces_move_as_usi_and_policy_dictionary[piece_move_as_usi] += policy
            else:
                pieces_move_as_usi_and_policy_dictionary[piece_move_as_usi] = policy

        # ＰＱポリシー　ｉｎ　ＰＰテーブル
        pq_policy_dictionary = self._pp_policy_table.make_move_as_usi_and_policy_dictionary_2(
                a_move_collection_as_usi=pieces_move_collection_as_usi,
                b_move_collection_as_usi=quaffers_move_collection_as_usi,
                turn=turn)

        # 評価値をマージ
        for piece_move_as_usi, policy in pq_policy_dictionary.items():
            if piece_move_as_usi in pieces_move_as_usi_and_policy_dictionary:
                pieces_move_as_usi_and_policy_dictionary[piece_move_as_usi] += policy
            else:
                pieces_move_as_usi_and_policy_dictionary[piece_move_as_usi] = policy

        return (king_move_as_usi_and_policy_dictionary, pieces_move_as_usi_and_policy_dictionary)
