
class KoMemory():
    """囲碁のコウ。
    左右に往復するような、単純な千日手を避けるために、自分の２つ前の手は指せない、という制限

    FIXME go にしか対応していない。 do や undo にも対応するか？
    """

    def __init__(self):
        """初期化"""
        self._move_list = ["", ""]

    def enqueue(self, move_as_usi):
        """指した手を追加"""
        self._move_list.append(move_as_usi)
        self._move_list.pop(0)

    def get_head(self):
        """コウを取得"""
        return self._move_list[0]
