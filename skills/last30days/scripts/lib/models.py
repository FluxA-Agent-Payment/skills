"""Model selection for last30days skill.

With x402 payments, API keys are no longer needed. Models are configured
via config or use defaults.
"""

from typing import Dict, Optional

# Default models for x402 proxies
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_XAI_MODEL = "grok-4-1-fast-reasoning"


def get_models(config: Dict) -> Dict[str, str]:
    """Get models for both providers.

    Args:
        config: Configuration dict (may contain OPENAI_MODEL, XAI_MODEL)

    Returns:
        Dict with 'openai' and 'xai' keys
    """
    return {
        "openai": config.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        "xai": config.get("XAI_MODEL", DEFAULT_XAI_MODEL),
    }
