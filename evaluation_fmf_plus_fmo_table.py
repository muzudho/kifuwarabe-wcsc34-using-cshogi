import cshogi
import os
import random
import datetime
from evaluation_ee_table import EvaluationEeTable
from move import Move


class EvaluationFmfPlusFmoTable(EvaluationEeTable):
    """評価値ＦｍＦ＋ＦｍＯテーブル

    合法手（つまり利き）を E （Effect）と呼ぶとし、

    現局面（自分の手番）の合法手を E1、
    E1 を指したときの局目（相手の手番）の合法手を E2 とする

    Eは e1, e2, ... en の集合とし、
    評価値テーブルは
    e1 e1
    e1 e2
    e1 e3
    ...
    en en
    の形を取る。これを EE と呼ぶとする

    さらに自軍を F（Friend）、相手を O（Opponent） と呼ぶとし、
    玉の合法手を K（King）、玉以外の合法手を M (Minions) と呼ぶとする。
    Fk（自玉の合法手）と F（自分の合法手）の関係を FkF、
    Fm（自軍の玉以外の合法手）と F（自分の合法手）の関係を FmF、
    Fk（自玉の合法手）と O（相手の合法手）の関係を FkO、
    Fm（自軍の玉以外の合法手）と O（相手の合法手）の関係を FmO、
    と呼ぶとき、

    このテーブルを使って FmF + FmO の評価値を返す
    """

    def __init__(
            self,
            file_number):
        """評価値EEテーブル

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

                (14256 - 1) * 14256 = 203_219_280

            ２億超えの組み合わせがある。

            ----------

            しかし、家のＰＣでこのサイズの配列を２つ読み込んで対局させることはできないようだ。
            左右対称と仮定して、９筋ではなく、５筋にする。

                (5 * 9 + 7) * 81 * 2 = 8424
                (8424 - 1) * 8424 = 70_955_352

            ----------

            値は、 -1,0,1 を入れる代わりに、+1 して 0,1,2 を入れてある。保存時にマイナスの符号で１文字使うのを省くため

            ----------

            TODO 駒は任意の点ＡからＢへ移動できるわけではないので、本来はもっと圧縮できるはず

            (2024-04-12 fri) 敵の指し手も利用するように変更

            ----------

        """

        evaluation_kind = "fmf_fmo"

        EvaluationEeTable.__init__(
                self,
                file_number=file_number,
                evaluation_kind=evaluation_kind,
                file_name=f'n{file_number}_eval_{evaluation_kind}.txt',            # 旧
                bin_file_name=f'n{file_number}_eval_{evaluation_kind}.bin',        # 旧
                bin_v2_file_name=f'n{file_number}_eval_{evaluation_kind}_v2.bin',  # 新
                move_size=8424,
                table_size = 70_955_352)
