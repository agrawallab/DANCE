Video Cropping Tool
===================

This code is designed to detect bright circular regions (chambers) in videos, crop these regions, and save them as individual video files for further analysis. It uses OpenCV for image processing and ffmpeg for video editing, making it ideal for tasks like analyzing experimental setups.

------------------------------------------------
Features
------------------------------------------------
1. Automatic Circle Detection:
   - Detects bright circular regions in a given video using Hough Circle Transform.

2. Video Cropping:
   - Extracts detected circular regions as separate video files.
   - Ensures compatibility with most video formats.

3. Object Detection:
   - Skips regions that do not contain significant objects, based on pixel intensity analysis.

4. Configurable Parameters:
   - Adjustable circle detection settings for flexibility in diverse use cases.

------------------------------------------------
Prerequisites
------------------------------------------------
1. Python 3.7+ installed on your system.
2. Required Python libraries:
   - OpenCV (`cv2`)
   - NumPy (`numpy`)
3. ffmpeg installed and added to the system PATH.

------------------------------------------------
Setup Instructions
------------------------------------------------
1. Clone or download the project repository to your local system.
2. Install required Python libraries using: pip install opencv-python-headless numpy
3. Ensure FFmpeg is installed and accessible via the command line.

------------------------------------------------
Usage
------------------------------------------------
1. Run the script:
2. Provide the required inputs when prompted:
- **Master Video Folder**: Path to the directory containing the video files.
- **Number of Chambers**: The number of circular regions to detect per video.
3. The program processes each video, detects circular regions, and saves cropped videos in subdirectories named `chamber_<index>`.

------------------------------------------------
How It Works
------------------------------------------------
1. **Frame Extraction**: Extracts a specific frame from the video to detect circles.
2. **Circle Detection**: Uses the Hough Circle Transform to identify circular regions.
3. **Object Validation**: Checks if detected circles contain significant objects.
4. **Video Cropping**: Crops and saves the regions as separate videos using FFmpeg.

------------------------------------------------
Error Handling
------------------------------------------------
- If FFmpeg is not installed, the program will terminate and prompt you to install it.
- Videos without detectable circles are skipped with a message.
- Invalid input paths or numbers are handled gracefully with error messages.

------------------------------------------------
Output
------------------------------------------------
- Cropped videos are saved in subdirectories within the same directory as the original video files.
- Each subdirectory is named `chamber_<index>`.






