import os


def validate_directory():
    """
    Validates the directory path provided by the user.
    Uses the user's Downloads folder if no directory is provided.
    Prompts the user again if the directory does not exist.
    """
    while True:
        directory = input("Enter the directory path to organize: ").strip()
        if not directory:
            directory = os.path.join(os.path.expanduser("~"), "Downloads")

        if os.path.isdir(directory):
            return directory


def get_category():
    """
    Prompts the user to select a category for organizing files.
    Returns the selected category as a string.
    """
    categories = {
        "1": "Images",
        "2": "Documents",
        "3": "Videos",
        "4": "Music",
        "5": "Archives",
        "6": "Others"
    }

    print("Select a category to organize files:")
    for key, value in categories.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Enter the number corresponding to your choice: ").strip()
        if choice in categories:
            return categories[choice]
        else:
            print("Invalid choice. Please try again.")


def build_plan():
    """
    Builds a plan for organizing files based on user input.
    Returns a dictionary mapping categories to their respective file extensions.
    """
    plan = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Videos": [".mp4", ".avi", ".mov", ".mkv"],
        "Music": [".mp3", ".wav", ".aac"],
        "Archives": [".zip", ".rar", ".tar.gz"],
        "Others": []
            }
    return plan


def show_plan(plan):
    print ("\nOrganizing Plan:")
    for category, extensions in plan.items():
        print (f"{category}: {', '.join(extensions) if extensions else 'no specific extensions'}")


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


def organize_files(directory, category, plan):
    """
    Organizes files in the specified directory based on the selected category and plan.
    Moves files to their respective category folders.
    """
    category_folder = os.path.join(directory, category)
    os.makedirs(category_folder, exist_ok=True)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in plan[category]:
                new_path = os.path.join(category_folder, filename)
                os.rename(file_path, new_path)
                print(f"Moved: {filename} -> {category_folder}")


def print_summary(directory, category):
    """
    Prints a summary of the organization process.
    """
    category_folder = os.path.join(directory, category)
    print(f"\nFiles have been organized into the '{category}' folder: {category_folder}")