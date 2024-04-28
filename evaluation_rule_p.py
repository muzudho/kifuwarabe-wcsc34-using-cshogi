class EvaluationRuleP():


    @staticmethod
    def get_piece_move_number():
        """玉以外の駒の指し手の数

        Returns
        -------
        - int
        """

        #  sq   drop    sq   pro
        # (81 +    7) * 81 *   2 = 14_256
        return 14_256
