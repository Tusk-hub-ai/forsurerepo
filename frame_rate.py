
import yaml
from get_specific_type_of_file import get_file
from config_path import ANNOTATION_PATH

path = get_file(path=ANNOTATION_PATH,specificType="*.geom.yml")
count = 0
for file in path:
    count += 1
    with open(file) as f:
        for line in f:
            reader = yaml.load(line, Loader=yaml.CSafeLoader)
            row = reader[0]
            if "meta" in row :
                    continue
            elif "geom" in row and row["geom"]["ts0"] == 0:
                    continue
            else :

                    if row["geom"]["ts0"] / row["geom"]["ts1"] <29 or  row["geom"]["ts0"] / row["geom"]["ts1"] > 31:
                        print(f"FrameRate smaller then 29 on {file} or over 31.")
                        break
                    break
print(f"number of checked files for a frame rate of 30 :{count}")
# Goes through all the files to check frame rate, It does not finish if frame is not between 29 -31. Final number should be 119.