from settings.directories import Dirs
import os

out_dir = Dirs.OUT_SEARCH

def create_dir(dir_name,path = out_dir)->str:
    if dir_name=="":
        dir_name="empty_string"
        
    full_path = build_dir_name(dir_name,path)
    import os
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return full_path

def build_dir_name(dir_name,path = out_dir)->str:
    full_path = path+dir_name.lower().replace(" ","_")+"/"
    return full_path