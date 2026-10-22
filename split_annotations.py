
from config_path import ANNOTATION_PATH
from get_specific_type_of_file import get_file

path = get_file(path=ANNOTATION_PATH, specificType="*.types.yml")

parent_folder = {}


for file in path:
    key = file.parent
    value = 1
    if key in parent_folder.keys():
        parent_folder[key] += 1
    else:
        parent_folder[key] = 1
        



print(parent_folder)