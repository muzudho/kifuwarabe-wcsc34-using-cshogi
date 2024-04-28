import os
from learn_candidates_move import LearnCandidatesMove
from learn_candidates_load import LearnCandidatesLoad


class LearnCandidatesKing(LearnCandidatesMove):


    def __init__(
            self,
            file_number):
        """初期化"""
        LearnCandidatesMove.__init__(self)
        self._file_name = f'n{file_number}_canditates_king.txt'


    @staticmethod
    def load_from_file(
            file_number):
        """読込"""
        candidates_king = LearnCandidatesKing(file_number)

        # 新称のファイルが存在するとき
        if os.path.isfile(candidates_king.file_name):
            candidates_king._move_set = LearnCandidatesLoad.read_file(candidates_king.file_name)

            ## （読込直後の）中身の確認
            #for move in candidates_memory._move_set:
            #    print(f"[{datetime.datetime.now()}] (loaded) move:{move}", flush=True)

            return candidates_king

        return candidates_king
