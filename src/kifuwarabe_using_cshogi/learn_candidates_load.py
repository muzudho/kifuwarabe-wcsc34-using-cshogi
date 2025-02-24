import datetime


class LearnCandidatesLoad():


    @staticmethod
    def read_file(file_name):
        """ファイルを読み込んで、集合を返します"""
        print(f"[{datetime.datetime.now()}] read {file_name} file ...", flush=True)

        try:
            with open(file_name, 'r', encoding="utf-8") as f:
                text = f.read().strip()

        except FileNotFoundError as ex:
            print(f"[canditates memory / load from file] [{file_name}] file error. {ex}")
            raise

        print(f"[{datetime.datetime.now()}] {file_name} read", flush=True)

        if text != "":
            return set(text.split(' '))

        return set()
