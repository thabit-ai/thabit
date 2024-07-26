import unittest
from thabit.evaluators.by_words import has_all_words, has_some_words, has_no_words


class TestByWords(unittest.TestCase):
    def test_has_all_words(self):
        test_cases = [
            ("Hello world", "Hello world", True),
            ("Hello world", "Hello", True),
            ("Hello world", "world Hello", True),
            ("Hello world", "Hello there", False),
            ("Goodbye world", "Goodbye", True),
            ("Goodbye world", "Goodbye everyone", False),
        ]

        for output, words, expected_result in test_cases:
            with self.subTest(output=output, words=words):
                self.assertEqual(has_all_words(output, words), expected_result)

    def test_has_some_words(self):
        test_cases = [
            ("Hello world", "Hello", True),
            ("Hello world", "world", True),
            ("Hello world", "Goodbye", False),
            ("Goodbye world", "Goodbye everyone", True),
            ("Fuzzy matching", "Fuzzy match", True),
            ("Fuzzy matching", "Fuzzy", True),
        ]

        for output, words, expected_result in test_cases:
            with self.subTest(output=output, words=words):
                self.assertEqual(has_some_words(output, words), expected_result)

    def test_has_no_words(self):
        test_cases = [
            ("Hello world", "Goodbye", True),
            ("Hello world", "Goodbye everyone", True),
            ("Goodbye", "Hello", True),
            ("Fuzzy matching", "Fuzzy match", False),
            ("", "Non-empty", False),
            ("Non-empty", "", False),
        ]

        for output, words, expected_result in test_cases:
            with self.subTest(output=output, words=words):
                self.assertEqual(has_no_words(output, words), expected_result)
