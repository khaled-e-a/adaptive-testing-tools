"""Utilities for generating small random values for tests."""

import random
import string
from typing import Iterable, Sequence, TypeVar

T = TypeVar("T")


def random_int(low: int = 0, high: int = 100) -> int:
    """Return a random integer between low and high (inclusive)."""
    return random.randint(low, high)


def random_choice(options: Sequence[T]) -> T:
    """Return a random element from a non-empty sequence."""
    if not options:
        raise ValueError("options must not be empty")
    return random.choice(options)


def random_string(length: int = 8, alphabet: Iterable[str] = None) -> str:
    """Return a random string of the given length."""
    if length < 0:
        raise ValueError("length must be non-negative")
    chars = alphabet or (string.ascii_letters + string.digits)
    return "".join(random.choice(chars) for _ in range(length))
