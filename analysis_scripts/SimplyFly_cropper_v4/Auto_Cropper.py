"""
SimplyFly Autocropper

Last edited by Paulami Dey on 11/08/2026

"""

import cv2
import numpy as np
import subprocess
import os


# -----------------------------------------------------------------------------
# Tunable constants (defaults work for both the 8- and 12-chamber examples
# tested; override via the optional prompts in main() if a new rig needs it).
# -----------------------------------------------------------------------------
RADIUS_MIN_FRACTION = 0.035   # min chamber radius, as a fraction of min(h, w)
RADIUS_MAX_FRACTION = 0.22    # max chamber radius, as a fraction of min(h, w)
NMS_MERGE_FRACTION = 0.6      # merge detections closer than this * avg radius
GRID_GAP_FRACTION = 0.6       # gap (relative to radius) that starts a new row/col band
HOUGH_PARAM2_SWEEP = (45, 40, 35, 30, 25, 22, 20, 18, 16, 14)


# -----------------------------------------------------------------------------
# Preprocessing: normalise contrast so faint chambers are easier to find.
# -----------------------------------------------------------------------------
def _preprocess_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    gray = cv2.GaussianBlur(gray, (7, 7), 1.5)
    return gray


# -----------------------------------------------------------------------------
# Run Hough at several sensitivity levels and pool every candidate circle.
# -----------------------------------------------------------------------------
def _multi_pass_hough(gray, r_min, r_max):
    min_dist = max(20, int(r_min * 1.3))
    candidates = []
    for param2 in HOUGH_PARAM2_SWEEP:
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=min_dist,
            param1=100,
            param2=param2,
            minRadius=r_min,
            maxRadius=r_max,
        )
        if circles is not None:
            for c in np.round(circles[0]).astype(int):
                candidates.append((int(c[0]), int(c[1]), int(c[2])))
    return candidates


# -----------------------------------------------------------------------------
# Merge duplicate detections of the same physical chamber. Candidates are
# processed in the order they were found (most sensitive/confident passes
# first), and a candidate is dropped if it's too close to one already kept.
# -----------------------------------------------------------------------------
def _merge_duplicates(candidates, merge_fraction=NMS_MERGE_FRACTION):
    kept = []
    for (x, y, r) in candidates:
        too_close = False
        for (kx, ky, kr) in kept:
            dist = np.hypot(x - kx, y - ky)
            if dist < merge_fraction * ((r + kr) / 2.0):
                too_close = True
                break
        if not too_close:
            kept.append((x, y, r))
    return kept


# -----------------------------------------------------------------------------
# Cluster a set of 1D coordinates into bands (rows or columns), where a new
# band starts whenever the gap to the previous point exceeds a threshold
# relative to the local chamber radius.
# -----------------------------------------------------------------------------
def _cluster_axis(values, radii, gap_fraction=GRID_GAP_FRACTION):
    order = np.argsort(values)
    bands = [[order[0]]]
    for i in range(1, len(order)):
        prev_idx = bands[-1][-1]
        idx = order[i]
        gap = values[idx] - values[prev_idx]
        typical = (radii[idx] + radii[prev_idx]) / 2.0
        if gap > gap_fraction * typical * 2:
            bands.append([idx])
        else:
            bands[-1].append(idx)

    band_centers = [float(np.mean(values[b])) for b in bands]
    assign = {}
    for band_i, band in enumerate(bands):
        for idx in band:
            assign[idx] = band_i
    return band_centers, assign


# -----------------------------------------------------------------------------
# Grid-aware chamber detection. Replaces the old fixed-parameter Hough call.
# Same signature as the original function so the rest of the script is
# unaffected.
# -----------------------------------------------------------------------------
def detect_bright_circles(image, num_circles=5, r_min=None, r_max=None):
    """
    Detect chamber circles in `image`, reconstructing the plate's row/column
    grid so duplicate detections are merged and faint-but-real chambers are
    filled in from grid geometry rather than dropped.

    Returns an array of `num_circles` (x, y, r) tuples in reading order
    (top-to-bottom, then left-to-right), or None if detection failed.
    """
    h, w = image.shape[:2]
    gray = _preprocess_gray(image)

    if r_min is None:
        r_min = max(15, int(min(h, w) * RADIUS_MIN_FRACTION))
    if r_max is None:
        r_max = int(min(h, w) * RADIUS_MAX_FRACTION)

    raw_candidates = _multi_pass_hough(gray, r_min, r_max)
    if not raw_candidates:
        return None

    merged = _merge_duplicates(raw_candidates)
    if len(merged) < 2:
        return None

    merged_arr = np.array(merged, dtype=float)
    xs, ys, rs = merged_arr[:, 0], merged_arr[:, 1], merged_arr[:, 2]

    row_centers, row_assign = _cluster_axis(ys, rs)
    col_centers, col_assign = _cluster_axis(xs, rs)
    n_rows, n_cols = len(row_centers), len(col_centers)
    median_r = float(np.median(rs))

    # For each occupied grid cell, keep the earliest (most confident) match.
    grid = {}
    for i in range(len(merged)):
        key = (row_assign[i], col_assign[i])
        if key not in grid:
            grid[key] = (xs[i], ys[i], rs[i])

    if n_rows * n_cols == num_circles:
        # Clean rectangular grid: fill any missing cell by interpolating
        # its position from the row/column geometry instead of dropping it.
        full_circles = []
        for r_i in range(n_rows):
            for c_i in range(n_cols):
                key = (r_i, c_i)
                if key in grid:
                    full_circles.append(grid[key])
                else:
                    full_circles.append((col_centers[c_i], row_centers[r_i], median_r))
        result = full_circles
    elif len(merged) >= num_circles:
        # Grid didn't resolve to a clean rectangle (irregular layout, or
        # extra spurious detections survived). Fall back to the strongest
        # `num_circles` unique detections.
        result = merged[:num_circles]
    else:
        return None

    result = [(int(round(x)), int(round(y)), int(round(r))) for x, y, r in result]

    # Reading order: top-to-bottom (bucketed by radius so small jitter
    # within a row doesn't reorder it), then left-to-right.
    row_height = max(median_r, 1.0)
    result.sort(key=lambda c: (round(c[1] / row_height), c[0]))

    return np.array(result[:num_circles])


# -----------------------------------------------------------------------------
# ORIGINAL OBJECT-CHECK FUNCTION — unchanged from Autocropper.py
# -----------------------------------------------------------------------------
def contains_objects(circle_roi, r):
    """Return True when the chamber crop appears to contain objects."""
    gray_roi = cv2.cvtColor(circle_roi, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)

    mask = np.zeros_like(gray_roi)
    cv2.circle(mask, (r, r), r, 255, thickness=-1)

    masked = cv2.bitwise_and(thresholded, thresholded, mask=mask)

    non_white_percentage = (
        cv2.countNonZero(masked) / cv2.countNonZero(mask)
    ) * 100

    return non_white_percentage < 95


# -----------------------------------------------------------------------------
# ORIGINAL CROP CALCULATION, with output path and overwrite safety changed only
# -----------------------------------------------------------------------------
def save_cropped_videos(video_path, circles, output_dir):
    """
    Crop the detected chambers and save them into the shared output folder.

    The crop size, crop coordinates, object check, FFmpeg codec, CRF, preset,
    audio handling, and FPS handling remain the same as in Autocropper.py.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    ret, frame = cap.read()
    if not ret:
        print(f"Failed to read the first frame from {video_path}")
        cap.release()
        return

    frame_height, frame_width = frame.shape[:2]
    cap.release()

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Original logic: largest detected radius, enlarged by 20% for all crops.
    max_radius = max(circle[2] for circle in circles)
    max_radius = int(max_radius * 1.2)

    for idx, circle in enumerate(circles, start=1):
        x, y, r = circle

        # Original crop-boundary calculation.
        x_start = max(0, x - max_radius)
        y_start = max(0, y - max_radius)
        x_end = min(frame_width, x + max_radius)
        y_end = min(frame_height, y + max_radius)

        roi_width = x_end - x_start
        roi_height = y_end - y_start

        # Original even-dimension correction.
        roi_width -= roi_width % 2
        roi_height -= roi_height % 2

        if roi_width <= 0 or roi_height <= 0:
            print(f"Skipping chamber {idx}: invalid crop dimensions.")
            continue

        circle_roi = frame[
            y_start:y_start + roi_height,
            x_start:x_start + roi_width
        ]

        if not contains_objects(circle_roi, max_radius):
            print(
                f"Skipping chamber {idx} because it does not contain objects."
            )
            continue

        # Changed only here: save into main_folder/output using source name.
        output_file = os.path.join(
            output_dir,
            f"{video_name}_chamber_{idx}.mp4"
        )

        # Never silently replace an existing crop.
        if os.path.exists(output_file):
            print(
                f"Skipping chamber {idx}: output already exists:\n"
                f"{output_file}"
            )
            continue

        crop_filter = (
            f"crop={roi_width}:{roi_height}:{x_start}:{y_start}"
        )

        ffmpeg_command = [
            "ffmpeg",
            "-n",                       # Changed from -y: never overwrite
            "-i", video_path,
            "-vf", crop_filter,
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "medium",
            "-c:a", "copy",
            "-r", str(fps),
            output_file
        ]

        print(f"\nExecuting FFmpeg command for chamber {idx}:")
        print(" ".join(ffmpeg_command))

        try:
            subprocess.run(ffmpeg_command, check=True)
            print(
                f"Chamber {idx} cropped successfully:\n"
                f"{output_file}"
            )
        except FileNotFoundError:
            print(
                "FFmpeg was not found. Install FFmpeg and make sure it is "
                "available from the command line."
            )
            return
        except subprocess.CalledProcessError as error:
            print(
                f"FFmpeg failed while cropping chamber {idx}: "
                f"{error}"
            )


def main():
    """Process MP4 videos in first-level folders under the selected main folder."""
    input_folder = input(
        "What is the path of the main video folder? "
    ).strip('"').strip("'")

    if not os.path.isdir(input_folder):
        print(f"The provided path '{input_folder}' is not a valid directory.")
        return

    try:
        num_circles = int(input("How many chambers are there per video? "))
        if num_circles <= 0:
            print("Number of chambers must be a positive integer.")
            return
    except ValueError:
        print(
            "Invalid input for the number of chambers. "
            "Please enter a positive integer."
        )
        return

    # Optional manual radius override, in case a new rig's chambers fall
    # outside the auto-estimated range. Press Enter to keep auto-detection.
    r_min_input = input(
        "Minimum chamber radius in pixels (press Enter to auto-detect): "
    ).strip()
    r_max_input = input(
        "Maximum chamber radius in pixels (press Enter to auto-detect): "
    ).strip()
    r_min_override = int(r_min_input) if r_min_input else None
    r_max_override = int(r_max_input) if r_max_input else None

    output_dir = os.path.join(input_folder, "output")
    os.makedirs(output_dir, exist_ok=True)

    debug_dir = os.path.join(input_folder, "debug")
    os.makedirs(debug_dir, exist_ok=True)

    # Same first-level-folder traversal as the original, except that the shared
    # output and debug folders are explicitly skipped.
    for dir_name in os.listdir(input_folder):
        if dir_name.lower() in ("output", "debug"):
            continue

        dir_path = os.path.join(input_folder, dir_name)

        if not os.path.isdir(dir_path):
            continue

        for file_name in os.listdir(dir_path):
            video_path = os.path.join(dir_path, file_name)

            if not video_path.lower().endswith(".mp4"):
                continue

            print(f"\nProcessing video: {video_path}")

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Failed to open video: {video_path}")
                continue

            # Original detection frame.
            desired_frame_index = 1000
            cap.set(cv2.CAP_PROP_POS_FRAMES, desired_frame_index)
            ret, frame = cap.read()
            cap.release()

            if not ret:
                print(
                    f"Failed to load frame {desired_frame_index} from "
                    f"{video_path}. Skipping."
                )
                continue

            circles = detect_bright_circles(
                frame, num_circles, r_min=r_min_override, r_max=r_max_override
            )

            video_name = os.path.splitext(file_name)[0]
            detection_file = os.path.join(
                debug_dir,
                f"{video_name}_detected_circles.png"
            )

            frame_copy = frame.copy()
            if circles is not None:
                for i, circle in enumerate(circles, start=1):
                    cv2.circle(
                        frame_copy,
                        (circle[0], circle[1]),
                        circle[2],
                        (0, 255, 0),
                        2
                    )
                    cv2.putText(
                        frame_copy,
                        str(i),
                        (circle[0] - 10, circle[1] + 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

            # Refresh the check image on every run.
            cv2.imwrite(detection_file, frame_copy)
            print(f"Saved detection check: {detection_file}")

            if circles is None:
                print("Failed to detect enough circles. Skipping this video.")
                continue

            save_cropped_videos(video_path, circles, output_dir)
            print(
                f"Cropped videos for {len(circles)} circles have been saved "
                f"for {video_path}."
            )

    print(f"\nProcessing completed. Outputs are in:\n{output_dir}")


if __name__ == "__main__":
    main()
