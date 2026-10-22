# DIVA / VIRAT dataset analysis

Scripts used to inspect and analyse the DIVA v1 annotations of the VIRAT Ground Camera dataset.

## Requirements

Python 3 with the following packages:

    pip install pandas numpy pyyaml opencv-python

## 1. Download the annotations (required for all scripts)

1. Go to the VIRAT dataset website: https://viratdata.org
2. Find the new annotations made by the DIVA program (KPF/YAML format).
   They are hosted in the `viratannotations` repository on Kitware's GitLab.
3. Download or clone the repository to your computer.

## 2. Download the videos (only for `compare_names_scenes.py` and `overlay_check.py`)

These two scripts also need the video files:

1. On the VIRAT website, go to the download page for the Ground Camera dataset.
2. Download the full video release.
3. Also download the test videos from release 1.0.

## 3. Set your local paths

Open `config_path.py` and change the paths to where the files are on your computer:

    ANNOTATION_PATH = Path(r"C:\your\path\to\viratannotations")
    DATASET = r"C:\your\path\to\VIRAT Ground Dataset"

- `ANNOTATION_PATH` must point to the folder containing `train` and `validate`.
- `DATASET` is only needed for `compare_names_scenes.py` and `overlay_check.py`.

All scripts read their paths from `config_path.py`, so this is the only file you need to edit.
