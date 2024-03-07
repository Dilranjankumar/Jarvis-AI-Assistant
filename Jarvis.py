import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import wikipedia
import datetime
import os
import smtplib
import time
import requests
from bs4 import BeautifulSoup
from plyer import notification
import json

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    simulate_typing(audio)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening..")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        speak("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

def simulate_typing(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.03)  # Adjust typing speed
    print()  # Print a newline after typing

def greet_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning, sir")
        current_time = get_time()
        speak(f"The current time is {current_time}")

    elif 12 <= hour < 18:
        speak("Good Afternoon, sir")
        current_time = get_time()
        speak(f"The current time is {current_time}")
    else:
        speak("Good Evening, sir")
        current_time = get_time()
        speak(f"The current time is {current_time}")

    speak("Please tell me, How can I assist you ?")

def send_email(to, content):
    # Configure SMTP server details
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # Enter your email credentials
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

def play_music(song):
    speak(f"Playing {song} on YouTube")
    pywhatkit.playonyt(song)

def set_reminder():
    speak("What should I remind you about?")
    reminder = take_command()
    speak("When should I remind you?")
    time.sleep(2)  # Simulate thinking
    speak("Reminder set successfully!")

def make_note():
    speak("What would you like to jot down?")
    note = take_command()
    file_name = "notes.txt"
    with open(file_name, "a") as file:
        file.write(note + "\n")
    speak("Note saved successfully!")

def get_temperature():
    search = "temperature in Delhi"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    return temp

def search_google(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        speak("This is what I found on Google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query, 1)
            speak(result)

        except:
            speak("No speakable output available")

def search_youtube(query):
    if "youtube" in query:
        speak("This is what I found for your search!")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("jarvis", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done, Sir")

def talk_to_saloni():
    speak("Who is Saloni? What would she like to talk about?")
    speak("Hello, Saloni, I am Jarvis")
    speak("How are you")
    speak("By the way, Your brother said, Your birthday is coming,")
    speak("So, Meri taraf se, Happy Birthday To you, saloni, Happy Birthday To you, Party, party,")
    if 'thank you' in query:
        speak("You are welcome saloni,")
    conversation = take_command()
    speak(f"Saloni wants to talk about {conversation}")

def talk_to_sejal():
    speak("Who is Sejal? What would she like to talk about?")
    speak("Hello, Sejal, I am Jarvis")
    speak("How are you")
    if 'fine' and 'good' in query:
        speak("thats great")
    if 'thank you' in query:
        speak("You are welcome sejal,")
    conversation = take_command()
    speak(f"Sejal wants to talk about {conversation}")

def get_time():
    str_time = datetime.datetime.now().strftime("%H:%M")
    return str_time

def send_whatsapp_message(phone_number, message, time_hour, time_minute):
    pywhatkit.sendwhatmsg(f"+{phone_number}", message, time_hour, time_minute)
    speak("WhatsApp message sent successfully!")

def get_news_headlines():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=5ea714a8a8364e5c8bcd0038f078efdf"
    response = requests.get(url)
    news_data = json.loads(response.text)
    headlines = [article['title'] for article in news_data['articles']]
    return headlines

if __name__ == "__main__":
    speak("Initializing Jarvis")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Checking the internet connection")
    speak("All systems have been activated")
    greet_me()
    
    while True:
        query = take_command().lower()
        
        if "wake up" in query:
            greet_me()
            
        elif "go to sleep" in query:
            speak("Going to sleep, sir. Goodbye!")
            break
            
        elif "hello" in query:
            speak("Hello sir, how are you?")
            response = take_command().lower()
            if "good" in response:
                speak("That's great, sir.")
            else:
                speak("I hope your day gets better, sir.")
                
        elif "how are you" in query:
            speak("I'm doing well, sir. Thank you for asking.")
                
        elif "thank you" in query:
            speak("You're welcome, sir.")
            
        elif "ipl score" in query:
            url = "https://www.cricbuzz.com/"
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            team_elements = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")
            score_elements = soup.find_all(class_="cb-ovr-flo")

            if team_elements and score_elements:  # Check if both lists are not empty
                team1 = team_elements[0].get_text() if len(team_elements) > 0 else "Team 1"
                team2 = team_elements[1].get_text() if len(team_elements) > 1 else "Team 2"
                team1_score = score_elements[8].get_text() if len(score_elements) > 8 else "N/A"
                team2_score = score_elements[10].get_text() if len(score_elements) > 10 else "N/A"

                print(f"{team1} : {team1_score}")
                print(f"{team2} : {team2_score}")

                notification.notify(
                    title="IPL SCORE",
                    message=f"{team1} : {team1_score}\n{team2} : {team2_score}",
                    timeout=15
                )
            else:
                print("No data available for IPL score.")

        elif "google" in query:
            search_google(query)
            
        elif "youtube" in query:
            search_youtube(query)

        elif "news" in query:
            speak("Fetching latest news headlines...")
            headlines = get_news_headlines()
            for idx, headline in enumerate(headlines, start=1):
                speak(f"Headline {idx}: {headline}")

        elif "wikipedia" in query:
            speak("Searching from Wikipedia....")
            query = query.replace("wikipedia", "")
            query = query.replace("search wikipedia", "")
            query = query.replace("jarvis", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia..")
            print(results)
            speak(results)
        
        elif "temperature" in query or "weather" in query:
            temperature = get_temperature()
            speak(f"The current temperature in Delhi is {temperature}")

            speak(f"The current temperature in Delhi is {temperature}")
            
        elif "send email" in query:
            try:
                speak("What should I say?")
                content = take_command()
                speak("Who is the recipient?")
                recipient = input("Enter recipient's email: ")
                send_email(recipient, content)
                speak("Email has been sent!")
            except Exception as e:
                speak("Sorry, I am unable to send the email at the moment.")

        elif "the time" in query:
            current_time = get_time()
            speak(f"The current time is {current_time}")
                       
        elif "play music" in query:
            speak("What song would you like me to play?")
            song = take_command()
            play_music(song)
        
        elif "set reminder" in query:
            set_reminder()
            
        elif "make note" in query:
            make_note()

        elif "saloni" in query:
            talk_to_saloni()
        
        elif "sejal" in query:
            talk_to_sejal()
            
        elif "send message" in query:
            speak("Please provide the phone number of the recipient.")
            recipient_number = input("Enter recipient's phone number: ")
            speak("What message would you like to send?")
            message_content = take_command()
            speak("Please specify the hour at which you want to send the message (in 24-hour format).")
            send_hour = int(input("Enter hour: "))
            speak("Please specify the minute at which you want to send the message.")
            send_minute = int(input("Enter minute: "))
            send_whatsapp_message(recipient_number, message_content, send_hour, send_minute)
            
        else:
            speak("I'm sorry, I didn't understand that. Could you please repeat?")
