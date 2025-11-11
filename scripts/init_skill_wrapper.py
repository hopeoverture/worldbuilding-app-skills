#!/usr/bin/env python3
"""Wrapper to handle Windows encoding issues"""
import sys
import os

# Force UTF-8 encoding for stdout/stderr
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import and run the actual init_skill
sys.path.insert(0, os.path.dirname(__file__))
from init_skill import main

if __name__ == "__main__":
    main()
