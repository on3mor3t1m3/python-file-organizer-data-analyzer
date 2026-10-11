import argparse
import os

from src.organizer import build_plan, validate_directory, show_plan, organize_files

from src.analyzer import load_csv, get_basic_info, get_numeric_stats, save_json_report, save_txt_report

def organize_command(directory):
    """
    Handles the 'organize' command.
    """
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist or is not accessible.")
        return

    plan = build_plan(directory)
    
    if plan is None:
        print("No files found to organize.")
        return
    organize_files(directory, plan = plan)

def analyze_command(csv_path, output_format):
    """
    Handles the 'analyze' command.
    """
    if not os.path.isfile(csv_path):
        print(f"Error: The file '{csv_path}' does not exist or is not accessible.")
        return
    
    try:
        df = load_csv(csv_path)
        df = load_csv(csv_path)
        basic_info = get_basic_info(df)
        numeric_stats = get_numeric_stats(df)

        report = {
                "basic_info": basic_info,
                "numeric_stats": numeric_stats
                }

        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

        os.makedirs(reports_dir, exist_ok=True)

        json_path = os.path.join(reports_dir, "report.json")
        txt_path = os.path.join(reports_dir, "report.txt")

        save_json_report(report, json_path)
        save_txt_report(report, txt_path)
        print(f"Organization complete. Report saved in both JSON and TXT formats.")
    except Exception as error:
        print(f"Error during analysis: {os.error}")

def main():
    parser = argparse.ArgumentParser(description="File Organizer and Analyzer")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for the 'organize' command
    organize_parser = subparsers.add_parser("organize", help="Organize files in a directory")
    organize_parser.add_argument("directory", type=str, help="Path to the directory to organize")

    # Subparser for the 'analyze' command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a CSV file")
    analyze_parser.add_argument("csv_path", type=str, help="Path to the CSV file to analyze")
    analyze_parser.add_argument("--output-format", type=str, choices=["json", "txt"], default="json",
                                help="Output format for the report (default: json)")

    args = parser.parse_args()

    if args.command == "organize":
        organize_command(args.directory)
    elif args.command == "analyze":
        analyze_command(args.csv_path, args.output_format)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()