import datetime


class EvaluationLoad():


    @staticmethod
    def read_evaluation_file(
            file_name):
        """バイナリ・ファイル V2, V3 を読込む
        ファイルの存在チェックを済ませておくこと"""

        # ロードする。１分ほどかかる
        print(f"[{datetime.datetime.now()}] read {file_name} file ...", flush=True)

        raw_mm_table = []

        try:

            with open(file_name, 'rb') as f:

                one_byte_binary = f.read(1)

                while one_byte_binary:
                    one_byte_num = int.from_bytes(one_byte_binary, signed=False)

                    raw_mm_table.append(one_byte_num//128 % 2)
                    raw_mm_table.append(one_byte_num// 64 % 2)
                    raw_mm_table.append(one_byte_num// 32 % 2)
                    raw_mm_table.append(one_byte_num// 16 % 2)
                    raw_mm_table.append(one_byte_num//  8 % 2)
                    raw_mm_table.append(one_byte_num//  4 % 2)
                    raw_mm_table.append(one_byte_num//  2 % 2)
                    raw_mm_table.append(one_byte_num//      2)

                    one_byte_binary = f.read(1)

            print(f"[{datetime.datetime.now()}] (v2,v3) '{file_name}' file loaded. evaluation table size: {len(raw_mm_table)}", flush=True)

        except FileNotFoundError as ex:
            print(f"[evaluation table / load from file] [{file_name}] file error. {ex}")
            raise

        return raw_mm_table
