"""Entry point for ``python -m french``."""

from __future__ import annotations

import sys

from french.cli import main

if __name__ == "__main__":
    sys.exit(main())
