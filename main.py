import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai as OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "f97e360c1f03442fb1f299d6cd033112"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    # Initialize the client properly
    client = OpenAI(api_key="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",)  # Make sure to keep your key private

# Create a chat completion
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis."},
        {"role": "user", "content": command}
    ]
)
# Print the assistant's reply
    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
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
    elif c.lower().startswith("play"):
        song = c.lower().strip(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r= requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey= {newsapi}")
        if  r.status_code == 200: 
            # parse the JSON response
            data = r.json()

            # extract the articles
            articales = data.get("articles", [])

            # check if there are any articles
            for article in articales:
                    speak(article ['title'])
    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis......")
    while True:
        # Initialize the recognizer
        r = sr.Recognizer()
 
        # Recognize speech using Google Web Speech API
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source , timeout=2 , phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yaa")
                # listen for further commands
                with sr.Microphone() as source:
                    print("Jarvis active.....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        
        except Exception as e:
            print("Error!; {0}".format(e))
