"""
DrawBook - A Python library for drawing
"""

from .core import *
from pathlib import Path

def get_version():
    version_file = Path(__file__).parent.parent / 'version.txt'
    with open(version_file, 'r') as f:
        return f.read().strip()

__version__ = get_version() 