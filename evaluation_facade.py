import datetime
from evaluation_configuration import EvaluationConfiguration
from evaluation_kk_table import EvaluationKkTable
from evaluation_kk_file_versioning import EvaluationKkFileVersioning
from evaluation_kp_table import EvaluationKpTable
from evaluation_kp_file_versioning import EvaluationKpFileVersioning
from evaluation_pp_table import EvaluationPpTable
from evaluation_pp_file_versioning import EvaluationPpFileVersioning
from file_versioning import FileVersioning
from learn import Learn


class EvaluationFacade():
    """評価の窓口"""


    def __init__(self, file_number):
        self._file_number = file_number

        # 評価値テーブル：　ＫＫポリシー
        self._kk_policy_table = None
        self._is_symmetrical_connected_of_kk = None

        # 評価値テーブル：　ＫＰポリシー
        self._kp_policy_table = None
        self._is_symmetrical_connected_of_kp = None

        # 評価値テーブル：　ＰＰポリシー
        self._pp_policy_table = None
        self._is_symmetrical_connected_of_pp = None


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
        self.setup_kk_policy(
                king_canditates_memory=king_canditates_memory,
                result_file=result_file)

        #
        # ＫＰポリシー
        #
        self.setup_kp_policy(
                king_canditates_memory=king_canditates_memory,
                result_file=result_file)

        #
        # ＰＰポリシー
        #
        self.setup_pp_policy(
                pieces_canditates_memory=pieces_canditates_memory,
                result_file=result_file)


    def setup_kk_policy(
            self,
            king_canditates_memory,
            result_file):
        """ＫＫポリシー"""
        evaluation_kind = "kk"

        # ＫＫ評価値テーブルは V3 の途中から追加
        self._is_symmetrical_connected_of_kk = False

        tuple = EvaluationKkFileVersioning.check_file_version_and_name(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            file_version = None
            file_name = None
        if tuple is not None:
            file_version, file_name = tuple

        # 読込
        tuple = EvaluationKkFileVersioning.load_from_file_or_random_table(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version = tuple
            is_file_modified = mm_table is None

        # ファイルが存在しないとき
        if mm_table is None:
            mm_table = FileVersioning.reset_to_random_table(
                hint=f"n{self._file_number} kind=kk",
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        self._kk_policy_table = EvaluationKkTable(
                file_number=self._file_number,
                file_name=file_name,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=self._is_symmetrical_connected_of_kk)

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._kk_policy_table,
                canditates_memory=king_canditates_memory, # キング
                result_file=result_file)


    def setup_kp_policy(
            self,
            king_canditates_memory,
            result_file):
        """ＫＰポリシー"""
        evaluation_kind = "kp"

        tuple = EvaluationKpFileVersioning.check_file_version_and_name(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            file_version = None
            file_name = None
        if tuple is not None:
            file_version, file_name = tuple

        if file_version == None:
            evaluation_kind = "kp_ko" # V3の途中までの旧名その２

            tuple = EvaluationKpFileVersioning.check_file_version_and_name(
                    file_number=self._file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        if file_version == None:
            evaluation_kind = "fkf_fko" # V3の途中までの旧名

            tuple = EvaluationKpFileVersioning.check_file_version_and_name(
                    file_number=self._file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        # 読込
        tuple = EvaluationKpFileVersioning.load_from_file_or_random_table(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version = tuple
            is_file_modified = mm_table is None

        self._is_symmetrical_connected_of_kp = True
        if file_version == "V3":
            # V3 から盤面を左右対称ではなく、全体を使うよう変更
            self._is_symmetrical_connected_of_kp = False

        # ファイルが存在しないとき
        if mm_table is None:
            mm_table = FileVersioning.reset_to_random_table(
                hint=f"n{self._file_number} kind=kp",
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        self._kp_policy_table = EvaluationKpTable(
                file_number=self._file_number,
                file_name=file_name,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=self._is_symmetrical_connected_of_kp)

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._kp_policy_table,
                canditates_memory=king_canditates_memory, # キング
                result_file=result_file)


    def setup_pp_policy(
            self,
            pieces_canditates_memory,
            result_file):
        """ＰＰポリシー"""
        evaluation_kind = "pp"

        tuple = EvaluationPpFileVersioning.check_file_version_and_name(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind)

        if tuple is None:
            file_version = None
            file_name = None
        if tuple is not None:
            file_version, file_name = tuple

        if file_version is None:
            evaluation_kind = "pp_po"   # V3の途中までの旧称その２

            tuple = EvaluationPpFileVersioning.check_file_version_and_name(
                    file_number=self._file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        if file_version is None:
            evaluation_kind = "fmf_fmo"     # V3の途中までの旧称
            tuple = EvaluationPpFileVersioning.check_file_version_and_name(
                    file_number=self._file_number,
                    evaluation_kind=evaluation_kind)

            if tuple is None:
                file_version = None
                file_name = None
            if tuple is not None:
                file_version, file_name = tuple

        # 読込
        tuple = EvaluationPpFileVersioning.load_from_file_or_random_table(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version = tuple
            is_file_modified = mm_table is None

        self._is_symmetrical_connected_of_pp = True
        if file_version == "V3":
            # TODO 予定
            self._is_symmetrical_connected_of_pp = False

        if mm_table is None:
            # ファイルが存在しないとき
            mm_table = FileVersioning.reset_to_random_table(
                hint=f'n{self._file_number} kind=pp',
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        self._pp_policy_table = EvaluationPpTable(
                file_number=self._file_number,
                file_name=file_name,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=self._is_symmetrical_connected_of_pp)

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
            FileVersioning.save_evaluation_to_file(
                    file_number=self._file_number,
                    evaluation_kind="kk",
                    evaluation_mm_table=self._kk_policy_table.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kk file not changed", flush=True)


    def save_file_as_kp(self):
        """ＫＰ評価値ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._kp_policy_table.is_file_modified:
            # ＫＰポリシー
            FileVersioning.save_evaluation_to_file(
                    file_number=self._file_number,
                    evaluation_kind="kp",    # V3 の途中からの新名を使っていく
                    evaluation_mm_table=self._kp_policy_table.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kp file not changed", flush=True)


    def save_file_as_pp(self):
        """ＰＰ評価値ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._pp_policy_table.is_file_modified:
            # ＰＰ＋ＰＯポリシー
            FileVersioning.save_evaluation_to_file(
                    file_number=self._file_number,
                    evaluation_kind="pp",  # V3 の途中からの新名を使っていく
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
