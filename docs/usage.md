# Usage

## Adaptive Random Testing

Use `adaptive_random_testing` with two callables:

- `generate_candidate(rng: Random) -> str`: produce an input.
- `evaluate(candidate: str) -> Any`: run your system-under-test and return a result to record.

```python
from random import Random
from adaptive_testing_tools import adaptive_random_testing, levenshtein_distance

def generate_candidate(rng: Random) -> str:
    return " ".join(rng.sample(["alpha", "bravo", "charlie", "delta"], 3))

def evaluate(candidate: str) -> bool:
    return "alpha" in candidate

samples = adaptive_random_testing(
    generate_candidate,
    evaluate,
    pool_size=5,
    max_iterations=5,
    seed=123,
    distance_fn=levenshtein_distance,
)
for sample in samples:
    print(sample.iteration, sample.distance_to_previous, sample.result)
```

## Random helpers

```python
from adaptive_testing_tools import random_choice, random_int, random_string

print(random_int(1, 10))
print(random_choice(["x", "y", "z"]))
print(random_string(8))
```
