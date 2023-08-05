from typing import List, Optional

from yotsuba import ja
from yotsuba import yotsuba as ytb  # type: ignore


def clean_emails(text: str, replace: str = '') -> str:
    """Replace emails with given string.

    Args:
        text: A text want to clean emails.
        replace: Token to replace emails, default is ''.
    Returns:
        Cleaned text.
    Examples:
        >>> import yotsuba
        >>> text: str = 'Hello aaa@example.com!'
        >>> print(yotsuba.clean_emails(text))
        Hello !
        >>> print(yotsuba.clean_emails(text, '<URL>'))
        Hello <URL>!
    """
    return ytb.clean_emails(text, replace)


def clean_html_tags(text: str, replace: str = '') -> str:
    """Replace html tags and replace it with given token.

    Args:
        text: A text want to clean html tags.
        replace: Token to replace html tags, default is ''.
    Returns:
        Cleaned text.
    Examples:
        >>> import yotsuba
        >>> text: str = 'aaa<a>bbb</a>ccc'
        >>> print(yotsuba.clean_html_tags(text))
        aaabbbccc
        >>> print(yotsuba.clean_html_tags(text, '<HTML>'))
        aaa<HTML>bbb<HTML>ccc
    """
    return ytb.clean_html_tags(text, replace)


def clean_number(text: str, replace: str = '0') -> str:
    """Replace sequence of numbers with given string.

    Args:
        text: A text want to clean number.
        replace: Token to replace number, default is '0'.
    Returns:
        Cleaned text.
    Examples:
        >>> import yotsuba
        >>> text: str = 'I was born in 2020.'
        >>> print(yotsuba.clean_number(text))
        I was born in 0.
    """
    return ytb.clean_number(text, replace)


def clean_url(text: str, replace: str = '') -> str:
    """Replace urls with given string.

    Args:
        text: A text want to clean url.
        replace: Token to replace url, default is ''.
    Returns:
        Cleaned text.
    Examples:
        >>> import yotsuba
        >>> text: str = 'Wellcome to  https://github.com/yutayamazaki/yotsuba'
        >>> yotsuba.clean_url(text)
        'Wellcome to '
    """
    return ytb.clean_url(text, replace)


def get_stopwords(lang: str = 'ja') -> List[str]:
    """Get stopwords from http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt.

    Args:
        lang: Now, only support 'ja'.
    Returns:
        List of stopwords with length 310.
    Examples:
        >>> import yotsuba
        >>> stopwords = yotsuba.get_stopwords('ja')
        >>> len(stopwords)
        310
    """
    return ytb.get_stopwords(lang)


def get_stopwords_by_frequency(
    docs: List[List[str]], max_freq: int
) -> List[str]:
    """Compute word frequency and return them as stopwords.

    Args:
        docs: Like [['I', 'am', 'a', 'dog'], ...].
        max_freq: Words with over this frequecny are considered as stopwords.
    Returns:
        Computed stopwords.
    Examples:
        >>> import yotsuba
        >>> docs = [['I', 'am', 'a', 'dog'], ['this', 'is', 'a', 'pen']]
        >>> yotsuba.get_stopwords_by_frequency(docs, 2)
        ['a']
    """
    return ytb.get_stopwords_by_frequency(docs, max_freq)


def pad_sequence(
    sequence: List[int], maxlen: int, value: Optional[int] = None,
    padding: str = 'post'
) -> List[int]:
    """
    Pad sequence with given value like
    keras.preprocessing,sequence.pad_sequence.

    Args:
        sequence: Sequence to pad like [0, 3, 1, ...].
        maxlen: Maximum length of sequence to pad with.
        value: A value to pad, default=0.
        padding: 'pre' or 'post', default is 'post'.
    Returns:
        Padded sequence which has maxlen length.
    Examples:
        >>> import yotsuba
        >>> print(yotsuba.pad_sequence([0, 1, 2], 5))
        [0, 1, 2, 0, 0]
        >>> print(yotsuba.pad_sequence([0, 1, 2], 5, -1))
        [0, 1, 2, -1, -1]
    """
    return ytb.pad_sequence(sequence, maxlen, value, padding)


def pad_sequences(
    sequences: List[List[int]], maxlen: Optional[int] = None,
    value: Optional[int] = None, padding: str = 'post'
) -> List[List[int]]:
    """
    Pad sequences with given value like
    keras.preprocessing,sequence.pad_sequence.

    Args:
        sequences: A list of list to pad like [[0, 1], ...].
        maxlen:
            Maximum length of sequence to pad with. If None was passed,
            pad with maximum size of sequence.
        value: A value to pad, default=0.
        padding: 'pre' or 'post', default is 'post'.
    Returns:
        Padded sequences which has maxlen length.
    Examples:
        >>> import yotsuba
        >>> print(yotsuba.pad_sequences([[0, 1, 2], [0, 1]], 5))
        [[0, 1, 2, 0, 0], [0, 1, 0, 0, 0]]
        >>> print(yotsuba.pad_sequences([[0, 1, 2], [0, 1]], 5, padding='pre'))
        [[0, 0, 0, 1, 2], [0, 0, 0, 0, 1]]
    """
    return ytb.pad_sequences(sequences, maxlen, value, padding)


def remove_stopwords(tokens: List[str], stopwords: List[str]) -> List[str]:
    """Remove stopwords from given tokens.

    Args:
        tokens: A list of string want to remove stopwords.
        stopwords: Specify stopwords to remove.
    Returns:
        Stopwords removed tokens.
    Examples:
        >>> import yotsuba
        >>> tokens = ['I', 'am', 'a', 'dog']
        >>> stopwords = ['a']
        >>> print(yotsuba.remove_stopwords(tokens, stopwords))
            ['I', 'am', 'dog']
    """
    return ytb.remove_stopwords(tokens, stopwords)
