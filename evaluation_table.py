from evaluation_ff_plus_fo_table import EvaluationFfPlusFoTable
from evaluation_fk1_plus_fk2_table import EvaluationFk1PlusFk2Table
from move import Move


class EvaluationTable():
    """評価値テーブル"""


    def __init__(self, file_number):
        self._file_number = file_number

        # 評価値テーブル：　ＦＦ＋ＦＯポリシー
        self._ff_plus_fo_policy_table = None

        # 評価値テーブル：　Ｆｋ１＋Ｆｋ２ポリシー
        self._fk1_plus_fk2_policy_table = None


    def usinewgame(self, canditates_memory, result_file):
        """新規対局の準備"""

        # ＦＦ＋ＦＯポリシー
        self._ff_plus_fo_policy_table = EvaluationFfPlusFoTable(file_number=self._file_number)
        self._ff_plus_fo_policy_table.load_from_file_or_random_table()
        self._ff_plus_fo_policy_table.update_evaluation_table(canditates_memory, result_file)

        # Ｆｋ１＋Ｆｋ２ポリシー
        self._fk1_plus_fk2_policy_table = EvaluationFk1PlusFk2Table(file_number=self._file_number)


    def save_file(self):
        """ファイルの保存"""
        self._ff_plus_fo_policy_table.save_evaluation_to_file()


    def make_move_as_usi_and_policy_dictionary(
            self,
            friend_king_sq,
            opponent_king_sq,
            sorted_friend_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手にスコアが紐づく辞書を作成"""

        move_as_usi_and_score_dictionary = {}

        ## ＦＦ＋ＦＯポリシー
        ff_plus_fo_policy_dictionary = self._ff_plus_fo_policy_table.make_move_as_usi_and_policy_dictionary(
                sorted_friend_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                turn)

        ## 評価値をマージ
        for ff_plus_fo, policy in ff_plus_fo_policy_dictionary.items():
            if ff_plus_fo in move_as_usi_and_score_dictionary:
                move_as_usi_and_score_dictionary[ff_plus_fo] += policy
            else:
                move_as_usi_and_score_dictionary[ff_plus_fo] = policy

        ## TODO Ｆｋ１＋Ｆｋ２ポリシー
        fk1_plus_fk2_policy_dictionary = self._fk1_plus_fk2_policy_table.make_move_as_usi_and_policy_dictionary(
                friend_king_sq,
                opponent_king_sq,
                sorted_friend_legal_move_list_as_usi,
                opponent_legal_move_set_as_usi,
                turn)

        ## 評価値をマージ
        for fk1_plus_fk2, policy in fk1_plus_fk2_policy_dictionary.items():
            if fk1_plus_fk2 in move_as_usi_and_score_dictionary:
                move_as_usi_and_score_dictionary[fk1_plus_fk2] += policy
            else:
                move_as_usi_and_score_dictionary[fk1_plus_fk2] = policy

        return move_as_usi_and_score_dictionary


    def get_ee_table_index_from_move_as_usi(
            self,
            move_as_usi):
        """内容確認用
        指し手を１つ指定すると、その評価値が入っているＥＥテーブルのインデックスを返します"""
        return Move(move_as_usi).get_table_index(
                is_symmetrical_board=True)

