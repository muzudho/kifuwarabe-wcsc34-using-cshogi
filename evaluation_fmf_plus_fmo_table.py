from evaluation_ee_table import EvaluationEeTable


class EvaluationFmfPlusFmoTable(EvaluationEeTable):
    """評価値ＦｍＦ＋ＦｍＯテーブル
    このテーブルを使って FmF + FmO の評価値を返す
    """

    def __init__(
            self,
            file_number):
        """初期化"""

        evaluation_kind = "fmf_fmo"

        EvaluationEeTable.__init__(
                self,
                file_number=file_number,
                evaluation_kind=evaluation_kind,
                file_name=f'n{file_number}_eval_{evaluation_kind}.txt',            # 旧
                bin_file_name=f'n{file_number}_eval_{evaluation_kind}.bin',        # 旧
                bin_v2_file_name=f'n{file_number}_eval_{evaluation_kind}_v2.bin',  # 新
                move_size=8424,
                table_size = 70_955_352)
