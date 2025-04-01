import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit

# Text-to-Speech Engine Initialization
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Selecting an available voice
engine.setProperty('rate', 150)  # Set speech speed

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Function to greet based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How may I help you?")

def take_command():
    """Function to take voice input and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1  # Adjust the threshold for pause duration
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "none"
    except sr.RequestError:
        speak("Please check your internet connection.")
        return "none"

def search_wikipedia(query):
    """Function to search Wikipedia."""
    query = query.replace("wikipedia", "").strip()
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No results found on Wikipedia.")

def send_whatsapp_message(number, message):
    """Function to send a WhatsApp message."""
    try:
        pywhatkit.sendwhatmsg_instantly(f"+91{number}", message)
        speak("Message sent successfully.")
    except Exception as e:
        speak(f"Failed to send message. Error: {str(e)}")

def voice_chat():
    """Function for real-time voice chat."""
    speak("Starting voice chat. You can talk to me now.")
    while True:
        command = take_command()
        if "stop chat" in command:
            speak("Ending voice chat.")
            break
        process_command(command)

def process_command(command):
    """Function to process commands."""
    if 'wikipedia' in command:
        search_wikipedia(command)
    elif 'send message' in command:
        speak("Please provide the phone number.")
        number = take_command()
        speak("What message should I send?")
        message = take_command()
        send_whatsapp_message(number, message)
    elif 'voice chat' in command:
        voice_chat()
    elif 'exit' in command or 'quit' in command or 'stop' in command:
        speak("Goodbye! Have a great day!")
        exit(0)
    else:
        speak("I didn't understand that. Please try again.")

if __name__ == "__main__":
    wish_me()
    while True:
        command = take_command()
        if command and command != "none":
            process_command(command)