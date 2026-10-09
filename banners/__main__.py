"""Executable entry point when invoked as a module (e.g., python -m banners)."""

import sys

from banners.cli import main

if __name__ == "__main__":
    sys.exit(main())
