import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import requests
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("I didn't understand.")
        return None
    except sr.RequestError:
        speak("Sorry, there seems to be a network issue.")
        return None

# Feature 1: Tell Time
def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

# Feature 2: Play Music on YouTube
def play_song(song_name):
    query = song_name.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    speak(f"Playing {song_name} on YouTube.")
    webbrowser.open(url)

# Feature 3: Get Weather Information
def get_weather(city):
    api_key = "your_openweathermap_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        speak(f"The weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("I couldn't retrieve the weather information.")

# Feature 4: Set Reminders
def set_reminder(task):
    with open("reminders.txt", "a") as file:
        file.write(f"{task}\n")
    speak("Reminder set.")

# Feature 5: Tell a Joke
jokes = [
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "I would tell you a UDP joke, but I'm not sure if you'll get it."
]

def tell_joke():
    joke = random.choice(jokes)
    speak(joke)

# Feature 6: Get News Headlines for Today
def get_today_news():
    api_key = "your_news_api_key"
    today_date = datetime.today().strftime('%Y-%m-%d')
    url = f"https://newsapi.org/v2/everything?q=top-headlines&from={today_date}&sortBy=publishedAt&apiKey={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        speak("Here are the top news headlines for today:")
        for article in articles[:5]:  # Adjust the number of headlines as needed
            speak(article['title'])
    else:
        speak("I couldn't retrieve the news headlines.")

# Feature 7: Open Applications
def open_application(app_name):
    app_name = app_name.lower()
    if "notepad" in app_name:
        os.system("notepad")
    elif "calculator" in app_name:
        os.system("calc")
    elif "chrome" in app_name:
        os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
    else:
        speak("I couldn't find the application.")

# Feature 8: Basic Math Calculations
def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

# Feature 9: Activation Greeting
def activate_assistant():
    speak("How can I help you?")

# Command Handler
def handle_command(command):
    if "time" in command:
        tell_time()
    elif "play" in command:
        speak("Which song would you like to hear?")
        song_name = listen()
        if song_name:
            play_song(song_name)
    elif "weather" in command:
        speak("Please tell me the city name.")
        city = listen()
        if city:
            get_weather(city)
    elif "set reminder" in command:
        speak("What should I remind you about?")
        reminder = listen()
        if reminder:
            set_reminder(reminder)
    elif " Tell joke" in command:
        tell_joke()
    elif "news" in command:
        get_today_news()
    elif "open" in command:
        speak("Which application would you like to open?")
        app_name = listen()
        if app_name:
            open_application(app_name)
    elif "calculate" in command:
        speak("What would you like to calculate?")
        expression = listen()
        if expression:
            calculate(expression)
    else:
        speak("I didn't understand that command.")

# Main Loop
def main():
    while True:
        command = listen()
        if command:
            if "hey assistant" in command:
                activate_assistant()
                command = listen()
                if command:
                    handle_command(command)
            elif "exit" in command or "stop" in command:
                speak("Goodbye!")
                break

if __name__ == "__main__":
    main()
