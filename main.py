#!/usr/bin/env python3
"""botyaradash — A powerful system monitoring dashboard.

Usage:
    python main.py [OPTIONS]

Run with --help for all options.
"""

import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import main

if __name__ == "__main__":
    main()
