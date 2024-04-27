import cshogi
from move import Move
from move_helper import MoveHelper


class EvaluationConfiguration():


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
    def get_move_number(
            is_king,
            is_symmetrical_connected):
        """指し手の数

        Parameters
        ----------
        is_king : bool
            玉の動きか？
        is_symmetrical_connected : bool
            盤は左右対称か？

        Returns
        -------
        - int
        """

        # symmetrical connected move 数
        if is_symmetrical_connected:
            # 玉は成らないから pro を削れる
            if is_king:
                #  file   rank   drop     file   rank
                # (   5 *    9 +    7) * (   5 *    9) = 2_340
                return 2_340

            else:
                #  file   rank   drop     file   rank    pro
                # (   5 *    9 +    7) * (   5 *    9) *   2 = 4_680
                return 4_680

        # fully_connected move 数
        else:
            if is_king:
                #  sq   drop    sq
                # (81 +    7) * 81 = 7_128
                return 7_128
            else:
                #  sq   drop    sq   pro
                # (81 +    7) * 81 *   2 = 14_256
                return 14_256



    @staticmethod
    def get_table_size(
            is_king_of_a,
            is_king_of_b,
            is_symmetrical_connected):
        """テーブルのセル数

        Parameters
        ----------
        is_king_of_a : bool
            指し手 a は、玉の動きか？
        is_king_of_b : bool
            指し手 b は、玉の動きか？
        is_symmetrical_connected : bool
            盤は左右対称か？
        """

        a_number = EvaluationConfiguration.get_move_number(
                is_king=is_king_of_a,
                is_symmetrical_connected=is_symmetrical_connected)
        b_number = EvaluationConfiguration.get_move_number(
                is_king=is_king_of_b,
                is_symmetrical_connected=is_symmetrical_connected)

        # a と b のどちらを -1 するかで計算結果に違いが出てくるが、難しいところだ
        return a_number * (b_number - 1)
        #return (a_number - 1) * b_number

        # symmetrical
        #   b          |       king       piece
        # a            |    2_340-1     4_680-1
        # -------------+-----------------------
        # king   2_340 |  5_473_260  10_948_860
        # piece  4_680 | 10_946_520  21_897_720
        #
        # fully
        #   b           |        king        piece
        # a             |     7_128-1     14_256-1
        # --------------+-------------------------
        # king    7_128 |  50_801_256  101_609_640
        # piece  14_256 | 101_602_512  203_219_280



    @staticmethod
    def get_m_index_by_move(
            move,
            is_king,
            is_symmetrical_connected):
        """将棋盤の筋が左右対称のときの評価値テーブルのセルのインデックス

        Parameters
        ----------
        move : Move
            指し手
        is_king : bool
            玉の動きか？
        is_symmetrical_connected : bool
            盤は左右対称か？

        Returns
        -------
            - 指し手のインデックス
        """

        # 左右対称の盤か？
        if is_symmetrical_connected:
            # 移動元マス番号、または打の種類
            try:
                src_sq = Move._src_dst_str_1st_figure_to_sq_on_symmetrical_board[move.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.src_str[1]]
            except Exception as e:
                raise Exception(f"symmetrical_connected src_sq error in '{move.as_usi}'.  ('{move.src_str[0]}', '{move.src_str[1]}')  e: {e}")

            # 移動先マス番号
            try:
                dst_sq = Move._src_dst_str_1st_figure_to_sq_on_symmetrical_board[move.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.dst_str[1]]
            except Exception as e:
                raise Exception(f"symmetrical_connected dst_sq error in '{move.as_usi}'.  ('{move.dst_str[0]}', '{move.dst_str[1]}')  e: {e}")

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
            if move.is_promotion():
                pro_num = 1
            else:
                pro_num = 0

        rank_size = 9

        if is_symmetrical_connected:
            file_size = 5
        else:
            file_size = 9

        return (src_sq * file_size * rank_size * pro_size) + (dst_sq * pro_size) + pro_num


    @staticmethod
    def get_pair_of_list_of_move_as_usi_by_mm_index(
            mm_index,
            is_king_of_b,
            is_symmetrical_connected):
        """逆関数

        指し手２つ分返す

        Parameters
        ----------
        mm_index : int
            指し手 a, b のペアの通しインデックス
        is_king_of_b : bool
            指し手 b は、玉の動きか？
        is_symmetrical_connected : bool
            盤は左右対称か？
        """

        #
        # 下位の b から
        # ------------
        #

        b_size = EvaluationConfiguration.get_move_number(
            is_king=is_king_of_b,
            is_symmetrical_connected=is_symmetrical_connected)

        bits = mm_index

        b_index = bits % b_size
        bits //= b_size

        a_index = bits

        try:
            list_of_b_move = EvaluationConfiguration.get_list_of_move_as_usi_by_m_index(
                    m_index=b_index,
                    is_king=is_king_of_b,
                    is_symmetrical_connected=is_symmetrical_connected)
        except Exception as e:
            # 例： list_of_b_move error.  a_index:0  b_index:4680  mm_index:21902400  e:52
            print(f"list_of_b_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  e:{e}")
            raise

        try:
            list_of_a_move = EvaluationConfiguration.get_list_of_move_as_usi_by_m_index(
                    m_index=a_index,
                    is_king=is_king_of_b,
                    is_symmetrical_connected=is_symmetrical_connected)
        except Exception as e:
            # 例： list_of_a_move error.  a_index:4680  b_index:0  e:52
            # 例： list_of_a_move error.  a_index:4680  b_index:0  mm_index:21902400  e:52
            print(f"list_of_a_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  e:{e}")
            raise

        return [list_of_a_move, list_of_b_move]


    @staticmethod
    def get_list_of_move_as_usi_by_m_index(
            m_index,
            is_king,
            is_symmetrical_connected):
        """逆関数

        指し手１つ分。ただし鏡面の場合、共役が付いて２つ返ってくる

        Parameters
        ----------
        m_index : int
            指し手１つ分のインデックス
        is_king : bool
            玉の動きか？
        is_symmetrical_connected : bool
            盤は左右対称か？
        """

        # 玉は成らないから pro を削れる
        if is_king:
            pro_size = 1
        else:
            pro_size = 2

        rank_size = 9

        if is_symmetrical_connected:
            file_size = 5
        else:
            file_size = 9

        #     45 =         5 *         9
        dst_size = file_size * rank_size

        drop_kind = 7
        src_size = (file_size * rank_size) + drop_kind
        move_size = src_size * dst_size * pro_size

        #         4680
        bits = m_index

        #     0 = 4680 %            2
        pro_num = bits % pro_size
        # 2340
        bits //= pro_size

        #     0 = 2340 %       45
        dst_num = bits % dst_size
        # 52 = 2340 / 45
        bits //= dst_size

        # 52
        src_num = bits

        # 共役の移動元の筋。左右対称の盤で、反対側の方の筋
        conjugate_src_file_str = None
        conjugate_dst_file_str = None

        # 成りか？
        if pro_num == 1:
            pro_str = '+'
        else:
            pro_str = ''

        # 移動先（列は左右対称）
        if is_symmetrical_connected:
            if 36 <= dst_num:
                dst_file = '5'
                conjugate_dst_file_str = '5'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 36 + 1)
            elif 27 <= dst_num:
                dst_file = '4'
                conjugate_dst_file_str = '6'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 27 + 1)
            elif 18 <= dst_num:
                dst_file = '3'
                conjugate_dst_file_str = '7'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 18 + 1)
            elif 9 <= dst_num:
                dst_file = '2'
                conjugate_dst_file_str = '8'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 9 + 1)
            else:
                dst_file = '1'
                conjugate_dst_file_str = '9'
                dst_rank_str = Move.get_rank_num_to_str(dst_num + 1)

        else:
            if 72 <= dst_num:
                dst_file = '9'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 72 + 1)
            elif 63 <= dst_num:
                dst_file = '8'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 63 + 1)
            elif 54 <= dst_num:
                dst_file = '7'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 54 + 1)
            elif 45 <= dst_num:
                dst_file = '6'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 45 + 1)
            elif 36 <= dst_num:
                dst_file = '5'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 36 + 1)
            elif 27 <= dst_num:
                dst_file = '4'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 27 + 1)
            elif 18 <= dst_num:
                dst_file = '3'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 18 + 1)
            elif 9 <= dst_num:
                dst_file = '2'
                dst_rank_str = Move.get_rank_num_to_str(dst_num - 9 + 1)
            else:
                dst_file = '1'
                dst_rank_str = Move.get_rank_num_to_str(dst_num + 1)

        # 移動元（列は左右対称）
        if is_symmetrical_connected:
            # FIXME 52 以上は何？

            # 45 ～ 51 は打
            if 45 <= src_num:
                try:
                    src_file_str = EvaluationConfiguration._src_num_to_file_str_on_symmetrical_connected[src_num]
                except KeyError as e:
                    # 例： single_move error.  src_num:52  dst_num:0  pro_num:0  m_index:4680  move_size:4680  (src_size:52  dst_size:45  pro_size:2)  bits:52  drop_kind:7  file_size:5  rank_size:9  e:52
                    # 例： single_move error.  src_num:52  dst_num:0  pro_num:0  m_index:4680  move_size:4680  (src_size:52  dst_size:45  pro_size:2)  bits:52  drop_kind:7  file_size:5  rank_size:9  e:52
                    # 例： single_move error.  src_num:52  dst_num:0  pro_num:0  m_index:4680  move_size:4680  (src_size:52  dst_size:45  pro_size:2)  bits:52  drop_kind:7  file_size:5  rank_size:9  e:52
                    print(f"single_move error.  src_num:{src_num}  dst_num:{dst_num}  pro_num:{pro_num}  m_index:{m_index}  move_size:{move_size}  (src_size:{src_size}  dst_size:{dst_size}  pro_size:{pro_size})  bits:{bits}  drop_kind:{drop_kind}  file_size:{file_size}  rank_size:{rank_size}  e:{e}")
                    raise

                # FIXME 不具合調査
                if not src_file_str in Move._src_drop_files:
                    error_message = f"drop file error.  src_num:{src_num}  src_file_str:{src_file_str}"
                    print(error_message)
                    raise Exception(error_message)

                # 打の駒種類に左右の違いはない
                conjugate_src_file_str = src_file_str
                src_rank_str = '*'

            # 盤上
            else:
                if 36 <= src_num:
                    src_file_str = '5'
                    conjugate_src_file_str = '5'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 36 + 1)
                elif 27 <= src_num:
                    src_file_str = '4'
                    conjugate_src_file_str = '6'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 27 + 1)
                elif 18 <= src_num:
                    src_file_str = '3'
                    conjugate_src_file_str = '7'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 18 + 1)
                elif 9 <= src_num:
                    src_file_str = '2'
                    conjugate_src_file_str = '8'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 9 + 1)
                else:
                    src_file_str = '1'
                    conjugate_src_file_str = '9'
                    src_rank_str = Move.get_rank_num_to_str(src_num + 1)

        else:
            # 81 以上は打
            if 81 <= src_num:
                src_file_str = EvaluationConfiguration._src_num_to_file_str_on_fully_connected[src_num]
                src_rank_str = '*'

            # 盤上
            else:
                if 72 <= src_num:
                    src_file_str = '9'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 72 + 1)
                elif 63 <= src_num:
                    src_file_str = '8'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 63 + 1)
                elif 54 <= src_num:
                    src_file_str = '7'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 54 + 1)
                elif 45 <= src_num:
                    src_file_str = '6'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 45 + 1)
                elif 36 <= src_num:
                    src_file_str = '5'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 36 + 1)
                elif 27 <= src_num:
                    src_file_str = '4'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 27 + 1)
                elif 18 <= src_num:
                    src_file_str = '3'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 18 + 1)
                elif 9 <= src_num:
                    src_file_str = '2'
                    src_rank_str = Move.get_rank_num_to_str(src_num - 9 + 1)
                else:
                    src_file_str = '1'
                    src_rank_str = Move.get_rank_num_to_str(src_num + 1)

        list_of_move_as_usi = [
            f'{src_file_str}{src_rank_str}{dst_file}{dst_rank_str}{pro_str}'
        ]

        if conjugate_src_file_str is not None or conjugate_dst_file_str is not None:
            move_as_usi = f'{conjugate_src_file_str}{src_rank_str}{conjugate_dst_file_str}{dst_rank_str}{pro_str}'
            list_of_move_as_usi.append(move_as_usi)

        return list_of_move_as_usi


    @staticmethod
    def get_mm_index_by_2_moves(
            a_move_obj,
            a_is_king,
            b_move_obj,
            b_is_king,
            turn,
            list_of_move_size,
            is_symmetrical_connected):
        """指し手２つの組み合わせインデックス"""

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if a_move_obj.as_usi == b_move_obj.as_usi:
            return 0

        # 後手なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        if turn == cshogi.WHITE:
            a_move_obj = MoveHelper.flip_turn(a_move_obj)
            b_move_obj = MoveHelper.flip_turn(b_move_obj)

        a_index = EvaluationConfiguration.get_m_index_by_move(
                move=a_move_obj,
                is_king=a_is_king,
                is_symmetrical_connected=is_symmetrical_connected)

        b_index = EvaluationConfiguration.get_m_index_by_move(
                move=b_move_obj,
                is_king=b_is_king,
                is_symmetrical_connected=is_symmetrical_connected)

        move_indexes = [a_index, b_index]
        move_indexes.sort()

        # 昇順
        if a_index <= b_index:
            mm_index = a_index * list_of_move_size[1] + b_index
            #print(f"[DEBUG] 昇順 a:{a_index:3} b:{b_index:3} mm_index:{mm_index}", flush=True)

        # 降順
        else:
            mm_index = b_index * list_of_move_size[1] + a_index

        return mm_index
