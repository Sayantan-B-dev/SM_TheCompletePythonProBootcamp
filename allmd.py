import os
import shutil

# CONFIGURATION SECTION

# Root directory from where scanning starts
ROOT_DIRECTORY = os.getcwd()

# Base output directory
OUTPUT_DIRECTORY = os.path.join(ROOT_DIRECTORY, "AllMd")

# Subdirectory for coding exercise files
EXERCISES_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "exercises")

# Folder names to ignore during traversal
IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".idea",
    ".vscode",
    "dist",
    "build"
}

# Multiple patterns to detect exercise/assignment files
EXERCISE_PATTERNS = [
    "_-_Coding_Exercise_",
    "_-_Assignment_"
]

# CORE FUNCTION

def collect_markdown_files():
    """
    Traverse root directory recursively,
    copy .md files into AllMd/,
    route exercise/assignment files into AllMd/exercises/,
    and ignore any README-related markdown files.
    """

    # Ensure both output directories exist
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    os.makedirs(EXERCISES_DIRECTORY, exist_ok=True)

    # Separate counters to avoid naming collisions per destination
    root_file_counter = {}
    exercise_file_counter = {}

    for current_path, directory_names, file_names in os.walk(ROOT_DIRECTORY):

        # Skip ignored directories efficiently
        directory_names[:] = [
            d for d in directory_names if d not in IGNORED_DIRECTORIES
        ]

        for file_name in file_names:

        
            # FILE FILTERING
        

            # Process only markdown files
            if not file_name.lower().endswith(".md"):
                continue

            # Ignore any README files (case-insensitive)
            if "readme" in file_name.lower():
                continue

            source_file_path = os.path.join(current_path, file_name)

        
            # ROUTING DECISION
        

            # Check if file matches any exercise pattern
            if any(pattern in file_name for pattern in EXERCISE_PATTERNS):
                destination_directory = EXERCISES_DIRECTORY
                counter_dict = exercise_file_counter
            else:
                destination_directory = OUTPUT_DIRECTORY
                counter_dict = root_file_counter

        
            # DUPLICATE HANDLING
        

            if file_name in counter_dict:
                counter_dict[file_name] += 1
                name, extension = os.path.splitext(file_name)
                new_file_name = f"{name}_{counter_dict[file_name]}{extension}"
            else:
                counter_dict[file_name] = 1
                new_file_name = file_name

            destination_file_path = os.path.join(destination_directory, new_file_name)

        
            # FILE COPY OPERATION
        

            shutil.copy2(source_file_path, destination_file_path)

            print(f"Copied: {source_file_path} → {destination_file_path}")


# ENTRY POINT

if __name__ == "__main__":
    collect_markdown_files()