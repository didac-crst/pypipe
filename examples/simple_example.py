# examples/simple_example.py

from pypipe import step

# 1. Define functions and convert them to PipeSteps using the @step decorator.
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

def main():
    """
    Runs the simple calculation example.
    """
    print("--- Running Simple Example ---")
    
    # 2. Create the pipeline by chaining steps with the '|' operator.
    #    This creates an anonymous pipeline object.
    calculation_pipeline = multiply_by_10 | add_3 | square
    
    # 3. Execute the pipeline with an initial value.
    initial_value = 5
    result = calculation_pipeline(initial_value)
    
    print(f"Pipeline representation: {calculation_pipeline}")
    print(f"Executing with initial value: {initial_value}")
    print(f"Final result: {result}\n")
    
    # 4. Inspect the auto-generated documentation for the pipeline.
    print("--- Auto-generated Documentation ---")
    help(calculation_pipeline)


if __name__ == "__main__":
    main()
