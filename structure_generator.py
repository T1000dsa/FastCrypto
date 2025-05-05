import os
from pathlib import Path

def print_structure(startpath, max_level=10, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = {"__pycache__", "venv", ".git", ".idea"}
    
    for root, dirs, files in os.walk(startpath):
        level = root.count(os.sep)
        if level > max_level:
            continue
            
        dirs[:] = [d for d in dirs if d not in ignore_dirs]  # Modify in-place
        
        indent = "    " * (level)
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = "    " * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    project_root = Path(__file__).parent
    print_structure(project_root)