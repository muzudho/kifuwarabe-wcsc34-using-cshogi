import datetime
from evaluation_configuration import EvaluationConfiguration
from move import Move


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

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] update {file_name} file ...", flush=True)

        new_mm_table = [0] * EvaluationConfiguration.get_table_size(
                is_king_of_a=is_king_of_a,      # V4 は未対応
                is_king_of_b=is_king_of_b,      # V4 は未対応
                is_symmetrical_connected=False) # V4 は fully connected

        try:

            # 指し手 a, b のペアのインデックス
            mm_index = 0

            with open(file_name, 'rb') as f:

                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)

                    #
                    # V2 ---> V3 で、インデックスがずれる
                    #
                    two_powers = [128, 64, 32, 16, 8, 4, 2, 1]
                    for two_power in two_powers:

                        # ビットフィールドを全て使わず、途中で切れるケース
                        if EvaluationConfiguration.get_table_size(
                                is_king_of_a=is_king_of_a,
                                is_king_of_b=is_king_of_b,
                                is_symmetrical_connected=False) <= mm_index:
                            break

                        pair_of_list_of_move_as_usi = EvaluationConfiguration.get_pair_of_list_of_move_as_usi_by_mm_index(
                                mm_index=mm_index,
                                is_symmetrical_connected=False)

                        # 共役の指し手は付いていないはず
                        list_of_a_as_usi, list_of_b_as_usi = pair_of_list_of_move_as_usi

                        # 新しいテーブルでのインデックス
                        ab_new_index = EvaluationConfiguration.get_m_index_by_move(
                                move=Move(ab_as_usi),
                                is_king=is_king,
                                is_symmetrical_connected=False)

                        try:
                            bit = one_byte//two_power % 2
                            new_mm_table[ab_new_index] = bit

                        except IndexError as e:
                            print(f"table length:{len(new_mm_table)}  mm_index:{mm_index}  ab_new_index:{ab_new_index}  except:{e}")
                            raise

                        mm_index+=1

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] (v3 to v4) '{file_name}' file updated. evaluation table size: {len(new_mm_table)}", flush=True)

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

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] update {file_name} file ...", flush=True)

        evaluation_mm_table = [0] * EvaluationConfiguration.get_table_size(
                is_king_of_a=False,     # V2 は未対応
                is_king_of_b=False,     # V2 は未対応
                is_symmetrical_connected=True) # V2 は symmetrical connected

        try:

            # 指し手 a, b のペアのインデックス
            mm_index = 0

            with open(file_name, 'rb') as f:

                multiple_bytes = f.read(1)

                while multiple_bytes:
                    one_byte = int.from_bytes(multiple_bytes, signed=False)

                    #
                    # V2 ---> V3 で、インデックスがずれる
                    #
                    two_powers = [128, 64, 32, 16, 8, 4, 2, 1]
                    for two_power in two_powers:

                        # ビットフィールドを全て使わず、途中で切れるケース
                        if EvaluationConfiguration.get_table_size(
                                is_king_of_a=False,             # V3 は未対応
                                is_king_of_b=False,             # V3 は未対応
                                is_symmetrical_connected=False  # V3 は fully connected
                                ) <= mm_index:
                            break

                        pair_of_list_of_move_as_usi = EvaluationConfiguration.get_pair_of_list_of_move_as_usi_by_mm_index(
                                mm_index=mm_index,
                                # 左右対称の盤
                                is_symmetrical_connected=True)

                        # 共役の指し手も付いているケースがある
                        for list_of_move_as_usi in pair_of_list_of_move_as_usi:
                            for move_as_usi in list_of_move_as_usi:
                                converted_m_index = EvaluationConfiguration.get_m_index_by_move(
                                        move=Move(move_as_usi),
                                        is_king=False,  # 旧仕様では玉の区別なし
                                        # 左右が異なる盤
                                        is_symmetrical_connected=False)

                                try:
                                    bit = one_byte//two_power % 2
                                    evaluation_mm_table[converted_m_index] = bit

                                except IndexError as e:
                                    print(f"table length:{len(evaluation_mm_table)}  mm_index:{mm_index}  converted_m_index:{converted_m_index}  except:{e}")
                                    raise


                        mm_index+=1

                    multiple_bytes = f.read(1)

            print(f"[{datetime.datetime.now()}] (v2 to v3) '{file_name}' file updated. evaluation table size: {len(evaluation_mm_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return evaluation_mm_table
