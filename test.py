import os
from moviepy.editor import *
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: ./main.py <video file>")
if not os.path.isfile(sys.argv[1]):
    sys.exit("Video file is not found")

orig_filename = os.path.abspath(sys.argv[1])
splitted = os.path.splitext(orig_filename)
result_filename = splitted[0] + "_edited" + splitted[1]
# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip(orig_filename)


# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip("Test", fontsize=70, color='white')

# Say that you want it to appear 10s at the center of the screen
txt_clip = txt_clip.set_pos('center').set_duration(10)

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

# Write the result to a file (many options available !)
video.write_videofile(result_filename)