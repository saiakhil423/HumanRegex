"""
humanregex
~~~~~~~~~~
Write regex using plain English — no memorizing syntax required.

    >>> from humanregex import Pattern
    >>> Pattern().digit(3).dash().digit(4).match("123-4567")
    True
"""

from .core import Pattern

__all__ = ["Pattern"]
__version__ = "0.2.0"
