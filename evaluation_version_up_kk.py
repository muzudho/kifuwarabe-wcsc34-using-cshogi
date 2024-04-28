import cshogi
import datetime
from move import Move
from display_helper import DisplayHelper
from evaluation_table_size import EvaluationTableSize
from evaluation_rule_kk import EvaluationRuleKk
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
            EvaluationRuleKk.get_move_number(
                is_king=True,
                is_symmetrical_half_board=False),
            EvaluationRuleKk.get_move_number(
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

        new_kl_table = [0] * new_table_size

        print(f"[{datetime.datetime.now()}] KK (v4 to v5) updating {file_name} file open ...", flush=True)

        try:

            # 旧テーブルでの、指し手 a, b のペアのインデックス
            old_kl_index = 0

            with open(file_name, 'rb') as f:


                one_byte_binary = f.read(1)

                while one_byte_binary:

                    # プログレス表示
                    if old_kl_index % 10 == 0:
                        old_kl_index_with_underscore = DisplayHelper.with_underscore(old_kl_index)

                        if old_kl_index == 10:
                            print(f"[{datetime.datetime.now()}] old_kl_index:{old_kl_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_kl_index == 100:
                            print(f"[{datetime.datetime.now()}] old_kl_index:{old_kl_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_kl_index == 1_000:
                            print(f"[{datetime.datetime.now()}] old_kl_index:{old_kl_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_kl_index == 10_000:
                            print(f"[{datetime.datetime.now()}] old_kl_index:{old_kl_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_kl_index == 100_000:
                            print(f"[{datetime.datetime.now()}] old_kl_index:{old_kl_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                        elif old_kl_index == 1_000_000:
                            print(f"[{datetime.datetime.now()}] old_kl_index:{old_kl_index_with_underscore} / {new_table_size_with_underscore}", flush=True)
                            print(f"[{datetime.datetime.now()}] データが巨大で終わらないので、打ち切ります", flush=True)
                            break

                    one_byte_num = int.from_bytes(one_byte_binary, signed=False)
                    #print(f"old_kl_index:{old_kl_index_with_underscore}  one_byte_num:{one_byte_num}", flush=True)

                    #
                    # V4 ---> V5 で、インデックスがずれる
                    #
                    for two_power in two_powers:

                        # ビットフィールドを全て使わず、途中で切れるケース
                        if new_table_size <= old_kl_index:
                            print(f"new_table_size:{new_table_size_with_underscore} < old_kl_index:{old_kl_index_with_underscore} break", flush=True)
                            is_finish = True
                            break

                        # 指し手 k, l を取得
                        k_obj, l_obj = EvaluationRuleKk.get_move_by_index(
                                kl_index=old_kl_index)

                        # 新しいテーブルでのインデックス
                        new_mm_index = EvaluationRuleKk.get_kl_index_by_2_moves(
                                k_obj=k_obj,
                                l_obj=l_obj,
                                turn=cshogi.BLACK)  # FIXME 全部、先手視点？

                        try:
                            bit = one_byte_num//two_power % 2

                            new_kl_table[new_mm_index] = bit

                        except IndexError as e:
                            print(f"old_kl_index:{old_kl_index_with_underscore}  table length:{new_table_size_with_underscore}  new_mm_index:{new_mm_index}  except:{e}")
                            raise

                        old_kl_index+=1

                    if is_finish:
                        break

                    one_byte_binary = f.read(1)

            print(f"[{datetime.datetime.now()}] (v3 to v4) '{file_name}' file updated. evaluation table size: {new_table_size_with_underscore}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return new_kl_table
