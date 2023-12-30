"""
Consists of all variables needed to configure the
transcoder service
"""

DIMENSIONS = {
    "SD": [640, 480],
    "HD": [1280, 720],
    "FHD": [1920, 1080],
    "QHD": [2560, 1440],
    "2K": [2048, 1080],
    "4K": [3840, 2160],
    "8K": [7680, 4320],
}

# output video framerate
FRAMERATE = 30

# controls the approximate bitrate of the encode
# we currently only support constant bitrate, so videos can be encoded in advance
BITRATE = "6M"

# encoding speed:compression ratio
PRESET = "slow"

# output file format
# currently supporting only mp4, will add to config later as
# scalability of the system improves
OUTPUT_FILE_EXTENSION = "mp4"

# directory in which transcoded video is saved
TRANCODE_DIRECTORY = "transcoded"

# path of ffmpeg installation
FFMPEG_PATH = "/usr/bin/ffmpeg"
