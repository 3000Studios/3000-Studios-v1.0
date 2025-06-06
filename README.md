# 3000-Studios-v1.0

This repository provides a lightweight utility for transcribing English speech
from audio files. The `transcribe_boost.py` script applies optional amplification
and noise reduction before performing speech-to-text using the Whisper model.

## Requirements

- Python 3.8+
- `ffmpeg` installed and available on your system path
- Python packages listed in `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python transcribe_boost.py <input-audio> [--amplify DB] [--denoise]
```

- `--amplify DB` — increase the volume by the specified number of decibels.
- `--denoise` — apply simple noise reduction prior to transcription.

The script outputs the recognized English text to standard output.
