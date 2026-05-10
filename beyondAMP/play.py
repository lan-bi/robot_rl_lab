"""Convenience wrapper to launch scripts/factoryIsaac/play.py from the repository root."""

from __future__ import annotations

import os
import runpy
import sys


if __name__ == "__main__":
    script_dir = os.path.join(os.path.dirname(__file__), "scripts", "factoryIsaac")
    script_path = os.path.join(script_dir, "play.py")
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    runpy.run_path(script_path, run_name="__main__")
