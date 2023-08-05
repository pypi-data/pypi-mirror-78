import unittest
from typing import List

import yotsuba


class PadSequenceTests(unittest.TestCase):

    def test_simple(self):
        padding: List[int] = yotsuba.pad_sequence(
            sequence=[0, 2, 1], maxlen=5, value=-1, padding='post'
        )
        self.assertEqual(padding, [0, 2, 1, -1, -1])

    def test_padding_pre(self):
        padding: List[int] = yotsuba.pad_sequence(
            sequence=[0, 2, 1], maxlen=5, value=-1, padding='pre'
        )
        self.assertEqual(padding, [-1, -1, 0, 2, 1])

    def test_option_value(self):
        padding: List[int] = yotsuba.pad_sequence(
            sequence=[0, 2, 1], maxlen=5, padding='post'
        )
        self.assertEqual(padding, [0, 2, 1, 0, 0])

    def test_raise_invalid_padding(self):
        with self.assertRaises(ValueError):
            yotsuba.pad_sequence(
                sequence=[0, 2, 1], maxlen=5, padding='invalid-padding'
            )


class PadSequencesTests(unittest.TestCase):

    def test_simple(self):
        sequences: List[List[int]] = [[0, 2, 1], [0, 1]]
        padding: List[List[int]] = yotsuba.pad_sequences(
            sequences=sequences, maxlen=5, value=-1, padding='post'
        )
        self.assertEqual(padding, [[0, 2, 1, -1, -1], [0, 1, -1, -1, -1]])

    def test_option_maxlen(self):
        sequences: List[List[int]] = [[0, 2, 1], [0, 1]]
        padding: List[List[int]] = yotsuba.pad_sequences(
            sequences=sequences, value=-1, padding='post'
        )
        self.assertEqual(padding, [[0, 2, 1], [0, 1, -1]])

    def test_option_value(self):
        sequences: List[List[int]] = [[0, 2, 1], [0, 1]]
        padding: List[List[int]] = yotsuba.pad_sequences(
            sequences=sequences, padding='post'
        )
        self.assertEqual(padding, [[0, 2, 1], [0, 1, 0]])

    def test_raise_invalid_padding(self):
        sequences: List[List[int]] = [[0, 2, 1], [0, 1]]
        with self.assertRaises(ValueError):
            yotsuba.pad_sequences(
                sequences=sequences, padding='invalid'
            )


class RemoveStopwordsTests(unittest.TestCase):

    def test_simple(self):
        tokens: List[str] = ['I', 'am', 'a', 'dog']
        stopwords: List[str] = ['am', 'a']
        removed: List[str] = yotsuba.remove_stopwords(
            tokens, stopwords
        )
        self.assertEqual(removed, ['I', 'dog'])


class GetStopwordsTests(unittest.TestCase):

    def test_simple(self):
        stopwords: List[str] = yotsuba.get_stopwords(lang='ja')
        self.assertIsInstance(stopwords, list)
        self.assertEqual(len(stopwords), 310)


class GetStopwordsByFrequencyTests(unittest.TestCase):

    def test_simple(self):
        tokens: List[List[str]] = [
            ['I', 'am', 'a', 'pen', 'pen'] for _ in range(50)
        ]
        stopwords: List[str] = yotsuba.get_stopwords_by_frequency(tokens, 100)
        self.assertEqual(stopwords, ['pen'])


class CleanURLTests(unittest.TestCase):

    def test_simple(self):
        text: str = 'foohttp://example.com bar'
        cleaned: str = yotsuba.clean_url(text)
        self.assertEqual(cleaned, 'foo bar')

    def test_replace(self):
        text: str = 'foohttps://example.com bar'
        cleaned: str = yotsuba.clean_url(text=text, replace='<URL>')
        self.assertEqual(cleaned, 'foo<URL> bar')


class CleanHTMLTagsTests(unittest.TestCase):

    def test_simple(self):
        text: str = 'foo<a>hello</a>bar'
        cleaned: str = yotsuba.clean_html_tags(text)
        self.assertEqual(cleaned, 'foohellobar')

    def test_replace(self):
        text: str = 'foo<a>hello</a>bar'
        cleaned: str = yotsuba.clean_html_tags(text, replace=' ')
        self.assertEqual(cleaned, 'foo hello bar')


class CleanEmailsTests(unittest.TestCase):

    def test_simple(self):
        text: str = 'Regards, foo@example.com.'
        cleaned: str = yotsuba.clean_emails(text)
        self.assertEqual(cleaned, 'Regards, .')

    def test_replace(self):
        text: str = 'Regards, foo@example.com.'
        cleaned: str = yotsuba.clean_emails(text, replace='<EMAIL>')
        self.assertEqual(cleaned, 'Regards, <EMAIL>.')


class CleanNumberTests(unittest.TestCase):

    def test_simple(self):
        text: str = 'I was born in 1001.08.43.'
        cleaned: str = yotsuba.clean_number(text)
        self.assertEqual(cleaned, 'I was born in 0.0.0.')

    def test_replace(self):
        text: str = 'I was born in 1001.08.43.'
        cleaned: str = yotsuba.clean_number(text, '1')
        self.assertEqual(cleaned, 'I was born in 1.1.1.')


if __name__ == '__main__':
    unittest.main()
