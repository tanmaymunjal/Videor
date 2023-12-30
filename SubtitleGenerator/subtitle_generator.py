import torchaudio
from transformers import pipeline
import torch
import subprocess

# sets optimum cuda threads if available
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

def convert_m4a_to_wav(video_path: str, wav_path: str, sample_rate:int = 16000):
    command = f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar {sample_rate} -ac 2 {wav_path}"
    subprocess.call(command, shell=True)
    return wav_path


def load_waevform(wav_path: str):
    waveform, _ = torchaudio.load(wav_path)
    return waveform

def transcribe_audio_with_huggingface(audio_file_path):
    # Load the pre-trained model
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-medium",
        torch_dtype=torch_dtype,
        chunk_length_s=30,
        device=device,
        return_timestamps=True
    )

    # Load the audio file
    waveform = load_waevform(audio_file_path)

    # Transcribe audio
    transcription = asr_pipeline(waveform.numpy()[0])

    return transcription
