import os
import pandas as pd
from collections import defaultdict
import json
import numpy as np

def load_csv(file_path):
    """
    Loads a CSV file into a pandas DataFrame and checks for errors.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def get_basic_info(df):
    """
    Extracts basic information from the DataFrame.
    """
    return {
        "num_rows": df.shape[0],
        "num_columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "skipped_rows": df.isnull().sum().to_dict(),
        "duplicate_rows": int (df.duplicated().sum())
    }

def get_numeric_stats(df):
    """
    Computes basic statistics for numeric columns in the DataFrame.
    """
    if df.empty:
        return {}
    
    numeric_df = df.select_dtypes(include=['number'])
    stats = {}
    
    for column in numeric_df.columns:
        stats[column] = {
            "mean": numeric_df[column].mean(),
            "median": numeric_df[column].median(),
            "std_dev": numeric_df[column].std(),
            "min": numeric_df[column].min(),
            "max": numeric_df[column].max()
        }
    
    return stats

def save_json_report(report, output_path):
    """
    Saves the report dictionary as a JSON file.
    """
    try:
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=4, 
                      default = lambda value: value.item()
                      if isinstance(value, np.generic)
                        else str(value))
        print(f"Report saved to {output_path}")
    except Exception as e:
        print(f"Error saving report: {e}")

def save_txt_report(report, output_path):
    """
    Saves the report dictionary as a text file.
    """
    try:
        with open(output_path, 'w') as f:
            for key, value in report.items():
                f.write(f"{key}: {value}\n")
        print(f"Report saved to {output_path}")
    except Exception as e:
        print(f"Error saving report: {e}")

if __name__ == "__main__":
    # Example usage
    csv_path = "C:\\Python_data_organizer\\test_files\\test_data.csv"  # Replace with your CSV file path
    df = load_csv(csv_path)
    
    basic_info = get_basic_info(df)
    numeric_stats = get_numeric_stats(df)
    
    report = {
        "basic_info": basic_info,
        "numeric_stats": numeric_stats
    }
    save_json_report(report, "report.json")
    save_txt_report(report, "report.txt")