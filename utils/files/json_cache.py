import json
import os


def load_json(file: str,) -> dict:
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_json(file: str, data: dict,merge:bool=False):
    if merge:
        data_to_save = load_json(file)
        data_to_save.update(data)
    else:
        if os.path.exists(file):
            os.remove(file)
        data_to_save = data

    with open(file, 'w') as f:
        json.dump(data_to_save, f)
    return data_to_save