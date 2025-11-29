# adaptive-testing-tools

Adaptive random testing helpers for Python. Generate diverse candidates using a fixed-size candidate set (FSCs) selector plus a few lightweight random utilities.

## Install

```bash
pip install adaptive-testing-tools
```

## Quick start

```python
from adaptive_testing_tools import adaptive_random_testing
from random import Random

def make_candidate(rng: Random) -> str:
    return "".join(rng.choice("abc") for _ in range(6))

def evaluate(candidate: str) -> int:
    return candidate.count("a")

samples = adaptive_random_testing(
    make_candidate,
    evaluate,
    pool_size=5,
    max_iterations=3,
    seed=42,
)
for sample in samples:
    print(sample.iteration, sample.candidate, sample.distance_to_previous, sample.result)
```

## Features

- Adaptive Random Testing with FSCs selection.
- Configurable distance function (defaults to Levenshtein with rapidfuzz fallback).
- Simple random helpers: ints, choice, strings.

See the API reference (from the menu) for details.
