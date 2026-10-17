import sys
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
"""Verticals — AI-Native Content Engine for vertical video."""

__version__ = "3.0.0"
