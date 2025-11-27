"""General-purpose Adaptive Random Testing helpers."""

from dataclasses import dataclass
import random
from typing import Callable, Generic, List, Optional, Sequence, TypeVar

try:
    from rapidfuzz.distance import Levenshtein as _Levenshtein  # type: ignore
except Exception:  # pragma: no cover - fallback when rapidfuzz is missing
    _Levenshtein = None

R = TypeVar("R")


def levenshtein_distance(a: str, b: str) -> int:
    """Return Levenshtein edit distance using rapidfuzz when available."""
    if _Levenshtein is not None:
        return int(_Levenshtein.distance(a, b))
    return _python_levenshtein(a, b)


def _python_levenshtein(a: str, b: str) -> int:
    """Pure Python Levenshtein distance fallback."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    previous_row = list(range(len(b) + 1))
    for i, char_a in enumerate(a, start=1):
        current_row = [i]
        for j, char_b in enumerate(b, start=1):
            insertions = current_row[j - 1] + 1
            deletions = previous_row[j] + 1
            substitutions = previous_row[j - 1] + (char_a != char_b)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def select_fscs_candidate(
    previous: Sequence[str],
    generate_candidate: Callable[[], str],
    *,
    pool_size: int = 10,
    distance_fn: Callable[[str, str], int] = levenshtein_distance,
) -> str:
    """
    Pick the candidate with the largest minimum distance to prior samples (FSCs).

    FSCs = Fixed Size Candidate Set. A pool of random candidates is generated and
    the one farthest from all previously tested inputs is selected.
    """
    if not previous:
        return generate_candidate()
    best_candidate: Optional[str] = None
    best_distance = -1
    for _ in range(pool_size):
        candidate = generate_candidate()
        distance = min(distance_fn(candidate, seen) for seen in previous)
        if distance > best_distance:
            best_candidate = candidate
            best_distance = distance
    return best_candidate if best_candidate is not None else generate_candidate()


@dataclass(frozen=True)
class AdaptiveSample(Generic[R]):
    iteration: int
    candidate: str
    result: R
    distance_to_previous: Optional[int]


def adaptive_random_testing(
    generate_candidate: Callable[[random.Random], str],
    evaluate: Callable[[str], R],
    *,
    pool_size: int = 10,
    max_iterations: int = 5,
    seed: Optional[int] = None,
    distance_fn: Callable[[str, str], int] = levenshtein_distance,
) -> List[AdaptiveSample[R]]:
    """
    Run Adaptive Random Testing using FSCs to spread out sampled inputs.

    Args:
        generate_candidate: Callable that accepts a Random instance and returns an input to test.
        evaluate: Callable invoked on each candidate; its return value is recorded.
        pool_size: Number of candidates generated per iteration to select the farthest one.
        max_iterations: Total samples to run.
        seed: Optional seed to make sampling repeatable.
        distance_fn: Distance function used to measure spread between candidates.

    Returns:
        A list of AdaptiveSample entries containing the candidate, distance to prior inputs,
        and the evaluation result.
    """
    rng = random.Random(seed)
    tested: List[str] = []
    samples: List[AdaptiveSample] = []

    for iteration in range(1, max_iterations + 1):
        candidate = select_fscs_candidate(
            tested,
            lambda: generate_candidate(rng),
            pool_size=pool_size,
            distance_fn=distance_fn,
        )
        result = evaluate(candidate)
        distance = (
            min(distance_fn(candidate, seen) for seen in tested) if tested else None
        )
        tested.append(candidate)
        samples.append(
            AdaptiveSample(
                iteration=iteration,
                candidate=candidate,
                result=result,
                distance_to_previous=distance,
            )
        )
    return samples
