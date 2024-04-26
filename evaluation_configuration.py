from move import Move


class EvaluationConfiguration():


    @staticmethod
    def get_fully_connected_move_number():
        return 14_256


    @staticmethod
    def get_fully_connected_table_size():
        return 203_219_280


    @staticmethod
    def get_symmetrical_connected_move_number():
        return 8_424


    @staticmethod
    def get_symmetrical_connected_table_size():
        return 70_955_352


    @staticmethod
    def get_table_index(
            move,
            is_symmetrical_connected):
        """将棋盤の筋が左右対称のときの評価値テーブルのセルのインデックス

        Parameters
        ----------
        move : Move
            指し手
        is_symmetrical_connected : bool
            盤は左右対称か？
        """

        try:
            if is_symmetrical_connected:
                src_num = Move._src_dst_str_1st_figure_to_index_on_symmetrical_board[move.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.src_str[1]]
                dst_num = Move._src_dst_str_1st_figure_to_index_on_symmetrical_board[move.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.dst_str[1]]
            else:
                src_num = Move._src_dst_str_1st_figure_to_index_on_fully_connected[move.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.src_str[1]]
                dst_num = Move._src_dst_str_1st_figure_to_index_on_fully_connected[move.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.dst_str[1]]

        except:
            raise Exception(f"dst dst error in '{move.as_usi}'")

        # 成りか？
        if move.is_promotion():
            pro_num = 1
        else:
            pro_num = 0

        rank_size = 9
        pro_num_size = 2

        if is_symmetrical_connected:
            file_size = 5
        else:
            file_size = 9

        return (src_num * file_size * rank_size * pro_num_size) + (dst_num * pro_num_size) + pro_num
