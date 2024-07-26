import unittest
from thabit.evaluators.exact import exact_match


class TestExactMatch(unittest.TestCase):
    def test_exact_match(self):
        test_cases = [
            ("Hello world", "Hello world", True),
            ("Hello world", " hello world ", False),
            ("Hello", "Hello", True),
            ("Hello", "Hello there", False),
            ("Goodbye", "Goodbye", True),
            ("Goodbye", "Goodbye everyone", False),
            ("Fuzzy matching", "Fuzzy matching", True),
            ("Fuzzy matching", "Fuzzy match", False),
            ("", "", True),
            ("Non-empty", "", False),
        ]

        for output, expected_output, expected_result in test_cases:
            with self.subTest(output=output, expected_output=expected_output):
                self.assertEqual(exact_match(output, expected_output), expected_result)
