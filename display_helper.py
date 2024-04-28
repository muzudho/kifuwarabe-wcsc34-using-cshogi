class DisplayHelper():


    @staticmethod
    def with_underscore(number):
        """数を、アンダースコア区切りの文字列に変換します

        'abc' ３文字なら 'abc' アンダースコア要らない
        'abcd' ４文字なら 'a_bcd' ２文字目にアンダースコアを追加
        'abcde' ５文字なら 'ab_cde' ３文字目にアンダースコアを追加
        'abcdef' ６文字なら 'abc_def' ４文字目にアンダースコアを追加
        'abcdefg' ７文字なら 'a_bcd_efg' ２文字目にアンダースコアを追加
        'abcdefgh' ８文字なら 'ab_cde_fgh' ３文字目にアンダースコアを追加
         ４文字以降、２、３、４でループしてそうだ
        """

        text = str(number)
        text_len = len(text)
        #print(f"text:'{text}'  len(text):{len(text)}")

        # １文字ずつに分解
        characters = list(text)


        #print(f"characters len:{len(characters)}")
        new_text = []

        # 4文字未満なら区切り要らない
        if text_len < 4:
            return text

        # アンダースコア挿入の次位置を指すカウンター target を用意する
        target = (text_len - 4) % 3 + 1

        # ループカウンタ―
        i = 0
        for char in characters:

            # アンダースコア挿入位置に来たら
            if i == target:
                new_text.append("_")
                target += 3

            new_text.append(char)
            i += 1

        return ''.join(new_text)


if __name__ == '__main__':
    """コマンドから実行時"""

    for i in [1, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000, 1_000_000_000_000]:
        print(f"{i} --> {DisplayHelper.with_underscore(i)}")
