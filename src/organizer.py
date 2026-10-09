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

    return "Others"


def get_categories(directory, plan=None):
    """
    Groups files in a directory by their extension-based category.
    """
    return build_plan(directory, plan)


def get_extension_plan():
    """
    Returns the supported file extensions for each category.
    """
    return {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xlsx", ".xls", ".csv", ".ppt", ".pptx"],
        "Videos": [".mp4", ".avi", ".mov", ".mkv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
        "Archives": [".zip", ".rar", ".tar.gz"],
        "Others": []
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
    print("\nOrganizing Plan:")
    total_files = 0
    for category, filenames in plan.items():
        for filename in filenames:
            destination = os.path.join(directory, category)
            print(f"{filename} -> {destination}")
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
    If a category is provided, only files in that category are moved.
    """
    if plan is None:
        plan = build_plan(directory)

    selected_categories = [category] if category is not None else plan
    for selected_category in selected_categories:
        category_folder = os.path.join(directory, selected_category)
        os.makedirs(category_folder, exist_ok=True)

        for filename in plan.get(selected_category, []):
            file_path = os.path.join(directory, filename)
            new_path = get_unique_path(category_folder, filename)
            os.rename(file_path, new_path)
            print(f"Moved: {filename} -> {category_folder}")


def print_summary(directory, category):
    """
    Prints a summary of the organization process.
    """
    category_folder = os.path.join(directory, category)
    print(f"\nFiles have been organized into the '{category}' folder: {category_folder}")