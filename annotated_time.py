
from get_specific_type_of_file import get_file
from config_path import ANNOTATION_PATH



path = ANNOTATION_PATH


def time():
    numbers = 0
    for file in get_file(path=path,specificType="*.types.yml"):
        if len(file.name) > 40:# if it goes here it is a clip
            number = int(file.name[25:31]) - int(file.name[18:24])
            numbers += number
        else: # full video / no timestamp in the name
            geom = file.with_name(file.name.replace(".types.yml", ".geom.yml"))
            # third line in a geam file shows the frames in the file
            with open(geom) as g:
                line = [g.readline() for _ in range(3)][2]
            numbers += float(line.split("timestamp:")[1].split()[1])
    minutes = numbers/60
    print(f"{minutes} minutes")
    rest = int(minutes % 60)
    hours = int(minutes // 60)
    print(f"{hours}:{rest}  hours and minutes") 

def main():
    time()
main()
    