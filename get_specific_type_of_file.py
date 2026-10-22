

import pathlib 



path_annotation_new = r"C:\exercices\dataretriever\viratannotations"
#Put your local path here

def get_file(path, specificType = "*.types.yml"):
      files = [file for file in pathlib.Path(path).rglob(pattern=specificType)]
      return files