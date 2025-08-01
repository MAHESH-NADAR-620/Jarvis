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
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

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
            {"role": "system", "content": "You are a virtual assistant named Sweety,you take orders from your Mahesh (your master)only."},
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
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open twitter" in c.lower():
        webbrowser.open("https://www.twitter.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open chrome" in c.lower():
        webbrowser.open("https://www.google.com/chrome/")
    elif "open spotify" in c.lower():
        webbrowser.open("https://open.spotify.com/")
    elif c.lower().startswith("open "):
        site = c.lower().split("open ")[1].strip()
        # If user says only the name (e.g., "instagram"), add ".com"
    if not site.startswith("http"):
        if "." not in site:
            site = site + ".com"
        site = "https://www." + site
        webbrowser.open(site)
        speak(f"Opening {site}")
    elif c.lower().startswith("play"):
        song_query = c[5:].strip()
        if " by " in song_query.lower():
            parts = song_query.split(" by ")
            track = parts[0].strip()
            artist = parts[1].strip()
            search_query = f"track:{track} artist:{artist}"
        else:
            search_query = song_query
        results = musicLibrary.sp.search(q=search_query, type='track', limit=1)
        tracks = results['tracks']['items']
        if tracks:
            track_url = tracks[0]['external_urls']['spotify']
            webbrowser.open(track_url)
            speak(f"Opening {tracks[0]['name']} by {tracks[0]['artists'][0]['name']} on Spotify.")
        else:
            speak("Song not found on Spotify.")
            print("Song not found on Spotify.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            for article in articles:
                speak(article['title'])
        else:
            speak("Failed to fetch news.")
            print("Failed to fetch news.")
    else:
        # If command is not recognized, answer as a question using AI
        answer = aiprocess(c)
        print(f"Jarvis: {answer}")
        speak(answer)

# Main program loop
if __name__ == "__main__":
    speak("Jarvis, on your service......")  # Start message
    r = sr.Recognizer()

    # Calibrate for background noise once
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Calibrated for ambient noise.")

    activated = False  # Track whether Sweety is active

    while True:
        try:
            with sr.Microphone() as source:
                if not activated:
                    print("Say 'Jarvis' to activate...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    word = r.recognize_google(audio)
                    print(f"Heard: {word}")
                    if word.lower() == "Jarvis":
                        speak("Yaa, How may I help you.")
                        activated = True
                else:
                    print("Listening for command...")
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
            print(f"Error!; {e}")
