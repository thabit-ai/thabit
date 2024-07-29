import unittest
from thabit.evaluators.by_words import (
    contains_all_words,
    contains_words,
    contains_no_words,
)


class TestByWords(unittest.TestCase):
    def test_contains_all_words(self):
        test_cases = [
            ("Hello world", "Hello, world", True),
            ("Hello world", "Hello", True),
            ("Hello world", "world, Hello, ", True),
            ("Hello world", "Hello there", False),
            ("Goodbye world", "Goodbye", True),
            ("Goodbye world", "Goodbye, everyone", False),
        ]

        for output, words, expected_result in test_cases:
            with self.subTest(output=output, words=words):
                self.assertEqual(contains_all_words(output, words), expected_result)

    def test_contains_words(self):
        test_cases = [
            ("Hello world", "Hello", True),
            ("Hello world", "world", True),
            ("Hello world", "Goodbye", False),
            ("Goodbye world", "Goodbye, everyone", True),
            ("Fuzzy matching", "Fuzzy, match", True),
            ("Fuzzy matching", "Fuzzy, ", True),
        ]

        for output, words, expected_result in test_cases:
            with self.subTest(output=output, words=words):
                self.assertEqual(contains_words(output, words), expected_result)

    def test_contains_no_words(self):
        test_cases = [
            ("Hello world", "Goodbye", True),
            ("Hello world", "Goodbye, everyone", True),
            ("Goodbye", "Hello", True),
            ("Fuzzy matching", "Fuzzy, match", False),
            ("", "Non-empty", False),
            ("Non-empty", "", False),
        ]

        for output, words, expected_result in test_cases:
            with self.subTest(output=output, words=words):
                self.assertEqual(contains_no_words(output, words), expected_result)
