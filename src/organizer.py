import os


def validate_directory():
    """
    Validates the directory path provided by the user.
    Uses the user's Downloads folder if no directory is provided.
    Prompts the user again if the directory does not exist.
    """
    while True:
        directory = input("Enter the directory path to organize: ").strip()
        if directory == "":
            directory = os.path.join(os.path.expanduser("~"), "Downloads")

        if os.path.isdir(directory):
            return directory
        else:
            print("Invalid directory. Please try again.")


def get_category(filename, plan=None):
    """
    Returns the category for a filename based on its extension.
    """
    if plan is None:
        plan = get_extension_plan()

    filename = filename.lower()
    for category, extensions in plan.items():
        if any(filename.endswith(extension.lower()) for extension in extensions):
            return category

    return "Other"


def get_extension_plan():
    """
    Returns the supported file extensions for each category.
    """
    return {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],

        "Documents": [".pdf", ".docx", ".doc", ".txt", ".odt", ".rtf"],

        "Spreadsheets": [".csv", ".xlsx", ".xls", ".ods"],

        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],

        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],

        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".tar.gz"],

        "Programs": [".exe", ".msi", ".bat", ".ps1", ".py", ".cpp", ".java", ".sh", ".c"],

        "Other": []
    }


def build_plan(directory, extension_plan=None):
    """
    Builds a category-to-filenames plan from the files in a directory.
    """
    if extension_plan is None:
        extension_plan = get_extension_plan()

    categories = {}
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            category = get_category(filename, extension_plan)
            categories.setdefault(category, []).append(filename)

    return categories


def show_plan(plan, directory):
    """
    Prints each file's destination and the total number of files to move.
    """
    print("Organization Plan:")
    total_files = 0
    planned_paths = set()
    for category, filenames in plan.items():
        destination_folder = os.path.join(directory, category)
        for filename in filenames:
            source_path = os.path.join(directory, filename)
            destination_path = get_unique_path(destination_folder, filename)
            base_name, extension = os.path.splitext(filename)
            counter = 1
            while destination_path.lower in planned_paths:
                unique_filename = f"{base_name} ({counter}){extension}"
                destination_path = os.path.join(destination_folder, unique_filename)
                counter += 1
            planned_paths.add(destination_path.lower())
            print(f"{source_path} -> {destination_path}")
            total_files += 1
    print(f"Total files to move: {total_files}")
    return total_files



def get_unique_path(directory, filename):
    """
    Generates a unique file path in the specified directory to avoid overwriting existing files.
    If a file with the same name exists, appends a number to the filename.
    """
    base_name, extension = os.path.splitext(filename)
    counter = 1
    unique_path = os.path.join(directory, filename)

    while os.path.exists(unique_path):
        unique_filename = f"{base_name} ({counter}){extension}"
        unique_path = os.path.join(directory, unique_filename)
        counter += 1

    return unique_path


def organize_files(directory, category=None, plan=None):
    """
    Organizes files into category folders based on their extensions.
    Firstly shows plan, asks user for confirmation before moving files. If the user confirms, it moves the files to their respective category folders.
    If a category is provided, only files in that category are moved.
    """
    if plan is None:
        plan = build_plan(directory)
    if category is not None:
        if category not in plan:
            print(f"No files found for category '{category}'.")
            return
        selected_categories = [category]
    else:
        selected_categories = list(plan.keys())
    selected_plan = {selected_category: plan[selected_category] for selected_category in selected_categories}
    total_files = show_plan(selected_plan, directory)
    if total_files == 0:
        print("No files to move.")
        return
    confirmation = input("Do you want to proceed with moving the files? (y/n): ").strip().lower()
    if confirmation != 'y':
        print("Operation cancelled.")
        return
    moved_files = 0
    failed_files = 0
    for category, filenames in selected_plan.items():
        category_folder = os.path.join(directory, category)
        os.makedirs(category_folder, exist_ok=True)
        for filename in filenames:
            source_path = os.path.join(directory, filename)
            destination_path = get_unique_path(category_folder, filename)
            try:
                os.rename(source_path, destination_path)
                moved_files += 1
            except Exception as e:
                print(f"Failed to move {source_path} to {destination_path}: {e}")
                failed_files += 1

    print("\nOrganization complete.")
    print(f"Total files moved: {moved_files}")
    print(f"Total files failed to move: {failed_files}")


def print_summary(directory, category):
    """
    Prints a summary of the organization process.
    """
    category_folder = os.path.join(directory, category)
    print(f"\nFiles have been organized into the '{category}' folder: {category_folder}")


if __name__ == "__main__":
    directory = validate_directory()
    plan = build_plan(directory)
    show_plan(plan, directory)