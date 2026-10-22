import pandas as pd
import yaml
from get_specific_type_of_file import get_file
from config_path import ANNOTATION_PATH


path = ANNOTATION_PATH

def types_file(data):
    rows = []
    for row in data:
        if "meta" in row:
            continue
        else:
            types = row["types"]["id1"]
            #id1 is the id of the type of the object, all types have one unique id object key.
            namel = list(row["types"]["cset3"].keys())
            name = namel[0]
            rows.append({"object_id": types , "type" : name})
    return pd.DataFrame(rows)
    # retreives id and the type name and puts it in a dataframe           
          
def statfunctions(table :  pd.DataFrame):
    #tells the function what the variable will be
    n_objects = len(table)
    per_type = table["type"].value_counts()

    print(f"Objects: {n_objects}")
    print(f"Objects per type:\n{per_type}")

def main():
    tables = []

    for file in get_file(path=path,specificType="*.types.yml"):
        with open(file) as f:
            data = yaml.load(f, Loader=yaml.CSafeLoader) 
            #each opened file goes through yaml which makes a list of dictionnaries
            table = types_file(data)
            table["singular video"] = file.name.replace(".types.yml", "")
            tables.append(table)

    tables_concat = pd.concat(tables, ignore_index= True)
    statfunctions(tables_concat)

if __name__ == "__main__":
    main()