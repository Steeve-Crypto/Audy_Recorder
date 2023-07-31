import os
import sounddevice as sd
import numpy as np
import wavio
import keyboard
#from pynput import keyboard as kb

def get_next_filename(filename):
    """Helper function to create a new filename with an incremental number if the file exists."""
    filename_base, file_extension = os.path.splitext(filename)
    i = 1
    new_filename = f"{filename_base}_{i}{file_extension}"
    while os.path.exists(new_filename):
        i += 1
        new_filename = f"{filename_base}_{i}{file_extension}"
    return new_filename

def record_audio(filename, samplerate=44100, channels=2, device=None):
    frames = []
    recording = False
    paused = False

    def save_file(frames):
        audio_data = np.concatenate(frames, axis=0)
        wavio.write(filename, audio_data, samplerate, sampwidth=2)

    print("Press 'r' to start recording, 'p' to pause recording, and 'q' to stop recording.")

    with sd.InputStream(samplerate=samplerate, channels=channels, device=device) as stream:
        while True:
            if keyboard.is_pressed('r') and not recording and not paused:
                if os.path.exists(filename):
                    # Create a new filename with an incremental number if the file already exists.
                    filename = get_next_filename(filename)
                print("Recording started. Press 'p' to pause recording and 'q' to stop recording.")
                recording = True
                paused = False

            if keyboard.is_pressed('p') and recording and not paused:
                print("Recording paused. Press 'p' to resume recording.")
                paused = True

            if keyboard.is_pressed('p') and recording and paused:
                print("Recording resumed. Press 'p' to pause recording.")
                paused = False

            if keyboard.is_pressed('q') and (recording or paused):
                print("Recording stopped.")
                break

            if recording and not paused:
                data, overflowed = stream.read(samplerate)
                frames.append(data)

    if frames:
        save_file(frames)

if __name__ == "__main__":
    filename = "recorded_audio.wav"
    # Set the appropriate device name (e.g., 'Microphone (Realtek HD Audio Mic input)')
    device = None  # Replace with the desired input device name

    record_audio(filename, device=device)
