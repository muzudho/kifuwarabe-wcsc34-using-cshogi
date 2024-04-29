from move import Move


class EvaluationRuleK():


    @staticmethod
    def get_king_direction_max_number():
        """玉の移動方向の最大数

        Returns
        -------
        - int
        """
        return 8


    @staticmethod
    def get_king_move_number():
        """玉の指し手の数

        Returns
        -------
        - int
        """
        # move_number = sq * directions
        #         648 = 81 *          8
        return 648


    @staticmethod
    def get_m_index_by_move(
            move_obj):
        """指し手を指定すると、指し手のインデックスを返す。

        Parameters
        ----------
        move_obj : Move
            指し手

        Returns
        -------
            - 指し手のインデックス
        """

        # 移動元マス番号。打も含む
        try:
            src_sq = Move._src_dst_str_1st_figure_to_sq[move_obj.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move_obj.src_str[1]]
        except Exception as e:
            raise Exception(f"src_sq error in '{move_obj.as_usi}'.  ('{move_obj.src_str[0]}', '{move_obj.src_str[1]}')  e: {e}")

        # 移動先マス番号
        try:
            dst_sq = Move._src_dst_str_1st_figure_to_sq[move_obj.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move_obj.dst_str[1]]
        except Exception as e:
            raise Exception(f"dst_sq error in '{move_obj.as_usi}'.  ('{move_obj.dst_str[0]}', '{move_obj.dst_str[1]}')  e: {e}")

        # 玉は成らない

        #      src_sq * dst_sq_squares + dst_sq
        #               9 * 9
        return src_sq * 81             + dst_sq
