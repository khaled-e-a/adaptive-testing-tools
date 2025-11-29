# adaptive-testing-tools

[![PyPI](https://img.shields.io/pypi/v/adaptive-testing-tools.svg)](https://pypi.org/project/adaptive-testing-tools/)


Adaptive random testing helpers for generating spread-out random inputs and a few small random data utilities.

## Installation

Install directly from the repository or a built wheel:

```bash
pip install .
```

## Usage

```python
from adaptive_testing_tools import random_choice, random_int, random_string

value = random_int(10, 99)
letter = random_choice(["a", "b", "c"])
token = random_string(length=12)

# Adaptive random testing with FSCs
from random import Random
from adaptive_testing_tools import adaptive_random_testing

def make_candidate(rng: Random) -> str:
    # Example: random 4-word phrase; replace with your own generator
    words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
    return " ".join(rng.sample(words, 4))

def evaluate(candidate: str) -> bool:
    # Replace with your system-under-test invocation
    return "alpha" in candidate

samples = adaptive_random_testing(
    make_candidate,
    evaluate,
    pool_size=5,
    max_iterations=3,
    seed=42,
)
for sample in samples:
    print(sample.iteration, sample.distance_to_previous, sample.result)
```

## Development

- Build artifacts: `python -m build`
- Install locally in editable mode: `pip install -e .`

Feel free to extend the helpers in `src/adaptive_testing_tools/generator.py` to fit your projects.

## Documentation (MkDocs)

API documentation is available at: https://khaled-e-a.github.io/adaptive-testing-tools/

To build it yourself:
- Install docs deps: `pip install mkdocs mkdocs-material mkdocstrings[python]`
- Serve locally: `mkdocs serve`
- Build static site: `mkdocs build`
