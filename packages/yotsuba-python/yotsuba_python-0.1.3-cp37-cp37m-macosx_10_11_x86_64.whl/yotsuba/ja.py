from yotsuba import yotsuba as ytb  # type: ignore


def normalize_neologd(text: str) -> str:
    """
    Do preprocessing for mecab-ipadic-neologd.
    https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja

    Args:
        text: Text to apply normalizing.
    Returns:
        Normalized text.
    Examples:
        >>> import yotsuba
        >>> text: str = '南アルプスの　天然水　Ｓｐａｒｋｉｎｇ　Ｌｅｍｏｎ　レモン一絞り'
        >>> yotsuba.ja.normalize_neologd(text)
        '南アルプスの天然水Sparking Lemonレモン一絞り'
    """
    return ytb.ja.normalize_neologd(text)
