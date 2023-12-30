import subprocess


def create_segments(video_input_path, output_format):
    subprocess.call(["ffmpeg", "-i", video_input_path, output_format])


video_input_path = "../VideoTranscoder/VideoToTranscode/test.mp4"
output = "Segment/output_%04d.png"

create_segments(video_input_path, output)
