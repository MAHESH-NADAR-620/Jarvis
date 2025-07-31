# Importing necessary libraries
import speech_recognition as sr  # For voice recognition
import webbrowser  # To open websites
import pyttsx3  # For text-to-speech
import musicLibrary  # Custom music library with predefined songs and links
import requests  # For API requests (like news)
from together import Together  # AI processing library (free alternative to OpenAI)

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer() 
engine = pyttsx3.init()

# Configure voice settings (can be customized)
voices = engine.getProperty('voices')
# for voice in voices:
#     if "female" in voice.name.lower() or "zira" in voice.name.lower():
#         engine.setProperty('voice', voice.id)
        # break

# NewsAPI key (used for fetching news)
newsapi = "f97e360c1f03442fb1f299d6cd033112"

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to generate AI response using Together API
def aiprocess(command):
    # Initialize Together client with your API key
    client = Together(api_key="")

    # Create a chat completion using Mixtral model
    completion = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis,you take orders from your Mahesh (your master)only."},
            {"role": "user", "content": command}
        ]
    )
    # Return the AI-generated response
    return completion.choices[0].message.content

# Function to process spoken commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open Facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open Twitter" in c.lower():
        webbrowser.open("https://www.twitter.com")
    elif "open Linkedin" in c.lower():  
        webbrowser.open("https://www.linkedin.com") 
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open Chrome" in c.lower(): 
        webbrowser.open("https://www.google.com/chrome/") 
    elif "open Spotify" in c.lower():
        webbrowser.open("https://open.spotify.com/")
    
    # If command starts with "play", try playing the song
    elif c.lower().startswith("play"):
        song = c[5:].strip()  # Extract song name after "play"
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            musicLibrary.play_song(song)  # Play using Spotify
            speak(f"Playing {song} on Spotify.")

    # Handle news fetching
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey= {newsapi}")
        if r.status_code == 200: 
            data = r.json()
            articales = data.get("articles", [])
            for article in articales:
                speak(article['title'])

    # If none of the above, send to AI
    else:
        output = aiprocess(c)
        speak(output)

# Main program loop
if __name__ == "__main__":
    speak("Initializing Jarvis......")  # Start message
    r = sr.Recognizer()

    # Calibrate for background noise
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Calibrated for ambient noise.")
    
    activated = False  # Track whether Jarvis is active

    while True:
        try:
            with sr.Microphone() as source:
                if not activated:
                    print("Say 'Jarvis' to activate...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    word = r.recognize_google(audio)
                    print(f"Heard: {word}")
                    if word.lower() == "jarvis":
                        speak("Yaa, How may I help you.")
                        activated = True
                else:
                    print("Listening for command...")
                    r.adjust_for_ambient_noise(source, duration=0.3)
                    audio = r.listen(source, timeout=5, phrase_time_limit=7)
                    try:
                        command = r.recognize_google(audio)
                        print(f"Command: {command}")
                        if command.lower() in ["exit", "quit", "stop listening"]:
                            speak("Thank you, going to sleep. Say 'Jarvis' to wake me up.")
                            activated = False
                        else:
                            processCommand(command)
                    except sr.UnknownValueError:
                        speak("Sorry, I did not understand that. Please repeat your command.")
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that, there is noise around you.")
        except Exception as e:
            print("Error!; {0}".format(e))
