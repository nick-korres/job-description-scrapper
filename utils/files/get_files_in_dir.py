import os


def get_files_in_dir(directory)->list[str]:
    return [item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item)) and item.endswith('.txt')]