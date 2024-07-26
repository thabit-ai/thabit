import unittest
from thabit.evaluators.similarity import similarity


class TestSimilarity(unittest.TestCase):
    def test_similarity(self):
        test_cases = [
            ("Hello world", "Hello world", 80, True),
            ("Hello world", "world Hello", 80, True),
            ("Hello", "Hello", 80, True),
            ("Hello", "Hello there", 80, False),
            ("Goodbye", "Goodbye", 80, True),
            ("Goodbye", "Goodbye everyone", 80, False),
            ("Fuzzy matching", "Fuzzy match", 80, True),
            ("Fuzzy matching", "Fuzzy matching", 80, True),
            ("Fuzzy wuzzy was a bear", "Fuzzy wuzzy was a bear", 80, True),
            ("Fuzzy wuzzy was a bear", "Fuzzy wuzzy was a bee", 80, True),
        ]

        for output, expected_output, threshold, expected_result in test_cases:
            with self.subTest(
                output=output, expected_output=expected_output, threshold=threshold
            ):
                self.assertEqual(
                    similarity(output, expected_output, threshold), expected_result
                )
