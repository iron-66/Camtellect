import cv2
import pyttsx3
import speech_recognition as sr
from openai import OpenAI

client = OpenAI(api_key="")


def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print("Вы сказали:", text)
        return text
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
        return ""
    except sr.RequestError:
        print("Ошибка соединения с сервисом распознавания.")
        return ""


def capture_photo(filename="photo.jpg"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось открыть камеру.")
        return None
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
        print(f"Фото сохранено как {filename}")
    cap.release()
    return filename if ret else None


def ask_gpt(prompt_text, image_path=None):
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]

    if image_path:
        with open(image_path, "rb") as img_file:
            import base64
            image_data = base64.b64encode(img_file.read()).decode("utf-8")
        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
            }
        })

    print("Отправка запроса в OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=500
    )
    return response.choices[0].message.content


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def main():
    text = record_audio()
    if not text:
        return
    photo = capture_photo()
    gpt_response = ask_gpt(text, image_path=photo)
    print("Ответ GPT:\n", gpt_response)
    speak_text(gpt_response)

if __name__ == "__main__":
    main()
