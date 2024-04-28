import cshogi
import datetime
from move import Move
from display_helper import DisplayHelper
from evaluation_table_size import EvaluationTableSize
from evaluation_rule_mm import EvaluationRuleMm


class EvaluationVersionUpKk():


    @staticmethod
    def update_v4_to_v5(
            file_name):
        """バイナリ・ファイル V3 を読込み、V4 にバージョンアップして使う
        ファイルの存在チェックを済ませておくこと

        Parameters
        ----------
        file_name : str
            ファイル名

        Returns
        -------
        - mm_table
        """

        is_finish = False

        new_table_size_obj = EvaluationTableSize(
                is_king_of_a=True,                  # KK なんで
                is_king_of_b=True,                  # KK なんで
                is_symmetrical_half_board=False)    # fully connected
        new_table_size = new_table_size_obj.combination

        list_of_move_size = [
            EvaluationRuleMm.get_move_number(
                is_king=True,
                is_symmetrical_half_board=False),
            EvaluationRuleMm.get_move_number(
                is_king=True,
                is_symmetrical_half_board=False)]

        # ２の累乗、１バイト分
        two_powers = [128, 64, 32, 16, 8, 4, 2, 1]

        # サイズに応じて時間のかかる処理
        #
        new_table_size_with_underscore = DisplayHelper.with_underscore(new_table_size)
        a_size_with_underscore = list_of_move_size[0]
        b_size_with_underscore = list_of_move_size[1]
        print(f"[{datetime.datetime.now()}] KK (v4 to v5) update {file_name} file initialize ... new_table_size_obj:({new_table_size_obj.to_debug_str()})  (a_size:{a_size_with_underscore}, b_size:{b_size_with_underscore})", flush=True)

        new_mm_table = [0] * new_table_size

        print(f"[{datetime.datetime.now()}] KK (v4 to v5) updating {file_name} file open ...", flush=True)

        try:

            # 旧テーブルでの、指し手 a, b のペアのインデックス
            old_mm_index = 0

            with open(file_name, 'rb') as f:


                one_byte_binary = f.read(1)

                while one_byte_binary:

                    # プログレス表示
                    if old_mm_index % 10 == 0:
                        old_mm_index_with_underscore = DisplayHelper.with_underscore(old_mm_index)

                        if old_mm_index == 10:
                            print(f"[{datetime.datetime.now()}] old_mm_index:{old_mm_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_mm_index == 100:
                            print(f"[{datetime.datetime.now()}] old_mm_index:{old_mm_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_mm_index == 1_000:
                            print(f"[{datetime.datetime.now()}] old_mm_index:{old_mm_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_mm_index == 10_000:
                            print(f"[{datetime.datetime.now()}] old_mm_index:{old_mm_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_mm_index == 100_000:
                            print(f"[{datetime.datetime.now()}] old_mm_index:{old_mm_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_mm_index == 1_000_000:
                            print(f"[{datetime.datetime.now()}] old_mm_index:{old_mm_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                            print(f"[{datetime.datetime.now()}] データが巨大で終わらないので、打ち切ります", flush=True)
                            break

                    one_byte_num = int.from_bytes(one_byte_binary, signed=False)
                    #print(f"old_mm_index:{old_mm_index_with_underscore}  one_byte_num:{one_byte_num}", flush=True)

                    #
                    # V4 ---> V5 で、インデックスがずれる
                    #
                    for two_power in two_powers:

                        # ビットフィールドを全て使わず、途中で切れるケース
                        if new_table_size <= old_mm_index:
                            print(f"new_table_size:{new_table_size_with_underscore} < old_mm_index:{old_mm_index_with_underscore} break", flush=True)
                            is_finish = True
                            break

                        pair_of_list_of_move_as_usi = EvaluationRuleMm.get_pair_of_list_of_move_as_usi_by_mm_index(
                                mm_index=old_mm_index,
                                is_king_of_b=True,
                                is_symmetrical_half_board=False)

                        list_of_a_as_usi, list_of_b_as_usi = pair_of_list_of_move_as_usi

                        # 共役の指し手は付いていないはず
                        a_as_usi = list_of_a_as_usi[0]
                        b_as_usi = list_of_b_as_usi[0]
                        #print(f"old_mm_index:{old_mm_index_with_underscore}  a_as_usi:{a_as_usi}  b_as_usi:{b_as_usi}", flush=True)

                        a_obj = Move.from_usi(a_as_usi)
                        b_obj = Move.from_usi(b_as_usi)

                        # 新しいテーブルでのインデックス
                        new_mm_index = EvaluationRuleMm.get_mm_index_by_2_moves(
                                a_move_obj=a_obj,
                                a_is_king=True,
                                b_move_obj=b_obj,
                                b_is_king=True,
                                turn=cshogi.BLACK,  # FIXME 全部、先手視点？
                                list_of_move_size=list_of_move_size,
                                is_symmetrical_half_board=False)
                        #print(f"old_mm_index:{old_mm_index_with_underscore}  new_mm_index:{new_mm_index}", flush=True)

                        try:
                            bit = one_byte_num//two_power % 2
                            #print(f"old_mm_index:{old_mm_index_with_underscore}  bit:{bit}", flush=True)

                            new_mm_table[new_mm_index] = bit

                        except IndexError as e:
                            print(f"old_mm_index:{old_mm_index_with_underscore}  table length:{new_table_size_with_underscore}  new_mm_index:{new_mm_index}  except:{e}")
                            raise

                        old_mm_index+=1
                        #print(f"old_mm_index:{old_mm_index_with_underscore}  incremented", flush=True)

                    if is_finish:
                        break

                    one_byte_binary = f.read(1)

            print(f"[{datetime.datetime.now()}] (v3 to v4) '{file_name}' file updated. evaluation table size: {new_table_size_with_underscore}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return new_mm_table
