import pyaudio
import wave
import sys
import tkinter as tk
import numpy as np
from vosk import Model, KaldiRecognizer
# Load the pre-trained model
# Load the pre-trained model
model_file_path = 'vosk-model-small-en-us-0.15'
model = Model(model_file_path)
recognizer = KaldiRecognizer(model, 16000)

def transcribe_audio(data):
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print(result)

def record_audio():
    output_filename = "output.wav"
    record_seconds = 10

    # Set the configuration for the audio recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    # Initialize the PyAudio object
    audio = pyaudio.PyAudio()

    # Open a new stream for recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    # Record audio data for the specified duration
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
        transcribe_audio(data)

    print("\nFinished recording")

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def main():
    # Create a simple Tkinter window
    root = tk.Tk()
    root.title("Audio Recorder")
    root.geometry("300x100")

    # Add a button to start the recording
    record_button = tk.Button(root, text="Record", command=record_audio)
    record_button.pack(expand=True, fill=tk.BOTH)

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
