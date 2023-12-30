import shutil
from os import listdir, makedirs
from os import path


# removes all files in the directory
def clean_directory(dir_path):
    shutil.rmtree(dir_path, ignore_errors=True)
    makedirs(dir_path)


def format_input_directory_path(input_directory: str) -> str:
    input_directory = path.join(
        input_directory, ""
    )  # to check if it ends in a /, and if not add the / to it.
    return input_directory


def get_files_in_input_directory(input_directory: str):
    filesInInputDirectory = [
        input_directory + fileName for fileName in listdir(input_directory)
    ]
    filesToEncode = filter(path.isfile, filesInInputDirectory)  # exclude folders
    return filesToEncode
