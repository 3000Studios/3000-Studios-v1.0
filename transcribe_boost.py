import argparse
import os

from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import soundfile as sf
try:
    import whisper
except ImportError:
    whisper = None


def load_audio(path: str) -> AudioSegment:
    """Load an audio file using pydub."""
    return AudioSegment.from_file(path)


def amplify(audio: AudioSegment, db: float) -> AudioSegment:
    """Amplify audio by the specified decibels."""
    return audio + db


def reduce_noise(audio: AudioSegment) -> AudioSegment:
    """Apply simple noise reduction using noisereduce."""
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    reduced = nr.reduce_noise(y=samples, sr=audio.frame_rate)
    # convert back to pydub AudioSegment
    return audio._spawn(reduced.astype(np.int16).tobytes())


def transcribe(audio: AudioSegment) -> str:
    """Transcribe audio using whisper if available."""
    temp_path = "_temp.wav"
    audio.export(temp_path, format="wav")
    if whisper is None:
        raise ImportError("whisper library is required for transcription")
    model = whisper.load_model("base")
    result = model.transcribe(temp_path, language="en")
    os.remove(temp_path)
    return result.get("text", "")


def main():
    parser = argparse.ArgumentParser(description="Transcribe and clean English audio")
    parser.add_argument("input", help="Path to input audio file")
    parser.add_argument("--amplify", type=float, default=0.0, help="Amplify volume in dB")
    parser.add_argument("--denoise", action="store_true", help="Apply noise reduction")
    args = parser.parse_args()

    audio = load_audio(args.input)
    if args.amplify:
        audio = amplify(audio, args.amplify)
    if args.denoise:
        audio = reduce_noise(audio)

    text = transcribe(audio)
    print(text)


if __name__ == "__main__":
    main()
