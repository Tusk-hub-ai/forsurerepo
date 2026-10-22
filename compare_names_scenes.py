

from collections import Counter, defaultdict
from config_path import ANNOTATION_PATH, DATASET
from get_specific_type_of_file import get_file



PREFIX = "VIRAT_S_"
#Every video starts with this prefix in the dataset

def annotation_names(ANNOTATION_PATH):
    names = {}
    for f in get_file(path = ANNOTATION_PATH,specificType= "*.types.yml"):
        names[f.name.replace(".types.yml", "")] = f.parent.name
    return names
#makes a dictionary to find out where a file comes from


def dataset_names(DATASET):
    """name -> where it was found (folder or zip archive)."""
    names = {}
    for f in get_file(path=DATASET,specificType="*"):
        if not f.is_file():
            continue
        if f.suffix.lower() == ".mp4":
            names[f.stem] = f.parent.name

    return names
#makes a dictionary to find out where a file comes from

def site(name):
    return name[8:10]


def view(name):
    return name[8:12]


def scene_report(title, names, splits=None):
    print(f"\n=== {title} ===")
    print(f"Videos: {len(names)}")

    # map applies site() to every video name, giving its 2-digit site code ("00", "00", "01", ...).
    # set removes the duplicates, so only the different sites remain.
    # len(sites) is therefore the number of distinct sites, not the number of videos.
    sites = set(map(site, names))
    print(f"Sites (first 2 digits): {len(sites)} -> {sorted(sites)}")

    # map applies view() to every video name, giving its 4-digit view code.
    # Counter counts how often each view occurs, e.g. {"0002": 14, "0100": 9}:
    # a dict of view -> number of videos.
    views = Counter(map(view, names))
    print(f"Camera views (first 4 digits): {len(views)}")
    for v, count in sorted(views.items()):
        print(f"   {v}: {count} videos")

    if splits:
        # defaultdict(set) is a dict that creates an empty set the first time a key is used,
        # so .add() works without first checking whether the split exists.
        # Result: {"train": {views in train}, "validate": {views in validate}}.
        # Using sets means each view is stored once per split, however many videos it has.
        per_split = defaultdict(set)
        for n in names:
            per_split[splits[n]].add(view(n))
        for s, v in sorted(per_split.items()):
            print(f"Views in {s}: {len(v)} -> {sorted(v)}")
        if len(per_split) == 2:
            a, b = per_split.values()
            # a & b is the set intersection: views present in both train and validate.
            # Shared views mean validation is not fully unseen data (same scenes as training).
            print(f"Views in BOTH splits: {len(a & b)} -> {sorted(a & b)}")


def main():
    ann = annotation_names(ANNOTATION_PATH)
    data = dataset_names(DATASET)
    if not ann:
        print("No *.types.yml found - check ANNOTATIONS path.")
        return
    if not data:
        print("No .mp4 videos found (unpacked or in zip) - check DATASET path.")
        return
    #   Check for right paths
    both = set(ann) & set(data)
    missing_video = sorted(set(ann) - set(data))
    not_annotated = sorted(set(data) - set(ann))

    print("=== Name comparison ===")
    print(f"Annotated videos (DIVA): {len(ann)}")
    print(f"Videos in dataset:       {len(data)}")
    print(f"Matched:                 {len(both)}")
    print(f"Annotated but no video:  {len(missing_video)}")
    for n in missing_video:
        print(f"   {n}")
    print(f"Videos without DIVA annotation: {len(not_annotated)}")

    scene_report("Full dataset", list(data))
    scene_report("DIVA annotations", list(ann), splits=ann)


if __name__ == "__main__":
    main()