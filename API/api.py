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
from api_auth import (
    get_current_active_user,
    Token,
    authenticate_user,
    user_db,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    User,
)
from static_auth import AuthStaticFiles
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, File, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
import aiofiles

app = FastAPI()

# creates all statiic folders need to mount
# leaves the folder alone if exists already
create_needed_folders()

app.mount("/video", AuthStaticFiles(directory="Videos/"), name="video")
app.mount("/thumbnail", AuthStaticFiles(directory="Thumbnails/"), name="thumbnail")
app.mount("/segment", AuthStaticFiles(directory="Segments/"), name="segment")
app.mount("/audio", AuthStaticFiles(directory="Audios/"), name="audio")


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/upload_video")
async def upload_video(
    current_user: Annotated[User, Depends(get_current_active_user)],
    in_file: UploadFile = File(...),
):
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
async def generate_thumbnail(
    current_user: Annotated[User, Depends(get_current_active_user)],
    video_file_path: str,
):
    parsed_file_path = video_file_path.split(".")
    thumbnail_path = f"Thumbnails/{parsed_file_path[0]}.png"
    video_file_path = f"Videos/{video_file_path}"
    create_image_thumbnail(video_file_path, thumbnail_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"thumbnail_path": thumbnail_path}
    )


@app.post("/generate_segments")
async def generate_segments(
    current_user: Annotated[User, Depends(get_current_active_user)],
    video_file_path: str,
):
    parsed_file_path = video_file_path.split(".")
    video_file_path = f"Videos/{video_file_path}"
    segment_path = "Segments/" + parsed_file_path[0] + "%d." + ".png"
    create_segments(video_file_path, segment_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"segment_path": segment_path}
    )


@app.post("/generate_subtitles")
async def generate_subtitles(
    current_user: Annotated[User, Depends(get_current_active_user)],
    video_file_path: str,
):
    parsed_file_path = video_file_path.split(".")
    audio_file_path = f"Audios/{parsed_file_path[0]}.wav"
    video_file_path = f"Videos/{video_file_path}"
    convert_video_to_wav(video_file_path, audio_file_path)
    transcription = transcribe_audio_with_huggingface(audio_file_path)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"transcription": transcription}
    )


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
