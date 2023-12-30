import subprocess


def create_image_thumbnail(video_input_path, img_output_path):
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            video_input_path,
            "-ss",
            "00:00:00.000",
            "-vframes",
            "1",
            img_output_path,
        ]
    )
