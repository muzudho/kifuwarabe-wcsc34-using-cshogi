import datetime
from evaluation_configuration import EvaluationConfiguration
from evaluation_fmf_plus_fmo_table import EvaluationFmfPlusFmoTable
from evaluation_fkf_plus_fko_table import EvaluationFkfPlusFkoTable
from file_versioning import FileVersioning


class EvaluationTable():
    """評価値テーブル"""


    def __init__(self, file_number):
        self._file_number = file_number

        # 評価値テーブル：　ＦｋＦ＋ＦｋＯポリシー
        self._fkf_plus_fko_policy_table = None
        self._is_symmetrical_connected_of_fkf_plus_fko = None

        # 評価値テーブル：　ＦｍＦ＋ＦｍＯポリシー
        self._fmf_plus_fmo_policy_table = None
        self._is_symmetrical_connected_of_fmf_plus_fmo = None


    @property
    def fkf_plus_fko_policy_table(self):
        return self._fkf_plus_fko_policy_table


    @property
    def fmf_plus_fmo_policy_table(self):
        return self._fmf_plus_fmo_policy_table


    def usinewgame(
            self,
            king_canditates_memory,
            minions_canditates_memory,
            result_file):
        """新規対局の準備

        Parameters
        ----------
        king_canditates_memory : CanditatesMemory
            自玉の指し手
        minions_canditates_memory : CanditatesMemory
            自軍の玉以外の指し手
        result_file : ResultFile
            結果
        """

        #
        # ＦｋＦ＋ＦｋＯポリシー
        #
        file_version = FileVersioning.check_file_version(
                file_number=self._file_number,
                evaluation_kind="fkf_fko")
        tuple = FileVersioning.load_from_file_or_random_table(
                file_number=self._file_number,
                evaluation_kind="fkf_fko",
                file_version=file_version)

        if tuple is None:
            ee_table = None
            is_file_modified = True     # 新規作成だから
        else:
            ee_table, file_version = tuple
            is_file_modified = ee_table is None

        self._is_symmetrical_connected_of_fkf_plus_fko = True
        if file_version == "V3":
            # TODO 予定
            self._is_symmetrical_connected_of_fkf_plus_fko = False

        if ee_table is None:
            # ファイルが存在しないとき
            ee_table = FileVersioning.reset_to_random_table(
                file_number=self._file_number,
                evaluation_kind="fkf_fko",
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        self._fkf_plus_fko_policy_table = EvaluationFkfPlusFkoTable(
                file_number=self._file_number,
                evaluation_ee_table=ee_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=self._is_symmetrical_connected_of_fkf_plus_fko)

        self._fkf_plus_fko_policy_table.update_evaluation_table(
                king_canditates_memory, # キング
                result_file)

        #
        # ＦｍＦ＋ＦｍＯポリシー
        #
        file_version = FileVersioning.check_file_version(
                file_number=self._file_number,
                evaluation_kind="fmf_fmo")
        tuple = FileVersioning.load_from_file_or_random_table(
                file_number=self._file_number,
                evaluation_kind="fmf_fmo",
                file_version=file_version)

        if tuple is None:
            ee_table = None
            is_file_modified = True     # 新規作成だから
        else:
            ee_table, file_version = tuple
            is_file_modified = ee_table is None

        self._is_symmetrical_connected_of_fmf_plus_fmo = True
        if file_version == "V3":
            # TODO 予定
            self._is_symmetrical_connected_of_fmf_plus_fmo = False

        if ee_table is None:
            # ファイルが存在しないとき
            ee_table = FileVersioning.reset_to_random_table(
                file_number=self._file_number,
                evaluation_kind="fmf_fmo",
                table_size=EvaluationConfiguration.get_symmetrical_connected_table_size())

        self._fmf_plus_fmo_policy_table = EvaluationFmfPlusFmoTable(
                file_number=self._file_number,
                evaluation_ee_table=ee_table,
                is_file_modified=is_file_modified,
                is_symmetrical_connected=self._is_symmetrical_connected_of_fmf_plus_fmo)

        self._fmf_plus_fmo_policy_table.update_evaluation_table(
                minions_canditates_memory,  # ミニオンズ
                result_file)


    def save_file(self):
        """ファイルの保存"""

        # 保存するかどうかは先に判定しておくこと
        if self._fkf_plus_fko_policy_table.is_file_modified:
            # ＦｋＦ＋ＦｋＯポリシー
            FileVersioning.save_evaluation_to_file(
                    file_number=self._file_number,
                    evaluation_kind="fkf_fko",
                    evaluation_ee_table=self._fkf_plus_fko_policy_table.evaluation_ee_table)
        else:
            print(f"[{datetime.datetime.now()}] fkf_fko file not changed", flush=True)

        # 保存するかどうかは先に判定しておくこと
        if self._fmf_plus_fmo_policy_table.is_file_modified:
            # ＦｍＦ＋ＦｍＯポリシー
            FileVersioning.save_evaluation_to_file(
                    file_number=self._file_number,
                    evaluation_kind="fmf_fmo",
                    evaluation_ee_table=self._fmf_plus_fmo_policy_table.evaluation_ee_table)
        else:
            print(f"[{datetime.datetime.now()}] fmf_fmo file not changed", flush=True)


    def make_move_as_usi_and_policy_dictionary(
            self,
            sorted_friend_king_legal_move_list_as_usi,
            sorted_friend_minions_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手にスコアが紐づく辞書を作成"""

        # 指し手に評価値を付ける
        king_move_as_usi_and_score_dictionary = {}
        minions_move_as_usi_and_score_dictionary = {}

        # ＦｋＦ＋ＦｋＯポリシー
        fkf_plus_fko_policy_dictionary = self._fkf_plus_fko_policy_table.make_move_as_usi_and_policy_dictionary(
                sorted_friend_king_legal_move_list_as_usi,
                sorted_friend_minions_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                turn)

        ## 評価値をマージ
        for fkf_plus_fko, policy in fkf_plus_fko_policy_dictionary.items():
            if fkf_plus_fko in king_move_as_usi_and_score_dictionary:
                king_move_as_usi_and_score_dictionary[fkf_plus_fko] += policy
            else:
                king_move_as_usi_and_score_dictionary[fkf_plus_fko] = policy

        # ＦｍＦ＋ＦｍＯポリシー
        fmf_plus_fmo_policy_dictionary = self._fmf_plus_fmo_policy_table.make_move_as_usi_and_policy_dictionary(
                sorted_friend_king_legal_move_list_as_usi,
                sorted_friend_minions_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                turn)

        ## 評価値をマージ
        for fmf_plus_fmo, policy in fmf_plus_fmo_policy_dictionary.items():
            if fmf_plus_fmo in minions_move_as_usi_and_score_dictionary:
                minions_move_as_usi_and_score_dictionary[fmf_plus_fmo] += policy
            else:
                minions_move_as_usi_and_score_dictionary[fmf_plus_fmo] = policy

        return (king_move_as_usi_and_score_dictionary, minions_move_as_usi_and_score_dictionary)
