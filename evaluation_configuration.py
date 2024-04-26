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
    def get_table_index_by_move(
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


    _src_num_to_file_str_on_symmetrical_connected = {
        45:'R',   # 'R*' 移動元の打 36+9=45
        46:'B',   # 'B*'
        47:'G',   # 'G*'
        48:'S',   # 'S*'
        49:'N',   # 'N*'
        50:'L',   # 'L*'
        51:'P',   # 'P*'
    }

    _src_num_to_file_str_on_fully_connected = {
        81:'R',   # 'R*' 移動元の打 72+9=81
        82:'B',   # 'B*'
        83:'G',   # 'G*'
        84:'S',   # 'S*'
        85:'N',   # 'N*'
        86:'L',   # 'L*'
        87:'P',   # 'P*'
    }


    @staticmethod
    def get_move_as_usi_by_table_index(
            table_index,
            is_symmetrical_connected):
        """逆関数"""

        rank_size = 9

        if is_symmetrical_connected:
            file_size = 5
        else:
            file_size = 9

        dst_size = file_size * rank_size
        pro_num_size = 2

        pro_num = table_index % 2
        table_index //= pro_num_size

        dst_num = table_index % dst_size
        table_index //= dst_size

        src_num = table_index

        # 成りか？
        if pro_num == 1:
            pro_str = '+'
        else:
            pro_str = ''

        # 移動先（列は左右対称）
        if is_symmetrical_connected:
            if 36 <= dst_num:
                dst_file = '5'
                dst_rank = Move.get_rank_num_to_str(dst_num - 36 + 1)
            elif 27 <= dst_num:
                dst_file = '4'  # or '6'
                dst_rank = Move.get_rank_num_to_str(dst_num - 27 + 1)
            elif 18 <= dst_num:
                dst_file = '3'  # or '7'
                dst_rank = Move.get_rank_num_to_str(dst_num - 18 + 1)
            elif 9 <= dst_num:
                dst_file = '2'  # or '8'
                dst_rank = Move.get_rank_num_to_str(dst_num - 9 + 1)
            else:
                dst_file = '1'  # or '9'
                dst_rank = Move.get_rank_num_to_str(dst_num + 1)

        else:
            if 72 <= dst_num:
                dst_file = '9'
                dst_rank = Move.get_rank_num_to_str(dst_num - 72 + 1)
            elif 63 <= dst_num:
                dst_file = '8'
                dst_rank = Move.get_rank_num_to_str(dst_num - 63 + 1)
            elif 54 <= dst_num:
                dst_file = '7'
                dst_rank = Move.get_rank_num_to_str(dst_num - 54 + 1)
            elif 45 <= dst_num:
                dst_file = '6'
                dst_rank = Move.get_rank_num_to_str(dst_num - 45 + 1)
            elif 36 <= dst_num:
                dst_file = '5'
                dst_rank = Move.get_rank_num_to_str(dst_num - 36 + 1)
            elif 27 <= dst_num:
                dst_file = '4'
                dst_rank = Move.get_rank_num_to_str(dst_num - 27 + 1)
            elif 18 <= dst_num:
                dst_file = '3'
                dst_rank = Move.get_rank_num_to_str(dst_num - 18 + 1)
            elif 9 <= dst_num:
                dst_file = '2'
                dst_rank = Move.get_rank_num_to_str(dst_num - 9 + 1)
            else:
                dst_file = '1'
                dst_rank = dst_num + 1

        # 移動元（列は左右対称）
        if is_symmetrical_connected:
            # 45 以上は打
            if 45 <= src_num:
                src_file = EvaluationConfiguration._src_num_to_file_str_on_symmetrical_connected[src_num]
                src_rank = '*'

            # 盤上
            else:
                if 36 <= src_num:
                    src_file = '5'
                    src_rank = Move.get_rank_num_to_str(src_num - 36 + 1)
                elif 27 <= src_num:
                    src_file = '4'  # or '6'
                    src_rank = Move.get_rank_num_to_str(src_num - 27 + 1)
                elif 18 <= src_num:
                    src_file = '3'  # or '7'
                    src_rank = Move.get_rank_num_to_str(src_num - 18 + 1)
                elif 9 <= src_num:
                    src_file = '2'  # or '8'
                    src_rank = Move.get_rank_num_to_str(src_num - 9 + 1)
                else:
                    src_file = '1'  # or '9'
                    src_rank = Move.get_rank_num_to_str(src_num + 1)

        else:
            # 81 以上は打
            if 81 <= src_num:
                src_str = EvaluationConfiguration._src_num_to_file_str_on_fully_connected[src_num]
                src_rank = '*'

            # 盤上
            else:
                if 72 <= src_num:
                    src_file = '9'
                    src_rank = Move.get_rank_num_to_str(src_num - 72 + 1)
                elif 63 <= src_num:
                    src_file = '8'
                    src_rank = Move.get_rank_num_to_str(src_num - 63 + 1)
                elif 54 <= src_num:
                    src_file = '7'
                    src_rank = Move.get_rank_num_to_str(src_num - 54 + 1)
                elif 45 <= src_num:
                    src_file = '6'
                    src_rank = Move.get_rank_num_to_str(src_num - 45 + 1)
                elif 36 <= src_num:
                    src_file = '5'
                    src_rank = Move.get_rank_num_to_str(src_num - 36 + 1)
                elif 27 <= src_num:
                    src_file = '4'
                    src_rank = Move.get_rank_num_to_str(src_num - 27 + 1)
                elif 18 <= src_num:
                    src_file = '3'
                    src_rank = Move.get_rank_num_to_str(src_num - 18 + 1)
                elif 9 <= src_num:
                    src_file = '2'
                    src_rank = Move.get_rank_num_to_str(src_num - 9 + 1)
                else:
                    src_file = '1'
                    src_rank = Move.get_rank_num_to_str(src_num + 1)

        return f'{src_file}{src_rank}{dst_file}{dst_rank}{pro_str}'
