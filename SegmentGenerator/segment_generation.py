import subprocess


def create_segments(video_input_path, output_format):
    subprocess.call(["ffmpeg", "-i", video_input_path, output_format])
