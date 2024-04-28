import cshogi
from evaluation_move_specification import EvaluationMoveSpecification
from move import Move
from move_helper import MoveHelper


class EvaluationRuleFacade():


    _src_num_to_file_str = {
        81:'R',   # 'R*' 移動元の打 72+9=81
        82:'B',   # 'B*'
        83:'G',   # 'G*'
        84:'S',   # 'S*'
        85:'N',   # 'N*'
        86:'L',   # 'L*'
        87:'P',   # 'P*'
    }


    # FIXME KK,KP,PP で分けたい
    @staticmethod
    def get_m_index_by_move(
            move,
            is_king):
        """指し手を指定すると、指し手のインデックスを返す。
        ＭＭ関係用。ただしＫＫ関係を除く

        Parameters
        ----------
        move : Move
            指し手
        is_king : bool
            玉の動きか？

        Returns
        -------
            - 指し手のインデックス
        """

        # 移動元マス番号
        try:
            src_sq = Move._src_dst_str_1st_figure_to_sq[move.src_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.src_str[1]]
        except Exception as e:
            raise Exception(f"src_sq error in '{move.as_usi}'.  ('{move.src_str[0]}', '{move.src_str[1]}')  e: {e}")

        # 移動先マス番号
        try:
            dst_sq = Move._src_dst_str_1st_figure_to_sq[move.dst_str[0]] + Move._src_dst_str_2nd_figure_to_index[move.dst_str[1]]
        except Exception as e:
            raise Exception(f"dst_sq error in '{move.as_usi}'.  ('{move.dst_str[0]}', '{move.dst_str[1]}')  e: {e}")

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

        file_size = 9

        return (src_sq * file_size * rank_size * pro_size) + (dst_sq * pro_size) + pro_num




    @staticmethod
    def get_move_number(
            is_king):
        """指し手の数

        Parameters
        ----------
        is_king : bool
            玉の動きか？

        Returns
        -------
        - int
        """

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
            is_king_of_b):
        """逆関数

        指し手２つ分返す

        Parameters
        ----------
        mm_index : int
            指し手 a, b のペアの通しインデックス
        is_king_of_b : bool
            指し手 b は、玉の動きか？
        """

        #
        # 下位の b から
        # ------------
        #

        b_size = EvaluationRuleFacade.get_move_number(
            is_king=is_king_of_b)

        rest = mm_index

        b_index = rest % b_size
        rest //= b_size

        a_index = rest

        try:
            list_of_b_move = EvaluationRuleFacade.get_list_of_move_as_usi_by_m_index(
                    m_index=b_index,
                    is_king=is_king_of_b)
        except Exception as e:
            # 例： list_of_b_move error.  a_index:0  b_index:4680  mm_index:21902400  e:52
            print(f"list_of_b_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  e:{e}")
            raise

        try:
            list_of_a_move = EvaluationRuleFacade.get_list_of_move_as_usi_by_m_index(
                    m_index=a_index,
                    is_king=is_king_of_b)
        except Exception as e:
            # mm_index がでかすぎる？
            # 例： list_of_a_move error.  a_index:4680  b_index:0  e:52
            # 例： list_of_a_move error.  a_index:4680  b_index:0  mm_index:21902400  e:52
            print(f"list_of_a_move error.  a_index:{a_index}  b_index:{b_index}  mm_index:{mm_index}  is_king_of_b:{is_king_of_b}  e:{e}")
            raise

        return [list_of_a_move, list_of_b_move]


    @staticmethod
    def get_list_of_move_as_usi_by_m_index(
            m_index,
            is_king):
        """逆関数

        指し手１つ分。ただし鏡面の場合、共役が付いて２つ返ってくる

        Parameters
        ----------
        m_index : int
            指し手１つ分のインデックス
        is_king : bool
            玉の動きか？
        """

        m_spec = EvaluationMoveSpecification(
            # 玉は成らないから pro を削れる
            is_king=is_king)

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

        # 81 以上は打
        if 81 <= src_value:
            src_file_str = EvaluationRuleFacade._src_num_to_file_str[src_value]
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


    # FIXME KK,KP,PP で分けたい
    @staticmethod
    def get_mm_index_by_2_moves(
            a_move_obj,
            a_is_king,
            b_move_obj,
            b_is_king,
            turn,
            list_of_move_size):
        """指し手２つの組み合わせインデックス"""

        # 同じ指し手を比較したら 0 とする（総当たりの二重ループとかでここを通る）
        if a_move_obj.as_usi == b_move_obj.as_usi:
            return 0

        # 相手番なら、指し手の先後をひっくり返す（将棋盤を１８０°回転させるのと同等）
        # 常に自分の盤から見た状態にする
        if turn == cshogi.WHITE:
            a_move_obj = MoveHelper.flip_turn(a_move_obj)
            b_move_obj = MoveHelper.flip_turn(b_move_obj)

        # FIXME KK,KP,PP で分けたい
        a_index = EvaluationRuleFacade.get_m_index_by_move(
                move=a_move_obj,
                is_king=a_is_king)

        # FIXME KK,KP,PP で分けたい
        b_index = EvaluationRuleFacade.get_m_index_by_move(
                move=b_move_obj,
                is_king=b_is_king)


        # 組み合わせは実装が難しいので、ただの ab 関係とします
        mm_index = a_index * list_of_move_size[1] + b_index
        return mm_index
