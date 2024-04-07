import os


def delete_files_in_directory(directory:str="./temp/",file_names: list[str] = None):

    file_list = os.listdir(directory) if file_names is None else file_names

    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")