# Import Necessary Libraries
import speech_recognition as spr
import webbrowser as wb
import pafy
import vlc
import urllib.request
from bs4 import BeautifulSoup
import time

# Create an empty list to store all the video URLs from the youtube.com page
linklist = []

# Create Recognizer() class objects called recog1 and recog2
recog1 = spr.Recognizer()
recog2 = spr.Recognizer()

# Create microphone instance with device microphone chosen whose index value is 0
mc = spr.Microphone(device_index=0)

# Capture voice
with mc as source:
    print("Search Youtube video to play")
    print("----------------------------")
    print("You can speak now")
    audio = recog1.listen(source)

# Based on speech, open youtube search page in a browser, get the first video link and play it in VLC media player
if 'search' in recog1.recognize_google(audio):
    recog1 = spr.Recognizer()
    url = 'https://www.youtube.com/results?search_query='
    with mc as source:
        print('Searching for the video(s)...')
        audio = recog2.listen(source)

        try:
            get_keyword = recog1.recognize_google(audio)
            print(get_keyword)
            wb.get().open_new(url + get_keyword)
            response = urllib.request.urlopen(url + get_keyword)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
                linklist.append('https://www.youtube.com' + vid['href'])
            videolink = pafy.new(linklist[1])
            bestlink = videolink.getbest()
            media = vlc.MediaPlayer(bestlink.url)
            media.play()
        #             time.sleep(60)
        #             media.stop()
        except spr.UnknownValueError:
            print("Unable to understand the input")
        except spr.RequestError as e:
            print("Unable to provide required output".format(e))