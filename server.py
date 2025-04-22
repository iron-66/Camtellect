from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional
import tempfile
import os
import base64
import traceback
import subprocess

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_PLUS_KEY"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def convert_webm_to_wav(input_path: str, output_path: str):
    subprocess.run([
        "ffmpeg", "-i", input_path, output_path
    ], check=True)


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/process")
async def process_input(audio: Optional[UploadFile] = File(None), image: UploadFile = File(...)):
    try:
        transcript_text = ""

        if audio is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
                temp_audio.write(await audio.read())
                webm_path = temp_audio.name

            wav_path = webm_path.replace(".webm", ".wav")
            convert_webm_to_wav(webm_path, wav_path)

            with open(wav_path, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    response_format="text",
                    language="ru"
                )
                transcript_text = transcript.strip()

            os.remove(webm_path)
            os.remove(wav_path)
        else:
            transcript_text = "Опиши, что изображено на этом фото"

        image_data = await image.read()
        image_b64 = base64.b64encode(image_data).decode("utf-8")
        image_prompt = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_b64}"
            }
        }

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Отвечай кратко, строго в виде обычного текста."
                        "Не используй Markdown или символы форматирования: без **жирного**, # заголовков, подчёркиваний и прочего."
                        "Выводи только чистый текст."
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": transcript_text.strip()},
                        image_prompt
                    ]
                }
            ],
            max_tokens=500
        )

        return JSONResponse({"reply": response.choices[0].message.content.strip()})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})