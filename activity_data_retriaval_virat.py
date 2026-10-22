
import yaml
from config_path import ANNOTATION_PATH
from get_specific_type_of_file import get_file
path = get_file(path=ANNOTATION_PATH, specificType="*.activities.yml")



activity_types =  {}
activity_time = {}
total_activities = 0



for file in path:
    with open(file) as f:
        reader = yaml.load(f,Loader=yaml.CSafeLoader)
        for row in reader:
            if "meta" in row:
                continue
            elif "act" in row:
                total_activities += 1
                action = list(row["act"]["act2"].keys())[0]
                activity_types[action] = activity_types.get(action, 0) + 1
                #Retrieves information about the type of activity
                # act2 is a dict {activity_name: confidence}, e.g. {"Talking": 1.0}.
                # The activity name is stored as the KEY, not the value.
                # .keys() returns a view that cannot be indexed, so we convert it to a list
                # (["Talking"]) and take its first and only element with [0] -> "Talking".
                start, end = row["act"]["timespan"][0]["tsr0"]
                activity_time[action] = activity_time.get(action, 0) + (end - start + 1)
                #Retrieves information about the how long the specific activity is.
                # timespan is a list of time spans, e.g. [{"tsr0": [3480, 3600]}].
                # [0] takes the first (and in this dataset only) span out of the list,
                # ["tsr0"] takes the [start, end] frame range out of that dict
                # (tsr0 = time span range in frame numbers, not seconds).
                # The two values are unpacked into start and end.


print(f"{total_activities} is the number of unique id activities in the annotations")
print(f"{len(activity_types)} is the number of different activities found in the annotations")
print(sum(activity_types.values())== total_activities)
print("\nunique activities for each categories: ")
print(sorted(activity_types.items(), key=lambda pair: pair[1], reverse=True))
print("\ntotal amount of activities in frames:")
print(sum(activity_time.values()))
print("in minutes")
print((sum(activity_time.values())//30)//60)
print("in hours")
print((sum(activity_time.values())//30)//3600)
print("\nframes for each activity categorie:")
print(sorted(activity_time.items(), key=lambda pair: pair[1], reverse=True))