# Importing Necessary Libraries
import wave
import vlc
import pafy
import time

from pyaudio import PyAudio
from speech_recognition import Recognizer, AudioFile
from apiclient.discovery import build

# Initializing the Microphone and setting it to record voice command for 4 seconds
CHUNK = 1024
FORMAT = 8
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 4

p = PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
print("Say Something to search on Youtube")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Searching....")
stream.stop_stream()
stream.close()
p.terminate()

# The developer key is collected from Google API's. I used the YouTube Data API version 3 for this project.
DEVELOPER_KEY = "AIzaSyCE5ZroTAISq_1IzfURnqzKp-CC3ZZIT0Y"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

# Here, I am saving the recorded audio into a file named output.wav
WAVE_OUTPUT_FILENAME = "output.wav"

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Now, I am using the Speech recoginition library to recognize the speech stored in the audio file.
# I am passing the recorded audio file to the Speech recoginition library
r = Recognizer()
temp_audio = AudioFile(WAVE_OUTPUT_FILENAME)
with temp_audio as source:
    audio = r.record(source)
try:
    output = r.recognize_google(audio)
except:
    print("Error Try again")
if "play" in output:
    output.replace("play", "")
# This part will search in youtube with the given keyword through microphone. It will use the YouTube data API for that.
search_keyword = youtube.search().list(q=output, part="id, snippet",
                                       maxResults=1).execute()
url = f"https://www.youtube.com/watch?v={search_keyword['items'][0]['id']['videoId']}"
# Checking if I have the right youtube url of the video I'm looking for
print(url)

video = pafy.new(url)
best = video.getbest()
playurl = best.url
ins = vlc.Instance()
player = ins.media_player_new()

Media = ins.media_new(playurl)
Media.get_mrl()
player.set_media(Media)
player.play()

time.sleep(50)

