import os
from learn_candidates_move import LearnCandidatesMove
from learn_candidates_load import LearnCandidatesLoad


class LearnCandidatesPieces(LearnCandidatesMove):


    def __init__(
            self,
            file_number):
        """初期化"""
        LearnCandidatesMove.__init__(self)
        self._file_name = f'n{file_number}_canditates_pieces.txt'


    @staticmethod
    def from_file(
            file_number):
        """読込"""
        candidates_pieces = LearnCandidatesPieces(file_number)

        # 新称のファイルが存在するとき
        if os.path.isfile(candidates_pieces.file_name):
            candidates_pieces._move_set = LearnCandidatesLoad.read_file(candidates_pieces.file_name)

            ## （読込直後の）中身の確認
            #for move in candidates_memory._move_set:
            #    print(f"[{datetime.datetime.now()}] (loaded) move:{move}", flush=True)

            return candidates_pieces

        return candidates_pieces
