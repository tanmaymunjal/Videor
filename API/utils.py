import os
from pathlib import Path


def check_file_exists(file_path: str):
    return os.path.isfile(file_path)


def create_needed_folders():
    needed_folders = [
        "Videos/",
        "Segments/",
        "Thumbnails/",
        "Audios/",
        "TrancodedVideos/",
    ]
    for needed_folder in needed_folders:
        Path(needed_folder).mkdir(parents=True, exist_ok=True)
