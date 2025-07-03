# examples/lambda_example.py

# This example demonstrates how to use lambda functions within a pipeline.
# It shows how to give explicit names to lambda-based steps for better
# representation and auto-documentation.

from pypipe import PipeStep, step

# 1. Define a regular, decorated function to mix with our lambdas.
@step
def to_string_report(x: int) -> str:
    """Formats the final number into a report string."""
    return f"Final Report Value: {x}"

def main():
    """
    Runs the lambda function example.
    """
    print("--- Running Lambda Function Example ---")

    # 2. Create a pipeline that uses lambda functions for simple, one-off steps.
    #    We wrap them in PipeStep and provide an explicit `name` for clarity.
    #    Without a `name`, they would appear as '<lambda>' in the output.
    calculation_pipeline = (
        PipeStep(lambda x: x + 100, name="add_100")
        | PipeStep(lambda x: x // 2, name="halve_integer")
        | to_string_report
    )
    
    # 3. Execute the pipeline with an initial value.
    initial_value = 50
    result = calculation_pipeline(initial_value)
    
    print(f"\nPipeline representation: {calculation_pipeline}")
    print(f"Executing with initial value: {initial_value}")
    print(f"Final result: '{result}'\n")
    
    # 4. Inspect the auto-generated documentation for the pipeline.
    #    Notice how the names for the lambda steps appear correctly.
    print("--- Auto-generated Documentation for Lambda Pipeline ---")
    help(calculation_pipeline)


if __name__ == "__main__":
    main()
