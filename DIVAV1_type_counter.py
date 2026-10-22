from pathlib import Path

path = Path(r"C:\exercices\dataretriever\viratannotations")
# This must be YOUR local path to the DIVA V1 annotations.

types = ["*.activities.yml", "*.geom.yml", "*.types.yml", "*.regions.yml"]
counts = {}

for pattern in types:
    count = 0
    for file in path.rglob(pattern):
        #rglob stands for recursive glob, it checks every folder/files in the path for a patern.
        count += 1
    counts[pattern] = count
count_files = 0    


print(counts)
print(sum(counts.values()))



# The file checks the number of files for each type and also return the number of files in the folder. 