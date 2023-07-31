# Give you a list of availalble recording devices
import sounddevice as sd

def list_input_devices():
    devices = sd.query_devices()
    input_devices = [device['name'] for device in devices if device['max_input_channels'] > 0]
    return input_devices

if __name__ == "__main__":
    input_devices = list_input_devices()
    print("Available input devices:")
    for i, device in enumerate(input_devices, 1):
        print(f"{i}. {device}")
