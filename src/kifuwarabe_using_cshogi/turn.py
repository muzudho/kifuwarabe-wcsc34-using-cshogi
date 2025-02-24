import cshogi


class Turn():
    """手番"""


    _turn_string = {
        cshogi.BLACK: 'black',
        cshogi.WHITE: 'white',
    }


    @classmethod
    def to_string(clazz, my_turn):
        return clazz._turn_string[my_turn]
