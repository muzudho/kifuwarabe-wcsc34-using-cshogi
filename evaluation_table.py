import datetime
from evaluation_configuration import EvaluationConfiguration
from evaluation_pp_plus_po_table import EvaluationPpPoTable
from evaluation_kp_plus_ko_table import EvaluationKpPlusKoTable
from file_versioning import FileVersioning
from learn import Learn


class EvaluationTable():
    """評価値テーブル"""


    def __init__(self, file_number):
        self._file_number = file_number

        # 評価値テーブル：　ＫＰ＋ＫＯポリシー
        self._kp_plus_ko_policy_table = None
        self._is_symmetrical_connected_of_kp_plus_ko = None

        # 評価値テーブル：　ＰＰ＋ＰＯポリシー
        self._pp_plus_po_policy_table = None
        self._is_symmetrical_connected_of_pp_plus_po = None


    @property
    def kp_plus_ko_policy_table(self):
        return self._kp_plus_ko_policy_table


    @property
    def pp_plus_po_policy_table(self):
        return self._pp_plus_po_policy_table


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
        # ＦｋＦ＋ＦｋＯポリシー
        #
        evaluation_kind = "kp_ko"

        file_version = FileVersioning.check_file_version(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind)

        if file_version == None:
            evaluation_kind = "fkf_fko" # V3の途中までの旧名

            file_version = FileVersioning.check_file_version(
                    file_number=self._file_number,
                    evaluation_kind=evaluation_kind)

        tuple = FileVersioning.load_from_file_or_random_table(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version = tuple
            is_file_modified = mm_table is None

        self._is_symmetrical_connected_of_kp_plus_ko = True
        if file_version == "V3":
            # V3 から盤面を左右対称ではなく、全体を使うよう変更
            self._is_symmetrical_connected_of_kp_plus_ko = False

        if mm_table is None:
            # ファイルが存在しないとき
            mm_table = FileVersioning.reset_to_random_table(
                hint=f"n{self._file_number} kind=kp_ko",
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        self._kp_plus_ko_policy_table = EvaluationKpPlusKoTable(
                file_number=self._file_number,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=self._is_symmetrical_connected_of_kp_plus_ko)

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._kp_plus_ko_policy_table,
                canditates_memory=king_canditates_memory, # キング
                result_file=result_file)

        #
        # ＦｍＦ＋ＦｍＯポリシー
        #
        evaluation_kind = "pp_po"

        file_version = FileVersioning.check_file_version(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind)

        if file_version is None:
            evaluation_kind = "fmf_fmo"     # V3の途中までの旧称
            file_version = FileVersioning.check_file_version(
                    file_number=self._file_number,
                    evaluation_kind=evaluation_kind)

        tuple = FileVersioning.load_from_file_or_random_table(
                file_number=self._file_number,
                evaluation_kind=evaluation_kind,
                file_version=file_version)

        if tuple is None:
            mm_table = None
            is_file_modified = True     # 新規作成だから
        else:
            mm_table, file_version = tuple
            is_file_modified = mm_table is None

        self._is_symmetrical_connected_of_pp_plus_po = True
        if file_version == "V3":
            # TODO 予定
            self._is_symmetrical_connected_of_pp_plus_po = False

        if mm_table is None:
            # ファイルが存在しないとき
            mm_table = FileVersioning.reset_to_random_table(
                hint=f'n{self._file_number} kind=pp_po',
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        self._pp_plus_po_policy_table = EvaluationPpPoTable(
                file_number=self._file_number,
                evaluation_mm_table=mm_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=self._is_symmetrical_connected_of_pp_plus_po)

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._pp_plus_po_policy_table,
                canditates_memory=pieces_canditates_memory,  # 自軍の玉以外の合法手
                result_file=result_file)


    def save_file_as_kp_plus_ko(self):
        """ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._kp_plus_ko_policy_table.is_file_modified:
            # ＫＰ＋ＫＯポリシー
            FileVersioning.save_evaluation_to_file(
                    file_number=self._file_number,
                    evaluation_kind="kp_ko",    # V3 の途中からの新名を使っていく
                    evaluation_mm_table=self._kp_plus_ko_policy_table.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] kp_ko file not changed", flush=True)


    def save_file_as_pp_po(self):
        """ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._pp_plus_po_policy_table.is_file_modified:
            # ＰＰ＋ＰＯポリシー
            FileVersioning.save_evaluation_to_file(
                    file_number=self._file_number,
                    evaluation_kind="pp_po",  # V3 の途中からの新名を使っていく
                    evaluation_mm_table=self._pp_plus_po_policy_table.evaluation_mm_table)
        else:
            print(f"[{datetime.datetime.now()}] pp_po file not changed", flush=True)


    def make_move_as_usi_and_policy_dictionary(
            self,
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_pieces_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手にスコアが紐づく辞書を作成"""

        # 指し手に評価値を付ける
        king_move_as_usi_and_score_dictionary = {}
        pieces_move_as_usi_and_score_dictionary = {}

        # ＫＰ＋ＫＯポリシー
        kp_plus_ko_policy_dictionary = self._kp_plus_ko_policy_table.make_move_as_usi_and_policy_dictionary(
                sorted_friend_king_legal_move_list_as_usi,
                sorted_friend_pieces_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                turn)

        ## 評価値をマージ
        for kp_plus_ko, policy in kp_plus_ko_policy_dictionary.items():
            if kp_plus_ko in king_move_as_usi_and_score_dictionary:
                king_move_as_usi_and_score_dictionary[kp_plus_ko] += policy
            else:
                king_move_as_usi_and_score_dictionary[kp_plus_ko] = policy

        # ＰＰ＋ＰＯポリシー
        pp_plus_po_policy_dictionary = self._pp_plus_po_policy_table.make_move_as_usi_and_policy_dictionary(
                sorted_friend_king_legal_move_list_as_usi,
                sorted_friend_pieces_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                turn)

        ## 評価値をマージ
        for pp_plus_po, policy in pp_plus_po_policy_dictionary.items():
            if pp_plus_po in pieces_move_as_usi_and_score_dictionary:
                pieces_move_as_usi_and_score_dictionary[pp_plus_po] += policy
            else:
                pieces_move_as_usi_and_score_dictionary[pp_plus_po] = policy

        return (king_move_as_usi_and_score_dictionary, pieces_move_as_usi_and_score_dictionary)
