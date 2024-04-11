class CanditatesMemory():
    """候補に挙がった手は全て覚えておく"""


    @classmethod
    def load_from_file(clazz, file_number):

        # TODO ファイル読込
        return CanditatesMemory()


    def __init__(self):
        self.move_dictionary = {}


    def from_dictionary(self, move_score_dictionary):
        for move_as_usi in move_score_dictionary.keys():
            # 値は一律、１
            self.move_dictionary[move_as_usi] = 1


    def save_canditates_memory(self):
        pass
