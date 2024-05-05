import json
import os


def load_json(file_path: str,) -> dict:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_json(file_path: str, data: dict,merge:bool=False):
    file_exists = os.path.exists(file_path)
    if merge:
        data_to_save = load_json(file_path)
        data_to_save.update(data)
    else:
        if file_exists:
            os.remove(file_path)
        data_to_save = data

    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'w') as f:
        json.dump(data_to_save, f)
    return data_to_save