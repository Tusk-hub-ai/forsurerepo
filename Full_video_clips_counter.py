from pathlib import Path

number = 0
path = Path(r"C:\exercices\dataretriever\viratannotations").rglob( pattern= "*types.yml")
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