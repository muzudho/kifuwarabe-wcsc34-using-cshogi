import cshogi
import datetime
from evaluation_configuration import EvaluationConfiguration
from move import Move
from display_helper import DisplayHelper
from evaluation_table_size import EvaluationTableSize
from evaluation_rule_mm import EvaluationRuleMm


class EvaluationFileVersionUp():


    @staticmethod
    def read_evaluation_v3_file_and_convert_to_v4(
            is_king_of_a,
            is_king_of_b,
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
                is_king_of_a=is_king_of_a,          # V4 は未対応
                is_king_of_b=is_king_of_b,          # V4 は未対応
                is_symmetrical_half_board=False)     # V4 は fully connected
        new_table_size = new_table_size_obj.combination

        list_of_move_size = [
            EvaluationConfiguration.get_move_number(
                is_king=is_king_of_a,
                is_symmetrical_half_board=False),
            EvaluationConfiguration.get_move_number(
                is_king=is_king_of_b,
                is_symmetrical_half_board=False)]

        # ２の累乗、１バイト分
        two_powers = [128, 64, 32, 16, 8, 4, 2, 1]

        # サイズに応じて時間のかかる処理
        #
        new_table_size_with_underscore = DisplayHelper.with_underscore(new_table_size)
        a_size_with_underscore = list_of_move_size[0]
        b_size_with_underscore = list_of_move_size[1]
        print(f"[{datetime.datetime.now()}] (v3 to v4) update {file_name} file initialize ... new_table_size_obj:({new_table_size_obj.to_debug_str()})  (a_size:{a_size_with_underscore}, b_size:{b_size_with_underscore})", flush=True)

        new_mm_table = [0] * new_table_size

        print(f"[{datetime.datetime.now()}] (v3 to v4) updating {file_name} file open ...", flush=True)

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
                    # V2 ---> V3 で、インデックスがずれる
                    #
                    for two_power in two_powers:

                        # ビットフィールドを全て使わず、途中で切れるケース
                        if new_table_size <= old_mm_index:
                            print(f"new_table_size:{new_table_size_with_underscore} < old_mm_index:{old_mm_index_with_underscore} break", flush=True)
                            is_finish = True
                            break

                        pair_of_list_of_move_as_usi = EvaluationConfiguration.get_pair_of_list_of_move_as_usi_by_mm_index(
                                mm_index=old_mm_index,
                                is_king_of_b=is_king_of_b,
                                is_symmetrical_half_board=False)

                        list_of_a_as_usi, list_of_b_as_usi = pair_of_list_of_move_as_usi

                        # 共役の指し手は付いていないはず
                        a_as_usi = list_of_a_as_usi[0]
                        b_as_usi = list_of_b_as_usi[0]
                        #print(f"old_mm_index:{old_mm_index_with_underscore}  a_as_usi:{a_as_usi}  b_as_usi:{b_as_usi}", flush=True)

                        a_obj = Move.from_usi(a_as_usi)
                        b_obj = Move.from_usi(b_as_usi)

                        # 新しいテーブルでのインデックス
                        new_mm_index = EvaluationConfiguration.get_mm_index_by_2_moves(
                                a_move_obj=a_obj,
                                a_is_king=is_king_of_a,
                                b_move_obj=b_obj,
                                b_is_king=is_king_of_b,
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


    @staticmethod
    def read_evaluation_v2_file_and_convert_to_v3(
            file_name):
        """バイナリ・ファイル V2 を読込み、V3 にバージョンアップして使う
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
                is_king_of_a=False,             # V3 は未対応
                is_king_of_b=False,             # V3 は未対応
                is_symmetrical_half_board=False) # V3 は fully connected
        new_table_size = new_table_size_obj.combination

        # ２の累乗、１バイト分
        two_powers = [128, 64, 32, 16, 8, 4, 2, 1]

        # サイズに応じて時間のかかる処理
        #
        new_table_size_with_underscore = DisplayHelper.with_underscore(new_table_size)
        print(f"[{datetime.datetime.now()}] (v2 to v3) update {file_name} file ... new_table_size_obj:({new_table_size_obj.to_debug_str()})", flush=True)

        evaluation_mm_table = [0] * new_table_size

        print(f"[{datetime.datetime.now()}] (v2 to v3) updating {file_name} file open ...", flush=True)

        try:

            # 指し手 a, b のペアのインデックス
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
                    # V2 ---> V3 で、インデックスがずれる
                    #
                    for two_power in two_powers:

                        # ビットフィールドを全て使わず、途中で切れるケース
                        if new_table_size <= old_mm_index:
                            is_finish = True
                            break

                        pair_of_list_of_move_as_usi = EvaluationConfiguration.get_pair_of_list_of_move_as_usi_by_mm_index(
                                mm_index=old_mm_index,
                                is_king_of_b=False,             # V3 は未対応
                                # 左右対称の盤
                                is_symmetrical_half_board=True)

                        # 共役の指し手も付いているケースがある
                        for list_of_move_as_usi in pair_of_list_of_move_as_usi:
                            for move_as_usi in list_of_move_as_usi:
                                converted_m_index = EvaluationRuleMm.get_m_index_by_move(
                                        move=Move.from_usi(move_as_usi),
                                        is_king=False,                  # 旧仕様では玉の区別なし
                                        is_symmetrical_half_board=True)  # V2 では、左右が異なる盤

                                try:
                                    bit = one_byte_num//two_power % 2
                                    evaluation_mm_table[converted_m_index] = bit

                                except IndexError as e:
                                    print(f"table length:{new_table_size_with_underscore}  old_mm_index:{old_mm_index_with_underscore}  converted_m_index:{converted_m_index}  except:{e}")
                                    raise


                        old_mm_index+=1

                    if is_finish:
                        break

                    one_byte_binary = f.read(1)

            print(f"[{datetime.datetime.now()}] (v2 to v3) '{file_name}' file updated. evaluation table size: {new_table_size_with_underscore}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_mm_table
