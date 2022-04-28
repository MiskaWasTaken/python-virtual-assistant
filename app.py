import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import playsound
import pyjokes
import wikipedia
import webbrowser
import winshell
from pygame import mixer
import dirCleanUp
import wolframalpha

r = sr.Recognizer()
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
# paste google cloud text to speech api credentials here
}"""


# get mic audio
def calibrate():
    with sr.Microphone() as source:
        print("calibrating")
        r.adjust_for_ambient_noise(source, duration=5)
        energy_threshold = r.energy_threshold
    return energy_threshold


energy_threshold = calibrate()


def get_audio():
    with sr.Microphone() as source:
        r.energy_threshold = energy_threshold
        r.dynamic_energy_threshold = False
        print(r.energy_threshold)
        print("Listening...")
        audio = r.listen(source)
        try:
            my_text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            my_text = my_text.lower()
            print(my_text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return
    return my_text.lower()


# speak converted audio to text
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        print("os error")
    tts.save(filename)
    playsound.playsound(filename)


def open_youtube(text):
    speak("What do you want to search for on youtube?")
    keyword = get_audio()
    if keyword != '':
        url = f"https://www.youtube.com/results?search_query={keyword}"
        webbrowser.get().open(url)
        speak(f"Here is what I have found for {keyword} on youtube")


def on_youtube(text):
    if 'for' in text:
        stopwords = ['for', 'on', 'youtube', 'search']
        text_words = text.split()
        result_words = [word for word in text_words if word.lower() not in stopwords]
        result = ' '.join(result_words)

        url = f"https://www.youtube.com/results?search_query={result}"
        webbrowser.get().open(url)
        speak(f"Here is what I have found for {result} on youtube")

    elif 'for' not in text:
        stopwords = ['on', 'youtube', 'search']
        text_words = text.split()
        result_words = [word for word in text_words if word.lower() not in stopwords]
        result = ' '.join(result_words)

        url = f"https://www.youtube.com/results?search_query={result}"
        webbrowser.get().open(url)
        speak(f"Here is what I have found for {result} on youtube")


def search_no_engine_provided(text):
    speak("Please rerun your command with a valid search engine, google or wikipedia")

def search_engine_google(text):
    if 'for' in text:
        stopwords = ['for', 'on', 'google', 'search']
        text_words = text.split()
        result_words = [word for word in text_words if word.lower() not in stopwords]
        result = ' '.join(result_words)
        if " " in result:
            result.replace(" ", "+")

        url = f"https://google.com/search?q{result}"
        webbrowser.get().open(url)
        speak(f"Here is what I have found for {result} on google")

    elif 'for' not in text:
        stopwords = ['on', 'google', 'search']
        text_words = text.split()
        result_words = [word for word in text_words if word.lower() not in stopwords]
        result = ' '.join(result_words)
        if " " in result:
            result.replace(" ", "+")

        url = f"https://google.com/search?q{result}"
        webbrowser.get().open(url)
        speak(f"Here is what I have found for {result} on google")

def search_engine_wikipedia(text):
    if 'for' in text:
        stopwords = ['for', 'on', 'wikipedia', 'search']
        text_words = text.split()
        result_words = [word for word in text_words if word.lower() not in stopwords]
        result = ' '.join(result_words)

        try:
            wikipedia_page = wikipedia.page(result)
            speak(wikipedia.summary(result, sentences=1))
            webbrowser.get().open(wikipedia_page.url)
        except wikipedia.exceptions.PageError as a:
            speak("I could not find any results for your search")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Please be more specific on your search. I have found multiple results for your search")

    elif 'for' not in text:
        stopwords = ['on', 'wikipedia', 'search']
        text_words = text.split()
        result_words = [word for word in text_words if word.lower() not in stopwords]
        result = ' '.join(result_words)

        try:
            wikipedia_page = wikipedia.page(result)
            speak(wikipedia.summary(result, sentences=1))
            webbrowser.get().open(wikipedia_page.url)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("Please be more specific on your search. I have found multiple results for your search")
        except wikipedia.exceptions.PageError as a:
            speak("I could not find any results for your search")
        except wikipedia.exceptions.WikipediaException as b:
            speak("An unknown error has occurred")

def wolfram(text):

    try:
        question = text
        app_id = 'KX96V7-XJA8W64URP'

        client = wolframalpha.Client(app_id)

        res = client.query(question)

        answer = next(res.results).text
        speak(answer)

    except:
        speak("Sorry I dont understand")


# function to respond to commands
def respond(text):
    print("Spoken text: " + text)
    if "on youtube" in text:
        on_youtube(text)
    elif 'youtube' in text:
        open_youtube(text)
    elif 'google' not in text and 'wikipedia' not in text and 'search' in text:
        search_no_engine_provided(text)
    elif 'google' in text:
        search_engine_google(text)
    elif 'wikipedia' in text:
        search_engine_wikipedia(text)
    elif 'joke' in text:
        speak(pyjokes.get_joke())
    elif 'empty recycle bin' in text:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Recycle bin emptied")
    elif 'what time' in text:
        strTime = datetime.today().strftime("%H:%M %p")
        print(strTime)
        speak(strTime)
    elif 'play music' in text or 'play song' in text:
        speak("Now playing...")
        music_dir = "C:\\Users\\UserName\\Downloads\\Music\\music"  # Put your music folder here
        songs = os.listdir(music_dir)
        # counter = 0
        print(songs)
        playmusic(music_dir + "\\" + songs[0])
    elif 'stop music' in text:
        speak("Stopping playback.")
        stopmusic()
    elif 'directory cleanup' in text:
        speak("Provide directory path")
        dir_location = input()
        if os.path.exists(dir_location):
            dirCleanUp.clear_dir(dir_location)
            speak('Directory is organized')
    elif 'exit' in text:
        speak("Goodbye, till next time")
        exit()
    else:
        wolfram(text)


# play music
def playmusic(song):
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()


# stop music
def stopmusic():
    mixer.music.stop()


while True:
    print("I am listening...")
    try:
        text = get_audio()
    except TypeError:
        print("error getting audio, (no audio)")
        text = "blank"
    except UnboundLocalError:
        print("dumb error, ignore")
        text = "blank"

    respond(text)
