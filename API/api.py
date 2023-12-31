"""
This is the low level API for Video Transcoding,Subtitle,Segment, and Thumbnail Generation
Ideally, this should never be hit directly by an application/end-user
but hit on by the Balancer service that the application uses
The balancer service ensures which video requests should be distributed to which machine while 
all video processing happens locally to ensure minimum bandwidth required to push videos here and there
"""

from SegmentGeneration.segment_generation import create_segments
from SubtitleGenerator.subtitle_generator import (
    convert_video_to_wav,
    transcribe_audio_with_huggingface,
)
from ThumbnailGeneration.thumbnail import create_image_thumbnail
from VideoTranscoder.transcode_video import encode_file
from utils import check_file_exists, create_needed_folders
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import aiofiles

app = FastAPI()

# creates all statiic folders need to mount
# leaves the folder alone if exists already
create_needed_folders()

app.mount("/video", StaticFiles(directory="Videos/"), name="video")
app.mount("/thumbnail", StaticFiles(directory="Thumbnails/"), name="thumbnail")
app.mount("/segment", StaticFiles(directory="Segments/"), name="segment")
app.mount("/audio", StaticFiles(directory="Audios/"), name="audio")


@app.post("/upload_video")
async def upload_video(in_file: UploadFile = File(...)):
    out_file_name = "Videos/" + in_file.filename
    if check_file_exists(out_file_name):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"Result": "File already exists"},
        )
    async with aiofiles.open(out_file_name, "wb") as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write

    return JSONResponse(status_code=status.HTTP_200_OK, content={"Result": "OK"})


@app.post("/generate_thumbnail")
async def generate_thumbnail(video_file_path: str):
    thumbnail_path = f"Thumnails/{video_file_path}"
    create_image_thumbnail(video_file_path, thumbnail_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"thumbnail_path": thumbnail_path}
    )


@app.post("/generate_segments")
async def generate_segments(video_file_path: str):
    parsed_file_path = video_file_path.split(".")
    video_file_path = parsed_file_path[0] + "%d." + parsed_file_path[1]
    segment_path = f"Segments/{video_file_path}"
    create_segments(video_file_path, segment_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"segment_path": segment_path}
    )


@app.post("/generate_subtitles")
async def generate_subtitles(video_file_path: str):
    audio_path = f"Audios/{video_file_path}"
    convert_video_to_wav(video_file_path, audio_path)
    transcription = transcribe_audio_with_huggingface(audio_file_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"transcription": transcription}
    )


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
