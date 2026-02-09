"""Environment and configuration management for last30days skill.

With x402 payments via FluxA Agent Wallet, no API keys or .env files are needed.
Payments are handled via X-Payment headers passed to the script.
Configuration is minimal - just model preferences from environment variables.
"""

import os
from typing import Dict, Any


def get_config() -> Dict[str, Any]:
    """Get configuration from environment variables.

    With x402 payments, no API keys or config files are needed.
    Config is optional and only for model preferences.
    """
    return {
        # Model preferences (optional - defaults are used if not set)
        'OPENAI_MODEL': os.environ.get('OPENAI_MODEL', 'gpt-4o'),
        'XAI_MODEL': os.environ.get('XAI_MODEL', 'grok-4-1-fast-reasoning'),
    }
