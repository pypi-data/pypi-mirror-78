import time
import unittest

import yotsuba


class NormalizeTests(unittest.TestCase):

    def test_rust(self):
        start: float = time.time()
        self.assertEqual(
            yotsuba.ja.normalize_neologd("０１２３４５６７８９"),
            "0123456789"
        )
        self.assertEqual(yotsuba.ja.normalize_neologd(
            "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.assertEqual(
            yotsuba.ja.normalize_neologd("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"),
            "abcdefghijklmnopqrstuvwxyz"
        )
        # self.assertEqual(yotsuba.normalize_neologd(
        #     "！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝"),
        #     "!\"#$%&'()*+,-./:;<>?@[¥]^_`{|}"
        # )
        self.assertEqual(yotsuba.ja.normalize_neologd("＝。、・「」"), "＝。、・「」")
        self.assertEqual(yotsuba.ja.normalize_neologd("ﾊﾝｶｸ"), "ハンカク")
        self.assertEqual(yotsuba.ja.normalize_neologd("o₋o"), "o-o")
        self.assertEqual(yotsuba.ja.normalize_neologd("majika━"), "majikaー")
        self.assertEqual(yotsuba.ja.normalize_neologd("わ〰い"), "わい")
        self.assertEqual(yotsuba.ja.normalize_neologd("スーパーーーー"), "スーパー")
        self.assertEqual(yotsuba.ja.normalize_neologd("!#"), "!#")
        self.assertEqual(yotsuba.ja.normalize_neologd("ゼンカク　スペース"), "ゼンカクスペース")
        self.assertEqual(yotsuba.ja.normalize_neologd("お             お"), "おお")
        self.assertEqual(yotsuba.ja.normalize_neologd("      おお"), "おお")
        self.assertEqual(yotsuba.ja.normalize_neologd("おお      "), "おお")
        self.assertEqual(
            yotsuba.ja.normalize_neologd("検索 エンジン 自作 入門 を 買い ました!!!"),
            "検索エンジン自作入門を買いました!!!"
        )
        self.assertEqual(
            yotsuba.ja.normalize_neologd("アルゴリズム C"), "アルゴリズムC"
        )
        self.assertEqual(
            yotsuba.ja.normalize_neologd("　　　ＰＲＭＬ　　副　読　本　　　"), "PRML副読本"
        )
        self.assertEqual(
            yotsuba.ja.normalize_neologd("Coding the Matrix"),
            "Coding the Matrix"
        )
        self.assertEqual(
            yotsuba.ja.normalize_neologd("南アルプスの　天然水　Ｓｐａｒｋｉｎｇ　Ｌｅｍｏｎ　レモン一絞り"),
            "南アルプスの天然水Sparking Lemonレモン一絞り"
        )
        # self.assertEqual(
        #     '南アルプスの天然水-Sparking*Lemon+レモン一絞り',
        #     yotsuba.ja.normalize_neologd(
        #         '南アルプスの　天然水-　Ｓｐａｒｋｉｎｇ*　Ｌｅｍｏｎ+　レモン一絞り'
        #     )
        # )
        processing_time: float = time.time() - start
        print(f'Processing time of rust   : {processing_time}')


if __name__ == '__main__':
    unittest.main()
