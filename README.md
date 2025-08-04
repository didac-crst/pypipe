[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

# PyPipe: Functional Pipelines in Python

**_🧠 “Because functional flow shouldn’t look like a pipe full of spaghetti.”_**

> It started with a small script. Just a few transformations.  
> Then it grew.
>
> At first, it was just one nested function call:
> 
> ```python
> result = square(add_3(multiply_by_10(5)))
> ```
>
> Okay, not ideal — but manageable.
>
> Then the real world showed up.  
> Different inputs, conditionals, new edge cases… and suddenly the script looked like this:
>
> ```python
> # normalize first
> step1 = normalize(data)
>
> # maybe validate here?
> # step2 = validate(step1)
>
> step3 = enrich(step1)
> step4 = transform(step3)
>
> # whoops, where's step2 used?
> final = finalize(step4)  # ???
> ```
>
> Variables everywhere. Half of them unused. The other half overwritten.  
> Some steps commented out with mysterious TODOs from past-me.  
> The whole thing worked — *until I touched it.*
>
> At some point, it stopped feeling like programming and started feeling like excavating.
>
> That’s when `PyPipe` was born — a way to turn messy transformation chains into clean, readable pipelines.  
> With the `|` operator, every step flows left to right, just like thoughts do:
>
> ```python
> result = normalize | enrich | transform | finalize
> ```
>
> Now the logic is visible.  
> The pipeline is self-documenting.  
> No more `var_2 = func(var_1)` copy-pasta, no more “what was step4 again?”, and no more commented-out relics from the past.
>
> Just clean, functional pipes — the way it should’ve been from the start.

---

## Why PyPipe?

If you're tired of tangled logic and love clean, readable code, PyPipe offers a no-boilerplate, dependency-free way to structure your data flows functionally — and clearly.

---

## Key Features

- **Readable & Intuitive:** Chain functions with the `|` operator for a natural, left-to-right data flow.
- **Reusable Components:** Each function (`PipeStep`) and every complete workflow (`Pipeline`) is a reusable object.
- **Self-Documenting:** Pipelines automatically generate docstrings from their components, making them easy to inspect with `help()`.
- **Flexible:** Works with any function, including `lambdas`, and can be used for any data type, from simple numbers to complex pandas DataFrames.
- **Lightweight:** A single, dependency-free file that you can drop into any project.

---

## Installation

To use it, simply import the `pypipe` module (containing the `PipeStep`, `Pipeline`, and `step` definitions) into your project:

```python
from pypipe import PipeStep, Pipeline, step
```

---

## Quick Start

Transform complex nested calls into a clean, linear pipeline.

**Before (Spaghetti Code):**

```python
# Hard to read, executes "inside-out"
result = square(add_3(multiply_by_10(5)))
```

**After (Using PyPipe):**

```python
from pypipe import step

@step
def multiply_by_10(x):
    """Multiplies the input by 10."""
    return x * 10

@step
def add_3(x):
    """Adds 3 to the input."""
    return x + 3

@step
def square(x):
    """Squares the input."""
    return x ** 2

# 1. Create the pipeline by chaining steps
calculation_pipeline = multiply_by_10 | add_3 | square

# 2. Execute the pipeline
result = calculation_pipeline(5)

print(f"Pipeline: {calculation_pipeline}")
print(f"Result: {result}")
# Expected Output:
# Pipeline: Pipeline(multiply_by_10 | add_3 | square)
# Result: 2809
```

You can even inspect the anonymous pipeline you just created:

```python
help(calculation_pipeline)
# This will print a neatly formatted, auto-generated docstring!
```

---

## Advanced Usage

### 1. Processing Pandas DataFrames

`PyPipe` is perfect for creating readable data cleaning and transformation workflows with pandas.

```python
import pandas as pd
from pypipe import step

@step
def filter_employees_over_30(df: pd.DataFrame) -> pd.DataFrame:
    """Keeps employees older than 30."""
    return df[df['age'] > 30].copy()

@step
def calculate_bonus(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates a 10% bonus based on salary."""
    df['bonus'] = df['salary'] * 0.10
    return df

@step
def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Selects and reorders columns for the final report."""
    return df[['name', 'bonus']]

# Create the pipeline
employee_report_pipeline = (
    filter_employees_over_30
    | calculate_bonus
    | select_final_columns
)

# Dummy data
data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 42, 31],
    'salary': [60000, 85000, 72000]
})

# Run the DataFrame through the pipeline
report = employee_report_pipeline(data)
print(report)
```

### 2. Creating Named and Documented Pipelines

For complex, reusable workflows, you can create a named `Pipeline` object with a high-level docstring.

```python
from pypipe import Pipeline, PipeStep

# Assume multiply_by_10, add_3, and square are defined as PipeSteps
calculation_workflow = Pipeline(
    steps=(multiply_by_10, add_3, square),
    name="standard_calculation",
    doc="A workflow that performs the standard calculation: (x * 10 + 3)^2."
)

print(calculation_workflow)
# Output: Pipeline(name='standard_calculation')

help(calculation_workflow)
# Shows the custom docstring you provided.
```

### 3. Using `lambda` Functions

You can easily use `lambda` functions for simple, one-off steps by wrapping them in a `PipeStep` and giving them an explicit name.

```python
from pypipe import PipeStep, step

@step
def square(x): return x**2

# Create a pipeline with named lambdas
data_pipeline = (
    PipeStep(lambda x: x * 10, name="multiply_by_10")
    | PipeStep(lambda x: x + 3, name="add_3")
    | square
)

print(data_pipeline)
# Output: Pipeline(multiply_by_10 | add_3 | square)
```

---

## API Reference

- **`@step` (decorator)**
  Converts a standard Python function into a `PipeStep` instance, making it chainable with `|`.

- **`PipeStep(func, name=None, doc=None)` (class)**
  A wrapper for a single callable.
  - `func`: The function to execute.
  - `name` (optional): An explicit name for the step. Defaults to `func.__name__`.
  - `doc` (optional): An explicit docstring. Defaults to `func.__doc__`.

- **`Pipeline(steps, name=None, doc=None)` (class)**
  An ordered collection of `PipeStep` objects.
  - `steps`: A tuple of `PipeStep` instances.
  - `name` (optional): A high-level name for the entire pipeline.
  - `doc` (optional): A high-level docstring for the pipeline. If not provided, one is generated from its steps.

---

## Running the Test Suite

PyPipe ships with a lightweight pytest suite.  
If you’ve cloned the repo and want to verify everything works locally:

```bash
# Install library + dev dependencies (pytest, etc.)
poetry install --with dev

# Execute all tests
poetry run pytest -q
```

---

## Contributing

Contributions are welcome! If you have suggestions for improvements or find a bug, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
