import os

def get_directory_tree(start_path, prefix="", ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = {"env", ".git", "__pycache__", "build"}  # Набор игнорируемых директорий
    
    items = os.listdir(start_path)
    files = []
    folders = []

    for item in items:
        path = os.path.join(start_path, item)
        if os.path.isdir(path) and item not in ignore_dirs:
            folders.append(item)
        elif os.path.isfile(path):
            files.append(item)

    for folder in folders:
        print(f"{prefix}├── {folder}/")
        get_directory_tree(os.path.join(start_path, folder), prefix + "│   ", ignore_dirs)

    for i, file in enumerate(files):
        connector = "└── " if i == len(files) - 1 else "├── "
        print(f"{prefix}{connector}{file}")

if __name__ == "__main__":
    start_path = "."  # Путь к директории, например, "./my_project"
    print(f"Directory tree for '{os.path.abspath(start_path)}':")
    get_directory_tree(start_path)