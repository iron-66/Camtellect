# Camtellect Server & Landing 🎥🎙️🧠

FastAPI backend and static landing page for the Android app that streams camera frames (or a wireless camera feed) to a multimodal assistant.  
This repo is deployed on the server: it powers the mobile app API and hosts the landing site.

## Features

- **Static site** served from `/static` (landing, assets).
- **Image + optional audio** endpoint that:
  - transcribes `.webm` audio to `.wav` via **FFmpeg + Whisper**,
  - sends the user text + image to **GPT-4.1**,
  - returns a short plain-text answer.
- **Realtime token** endpoint that creates a short-lived client secret for **OpenAI Realtime** (`gpt-realtime`) sessions.
- **CORS enabled** for quick prototyping (defaults to `*`).

## Project layout
```
├─ static/
│ ├─ index.html
│ ├─ style.css
│ ├─ script.js
│ └─ Demo.mp4 # example media (gitignored)
├─ server.py # FastAPI app
├─ requirements.txt
├─ README.md
└─ .gitignore
```


## Requirements

- Python 3.10+
- FFmpeg (for WebM→WAV audio conversion)
- OpenAI API access

### Install FFmpeg

- macOS: `brew install ffmpeg`  
- Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y ffmpeg`  
- Windows (choco): `choco install ffmpeg`

## Quickstart

```bash
# 1) Clone and enter the repo
git clone https://github.com/iron-66/Camtellect
cd Camtellect

# 2) Python env + deps
python -m venv .venv        # Windows: python -m venv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
sudo apt update && sudo apt install -y ffmpeg

# 3) Environment
cp .env.example .env        # if provided; else create .env
# put your key inside:
# OPENAI_PLUS_KEY=sk-...

# 4) Run (dev)
uvicorn server:app --reload --host 0.0.0.0 --port 8000

# Open in browser:
# http://localhost:8000/             -> serves static/index.html
# http://localhost:8000/static/...   -> static assets
```

