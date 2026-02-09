"""Tests for models module."""

import sys
import unittest
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib import models


class TestGetModels(unittest.TestCase):
    def test_default_models(self):
        """Test that get_models returns default models when no config provided."""
        config = {}
        result = models.get_models(config)
        self.assertEqual(result["openai"], models.DEFAULT_OPENAI_MODEL)
        self.assertEqual(result["xai"], models.DEFAULT_XAI_MODEL)

    def test_custom_openai_model(self):
        """Test custom OpenAI model from config."""
        config = {"OPENAI_MODEL": "gpt-5"}
        result = models.get_models(config)
        self.assertEqual(result["openai"], "gpt-5")
        self.assertEqual(result["xai"], models.DEFAULT_XAI_MODEL)

    def test_custom_xai_model(self):
        """Test custom xAI model from config."""
        config = {"XAI_MODEL": "grok-5"}
        result = models.get_models(config)
        self.assertEqual(result["openai"], models.DEFAULT_OPENAI_MODEL)
        self.assertEqual(result["xai"], "grok-5")

    def test_both_custom_models(self):
        """Test both custom models from config."""
        config = {
            "OPENAI_MODEL": "gpt-5",
            "XAI_MODEL": "grok-5",
        }
        result = models.get_models(config)
        self.assertEqual(result["openai"], "gpt-5")
        self.assertEqual(result["xai"], "grok-5")


if __name__ == "__main__":
    unittest.main()
