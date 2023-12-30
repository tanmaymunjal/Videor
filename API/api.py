from SegmentGeneration.segment_generation import create_segments
from SubtitleGenerator.subtitle_generator import (
    convert_m4a_to_wav,
    load_waevform,
    transcribe_audio_with_huggingface,
)
from ThumbnailGeneration.thumbnail import create_image_thumbnail
from VideoTranscoder.transcode_video import encode_file
from fastapi import FastAPI, File, UploadFile
import uvicorn
import aiofiles


app = FastAPI()


@app.post("/upload_video")
async def post_endpoint(in_file: UploadFile = File(...)):
    async with aiofiles.open("Videos/" + in_file.filename, "wb") as out_file:
        content = await in_file.read()  # async read
        await out_file.write(content)  # async write

    return {"Result": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
