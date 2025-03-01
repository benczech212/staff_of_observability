import requests
import pyaudio
import wave

def identify_song(api_key, audio_data):
    url = "https://identify-eu-west-1.acrcloud.com/v1/identify"
    headers = {
        "Content-Type": "application/octet-stream",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers, data=audio_data)
    return response.json()

# Replace with your ACRCloud API key and audio data
api_key = "KgE7cWbqOyGrwhTjDrfpKXdmUOKQOMZURmcKFt3s"
# audio_data = open("sample.wav", "rb").read()

# result = identify_song(api_key, audio_data)
# print(result)
def record_audio(filename, duration, sample_rate=44100, channels=2):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1024)
    
    frames = []
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

# Record audio from the microphone
record_audio("recorded_sample.wav", duration=5)

# Use the recorded audio file for song identification
audio_data = open("recorded_sample.wav", "rb").read()
result = identify_song(api_key, audio_data)
print(result)
