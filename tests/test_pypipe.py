import dataclasses
import pytest

from pypipe import step, PipeStep, Pipeline


# ────────────────── Fixtures & helpers ────────────────── #
# Basic pipe steps used across tests
@step
def plus_one(x: int) -> int:  # noqa: D401 – simple
    """Add **1** to *x*."""
    return x + 1


@step
def times_two(x: int) -> int:  # noqa: D401 – simple
    """Multiply *x* by **2**."""
    return x * 2


# ────────────────────── Test cases ────────────────────── #

def test_pipestep_is_callable_and_frozen():
    """A `PipeStep` should behave like a function and be immutable."""
    assert plus_one(3) == 4, "PipeStep did not execute wrapped function correctly."
    assert isinstance(plus_one, PipeStep)

    # Immutability (frozen dataclass)
    with pytest.raises(dataclasses.FrozenInstanceError):
        plus_one.name = "something_else"


def test_or_operator_creates_pipeline():
    """`A | B` should yield a `Pipeline` containing both steps in order."""
    pipeline = plus_one | times_two
    assert isinstance(pipeline, Pipeline)
    assert pipeline.steps == (plus_one, times_two)


def test_pipeline_executes_sequentially():
    pipeline = plus_one | times_two
    # (3 + 1) * 2 == 8
    assert pipeline(3) == 8


def test_pipeline_can_be_extended():
    @step
    def minus_three(x: int) -> int:
        return x - 3

    pipeline = plus_one | times_two
    extended = pipeline | minus_three

    # (5 + 1) * 2 - 3 == 9
    assert extended(5) == 9
    assert extended.steps == (plus_one, times_two, minus_three)


def test_invalid_chain_raises_type_error():
    """Chaining a non‑PipeStep / Pipeline should raise a `TypeError`."""
    with pytest.raises(TypeError):
        _ = plus_one | 42  # type: ignore[operator]


def test_auto_docstring_generation():
    """`Pipeline.__doc__` should be auto‑generated from step docs when absent."""
    pipeline = plus_one | times_two
    doc = pipeline.__doc__

    assert doc is not None, "Pipeline docstring not generated."
    assert "plus_one" in doc and "times_two" in doc


def test_repr_includes_step_names_or_name():
    pipeline = plus_one | times_two
    rep = repr(pipeline)
    assert "Pipeline" in rep
    assert "plus_one" in rep or "times_two" in rep
