# safety/folder_analyzer.py

import os
from datetime import datetime


def format_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def analyze_folder(folder_path):

    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    total_size = 0
    total_files = 0
    files_list = []

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            fp = os.path.join(root, file)

            try:
                size = os.path.getsize(fp)
                total_size += size
                total_files += 1
                files_list.append((file, size))
            except:
                pass

    created = datetime.fromtimestamp(os.path.getctime(folder_path))

    print("\n📂 Folder Analysis")
    print("────────────────────────")
    print("Folder :", folder_path)
    print("Created:", created)
    print("Files  :", total_files)
    print("Size   :", format_size(total_size))

    if files_list:
        print("\nFiles inside:")
        for name, size in files_list[:10]:
            print(f"  {name} ({format_size(size)})")

    print("────────────────────────")