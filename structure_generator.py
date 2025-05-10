import os
from pathlib import Path

def print_structure(startpath, max_level=10, ignore_dirs=None, full=False):
    if ignore_dirs is None:
        ignore_dirs = {"__pycache__", "venv", ".git", ".idea", "versions", "migrations", "frontend", "poetry.lock", "pyproject.toml"}

    if full:
        with open('structure_generator_result.txt', 'w') as file_x:
            file_x.write('')
    
    for root, dirs, files in os.walk(startpath):
        level = root.count(os.sep)
        if level > max_level:
            continue
            
        dirs[:] = [d for d in dirs if d not in ignore_dirs]  # Modify in-place
        
        indent = "    " * (level)

        subindent = "    " * (level + 1)

        if full:
            with open('structure_generator_result.txt', 'a+') as file_main:
                data_file = []
                data_file.append(f"{indent}{os.path.basename(root)}/")
                for f in files:

                    if f in ignore_dirs:
                        continue
                    
                    data_file.append(f"{subindent}{f}")
                    data_file.append(f"##{f}##")
                    file_root = f"{root}\\{f}"
                    with open(file_root) as file:
                        data_file.append(str(file.read()))
                    data_file.append(f"##{f}##")

                    for i in data_file:
                        file_main.write(i)

                    data_file.clear()
        else:
            print(f"{indent}{os.path.basename(root)}/")
            for f in files:
                if f in ignore_dirs:continue
                print(f"{subindent}{f}") 

            
if __name__ == "__main__":
    project_root = Path(__file__).parent
    print_structure(project_root)