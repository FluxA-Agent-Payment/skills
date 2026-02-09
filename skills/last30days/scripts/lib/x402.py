"""x402 payment module for last30days skill.

Handles x402 payment protocol for paid API calls.
The calling agent (Claude Code) handles mandate creation and signing.
This module handles making paid requests with a provided mandate_id.
"""

import json
import sys
from typing import Any, Dict, Tuple

from . import http

# x402 proxy endpoints
X402_OPENAI_PROXY = "https://proxy-monetize.fluxapay.xyz/api/openai-api-endpoints/v1/responses"
X402_XAI_PROXY = "https://proxy-monetize.fluxapay.xyz/api/grok-api-call/v1/responses"


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[x402] {msg}\n")
    sys.stderr.flush()


def get_402_price(url: str, payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    """Make initial request to get 402 response with pricing.

    Args:
        url: API endpoint URL
        payload: Request payload

    Returns:
        Tuple of (price_atomic_units, full_402_response)

    Raises:
        http.HTTPError: On non-402 response or invalid pricing
    """
    headers = {"Content-Type": "application/json"}

    try:
        # This should fail with 402
        http.post(url, payload, headers=headers)
        # If we got here, the API didn't require payment
        raise http.HTTPError("API did not return 402 - payment not required")
    except http.HTTPError as e:
        if e.status_code != 402:
            raise

        # Parse 402 response body
        if not e.body:
            raise http.HTTPError("402 response missing body")

        try:
            response_402 = json.loads(e.body)
        except json.JSONDecodeError:
            raise http.HTTPError(f"Invalid 402 response JSON: {e.body[:200]}")

        # Extract maxAmountRequired
        max_amount = response_402.get("maxAmountRequired")
        if max_amount is None:
            raise http.HTTPError("402 response missing maxAmountRequired")

        return int(max_amount), response_402


def make_paid_request(
    url: str,
    x_payment_header: str,
    payload: Dict[str, Any],
    timeout: int = 120,
) -> Dict[str, Any]:
    """Make a paid API request with x402 payment.

    Args:
        url: API endpoint URL
        x_payment_header: The X-Payment header value (provided by calling agent)
        payload: Request payload
        timeout: Request timeout

    Returns:
        API response

    Raises:
        http.HTTPError: On request failure
    """
    headers = {
        "Content-Type": "application/json",
        "X-Payment": x_payment_header,
    }

    return http.post(url, payload, headers=headers, timeout=timeout)


def format_price_usdc(atomic_units: int) -> str:
    """Format atomic units as USDC string.

    Args:
        atomic_units: Amount in atomic units (1 USDC = 1,000,000)

    Returns:
        Formatted string like "$0.02"
    """
    usdc = atomic_units / 1_000_000
    return f"${usdc:.2f}"
