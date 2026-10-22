
from get_specific_type_of_file import get_file
from config_path import ANNOTATION_PATH



path = ANNOTATION_PATH

get_file(path= path, specificType="*.types.yml")
number = 0
#If the scripts fails it is probably the path.
for file in path:
    name = file.name
    counts = name.count("_")
    if counts < 3:
        print(file)
        number+= 1
print(f"The amount of full videos is {number}. As they have no time stamp.")
print(f"The amount of clips is { 119 - number }.")

#The script tells us the amount of full video based on the name of the annotation file.
