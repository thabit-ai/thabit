import unittest
from thabit.utils.load import load_config
from json import JSONDecodeError
import os


class TestLoadConfig(unittest.TestCase):
    def test_load_valid_config(self):
        os.environ["TEST"] = "test"
        config = load_config("./tests/utils/valid_config.json")
        self.assertIsInstance(config, dict)

    def test_load_invalid_config_file(self):
        with self.assertRaises(FileNotFoundError):
            load_config("./tests/utils/not_here.json")

    def test_load_empty_config(self):
        with self.assertRaises(ValueError):
            load_config("./tests/utils/empty_config.json")

    def test_loading_corrupted_config_file(self):
        with self.assertRaises(JSONDecodeError):
            load_config("./tests/utils/invalid_config.json")
