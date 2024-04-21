from evaluation_ee_table import EvaluationEeTable


class EvaluationTable():
    """評価値テーブル"""


    def __init__(self, file_number):
        self._file_number = file_number
        self._ee_table = None
        pass


    @property
    def ee_table(self):
        """ＥＥテーブル"""
        return self._ee_table


    def usinewgame(self, canditates_memory, result_file):
        """新規対局の準備"""
        self._ee_table = EvaluationEeTable(file_number=self._file_number)
        self._ee_table.load_from_file_or_random_table()
        self._ee_table.update_evaluation_table(canditates_memory, result_file)


    def save_file(self):
        """ファイルの保存"""
        self._ee_table.save_evaluation_to_file()


    def make_move_score_dictionary(
            self,
            sorted_friend_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn):
        """指し手にスコアが紐づく辞書を作成"""

        ## TODO ＫＦ＋ＫＦテーブル

        ## ＦＦ＋ＦＯテーブル
        return self._ee_table.make_move_score_dictionary_from_ff_plus_fo(
            sorted_friend_legal_move_list_as_usi,
            opponent_legal_move_set_as_usi,
            turn)


    def get_ee_table_index_from_move_as_usi(
            self,
            move_as_usi,
            turn):
        """内容確認用
        指し手を１つ指定すると、その評価値が入っているＥＥテーブルのインデックスを返します"""
        return self._ee_table.get_evaluation_table_index_from_move_as_usi(
                move_as_usi,
                turn)

