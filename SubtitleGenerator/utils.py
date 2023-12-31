import librosa


def load_waveform(wav_path: str):
    waveform, _ = librosa.load(wav_path)
    return waveform
