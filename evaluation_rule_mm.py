from move import Move


class EvaluationRuleMm():


    @staticmethod
    def get_m_index_by_move(
            move,
            is_king,
            is_symmetrical_half_board):
        """指し手を指定すると、指し手のインデックスを返す。
        ＭＭ関係用。ただしＫＫ関係を除く

        Parameters
        ----------
        move : Move
            指し手
        is_king : bool
            玉の動きか？
        is_symmetrical_half_board : bool
            盤は左右対称か？

        Returns
        -------
            - 指し手のインデックス
        """

        # 左右対称の盤か？
        if is_symmetrical_half_board:
            # 移動元マス番号、または打の種類
            try:
                src_sq = Move._src_dst_str_1st_figure_to_sq_on_symmetrical_board[move.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.src_str[1]]
            except Exception as e:
                raise Exception(f"symmetrical_half_board src_sq error in '{move.as_usi}'.  ('{move.src_str[0]}', '{move.src_str[1]}')  e: {e}")

            # 移動先マス番号
            try:
                dst_sq = Move._src_dst_str_1st_figure_to_sq_on_symmetrical_board[move.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.dst_str[1]]
            except Exception as e:
                raise Exception(f"symmetrical_half_board dst_sq error in '{move.as_usi}'.  ('{move.dst_str[0]}', '{move.dst_str[1]}')  e: {e}")

        else:
            # 移動元マス番号
            try:
                src_sq = Move._src_dst_str_1st_figure_to_sq_on_fully_connected[move.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.src_str[1]]
            except Exception as e:
                raise Exception(f"fully_connected src_sq error in '{move.as_usi}'.  ('{move.src_str[0]}', '{move.src_str[1]}')  e: {e}")

            # 移動先マス番号
            try:
                dst_sq = Move._src_dst_str_1st_figure_to_sq_on_fully_connected[move.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.dst_str[1]]
            except Exception as e:
                raise Exception(f"fully_connected dst_sq error in '{move.as_usi}'.  ('{move.dst_str[0]}', '{move.dst_str[1]}')  e: {e}")

        # 玉は成りの判定を削る
        if is_king:
            pro_size = 1
            pro_num = 0     # 玉は成らない

        else:
            pro_size = 2

            # 成りか？
            if move.promoted:
                pro_num = 1
            else:
                pro_num = 0

        rank_size = 9

        if is_symmetrical_half_board:
            file_size = 5
        else:
            file_size = 9

        return (src_sq * file_size * rank_size * pro_size) + (dst_sq * pro_size) + pro_num
