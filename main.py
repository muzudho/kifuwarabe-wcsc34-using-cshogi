import cshogi
# import numpy as np
import random

# テストケース

test_case_1 = "position sfen 4r4/4l4/3nlnb2/3kps3/3g1G3/3SPK3/2BNLN3/4L4/4R4 b GS8Pgs8p 1"
"""Ｎｏ．１　駒の取り合い。次の一手は５五銀 S*5e """

test_case_1_1 = "position sfen 4r4/4l4/3nlnb2/3kps3/3g1G3/3SPK3/2BNLN3/4L4/4R4 b GS8Pgs8p 1 moves 4e3e"
"""Ｎｏ．１．１　変形。３五金。posval 35 で局面評価値確認"""

test_case_2 = "position sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B1R5/LNSGKGSNL b - 1"
"""Ｎｏ．２　初手、四間飛車。振り飛車しているかどうかの確認"""

test_case_3 = "position sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B7/LNSGKGSNL b R 1"
"""Ｎｏ．３　平手初期局面から、先手が飛車を駒台に乗せた局面"""

# 📖 [_cshogi.pyx](https://github.com/TadaoYamaoka/cshogi/blob/master/cshogi/_cshogi.pyx)

"""
ターン（Turn；手番）

整数　　意味　　　表記
ーー　　ーーー　　ーーーーーーーーーーー
　０　　先手　　　cshogi.BLACK
　１　　後手　　　cshogi.WHITE
"""

def convert_jsa_to_sq(jsa):
    return (jsa//10-1) * 9 + jsa % 10 - 1

_jsa_to_sq_table = [convert_jsa_to_sq(jsa) for jsa in range(100)]

def jsa_to_sq(jsa):
    """逆関数
    （ｆｌｏｏｒ（ｊｓａ／１０）ー１）＊９＋（ｊｓａ％１０）ー１"""
    return _jsa_to_sq_table[jsa]

"""
リレーショナル・スクウェア（Relational Square；相対升位置）

　　９　　８　　７　　６　　５　　４　　３　　２　　１
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜６４｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜ー８｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー８０｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜５６｜　　｜　　｜　　｜　　｜　　｜　　｜ー７｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー７０｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜４８｜　　｜　　｜　　｜　　｜　　｜ー６｜　　　｜　　　｜　　　｜　　　｜　　　｜ー６０｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜４０｜　　｜　　｜　　｜　　｜ー５｜　　　｜　　　｜　　　｜　　　｜ー５０｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜３２｜　　｜　　｜　　｜ー４｜　　　｜　　　｜　　　｜ー４０｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜２４｜　　｜　　｜ー３｜　　　｜　　　｜ー３０｜　　　｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜１６｜　７｜ー２｜ー１１｜ー２０｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜　８｜ー１｜ー１０｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜７２｜６３｜５４｜４５｜３６｜２７｜１８｜　９｜　★｜　ー９｜ー１８｜ー２７｜ー３６｜ー４５｜ー５４｜ー６３｜ー７２｜　一
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜１０｜　１｜　ー８｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　二
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜２０｜１１｜　２｜　ー７｜ー１６｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　三
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜３０｜　　｜　　｜　３｜　　　｜　　　｜ー２４｜　　　｜　　　｜　　　｜　　　｜　　　｜　四
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜４０｜　　｜　　｜　　｜　４｜　　　｜　　　｜　　　｜ー３２｜　　　｜　　　｜　　　｜　　　｜　五
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜５０｜　　｜　　｜　　｜　　｜　５｜　　　｜　　　｜　　　｜　　　｜ー４０｜　　　｜　　　｜　　　｜　六
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜６０｜　　｜　　｜　　｜　　｜　　｜　６｜　　　｜　　　｜　　　｜　　　｜　　　｜ー４８｜　　　｜　　　｜　七
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜７０｜　　｜　　｜　　｜　　｜　　｜　　｜　７｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー５６｜　　　｜　八
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜８０｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜　８｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー６４｜　九
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋

名前と値
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＮｏｒｔｈＮｏｒｔｈＷｅｓｔ　　７｜　　　　　　　　｜ＮｏｒｔｈＮｏｒｔｈＥａｓｔ　ー１１｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＮｏｒｔｈＷｅｓｔ　　　　　　　８｜Ｎｏｒｔｈ　ー１｜ＮｏｒｔｈＥａｓｔ　　　　　　ー１０｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜Ｗｅｓｔ　　　　　　　　　　　　９｜★　　　　　　　｜Ｅａｓｔ　　　　　　　　　　　　ー９｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＳｏｕｔｈＷｅｓｔ　　　　　　１０｜Ｓｏｕｔｈ　　１｜ＳｏｕｔｈＥａｓｔ　　　　　　　ー８｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＳｏｕｔｈＳｏｕｔｈＷｅｓｔ　１１｜　　　　　　　　｜ＳｏｕｔｈＳｏｕｔｈＥａｓｔ　　ー７｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
"""
north_north_east = -11
north_east = -10
east = -9
south_east = -8
south_south_east = -7
north = -1
south = 1
north_north_west = 7
north_west = 8
west = 9
south_west = 10
south_south_west = 11

"""
ピースタイプ（PieceType, pt；駒種類）

整数　　意味　　　表記
ーー　　ーーー　　ーーーーーーーーーーー
　０　　未使用
　１　　歩　　　　cshogi.PAWN
　２　　香　　　　cshogi.LANCE
　３　　桂　　　　cshogi.KNIGHT
　４　　銀　　　　cshogi.SILVER
　５　　角　　　　cshogi.BISHOP
　６　　飛　　　　cshogi.ROOK
　７　　金　　　　cshogi.GOLD
　８　　玉　　　　cshogi.KING
　９　　と　　　　cshogi.PROM_PAWN
１０　　杏　　　　cshogi.PROM_LANCE
１１　　圭　　　　cshogi.PROM_KNIGHT
１２　　全　　　　cshogi.PROM_SILVER
１３　　馬　　　　cshogi.PROM_BISHOP
１４　　竜　　　　cshogi.PROM_ROOK
"""

_piece_to_string_array = [
    "　　", # ０．　空升
    "＿歩", # １．　piece_type でも使用可能
    "＿香", # ２．
    "＿桂", # ３．
    "＿銀", # ４．
    "＿角", # ５．
    "＿飛", # ６．
    "＿金", # ７．
    "＿玉", # ８．
    "＿と", # ９．
    "＿杏", # １０．
    "＿圭", # １１．
    "＿全", # １２．
    "＿馬", # １３．
    "＿竜", # １４．
    "１５", # １５. 未使用
    "１６", # １６. 未使用
    "ｖ歩", # １７．
    "ｖ香", # １８．
    "ｖ桂", # １９．
    "ｖ銀", # ２０．
    "ｖ角", # ２１．
    "ｖ飛", # ２２．
    "ｖ金", # ２３．
    "ｖ玉", # ２４．
    "ｖと", # ２５．
    "ｖ杏", # ２６．
    "ｖ圭", # ２７．
    "ｖ全", # ２８．
    "ｖ馬", # ２９．
    "ｖ竜", # ３０．
    "３１", # ３１. 未使用
    ]

def piece_to_string(pc):
    """
    ピース（Piece, pc；駒番号）

    　０　空升
    １６　未使用

    　　　　　先手　　　後手
    　　　　ーーー　　ーーー
    　　歩　　　１　　　１７
    　　香　　　２　　　１８
    　　桂　　　３　　　１９
    　　銀　　　４　　　２０
    　　角　　　５　　　２１
    　　飛　　　６　　　２２
    　　金　　　７　　　２３
    　　玉　　　８　　　２４
    　　と　　　９　　　２５
    　　杏　　１０　　　２６
    　　圭　　１１　　　２７
    　　全　　１２　　　２８
    　　馬　　１３　　　２９
    　　竜　　１４　　　３０
    未使用　　１５　　　３１
    """

    if 0 <= pc and pc < 32:
        return _piece_to_string_array[pc]
    else:
        return f'{pc}' # エラー

def piece_type_to_string(pt):
    """ピースタイプ（Piece Type, pt；駒種類）を文字列に変換"""
    if 0 <= pt and pt < 16:
        return _piece_to_string_array[pt]
    else:
        return f'{pt}' # エラー

_number_of_hand_to_string_list = [
    "　　", #  0
    "　１", #  1
    "　２", #  2
    "　３", #  3
    "　４", #  4
    "　５", #  5
    "　６", #  6
    "　７", #  7
    "　８", #  8
    "　９", #  9
    "１０", # 10
    "１１", # 11
    "１２", # 12
    "１３", # 13
    "１４", # 14
    "１５", # 15
    "１６", # 16
    "１７", # 17
    "１８", # 18
]

def number_of_hand_to_string(number):
    """持ち駒の数の表示文字列"""
    return _number_of_hand_to_string_list[number]

_string_to_piece_table = {
    "　　":0, # 空升
    "＿歩":1,
    "＿香":2,
    "＿桂":3,
    "＿銀":4,
    "＿角":5,
    "＿飛":6,
    "＿金":7,
    "＿玉":8,
    "＿と":9,
    "＿杏":10,
    "＿圭":11,
    "＿全":12,
    "＿馬":13,
    "＿竜":14,
    "１５":15, # 未使用
    "１６":16, # 未使用
    "ｖ歩":17,
    "ｖ香":18,
    "ｖ桂":19,
    "ｖ銀":20,
    "ｖ角":21,
    "ｖ飛":22,
    "ｖ金":23,
    "ｖ玉":24,
    "ｖと":25,
    "ｖ杏":26,
    "ｖ圭":27,
    "ｖ全":28,
    "ｖ馬":29,
    "ｖ竜":30,
    "３１":31, # 未使用
}

def string_to_piece(s):
    """逆関数"""
    if 0 <= s and s < 32:
        return _string_to_piece_table[s]
    else:
        return f'{s}' # エラー

"""
定数　　表記　　　　　　　　　　意味
ーー　　ーーーーーーー　　　　　ーーーーー
　 0　　cshogi.NONE 　　　　　例えば空升
　 1　　cshogi.BPAWN　　　　　▲歩
　 2　　cshogi.BLANCE 　　　　▲香
　 3　　cshogi.BKNIGHT　　　　▲桂
　 4　　cshogi.BSILVER　　　　▲銀
　 5　　cshogi.BBISHOP　　　　▲角
　 6　　cshogi.BROOK　　　　　▲飛
　 7　　cshogi.BGOLD　　　　　▲金
　 8　　cshogi.BKING　　　　　▲玉
　 9　　cshogi.BPROM_PAWN　　▲と
　10　　cshogi.BPROM_LANCE 　▲杏
　11　　cshogi.BPROM_KNIGHT　▲圭
　12　　cshogi.BPROM_SILVER　▲全
　13　　cshogi.BPROM_BISHOP　▲馬
　14　　cshogi.BPROM_ROOK　　▲竜
　15　　　　　　　　　　　　　　未使用
　16　　　　　　　　　　　　　　未使用
　17　　cshogi.PPAWN　　　　　▽歩
　18　　cshogi.PLANCE 　　　　▽香
　19　　cshogi.PKNIGHT　　　　▽桂
　20　　cshogi.PSILVER　　　　▽銀
　21　　cshogi.PBISHOP　　　　▽角
　22　　cshogi.PROOK　　　　　▽飛
　23　　cshogi.PGOLD　　　　　▽金
　24　　cshogi.PKING　　　　　▽玉
　25　　cshogi.PPROM_PAWN　　▽と
　26　　cshogi.PPROM_LANCE 　▽杏
　27　　cshogi.PPROM_KNIGHT　▽圭
　28　　cshogi.PPROM_SILVER　▽全
　29　　cshogi.PPROM_BISHOP　▽馬
　30　　cshogi.PPROM_ROOK　　▽竜
　31　　　　　　　　　　　　　　未使用
"""

def non_zero_to_cross(number):
    """非ゼロなら　Ｘ　を表示"""
    if number == 0:
        return "　　"
    else:
        return "　Ｘ"

class Kifuwarabe():
    """きふわらべ"""

    def __init__(self):
        """初期化"""

        self._subordinate = KifuwarabesSubordinate()
        """きふわらべの部下"""

        self._colleague = KifuwarabesColleague(
            kifuwarabes_subordinate=self.subordinate)
        """きふわらべの同僚"""

    @property
    def subordinate(self):
        """きふわらべの部下"""
        return self._subordinate

    @property
    def colleague(self):
        """きふわらべの同僚"""
        return self._colleague

    def usi_loop(self):
        """USIループ"""

        while True:

            cmd = input().split(' ', 1)
            """入力"""

            if cmd[0] == 'usi':
                """USIエンジン握手"""
                print('id name KifuwarabeWCSC34')
                print('usiok', flush=True)

            elif cmd[0] == 'isready':
                """対局準備"""
                print('readyok', flush=True)

            elif cmd[0] == 'position':
                """局面データ解析"""
                pos = cmd[1].split('moves')
                self.position(pos[0].strip(), pos[1].split() if len(pos) > 1 else [])

            elif cmd[0] == 'go':
                """思考開始～最善手返却"""
                (bestmove, beta) = self.colleague.thought.do_it()
                alpha = -beta
                print(f'info depth 1 seldepth 1 time 1 nodes 1 score cp {alpha} string x')
                print(f'bestmove {bestmove}', flush=True)

            elif cmd[0] == 'stop':
                """中断"""
                print('bestmove resign' , flush=True)

            elif cmd[0] == 'quit':
                """終了"""
                break

            # 以下、独自拡張

            elif cmd[0] == 'do':
                """一手指す
                example: ７六歩
                   code: do 7g7f
                """
                self.subordinate.board.push_usi(cmd[1])

            elif cmd[0] == 'undo':
                """一手戻す
                   code: undo
                """
                self.subordinate.board.pop()

            elif cmd[0] == 'ctrltest':
                """利きテスト"""

                if len(cmd)<2:
                    print(f'miss\nexample: ctrltest 51')

                else:
                    sq_jsa = int(cmd[1])
                    sq = convert_jsa_to_sq(sq_jsa)
                    print(f'cmd1: "{cmd[1]}", jsa: {sq_jsa}, sq: {sq}')
                    piece = self.subordinate.board.pieces[sq]

            elif cmd[0] == 'posval':
                """独自拡張。局面評価表示
                example: 着手が４三だったとき
                   code: posval 43
                """

                if len(cmd)<2:
                    print(f'miss\nexample: posval 43')

                else:
                    try:
                        # 手番をひっくり返す（一手指したつもり）
                        self.subordinate.board.push_pass()

                        print('局面評価値内訳：')
                        value_list = 0
                        for index, value in enumerate(value_list):
                            print(f'　　（{index:2}） {value:10}')
                        print(f'　　（計） {sum(value_list):10}')

                        # 手番をひっくり返す（一手指したつもり）
                        self.subordinate.board.pop_pass()

                    except Exception as e:
                        print(f'例外：　{e}')
                        raise e

            elif cmd[0] == 'moveval':
                """１手読みでの指し手の評価値一覧"""

                old_depth = self.colleague.thought.depth
                self.colleague.thought.depth = 1

                for move in self.subordinate.board.legal_moves:
                    self.subordinate.board.push(move)
                    # 一手指す

                    # 局面評価値表示
                    print('局面評価値内訳：')
                    value_list = 0
                    for index, value in enumerate(value_list):
                        print(f'　　（{index:2}） {value:10}')
                    print(f'　　（計） {sum(value_list):10}')

                    self.subordinate.board.pop()
                    # 一手戻す

                self.colleague.thought.depth = old_depth


    def position(self, sfen, usi_moves):
        """局面データ解析"""

        if sfen == 'startpos':
            """平手初期局面に変更"""
            self.subordinate.board.reset()

        elif sfen[:5] == 'sfen ':
            """指定局面に変更"""
            self.subordinate.board.set_sfen(sfen[5:])

        for usi_move in usi_moves:
            """棋譜再生"""
            self.subordinate.board.push_usi(usi_move)

class KifuwarabesSubordinate():
    """きふわらべの部下"""

    def __init__(self):
        """初期化"""

        self._board = cshogi.Board()
        """盤"""

    @property
    def board(self):
        """盤"""
        return self._board


class KifuwarabesColleague():
    """きふわらべの同僚"""

    def __init__(self, kifuwarabes_subordinate):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        """

        self._kifuwarabes_subordinate = kifuwarabes_subordinate
        """きふわらべの部下"""

        self._board_value = BoardValue(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """盤の決まりきった価値"""

        self._thought = Thought(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """思考"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def board_value(self):
        """盤の決まりきった価値"""
        return self._board_value

    @property
    def thought(self):
        """思考"""
        return self._thought


class BoardValue():
    """盤の決まりきった価値"""

    def __init__(self, kifuwarabes_subordinate, kifuwarabes_colleague):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        kifuwarabes_colleague
            きふわらべの同僚
        """

        self._kifuwarabes_subordinate = kifuwarabes_subordinate
        """きふわらべの部下"""

        self._kifuwarabes_colleague = kifuwarabes_colleague
        """きふわらべの同僚"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def kifuwarabes_colleague(self):
        """きふわらべの同僚"""
        return self._kifuwarabes_colleague

    def eval(self):
        """評価"""

        if self.kifuwarabes_subordinate.board.is_game_over():
            # 負け
            return -30000

        if self.kifuwarabes_subordinate.board.is_nyugyoku():
            # 入玉宣言勝ち
            return 30000

        draw = self.kifuwarabes_subordinate.board.is_draw(16)

        if draw == cshogi.REPETITION_DRAW:
            # 千日手
            return 0

        if draw == cshogi.REPETITION_WIN:
            # 千日手で勝ち
            return 30000

        if draw == cshogi.REPETITION_LOSE:
            # 千日手で負け
            return -30000

        if draw == cshogi.REPETITION_SUPERIOR:
            # 千日手の上限？？
            return 30000

        if draw == cshogi.REPETITION_INFERIOR:
            # 千日手の下限？？
            return -30000

        """別途、計算が必要"""
        return None


class Thought():
    """思考。
    主に、そのための設定"""

    def __init__(self, kifuwarabes_subordinate, kifuwarabes_colleague):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        kifuwarabes_colleague
            きふわらべの同僚
        """

        self._kifuwarabes_subordinate = kifuwarabes_subordinate
        """きふわらべの部下"""

        self._kifuwarabes_colleague = kifuwarabes_colleague
        """きふわらべの同僚"""

        self._depth = 3
        """読みの深さ"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def kifuwarabes_colleague(self):
        """きふわらべの同僚"""
        return self._kifuwarabes_colleague

    @property
    def depth(self):
        """読みの深さ"""
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    def do_it(self):
        """それをする"""

        if self.kifuwarabes_subordinate.board.is_game_over():
            """投了局面時"""

            return ('resign', 0)
            """投了"""

        if self.kifuwarabes_subordinate.board.is_nyugyoku():
            """入玉宣言局面時"""

            return ('win', 0)
            """勝利宣言"""

        if not self.kifuwarabes_subordinate.board.is_check():
            """自玉に王手がかかっていない時"""

            if (matemove:=self.kifuwarabes_subordinate.board.mate_move_in_1ply()):
                """あれば、一手詰めの指し手を取得"""

                print('info score mate 1 pv {}'.format(cshogi.move_to_usi(matemove)))
                return (cshogi.move_to_usi(matemove), 0)

        bestmove_list = list(self.kifuwarabes_subordinate.board.legal_moves)
        bestmove = random.choice(bestmove_list)
        """候補手の中からランダムに選ぶ"""

        # 未使用
        alpha = 0

        return (cshogi.move_to_usi(bestmove), alpha)
        """指し手の記法で返却"""


if __name__ == '__main__':
    """コマンドから実行時"""

    kifuwarabe = Kifuwarabe()
    kifuwarabe.usi_loop()
