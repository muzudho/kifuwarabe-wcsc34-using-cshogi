from .move import Move


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

        # 移動元マス番号
        try:
            src_sq = Move._src_dst_str_1st_figure_to_sq[move_obj.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move_obj.src_str[1]]
        except Exception as e:
            raise Exception(f"src_sq error in '{move_obj.as_usi}'.  ('{move_obj.src_str[0]}', '{move_obj.src_str[1]}')  e: {e}")

        # 移動先マス番号
        try:
            dst_sq = Move._src_dst_str_1st_figure_to_sq[move_obj.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move_obj.dst_str[1]]
        except Exception as e:
            raise Exception(f"dst_sq error in '{move_obj.as_usi}'.  ('{move_obj.dst_str[0]}', '{move_obj.dst_str[1]}')  e: {e}")

        # 成りか？
        if move_obj.promoted:
            pro = 1
        else:
            pro = 0

        #      src_sq * dst_size * pro_size +
        #      ----------------------------   dst_sq * pro_size +
        #                     81          2   -----------------   pro
        #                                            *        2   ----
        return src_sq *                 162 + dst_sq *        2 + pro
