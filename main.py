from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os

model_path = os.path.join(os.getcwd(), "vosk-model-small-ru-0.22")
model = Model(model_path)

recognizer = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Speak now ...")
while True:
    data = stream.read(4000)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print(json.loads(result)['text'])
