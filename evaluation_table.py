import random
import datetime

__evaluation_table = [0] * 203_219_280
"""評価値テーブル

    指し手の種類は、 src, dst, pro で構成されるものの他、 resign 等の文字列がいくつかある。
    src は盤上の 81マスと、駒台の７種類の駒。

        (81 + 7)

    dst は盤上の 81マス。

        81

    pro は成りとそれ以外の２種類。

        2

    この数を配列のインデックスにしたときの範囲は、

        (81 + 7) * 81 * 2 = 14256

    この数を２つの組み合わせにすると

        (14256-1) * 14256 = 203_219_280

    ２億超えの組み合わせがある。
"""

# TODO あとで消す。ダミーデータを入れてみる。１分ほどかかる
print(f"[{datetime.datetime.now()}] make eval ...")

for index in range(0, 203_219_280):
    __evaluation_table[index] = random.randint(-1,1)

print(f"[{datetime.datetime.now()}] eval maked")

print(f"[{datetime.datetime.now()}] save ...")

# TODO あとで消す。ファイルに出力してみる
with open('eval.csv', 'w', encoding="utf-8") as f:
    # 配列の要素の整数型を文字列型に変換してカンマで連結
    text = ','.join(map(str,__evaluation_table))
    f.write(text)

print(f"[{datetime.datetime.now()}] saved")



def get_evaluation_table_index_from_move_as_usi(move_as_usi):
    """USIの指し手の符号を、評価値テーブルのインデックスへ変換します

    Parameters
    ----------
    move_as_usi : str
        "7g7f" や "3d3c+"、 "R*5e" のような文字列を想定。 "resign" のような文字列は想定外
    """

    # 移動元
    src_str = move_as_usi[0: 2]

    # 移動先
    dst_str = move_as_usi[2: 4]

    # 移動元
    if src_str == "R*":
        src_num = 81
    elif src_str == "B*":
        src_num = 82
    elif src_str == "G*":
        src_num = 83
    elif src_str == "S*":
        src_num = 84
    elif src_str == "N*":
        src_num = 85
    elif src_str == "L*":
        src_num = 86
    elif src_str == "P*":
        src_num = 87
    else:

        file_str = src_str[0]
        if file_str == "1":
            src_num = 0
        elif file_str == "2":
            src_num = 9
        elif file_str == "3":
            src_num = 18
        elif file_str == "4":
            src_num = 27
        elif file_str == "5":
            src_num = 36
        elif file_str == "6":
            src_num = 45
        elif file_str == "7":
            src_num = 54
        elif file_str == "8":
            src_num = 63
        elif file_str == "9":
            src_num = 72
        else:
            raise Exception(f"src file error: '{file_str}' in '{move_as_usi}'")

        rank_str = src_str[1]
        if rank_str == "a":
            src_num += 0
        elif rank_str == "b":
            src_num += 1
        elif rank_str == "c":
            src_num += 2
        elif rank_str == "d":
            src_num += 3
        elif rank_str == "e":
            src_num += 4
        elif rank_str == "f":
            src_num += 5
        elif rank_str == "g":
            src_num += 6
        elif rank_str == "h":
            src_num += 7
        elif rank_str == "i":
            src_num += 8
        else:
            raise Exception(f"src rank error: '{rank_str}' in '{move_as_usi}'")

    # 移動先
    file_str = dst_str[0]

    if file_str == "1":
        dst_num = 0
    elif file_str == "2":
        dst_num = 9
    elif file_str == "3":
        dst_num = 18
    elif file_str == "4":
        dst_num = 27
    elif file_str == "5":
        dst_num = 36
    elif file_str == "6":
        dst_num = 45
    elif file_str == "7":
        dst_num = 54
    elif file_str == "8":
        dst_num = 63
    elif file_str == "9":
        dst_num = 72
    else:
        raise Exception(f"dst file error: '{file_str}' in '{move_as_usi}'")

    rank_str = dst_str[1]
    if rank_str == "a":
        dst_num += 0
    elif rank_str == "b":
        dst_num += 1
    elif rank_str == "c":
        dst_num += 2
    elif rank_str == "d":
        dst_num += 3
    elif rank_str == "e":
        dst_num += 4
    elif rank_str == "f":
        dst_num += 5
    elif rank_str == "g":
        dst_num += 6
    elif rank_str == "h":
        dst_num += 7
    elif rank_str == "i":
        dst_num += 8
    else:
        raise Exception(f"dst rank error: '{rank_str}' in '{move_as_usi}'")

    # 成りかそれ以外（５文字なら成りだろう）
    if 4 < len(move_as_usi):
        pro_num = 1
    else:
        pro_num = 0

    return (2 * 81 * src_num) + (2 * dst_num) + pro_num


def get_evaluation_value(move_a_as_usi, move_b_as_usi):
    """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

    index_a = get_evaluation_table_index_from_move_as_usi(move_a_as_usi)
    index_b = get_evaluation_table_index_from_move_as_usi(move_b_as_usi)

    move_indexes = [index_a, index_b]
    move_indexes.sort()

    # 昇順
    if index_a <= index_b:
        index = index_a * 14256 + index_b
        #print(f"[DEBUG] 昇順 a:{index_a:3} b:{index_b:3} index:{index}")
        return __evaluation_table[index]

    # 降順
    index = index_b * 14256 + index_a
    #print(f"[DEBUG] 逆順 b:{index_b:3} a:{index_a:3} index:{index}")
    return __evaluation_table[index]
