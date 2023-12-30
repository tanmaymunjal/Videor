"""
This python script transcodes all video formats
Inspired by https://gist.github.com/hleb-albau/dced8b57fdb5d458f430
"""
from os import path
from subprocess import call


# example : ffmpeg -i i.mp4 -f mp4 -s 1920x1080 -b 6000k -r 30 -vcodec libx264 -preset veryslow -threads auto o.mp4
def encode_file(
    ffmpeg,
    input_file_path,
    output_directory,
    output_file_extension,
    dimension,
    bitrate,
    framerate,
    preset,
):
    output_file_path = output_directory + compile_output_file_name(
        input_file_path, output_file_extension, dimension, bitrate, framerate, preset
    )
    call(
        [
            ffmpeg,
            "-i",
            input_file_path,
            "-f",
            output_file_extension,
            "-s",
            dimension,
            "-b:v",
            bitrate,
            "-r",
            framerate,
            "-vcodec",
            "libx264",
            "-preset",
            preset,
            "-threads",  # setting threads to 0 automatically optimises
            "0",
            "-strict",
            "normal",
            output_file_path,
        ]
    )


def compile_output_file_name(
    input_file_path, output_file_extension, dimension, bitrate, framerate, preset
):
    input_file_name = path.basename(input_file_path)
    input_file_name_without_extension = path.splitext(input_file_name)[
        0
    ]  # split ext, not split text.
    return (
        input_file_name_without_extension
        + "_"
        + dimension
        + "frame"
        + framerate
        + "bitrate"
        + bitrate
        + "preset"
        + preset
        + "."
        + output_file_extension
    )
