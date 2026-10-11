# Python File Organizer & Data Analyzer

A Python command-line application for organizing files by type and analyzing CSV datasets. The application automatically categorizes files, calculates basic dataset statistics, detects missing values and duplicate rows, and generates JSON and TXT reports.

## Features

### File Organizer

* Organizes files into folders based on their extensions.
* Supports different file categories.
* Handles files with unknown or missing extensions.
* Prevents overwriting existing files by generating unique filenames.
* Displays an organization plan before moving files.

### CSV Data Analyzer

* Reads and analyzes CSV files using pandas.
* Reports the number of rows and columns.
* Lists column names.
* Counts missing values in each column.
* Detects duplicate rows.
* Calculates statistics for numeric columns:

  * Mean
  * Median
  * Standard deviation
  * Minimum
  * Maximum
* Handles datasets without numeric columns and CSV files containing column headers but no data rows.

### Reports

* Generates JSON reports for structured data.
* Generates TXT reports for convenient reading.
* Saves reports in the `reports/` directory.

## Technologies

* Python
* pandas
* argparse
* unittest
* JSON

## Project Structure

```text
Python_data_organizer/
├── src/
│   ├── __init__.py
│   ├── organizer.py
│   └── analyzer.py
├── tests/
│   ├── test_organizer.py
│   └── test_analyzer.py
├── examples/
│   ├── sample.csv
│   ├── text_only.csv
│   └── empty.csv
├── reports/
├── cli.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Python_data_organizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run commands from the project's root directory.

### Organize files

```bash
python cli.py organize "C:\path\to\your\folder"
```

The application displays a plan and asks for confirmation before moving files.

### Analyze a CSV file

```bash
python cli.py analyze "examples\sample.csv"
```

The generated reports are saved to:

```text
reports/report.json
reports/report.txt
```

### Analyze a CSV without numeric columns

```bash
python cli.py analyze "examples\text_only.csv"
```

### Analyze a CSV containing only column headers

```bash
python cli.py analyze "examples\empty.csv"
```

The analyzer reports the available columns even when the dataset contains no data rows.

## Running Tests

Run the automated test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover file categorization, organization plans, filename conflicts, dataset statistics, missing values, duplicate rows, and empty datasets.

## Example Output

A JSON report contains basic dataset information and numeric statistics:

```json
{
    "basic_info": {
        "num_rows": 6,
        "num_columns": 4,
        "column_names": ["Name", "Age", "Salary", "City"],
        "skipped_rows": {
            "Name": 0,
            "Age": 1,
            "Salary": 1,
            "City": 0
        },
        "duplicate_rows": 1
    },
    "numeric_stats": {
        "Age": {
            "mean": 23.4,
            "median": 24.0,
            "min": 21,
            "max": 25
        }
    }
}
```

*Note: The exact report contents depend on the input CSV file.*

## Future Improvements

* Add logging for file operations and analysis errors.
* Support additional input formats.
* Add more automated tests.
* Improve report formatting and customization.

## License

This project is available for educational and portfolio purposes.
