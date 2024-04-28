import datetime
from evaluation_file_kk import EvaluationFileKk
from evaluation_file_kp import EvaluationFileKp
from evaluation_file_pp import EvaluationFilePp
from evaluation_file import EvaluationFile
from learn import Learn
from evaluation_save_kk import EvaluationSaveKk
from evaluation_save_kp import EvaluationSaveKp
from evaluation_save_pp import EvaluationSavePp


class EvaluationFacade():
    """評価の窓口"""


    def __init__(self, file_number):
        self._file_number = file_number

        # 評価値テーブル：　ＫＫポリシー
        self._kk_table_obj = None

        # 評価値テーブル：　ＫＰポリシー
        self._kp_table_obj = None

        # 評価値テーブル：　ＰＰポリシー
        self._pp_table_obj = None


    @property
    def kk_table_obj(self):
        return self._kk_table_obj


    @property
    def kp_table_obj(self):
        return self._kp_table_obj


    @property
    def pp_table_obj(self):
        return self._pp_table_obj


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
        self._kk_table_obj, shall_save_file = EvaluationFileKk.load_on_usinewgame(
                file_number=self._file_number)

        if shall_save_file:
            EvaluationSaveKk.save_file_as_kk(
                    kk_table_obj=self._kk_table_obj)

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._kk_table_obj,
                canditates_memory=king_canditates_memory, # キング
                result_file=result_file)

        #
        # ＫＰポリシー
        #
        self._kp_table_obj, shall_save_file = EvaluationFileKp.load_on_usinewgame(
                file_number=self._file_number)

        if shall_save_file:
            EvaluationSaveKp.save_file_as_kp(
                    kp_table_obj=self._kp_table_obj)

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._kp_table_obj,
                canditates_memory=king_canditates_memory, # キング
                result_file=result_file)

        #
        # ＰＰポリシー
        #
        self._pp_table_obj, shall_save_file = EvaluationFilePp.load_on_usinewgame(
                file_number=self._file_number)

        if shall_save_file:
            EvaluationSavePp.save_file_as_pp(
                    pp_table_obj=self._pp_table_obj)

        # 学習
        Learn.update_evaluation_table(
                evaluation_mm_table_obj=self._pp_table_obj,
                canditates_memory=pieces_canditates_memory,  # 自軍の玉以外の合法手
                result_file=result_file)


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
        kp_policy_dictionary = self._kp_table_obj.make_move_as_usi_and_policy_dictionary_2(
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
        kl_policy_dictionary = self.kk_table_obj.make_move_as_usi_and_policy_dictionary_2(
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
        kq_policy_dictionary = self._kp_table_obj.make_move_as_usi_and_policy_dictionary_2(
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
        pp_policy_dictionary = self._pp_table_obj.make_move_as_usi_and_policy_dictionary_2(
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
        pl_policy_dictionary = self._kp_table_obj.make_move_as_usi_and_policy_dictionary_2(
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
        pq_policy_dictionary = self._pp_table_obj.make_move_as_usi_and_policy_dictionary_2(
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
