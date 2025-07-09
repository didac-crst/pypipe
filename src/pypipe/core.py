"""A lightweight and intuitive library for building functional data processing pipelines.

This module provides a set of classes and a decorator to create elegant, readable,
and reusable data processing workflows. By overloading the bitwise OR operator (`|`),
it allows functions to be chained together in a linear sequence, similar to shell
piping, transforming nested function calls into a clear, step-by-step process.

Key Components:
    - PipeStep: A wrapper for a single function, representing one atomic step.
    - Pipeline: An ordered sequence of PipeSteps that executes them in order.
    - @step: A decorator to easily convert any Python function into a PipeStep.

Basic Usage:
    >>> @step
    ... def add_10(x):
    ...     '''Adds 10 to a number.'''
    ...     return x + 10
    ...
    >>> @step
    ... def multiply_by_2(x):
    ...     '''Multiplies a number by 2.'''
    ...     return x * 2
    ...
    >>> # Chain steps into a pipeline
    >>> calculation_pipeline = add_10 | multiply_by_2
    >>>
    >>> # Execute the entire pipeline
    >>> result = calculation_pipeline(5)
    >>> print(result)
    30
    >>>
    >>> # Pipelines are self-documenting
    >>> help(calculation_pipeline)
"""

from dataclasses import dataclass
from typing import Any, Callable, Tuple, Optional

# ────── PipeStep: The smallest unit of a pipeline ───────────────────────────

@dataclass(frozen=True)
class PipeStep:
    """Represents a single, atomic step in a processing pipeline."""
    func: Callable[[Any], Any]
    name: Optional[str] = None
    doc: Optional[str] = None

    def __post_init__(self):
        """Sets name and doc from the function if they are not provided."""
        # Use object.__setattr__ to modify attributes on a frozen dataclass
        if self.name is None:
            object.__setattr__(self, 'name', self.func.__name__)
        if self.doc is None:
            object.__setattr__(self, 'doc', self.func.__doc__)
        
        # Also set the dunder attributes to make the object behave more like a function
        object.__setattr__(self, '__name__', self.name)
        object.__setattr__(self, '__doc__', self.doc)

    def __call__(self, data: Any) -> Any:
        """Executes the wrapped function."""
        return self.func(data)
    
    def __or__(self, other: Any) -> 'Pipeline':
        """Enables chaining with the `|` operator to create a Pipeline."""
        if isinstance(other, PipeStep):
            return Pipeline((self, other))
        elif isinstance(other, Pipeline):
            return Pipeline((self,) + other.steps)
        raise TypeError("A PipeStep can only be chained with another PipeStep or a Pipeline.")
    
    def __repr__(self) -> str:
        """Provides a developer-friendly string representation."""
        return f"PipeStep(name='{self.name}')"


# ────── Pipeline: A sequence of chained PipeSteps ───────────────────────────

@dataclass(frozen=True)
class Pipeline:
    """Represents a sequence of PipeSteps to be executed in order."""
    steps: Tuple[PipeStep, ...]
    name: Optional[str] = None
    doc: Optional[str] = None

    def __post_init__(self):
        """Sets the pipeline's docstring and name."""
        doc_to_set = self.doc
        
        # If no custom docstring is provided, generate one from the steps.
        if doc_to_set is None:
            docs_from_steps = []
            for i, step in enumerate(self.steps, 1):
                # Use the step's own name and doc attributes
                step_name = step.name or "<unnamed_step>"
                step_doc = step.doc or "No documentation."
                clean_doc = " ".join(step_doc.strip().split())
                docs_from_steps.append(f"Step {i}: {step_name}\n    {clean_doc}")

            if docs_from_steps:
                header = "Auto-generated documentation for this pipeline workflow:"
                doc_to_set = header + "\n\n" + "\n\n".join(docs_from_steps)
        
        # Set the final __doc__ and __name__ attributes on the instance
        if doc_to_set:
            object.__setattr__(self, '__doc__', doc_to_set)
        if self.name:
            object.__setattr__(self, '__name__', self.name)

    def __call__(self, data: Any) -> Any:
        """Executes all steps in the pipeline sequentially."""
        for step in self.steps:
            data = step(data)
        return data
    
    def __or__(self, other: Any) -> 'Pipeline':
        """Enables appending to the pipeline with the `|` operator."""
        if isinstance(other, PipeStep):
            return Pipeline(self.steps + (other,))
        elif isinstance(other, Pipeline):
            return Pipeline(self.steps + other.steps)
        raise TypeError("A Pipeline can only be chained with a PipeStep or another Pipeline.")
    
    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the pipeline."""
        if self.name:
            return f"Pipeline(name='{self.name}')"
        
        # Fallback for anonymous pipelines
        step_reprs = ' | '.join(step.name for step in self.steps)
        return f"Pipeline({step_reprs})"


# ────── Decorator: Turns a function into a PipeStep ───────────────────────

def step(func: Callable[[Any], Any]) -> PipeStep:
    """A decorator that converts a function into a pipeline-compatible PipeStep."""
    # The decorator now just needs to wrap the function in a PipeStep.
    # The PipeStep's __post_init__ handles the metadata.
    return PipeStep(func)