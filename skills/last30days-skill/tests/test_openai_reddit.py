"""Tests for openai_reddit module."""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from lib import openai_reddit


class TestBuildRedditPayload(unittest.TestCase):
    """Tests for build_reddit_payload function."""

    def test_builds_valid_payload(self):
        """Test that payload has required structure."""
        payload = openai_reddit.build_reddit_payload(
            model="gpt-4o",
            topic="Python testing",
            from_date="2026-01-01",
            to_date="2026-01-31",
            depth="default",
        )

        self.assertIn("model", payload)
        self.assertIn("tools", payload)
        self.assertIn("input", payload)
        self.assertEqual(payload["model"], "gpt-4o")

    def test_includes_web_search_tool(self):
        """Test that web_search tool is configured."""
        payload = openai_reddit.build_reddit_payload(
            model="gpt-4o",
            topic="test",
            from_date="2026-01-01",
            to_date="2026-01-31",
        )

        tools = payload["tools"]
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0]["type"], "web_search")
        self.assertIn("allowed_domains", tools[0]["filters"])

    def test_depth_configs(self):
        """Test different depth configurations."""
        for depth in ["quick", "default", "deep"]:
            payload = openai_reddit.build_reddit_payload(
                model="gpt-4o",
                topic="test",
                from_date="2026-01-01",
                to_date="2026-01-31",
                depth=depth,
            )
            # Should not raise
            self.assertIn("input", payload)


class TestParseRedditResponse(unittest.TestCase):
    """Tests for parse_reddit_response function."""

    def test_parses_valid_response(self):
        """Test parsing a valid API response."""
        response = {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": '{"items": [{"title": "Test Thread", "url": "https://reddit.com/r/test/comments/abc123/test_thread/", "subreddit": "test", "date": "2026-01-15", "why_relevant": "Relevant", "relevance": 0.9}]}'
                        }
                    ]
                }
            ]
        }

        items = openai_reddit.parse_reddit_response(response)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Test Thread")
        self.assertEqual(items[0]["subreddit"], "test")

    def test_handles_error_response(self):
        """Test handling API error response."""
        response = {"error": {"message": "API error"}}

        items = openai_reddit.parse_reddit_response(response)

        self.assertEqual(len(items), 0)

    def test_handles_empty_response(self):
        """Test handling empty response."""
        response = {}

        items = openai_reddit.parse_reddit_response(response)

        self.assertEqual(len(items), 0)


class TestDefaultModel(unittest.TestCase):
    """Tests for default model constant."""

    def test_default_model_is_gpt4o(self):
        """Test that default model is set correctly."""
        self.assertEqual(openai_reddit.DEFAULT_MODEL, "gpt-4o")


if __name__ == "__main__":
    unittest.main()
