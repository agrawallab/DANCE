# Last edited by Paulami Dey on 28/11/2024

import cv2
import numpy as np
import subprocess
import os
import shutil

# Global variables
circles = []

def detect_bright_circles(image, num_circles=5):
    """
    Detects bright circles in the given image using Hough Circle Transform.

    Args:
        image (numpy.ndarray): The input image in BGR format.
        num_circles (int): The number of circles to detect.

    Returns:
        numpy.ndarray or None: An array of detected circles (x, y, radius) or None if insufficient circles are detected.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=30,
        maxRadius=500
    )
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        if len(circles) >= num_circles:
            return circles[:num_circles]
    return None

def draw_rectangle(event, x, y, flags, param):
    """
    Placeholder for mouse callback function. Currently does nothing.

    Args:
        event: Mouse event.
        x: X-coordinate of the mouse event.
        y: Y-coordinate of the mouse event.
        flags: Any relevant flags passed by OpenCV.
        param: Additional parameters.
    """
    pass  # No drawing needed in this version

def get_video_bitrate(video_path):
    """
    Retrieves the bitrate of the specified video using ffprobe.

    Args:
        video_path (str): Path to the video file.

    Returns:
        int: The bitrate of the video in bits per second.
    """
    result = subprocess.run(
        [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=bit_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    try:
        bitrate = int(result.stdout)
        return bitrate
    except ValueError:
        print(f"Could not retrieve bitrate for {video_path}.")
        return 0

def contains_objects(circle_roi, r):
    """
    Determines whether the cropped ROI contains objects based on pixel intensity.

    Args:
        circle_roi (numpy.ndarray): The cropped region of interest.
        r (int): Radius used to create the circular mask.

    Returns:
        bool: True if the ROI contains objects, False otherwise.
    """
    # Convert the ROI to grayscale and apply a binary threshold
    gray_roi = cv2.cvtColor(circle_roi, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)

    # Create a circular mask
    mask = np.zeros_like(gray_roi)
    cv2.circle(mask, (r, r), r, 255, thickness=-1)

    # Apply the mask to the thresholded image
    masked = cv2.bitwise_and(thresholded, thresholded, mask=mask)

    # Calculate the percentage of non-white pixels within the circle
    non_white_percentage = (cv2.countNonZero(masked) / cv2.countNonZero(mask)) * 100

    # Consider the ROI to contain objects if more than 5% of pixels are non-white
    return non_white_percentage < 95

def save_cropped_videos(video_path, circles):
    """
    Crops the specified regions from the video and saves them as separate video files.

    Args:
        video_path (str): Path to the original video file.
        circles (numpy.ndarray): Array of detected circles (x, y, radius).
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

    video_dir = os.path.dirname(video_path)  # Directory of the video file

    # Find the maximum radius among all circles and adjust
    max_radius = max(circle[2] for circle in circles)
    max_radius = int(max_radius * 1.2)

    for idx, circle in enumerate(circles):
        x, y, r = circle

        # Define ROI boundaries with proper bounds checking
        x_start = max(0, x - max_radius)
        y_start = max(0, y - max_radius)
        x_end = min(frame_width, x + max_radius)
        y_end = min(frame_height, y + max_radius)

        # Calculate actual width and height in case ROI is near the edges
        roi_width = x_end - x_start
        roi_height = y_end - y_start

        # Crop the ROI from the frame for object detection
        circle_roi = frame[y_start:y_end, x_start:x_end]

        if not contains_objects(circle_roi, max_radius):
            print(f"Skipping chamber {idx} as it does not contain objects.")
            continue  # Skip this circle if it does not contain objects

        # Create directory for this circle's video in the same directory as the video file
        output_dir = os.path.join(video_dir, f'chamber_{idx}')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        # Construct FFmpeg crop filter with validated coordinates
        crop_filter = f"crop={roi_width}:{roi_height}:{x_start}:{y_start}"

        # Construct output file path
        output_file = os.path.join(output_dir, f'chamber_{idx}.mp4')

        # Construct FFmpeg command
        ffmpeg_command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', crop_filter,
            '-c:v', 'libx264',       # Use 'libx264' for better compatibility
            '-crf', '23',            # Reasonable quality
            '-preset', 'medium',     # Good balance between speed and quality
            '-c:a', 'copy',          # Copy audio without re-encoding
            '-r', str(int(fps)),
            output_file
        ]

        # Optionally, print the FFmpeg command for debugging
        print(f"Executing FFmpeg command for chamber {idx}:")
        print(' '.join(ffmpeg_command))

        try:
            # Run FFmpeg command
            subprocess.run(ffmpeg_command, check=True)
            print(f"Chamber {idx} cropped and saved successfully to {output_file}.")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg failed for chamber {idx} with error: {e}")

def main():
    """
    The main function that orchestrates the cropping process.
    It prompts the user for the input folder and the number of chambers,
    then processes each video file accordingly.
    """
    input_folder = input("What is the path of the master video folder? ").strip('"').strip("'")
    if not os.path.isdir(input_folder):
        print(f"The provided path '{input_folder}' is not a valid directory.")
        return

    try:
        num_circles = int(input("How many chambers are there per video? "))
        if num_circles <= 0:
            print("Number of chambers must be a positive integer.")
            return
    except ValueError:
        print("Invalid input for the number of chambers. Please enter a positive integer.")
        return

    for dir_name in os.listdir(input_folder):
        dir_path = os.path.join(input_folder, dir_name)
        if os.path.isdir(dir_path):
            for file_name in os.listdir(dir_path):
                video_path = os.path.join(dir_path, file_name)
                if video_path.lower().endswith(".mp4"):
                    print(f"\nProcessing video: {video_path}")
                    cap = cv2.VideoCapture(video_path)
                    if not cap.isOpened():
                        print(f"Failed to open video: {video_path}")
                        continue

                    desired_frame_index = 1000
                    cap.set(cv2.CAP_PROP_POS_FRAMES, desired_frame_index)
                    ret, frame = cap.read()
                    cap.release()

                    if not ret:
                        print(f"Failed to load frame {desired_frame_index} from {video_path}. Skipping.")
                        continue

                    # Optional: Save the frame with detected circles for verification
                    # Uncomment the following lines if you want to save the frame
                    # frame_copy = frame.copy()
                    # cv2.namedWindow('Frame')
                    # cv2.setMouseCallback('Frame', draw_rectangle)
                    # detected_circles = detect_bright_circles(frame_copy, num_circles)
                    # if detected_circles is not None:
                    #     for circle in detected_circles:
                    #         cv2.circle(frame_copy, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
                    # cv2.imwrite(os.path.join(dir_path, "detected_circles.png"), frame_copy)

                    circles = detect_bright_circles(frame, num_circles)
                    if circles is None:
                        print("Failed to detect enough circles. Skipping this video.")
                        continue

                    save_cropped_videos(video_path, circles)
                    print(f"Cropped videos for {len(circles)} circles have been saved for {video_path}.")

    print("\nProcessing completed.")

if __name__ == "__main__":
    main()
