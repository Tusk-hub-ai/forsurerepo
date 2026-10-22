

import numpy as np
import yaml
from get_specific_type_of_file import get_file
from config_path import ANNOTATION_PATH

FPS = 30
path = get_file(path=ANNOTATION_PATH, specificType="*.activities.yml")
# activity names that mean "an object changes position"
MOVEMENT = {
    "activity_walking", "activity_running", "Riding",
    "vehicle_moving", "vehicle_starting", "vehicle_stopping",
    "vehicle_turning_left", "vehicle_turning_right", "vehicle_u_turn",
}

totals = {}               # split -> [all frames, activity frames, movement frames, clips]
clips_no_activity = []
clips_no_movement = []
beyond_end = 0            # activities ending after the clip length taken from the name

def n_frames_of(file, stem, parts):
    """Number of frames in the clip or full video."""
    if len(parts) >= 6:                       # clip: start/end seconds are in the name
        return (int(parts[5]) - int(parts[4])) * FPS
    # full video: no timestamps in the name, read the max frame from the geom metadata
    geom = file.with_name(stem + ".geom.yml")
    with open(geom) as g:
        for line in g:
            if "min / max frame:" in line:
                max_frame = int(line.split("min / max frame:")[1].split()[1])
                return max_frame + 1          # +1: frame 0 counts too
    raise ValueError(f"No frame range found in {geom}")


for file in path:
    stem = file.name.split(".")[0]          # e.g. VIRAT_S_000200_05_001525_001575
    parts = stem.split("_")
    n_frames = n_frames_of(file, stem, parts)
    kind = "clip" if len(parts) >= 6 else "full"

    # one entry per frame, all False (= no activity) to begin with
    frames_all = np.zeros(n_frames, dtype=bool)
    frames_move = np.zeros(n_frames, dtype=bool)

    with open(file) as f:
        records = yaml.load(f, Loader=yaml.CSafeLoader) or []

    for row in records:
        if "act" not in row:                # skips meta lines
            continue
        action = list(row["act"]["act2"].keys())[0]
        start, end = row["act"]["timespan"][0]["tsr0"]
        if end >= n_frames:
            beyond_end += 1

        frames_all[start:end + 1] = True    # +1: the end frame is included
        if action in MOVEMENT:
            frames_move[start:end + 1] = True

    split = file.parent.name                # train / validate
    t = totals.setdefault(split, [0, 0, 0, 0])
    t[0] += n_frames
    t[1] += frames_all.sum()
    t[2] += frames_move.sum()
    t[3] += 1

    if frames_all.sum() == 0:
        clips_no_activity.append(stem)
    if frames_move.sum() == 0:
        clips_no_movement.append(stem)


# ---------------------------------------------------------------- results
def report(name, frames, act, move, clips):
    print(f"\n{name}: {clips} clips, {frames} frames = {frames / FPS / 3600:.2f} h")
    print(f"  any activity : {act:>8} frames = {act / frames:6.1%}"
          f"   no activity : {frames - act:>8} = {(frames - act) / frames:6.1%}")
    print(f"  movement     : {move:>8} frames = {move / frames:6.1%}"
          f"   no movement : {frames - move:>8} = {(frames - move) / frames:6.1%}")


grand = [0, 0, 0, 0]
for split, t in sorted(totals.items()):
    report(split, *t)
    grand = [g + v for g, v in zip(grand, t)]
report("ALL CLIPS", *grand)

print(f"\nClips without any activity ({len(clips_no_activity)}): {clips_no_activity}")
print(f"Clips without movement ({len(clips_no_movement)}): {clips_no_movement}")
print(f"Activities ending after the clip length from the name: {beyond_end}")

