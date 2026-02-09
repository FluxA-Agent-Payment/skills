"""OpenAI Responses API client for Reddit discovery via x402 payment proxy."""

import json
import re
import sys
from typing import Any, Dict, List, Optional

from . import http, x402

# Default model for Reddit search
DEFAULT_MODEL = "gpt-4o"


def _log_error(msg: str):
    """Log error to stderr."""
    sys.stderr.write(f"[REDDIT ERROR] {msg}\n")
    sys.stderr.flush()


def _log_info(msg: str):
    """Log info to stderr."""
    sys.stderr.write(f"[REDDIT] {msg}\n")
    sys.stderr.flush()


# x402 proxy endpoint for OpenAI web_search
OPENAI_PROXY_URL = x402.X402_OPENAI_PROXY

# Depth configurations: (min, max) threads to request
# Request MORE than needed since many get filtered by date
DEPTH_CONFIG = {
    "quick": (15, 25),
    "default": (30, 50),
    "deep": (70, 100),
}

REDDIT_SEARCH_PROMPT = """Find Reddit discussion threads about: {topic}

STEP 1: EXTRACT THE CORE SUBJECT
Get the MAIN NOUN/PRODUCT/TOPIC:
- "best nano banana prompting practices" → "nano banana"
- "killer features of clawdbot" → "clawdbot"
- "top Claude Code skills" → "Claude Code"
DO NOT include "best", "top", "tips", "practices", "features" in your search.

STEP 2: SEARCH BROADLY
Search for the core subject:
1. "[core subject] site:reddit.com"
2. "reddit [core subject]"
3. "[core subject] reddit"

Return as many relevant threads as you find. We filter by date server-side.

STEP 3: INCLUDE ALL MATCHES
- Include ALL threads about the core subject
- Set date to "YYYY-MM-DD" if you can determine it, otherwise null
- We verify dates and filter old content server-side
- DO NOT pre-filter aggressively - include anything relevant

REQUIRED: URLs must contain "/r/" AND "/comments/"
REJECT: developers.reddit.com, business.reddit.com

Find {min_items}-{max_items} threads. Return MORE rather than fewer.

Return JSON:
{{
  "items": [
    {{
      "title": "Thread title",
      "url": "https://www.reddit.com/r/sub/comments/xyz/title/",
      "subreddit": "subreddit_name",
      "date": "YYYY-MM-DD or null",
      "why_relevant": "Why relevant",
      "relevance": 0.85
    }}
  ]
}}"""


def _extract_core_subject(topic: str) -> str:
    """Extract core subject from verbose query for retry."""
    noise = ['best', 'top', 'how to', 'tips for', 'practices', 'features',
             'killer', 'guide', 'tutorial', 'recommendations', 'advice',
             'prompting', 'using', 'for', 'with', 'the', 'of', 'in', 'on']
    words = topic.lower().split()
    result = [w for w in words if w not in noise]
    return ' '.join(result[:3]) or topic  # Keep max 3 words


def build_reddit_payload(
    model: str,
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Build the payload for Reddit search.

    Args:
        model: Model to use
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth

    Returns:
        Request payload dict
    """
    min_items, max_items = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])

    input_text = REDDIT_SEARCH_PROMPT.format(
        topic=topic,
        from_date=from_date,
        to_date=to_date,
        min_items=min_items,
        max_items=max_items,
    )

    return {
        "model": model,
        "tools": [
            {
                "type": "web_search",
                "filters": {
                    "allowed_domains": ["reddit.com"]
                }
            }
        ],
        "include": ["web_search_call.action.sources"],
        "input": input_text,
    }


def get_reddit_price(
    model: str,
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> tuple:
    """Get the x402 price for Reddit search.

    Args:
        model: Model to use
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth

    Returns:
        Tuple of (price_atomic_units, payload, payload_402)
    """
    payload = build_reddit_payload(model, topic, from_date, to_date, depth)
    price, payload_402 = x402.get_402_price(OPENAI_PROXY_URL, payload)
    return price, payload, payload_402


def search_reddit(
    x_payment_header: str,
    model: str,
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
    mock_response: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Search Reddit for relevant threads using x402 payment proxy.

    Args:
        x_payment_header: X-Payment header value (provided by calling agent)
        model: Model to use
        topic: Search topic
        from_date: Start date (YYYY-MM-DD) - only include threads after this
        to_date: End date (YYYY-MM-DD) - only include threads before this
        depth: Research depth - "quick", "default", or "deep"
        mock_response: Mock response for testing

    Returns:
        Raw API response
    """
    if mock_response is not None:
        return mock_response

    payload = build_reddit_payload(model, topic, from_date, to_date, depth)

    # Adjust timeout based on depth (generous for OpenAI web_search which can be slow)
    timeout = 90 if depth == "quick" else 120 if depth == "default" else 180

    return x402.make_paid_request(
        OPENAI_PROXY_URL,
        x_payment_header,
        payload,
        timeout=timeout,
    )


def parse_reddit_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse OpenAI response to extract Reddit items.

    Args:
        response: Raw API response

    Returns:
        List of item dicts
    """
    items = []

    # Check for API errors first
    if "error" in response and response["error"]:
        error = response["error"]
        err_msg = error.get("message", str(error)) if isinstance(error, dict) else str(error)
        _log_error(f"OpenAI API error: {err_msg}")
        if http.DEBUG:
            _log_error(f"Full error response: {json.dumps(response, indent=2)[:1000]}")
        return items

    # Try to find the output text
    output_text = ""
    if "output" in response:
        output = response["output"]
        if isinstance(output, str):
            output_text = output
        elif isinstance(output, list):
            for item in output:
                if isinstance(item, dict):
                    if item.get("type") == "message":
                        content = item.get("content", [])
                        for c in content:
                            if isinstance(c, dict) and c.get("type") == "output_text":
                                output_text = c.get("text", "")
                                break
                    elif "text" in item:
                        output_text = item["text"]
                elif isinstance(item, str):
                    output_text = item
                if output_text:
                    break

    # Also check for choices (older format)
    if not output_text and "choices" in response:
        for choice in response["choices"]:
            if "message" in choice:
                output_text = choice["message"].get("content", "")
                break

    if not output_text:
        print(f"[REDDIT WARNING] No output text found in OpenAI response. Keys present: {list(response.keys())}", flush=True)
        return items

    # Extract JSON from the response
    json_match = re.search(r'\{[\s\S]*"items"[\s\S]*\}', output_text)
    if json_match:
        try:
            data = json.loads(json_match.group())
            items = data.get("items", [])
        except json.JSONDecodeError:
            pass

    # Validate and clean items
    clean_items = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            continue

        url = item.get("url", "")
        if not url or "reddit.com" not in url:
            continue

        clean_item = {
            "id": f"R{i+1}",
            "title": str(item.get("title", "")).strip(),
            "url": url,
            "subreddit": str(item.get("subreddit", "")).strip().lstrip("r/"),
            "date": item.get("date"),
            "why_relevant": str(item.get("why_relevant", "")).strip(),
            "relevance": min(1.0, max(0.0, float(item.get("relevance", 0.5)))),
        }

        # Validate date format
        if clean_item["date"]:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(clean_item["date"])):
                clean_item["date"] = None

        clean_items.append(clean_item)

    return clean_items
