# Camtellect – AIfy your camera & mic 🎥🎙️🧠

Camtellect — это opensource-приложение на FastAPI, превращающее обычную камеру и микрофон в умного помощника с GPT-4.1.

## Возможности
- 📷 Делает фото с камеры
- 🎙️ Распознаёт голосовые запросы (с Whisper или Google)
- 🤖 Передаёт голос и фото в OpenAI GPT для ответа
- 🔈 Озвучивает ответ голосом
- 🌐 Полноценный web-интерфейс (нажатие кнопки — запись, фото, ответ)

## Установка

```bash
git clone https://github.com/iron-66/Camtellect
cd Camtellect
python3 -m venv venv      # Windows: python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск
```bash
uvicorn server:app --reload
```
