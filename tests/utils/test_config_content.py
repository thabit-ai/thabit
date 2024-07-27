import unittest
from thabit.utils.load import validate_config


class TestValidateConfig(unittest.TestCase):
    def test_valid_config(self):
        valid_config = {
            "global_parameters": {"temperature": 0.7, "max_tokens": 150, "top_p": 0.9},
            "models": [
                {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "model_name": "gpt35",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "api_key_env_var": "your_api_key",
                }
            ],
        }
        try:
            validate_config(valid_config)
        except ValueError:
            self.fail("validate_config raised ValueError unexpectedly!")

    def test_missing_global_parameters(self):
        config = {"models": []}
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(
            str(context.exception), "Configuration is missing 'global_parameters' key."
        )

    def test_missing_required_global_key(self):
        config = {
            "global_parameters": {"temperature": 0.7, "max_tokens": 150},
            "models": [],
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(
            str(context.exception),
            "'global_parameters' is missing required key: top_p in the config file",
        )

    def test_missing_models_key(self):
        config = {
            "global_parameters": {"temperature": 0.7, "max_tokens": 150, "top_p": 0.9}
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(
            str(context.exception),
            "Configuration is missing 'models' key or it is not a valid array.",
        )

    def test_empty_models_array(self):
        config = {
            "global_parameters": {"temperature": 0.7, "max_tokens": 150, "top_p": 0.9},
            "models": [],
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(
            str(context.exception),
            "Configuration is missing 'models' key or it is not a valid array.",
        )

    def test_missing_model_keys(self):
        config = {
            "global_parameters": {"temperature": 0.7, "max_tokens": 150, "top_p": 0.9},
            "models": [{"provider": "openai", "model": "gpt-3.5-turbo"}],
        }
        with self.assertRaises(ValueError) as context:
            validate_config(config)
        self.assertEqual(
            str(context.exception),
            "Model is missing required key: model_name in the config file",
        )
