from evaluation_table_mm import EvaluationTableMm
from evaluation_rule_k import EvaluationRuleK
from evaluation_rule_p import EvaluationRuleP
from evaluation_rule_kp import EvaluationRuleKp
from evaluation_table_size_facade_kp import EvaluationTableSizeFacadeKp
from move import Move


class EvaluationTableFacadeKp():
    """評価値テーブル　ＫＰ"""


    @staticmethod
    def create_it(
            file_number,
            file_name,
            raw_mm_table,
            is_file_modified):
        """初期化

        Parameters
        ----------
        is_file_modified : bool
            保存されていない評価値テーブルを引数で渡したなら真
        """

        # テーブル・サイズ。計算過程付き
        table_size_obj = EvaluationTableSizeFacadeKp.create_it()

        k_size = EvaluationRuleK.get_king_move_number()
        p_size = EvaluationRuleP.get_piece_move_number()

        return EvaluationTableMm(
                file_number=file_number,
                file_name=file_name,
                table_size_obj=table_size_obj,
                list_of_move_size=[k_size, p_size],
                raw_mm_table=raw_mm_table,
                is_king_size_of_a=True,
                is_king_size_of_b=False,
                is_file_modified=is_file_modified)


    @staticmethod
    def get_kp_policy(
            self,
            k_obj,
            p_obj,
            turn):
        """両方残すなら 0点、インデックスが小さい方を残すなら -1点、インデックスが大きい方を残すなら +1点"""

        kp_index = EvaluationRuleKp.get_kp_index_by_2_moves(
                k_obj=k_obj,
                p_obj=p_obj,
                turn=turn)
        #print(f"[DEBUG] 逆順 b:{index_b:3} a:{index_a:3} kl_index:{kl_index}", flush=True)

        try:
            # 古いデータには 2 が入っているので、 2 は　1 に変換する
            if self._raw_mm_table[kp_index] == 2:
                self._raw_mm_table[kp_index] = 1

        except IndexError as e:
            # FIXME 大量に発生している。
            #pass

            ## 例： table length: 70955352  kl_index: 102593390  except: list index out of range
            ## 例： table length:64  kl_index:63456  k_obj.as_usi:5i4h  p_obj.as_usi:5a4b  turn:0  except: list index out of range
            ## 例： table length:419904  kl_index:4668914  k_obj.as_usi:5i4h  p_obj.as_usi:5a5b  turn:0  except: list index out of range
            ## 例： table length:419904  kl_index:2334457  k_obj:5i4h  p_obj:5a5b  turn:0  except: list index out of range
            print(f"table length:{len(self._raw_mm_table)}  kp_index:{kp_index}  k_obj:{k_obj.as_usi}  p_obj:{p_obj.as_usi}  turn:{turn}  except: {e}")
            raise

        try:
            policy = self._raw_mm_table[kp_index]
        except IndexError as e:
            # FIXME 大量に発生している。
            policy = 0

        return policy


    @staticmethod
    def make_move_as_usi_and_policy_dictionary_2(
            kp_table_obj,
            k_move_collection_as_usi,
            p_move_collection_as_usi,
            turn):
        """指し手に評価値を付ける

        Parameters
        ----------
        a_move_set_as_usi : set
            指し手の収集（主体）
        b_move_set_as_usi : set
            指し手の収集（客体）
        turn
            手番
        """

        # 指し手に評価値を付ける
        move_as_usi_and_policy_dictionary = {}

        # 主体
        for k_as_usi in k_move_collection_as_usi:
            k_obj = Move.from_usi(k_as_usi)
            sum_policy = 0

            # 客体と総当たり
            for p_as_usi in p_move_collection_as_usi:
                p_obj = Move.from_usi(p_as_usi)
                sum_policy += EvaluationRuleKp.get_kp_policy(
                        kp_table_obj=kp_table_obj,
                        k_obj=k_obj,
                        p_obj=p_obj,
                        turn=turn)

            move_as_usi_and_policy_dictionary[k_as_usi] = sum_policy

        return move_as_usi_and_policy_dictionary
