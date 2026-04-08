"""
ARMS Engine: Durable bridge path helpers

Normalizes interim bridge inputs into the achelion_arms/state directory so
ARMS has a consistent local operating backbone while vendor-native workflows
are still being wired.
"""

import os

STATE_DIR = "achelion_arms/state"


def bridge_path(env_var: str, default_filename: str) -> str:
    configured = os.environ.get(env_var)
    if configured:
        return configured
    return os.path.join(STATE_DIR, default_filename)
