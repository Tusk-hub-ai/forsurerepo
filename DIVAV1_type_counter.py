
from get_specific_type_of_file import get_file
from config_path import ANNOTATION_PATH

path = ANNOTATION_PATH
types = ["*.activities.yml", "*.geom.yml", "*.types.yml", "*.regions.yml"]
counts = {}

for pattern in types:
    count = 0
    for file in get_file(path=path,specificType=pattern):
        #rglob stands for recursive glob, it checks every folder/files in the path for a patern.
        count += 1
    counts[pattern] = count
count_files = 0    


print(counts)
print(sum(counts.values()))



# The file checks the number of files for each type and also return the number of files in the folder. 
