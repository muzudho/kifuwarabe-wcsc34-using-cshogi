from evaluation_fmf_plus_fmo_table import EvaluationFmfPlusFmoTable
from evaluation_fkf_plus_fko_table import EvaluationFkfPlusFkoTable
from move import Move


class EvaluationTable():
    """評価値テーブル"""


    def __init__(self, file_number):
        self._file_number = file_number

        # 評価値テーブル：　ＦｍＦ＋ＦｍＯポリシー
        self._fmf_plus_fmo_policy_table = None

        # 評価値テーブル：　ＦｋＦ＋ＦｋＯポリシー
        self._fkf_plus_fko_policy_table = None


    def usinewgame(
            self,
            king_canditates_memory,
            minions_canditates_memory,
            result_file):
        """新規対局の準備"""

        # ＦｍＦ＋ＦｍＯポリシー
        self._fmf_plus_fmo_policy_table = EvaluationFmfPlusFmoTable(file_number=self._file_number)
        self._fmf_plus_fmo_policy_table.load_from_file_or_random_table()
        self._fmf_plus_fmo_policy_table.update_evaluation_table(
                minions_canditates_memory,  # ミニオンズ
                result_file)

        # ＦｋＦ＋ＦｋＯポリシー
        self._fkf_plus_fko_policy_table = EvaluationFkfPlusFkoTable(file_number=self._file_number)
        self._fkf_plus_fko_policy_table.load_from_file_or_random_table()
        self._fkf_plus_fko_policy_table.update_evaluation_table(
                king_canditates_memory, # キング
                result_file)


    def save_file(self):
        """ファイルの保存"""

        # ＦｍＦ＋ＦｍＯポリシー
        self._fmf_plus_fmo_policy_table.save_evaluation_to_file()

        # ＦｋＦ＋ＦｋＯポリシー
        self._fmf_plus_fmo_policy_table.save_evaluation_to_file()


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
        fkf_plus_fko_policy_dictionary = self._fmf_plus_fmo_policy_table.make_move_as_usi_and_policy_dictionary(
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


    def get_ee_table_index_from_move_as_usi(
            self,
            move_as_usi):
        """内容確認用
        指し手を１つ指定すると、その評価値が入っているＥＥテーブルのインデックスを返します"""
        return Move(move_as_usi).get_table_index(
                is_symmetrical_board=True)

