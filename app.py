from flask import Flask, render_template, request, jsonify
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os
import threading
from datetime import datetime

app = Flask(__name__)

models = {
    'en': Model("models/vosk-model-small-en-us-0.15"),
    'fr': Model("models/vosk-model-small-fr-0.22"),
    'ru': Model("models/vosk-model-small-ru-0.22")
}

recording = False
recorded_text = ""
language_selected = 'en'

def record_audio():
    global recorded_text, recording, language_selected

    model = models[language_selected]
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    all_text = []

    while recording:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                all_text.append(text)

    # Final chunk
    final_result = json.loads(recognizer.FinalResult()).get("text", "")
    if final_result:
        all_text.append(final_result)

    stream.stop_stream()
    stream.close()
    p.terminate()

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]\n")
    session_text = " ".join(all_text).strip()

    if session_text:
        recorded_text += f"\n\n{timestamp}\n{session_text}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global recording, language_selected
    data = request.json
    language = data.get('language', 'en')

    if language not in models:
        return jsonify({"error": "Invalid language"}), 400

    language_selected = language
    recording = True
    threading.Thread(target=record_audio).start()
    return jsonify({"status": "recording started"})

@app.route('/stop', methods=['POST'])
def stop():
    global recording
    recording = False
    return jsonify({"status": "recording stopped"})

@app.route('/result', methods=['GET'])
def result():
    global recorded_text
    return jsonify({"text": recorded_text})

if __name__ == '__main__':
    app.run(debug=True)
