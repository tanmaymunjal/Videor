import librosa
from transformers import pipeline
import torch
import subprocess
from SubtitleGenerator.utils import load_waveform


def convert_video_to_wav(video_path: str, wav_path: str, sample_rate: int = 16000):
    command = f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar {sample_rate} -ac 2 {wav_path}"
    subprocess.call(command, shell=True)
    return wav_path


def transcribe_audio_with_huggingface(audio_file_path):
    # sets optimum cuda threads if available
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Load the pre-trained model
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-medium",
        torch_dtype=torch_dtype,
        chunk_length_s=30,
        device=device,
        return_timestamps=True,
    )

    # Load the audio file
    waveform = load_waveform(audio_file_path)

    # Transcribe audio
    transcription = asr_pipeline(waveform)

    return transcription
