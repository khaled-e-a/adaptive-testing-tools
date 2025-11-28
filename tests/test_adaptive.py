import random

import pytest

import adaptive_testing_tools.adaptive as adaptive
from adaptive_testing_tools import (
    adaptive_random_testing,
    levenshtein_distance,
    select_fscs_candidate,
)


def test_levenshtein_matches_known_value() -> None:
    assert levenshtein_distance("kitten", "sitting") == 3


def test_python_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adaptive, "_Levenshtein", None, raising=False)
    assert levenshtein_distance("flaw", "lawn") == 2


def test_prefers_farthest_candidate_in_pool() -> None:
    previous = ["aaaa", "bbbb"]
    candidates = iter(["aaac", "bbbb", "cccc"])
    generator = lambda: next(candidates)

    chosen = select_fscs_candidate(
        previous,
        generator,
        pool_size=3,
        distance_fn=levenshtein_distance,
    )

    assert chosen == "cccc"


def test_adaptive_random_testing_records_distances_and_results() -> None:
    def make_candidate(rng: random.Random) -> str:
        return "".join(rng.choice("abc") for _ in range(4))

    samples = adaptive_random_testing(
        make_candidate,
        evaluate=lambda s: s.count("a"),
        pool_size=4,
        max_iterations=3,
        seed=7,
    )

    assert len(samples) == 3
    assert samples[0].distance_to_previous is None

    for index, sample in enumerate(samples[1:], start=1):
        prior = [s.candidate for s in samples[:index]]
        expected_distance = min(
            levenshtein_distance(sample.candidate, seen) for seen in prior
        )
        assert sample.distance_to_previous == expected_distance
        assert isinstance(sample.result, int)
