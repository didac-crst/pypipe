# examples/pandas_example.py

# This example requires pandas to be installed:
# pip install pandas

import pandas as pd
from pypipe import step

# 1. Define functions to process a pandas DataFrame.
#    Each function takes a DataFrame and returns a DataFrame.
@step
def filter_employees_over_30(df: pd.DataFrame) -> pd.DataFrame:
    """Keeps employees older than 30."""
    print("-> Filtering employees over 30...")
    # Use .copy() to avoid SettingWithCopyWarning
    return df[df['age'] > 30].copy()

@step
def calculate_bonus(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates a 10% bonus based on salary."""
    print("-> Calculating salary bonus...")
    df['bonus'] = df['salary'] * 0.10
    return df

@step
def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Selects and reorders columns for the final report."""
    print("-> Selecting final columns for report...")
    return df[['name', 'bonus']]

def main():
    """
    Runs the pandas DataFrame processing example.
    """
    print("--- Running Pandas DataFrame Example ---\n")
    
    # 2. Create the pipeline for generating an employee report.
    employee_report_pipeline = (
        filter_employees_over_30
        | calculate_bonus
        | select_final_columns
    )
    
    # 3. Create dummy data.
    data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 42, 31, 29],
        'salary': [60000, 85000, 72000, 55000]
    })
    
    print("Initial DataFrame:")
    print(data, "\n")
    
    print("Executing pipeline...")
    # 4. Run the DataFrame through the pipeline.
    report = employee_report_pipeline(data)
    
    print("\nFinal Report:")
    print(report)


if __name__ == "__main__":
    main()
