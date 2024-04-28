import os
import datetime


class CandidatesMemory():
    """候補に挙がった手は全て覚えておく

    勝ったら、全部忘れる
    """


    def save(self):
        """保存"""
        print(f"[{datetime.datetime.now()}] save '{self.file_name}' file ...", flush=True)

        # ファイルに出力する
        with open(self.file_name, 'w', encoding="utf-8") as f:
            # 配列の要素の整数型を文字列型に変換して空白区切りで連結
            text = ' '.join(map(str,self._move_set))
            print(f"[{datetime.datetime.now()}] text created ...", flush=True)

            f.write(text)

        self._is_file_modified = False

        print(f"[{datetime.datetime.now()}] '{self.file_name}' file saved", flush=True)


    def union_dictionary(self, move_score_dictionary):
        """和集合"""
        before_size = len(self._move_set)
        print(f"[{datetime.datetime.now()}] (before size:{before_size}) merge candidates moves...", flush=True)

        ## （変更前の）中身の確認
        #for move in self._move_set:
        #    print(f"[{datetime.datetime.now()}] (before) move:{move}", flush=True)

        ## 中身の確認
        #for move in move_score_dictionary.keys():
        #    print(f"[{datetime.datetime.now()}] (input) move:{move}", flush=True)

        # 和集合
        self._move_set = self._move_set.union(move_score_dictionary)
        after_size = len(self._move_set)

        # 変わってないかも知らんけど
        self._is_file_modified = before_size != after_size

        print(f"[{datetime.datetime.now()}] (after size:{after_size}) candidates moves merged", flush=True)

        ## 中身の確認
        #for move in self._move_set:
        #    print(f"[{datetime.datetime.now()}] (after) move:{move}", flush=True)


    def union_set(self, move_set):
        """和集合"""
        before_size = len(self._move_set)
        print(f"[{datetime.datetime.now()}] (before size:{before_size}) merge candidates moves...", flush=True)

        ## （変更前の）中身の確認
        #for move in self._move_set:
        #    print(f"[{datetime.datetime.now()}] (before) move:{move}", flush=True)

        ## 中身の確認
        #for move in move_score_dictionary.keys():
        #    print(f"[{datetime.datetime.now()}] (input) move:{move}", flush=True)

        # 和集合
        self._move_set = self._move_set.union(move_set)
        after_size = len(self._move_set)

        # 変わってないかも知らんけど
        self._is_file_modified = before_size != after_size

        print(f"[{datetime.datetime.now()}] (after size:{after_size}) candidates moves merged", flush=True)

        ## 中身の確認
        #for move in self._move_set:
        #    print(f"[{datetime.datetime.now()}] (after) move:{move}", flush=True)
