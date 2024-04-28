import cshogi
from move import Move
from move_helper import MoveHelper
from evaluation_move_specification import EvaluationMoveSpecification
from evaluation_rule_mm import EvaluationRuleMm


class EvaluationConfiguration():


    _src_num_to_file_str_on_symmetrical_half_board = {
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
            is_symmetrical_half_board):
        """指し手の数

        Parameters
        ----------
        is_king : bool
            玉の動きか？
        is_symmetrical_half_board : bool
            盤は左右対称か？

        Returns
        -------
        - int
        """

        # symmetrical connected move 数
        if is_symmetrical_half_board:
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
    def get_pair_of_list_of_move_as_usi_by_mm_index(
            mm_index,
            is_king_of_b,
            is_symmetrical_half_board):
        """逆関数

        指し手２つ分返す

        Parameters
        ----------
        mm_index : int
            指し手 a, b のペアの通しインデックス
        is_king_of_b : bool
            指し手 b は、玉の動きか？
        is_symmetrical_half_board : bool
            盤は左右対称か？
        """

        #
        # 下位の b から
        # ------------
        #

        b_size = EvaluationConfiguration.get_move_number(
            is_king=is_king_of_b,
            is_symmetrical_half_board=is_symmetrical_half_board)

        bits = mm_index

        b_index = bits % b_size
        bits //= b_size

        a_index = bits

        try:
            list_of_b_move = EvaluationConfiguration.get_list_of_move_as_usi_by_m_index(
                    m_index=b_index,
                    is_king=is_king_of_b,
                    is_symmetrical_half_board=is_symmetrical_half_board)
        except Exception as e:
            # 例： list_of_b_move error.  a_index:0  b_index:4680  mm_index:21902400  e:52
            print(f"list_of_b_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  e:{e}")
            raise

        try:
            list_of_a_move = EvaluationConfiguration.get_list_of_move_as_usi_by_m_index(
                    m_index=a_index,
                    is_king=is_king_of_b,
                    is_symmetrical_half_board=is_symmetrical_half_board)
        except Exception as e:
            # mm_index がでかすぎる？
            # 例： list_of_a_move error.  a_index:4680  b_index:0  e:52
            # 例： list_of_a_move error.  a_index:4680  b_index:0  mm_index:21902400  e:52
            print(f"list_of_a_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  is_king_of_b:{is_king_of_b}  is_symmetrical_half_board:{is_symmetrical_half_board}  e:{e}")
            raise

        return [list_of_a_move, list_of_b_move]


    @staticmethod
    def get_list_of_move_as_usi_by_m_index(
            m_index,
            is_king,
            is_symmetrical_half_board):
        """逆関数

        指し手１つ分。ただし鏡面の場合、共役が付いて２つ返ってくる

        Parameters
        ----------
        m_index : int
            指し手１つ分のインデックス
        is_king : bool
            玉の動きか？
        is_symmetrical_half_board : bool
            盤は左右対称か？
        """

        m_spec = EvaluationMoveSpecification(
            # 玉は成らないから pro を削れる
            is_king=is_king,
            is_symmetrical_half_board=is_symmetrical_half_board)

        rest = m_index

        pro_value = None
        pro_str = ''
        if not is_king:
            pro_value = rest % m_spec.pro_patterns
            if pro_value == 1:
                # 成りだ
                pro_str = '+'

            rest //= m_spec.pro_patterns

        dst_value = rest % m_spec.dst_patterns
        rest //= m_spec.dst_patterns

        src_value = rest

        # 共役の移動元の筋。左右対称の盤で、反対側の方の筋
        conjugate_src_file_str = None
        conjugate_dst_file_str = None

        # 移動先（列は左右対称）
        if is_symmetrical_half_board:
            if 36 <= dst_value:
                dst_file = '5'
                conjugate_dst_file_str = '5'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 36 + 1)
            elif 27 <= dst_value:
                dst_file = '4'
                conjugate_dst_file_str = '6'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 27 + 1)
            elif 18 <= dst_value:
                dst_file = '3'
                conjugate_dst_file_str = '7'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 18 + 1)
            elif 9 <= dst_value:
                dst_file = '2'
                conjugate_dst_file_str = '8'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 9 + 1)
            else:
                dst_file = '1'
                conjugate_dst_file_str = '9'
                dst_rank_str = Move.get_rank_num_to_str(dst_value + 1)

        else:
            if 72 <= dst_value:
                dst_file = '9'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 72 + 1)
            elif 63 <= dst_value:
                dst_file = '8'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 63 + 1)
            elif 54 <= dst_value:
                dst_file = '7'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 54 + 1)
            elif 45 <= dst_value:
                dst_file = '6'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 45 + 1)
            elif 36 <= dst_value:
                dst_file = '5'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 36 + 1)
            elif 27 <= dst_value:
                dst_file = '4'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 27 + 1)
            elif 18 <= dst_value:
                dst_file = '3'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 18 + 1)
            elif 9 <= dst_value:
                dst_file = '2'
                dst_rank_str = Move.get_rank_num_to_str(dst_value - 9 + 1)
            else:
                dst_file = '1'
                dst_rank_str = Move.get_rank_num_to_str(dst_value + 1)

        # 移動元（列は左右対称）
        if is_symmetrical_half_board:
            # FIXME 52 以上は何？

            # 45 ～ 51 は打
            if 45 <= src_value:
                try:
                    src_file_str = EvaluationConfiguration._src_num_to_file_str_on_symmetrical_half_board[src_value]

                except KeyError as e:
                    # 例： single_move error.  src_value:52  dst_value:0  m_index:4680  move_patterns:4680  (src_size:52  dst_size:45  pro_size:2)  rest:52  drop_kind:7  file_size:5  rank_size:9  e:52
                    # 例： single_move error.  src_value:52  dst_value:0  m_index:4680  move_patterns:4680  (src_size:52  dst_size:45  pro_size:2)  rest:52  drop_kind:7  file_size:5  rank_size:9  e:52
                    # 例： single_move error.  src_value:52  dst_value:0  m_index:4680  move_patterns:4680  (src_size:52  dst_size:45  pro_size:2)  rest:52  drop_kind:7  file_size:5  rank_size:9  e:52
                    # 例： single_move error.  src_value:52  dst_value:0  m_index:4680  move_patterns:4680  (src_size:52  dst_size:45  pro_size:2)  rest:52  drop_kind:7  file_size:5  rank_size:9  e:52
                    # 例： single_move error.  src_value:52  dst_value:0  pro_str:''  m_index:4680  rest:52  m_spec:is_king:False  is_symmetrical_half_board:True  pro_patterns:2  rank_size:9  file_size:5  dst_patterns:45  drop_patterns:7  src_patterns:52  move_patterns:728  e:52
                    print(f"single_move error.  src_value:{src_value}  dst_value:{dst_value}  pro_str:'{pro_str}'  m_index:{m_index}  rest:{rest}  m_spec:{m_spec.to_debug_str()}  e:{e}")
                    raise

                # FIXME 不具合調査
                if not src_file_str in Move._src_drop_files:
                    error_message = f"drop file error.  src_value:{src_value}  src_file_str:{src_file_str}"
                    print(error_message)
                    raise Exception(error_message)

                # 打の駒種類に左右の違いはない
                conjugate_src_file_str = src_file_str
                src_rank_str = '*'

            # 盤上
            else:
                if 36 <= src_value:
                    src_file_str = '5'
                    conjugate_src_file_str = '5'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 36 + 1)
                elif 27 <= src_value:
                    src_file_str = '4'
                    conjugate_src_file_str = '6'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 27 + 1)
                elif 18 <= src_value:
                    src_file_str = '3'
                    conjugate_src_file_str = '7'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 18 + 1)
                elif 9 <= src_value:
                    src_file_str = '2'
                    conjugate_src_file_str = '8'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 9 + 1)
                else:
                    src_file_str = '1'
                    conjugate_src_file_str = '9'
                    src_rank_str = Move.get_rank_num_to_str(src_value + 1)

        else:
            # 81 以上は打
            if 81 <= src_value:
                src_file_str = EvaluationConfiguration._src_num_to_file_str_on_fully_connected[src_value]
                src_rank_str = '*'

            # 盤上
            else:
                if 72 <= src_value:
                    src_file_str = '9'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 72 + 1)
                elif 63 <= src_value:
                    src_file_str = '8'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 63 + 1)
                elif 54 <= src_value:
                    src_file_str = '7'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 54 + 1)
                elif 45 <= src_value:
                    src_file_str = '6'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 45 + 1)
                elif 36 <= src_value:
                    src_file_str = '5'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 36 + 1)
                elif 27 <= src_value:
                    src_file_str = '4'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 27 + 1)
                elif 18 <= src_value:
                    src_file_str = '3'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 18 + 1)
                elif 9 <= src_value:
                    src_file_str = '2'
                    src_rank_str = Move.get_rank_num_to_str(src_value - 9 + 1)
                else:
                    src_file_str = '1'
                    src_rank_str = Move.get_rank_num_to_str(src_value + 1)

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
            is_symmetrical_half_board):
        """指し手２つの組み合わせインデックス"""

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if a_move_obj.as_usi == b_move_obj.as_usi:
            return 0

        # 後手なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        if turn == cshogi.WHITE:
            a_move_obj = MoveHelper.flip_turn(a_move_obj)
            b_move_obj = MoveHelper.flip_turn(b_move_obj)

        a_index = EvaluationRuleMm.get_m_index_by_move(
                move=a_move_obj,
                is_king=a_is_king,
                is_symmetrical_half_board=is_symmetrical_half_board)

        b_index = EvaluationRuleMm.get_m_index_by_move(
                move=b_move_obj,
                is_king=b_is_king,
                is_symmetrical_half_board=is_symmetrical_half_board)

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
