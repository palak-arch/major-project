from tkinter import *
import tkinter as tk
import pyttsx3
import pywhatkit
import wikipedia
import os
import subprocess
import webbrowser
import datetime
from pyowm import OWM
import requests
import random

# GUI
root = Tk()
root.title("Chatbot")

# Initialize the text-to-speech engine
Assistant = pyttsx3.init('sapi5')
voices = Assistant.getProperty('voices')
Assistant.setProperty('voice', voices[1].id)

def Speak(audio):
    statement = "Assistant: " + audio
    print(statement)  # Print the statement

    # Stop the TTS engine if it's already running
    Assistant.stop()

    Assistant.say(audio)  # Speak the message
    Assistant.runAndWait()
    return statement  # Return the spoken statement

def get_current_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"The current time is {current_time}."
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        Speak("Good Morning!")
    elif 12 <= hour < 18:
        Speak("Good Afternoon!")
    else:
        Speak("Good Evening!")

def speak_date():
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    response=Speak(f"Today is {today}")
    bot_statement = "VERTIGO -> " + response
    txt.insert(END, "\n" + bot_statement)
    Speak(response)
def get_weather(city_name):
    owm = OWM('3b91764244d706e6dceab2dc46490cb5')  # Replace with your OpenWeatherMap API key
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(city_name)
    w = observation.weather

    weather_info = f"The weather in {city_name} is {w.detailed_status}. "
    weather_info += f"The temperature is {w.temperature('celsius')['temp']}°C."
    bot_statement = "VERTIGO -> " + weather_info
    txt.insert(END, "\n" + bot_statement)
    Speak(bot_statement)
    return weather_info
# Function to fetch a random English joke
def get_english_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a rose that wants to go to the moon? Gulab ja moon",
        "What do you call a labrador that becomes a magician? Labracadabrador",
        "What is the most shocking city in the world? Electricity",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "I told my wife she should embrace her mistakes. She gave me a hug.",
        # Add more English jokes as needed
    ]
    joke = random.choice(jokes)
    response = Speak(joke)
    bot_statement = "VERTIGO -> " + response
    txt.insert(END, "\n" + bot_statement)
    Speak(response)

# Function to fetch a random Hindi joke
def get_hindi_joke():
    jokes = [
        "Ek dost ne poocha: Teri girlfriend tere saath kaise rehti hai?\nMaine kaha: Bilkul nayi baat hai, main uske saath rehta hoon!",
        "Baccha: Papa, tum shaadi ke liye kaunsi baatein dekhte ho?\nPapa: Yahi ki kahin teri maa mujhse kam umar ki na ho!",
        "Mohabbat aur bank loot ek hi baat hai,\nbas fark itna hai ki\nek mein paisa lootte hain aur doosre mein dil!"
    ]
    joke = random.choice(jokes)
    response = Speak(joke)
    bot_statement = "VERTIGO -> " + response
    txt.insert(END, "\n" + bot_statement)
    Speak(response)

# Function to play a song on Spotify

# Replace 'YOUR_NEWS_API_KEY' with the actual API key you obtained from News API
NEWS_API_KEY = 'c099a32bdc704307a93c846fc0edbf06'

# Function to get today's news headlines
def get_news(num_articles=5):
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'  # Adjust the country code if needed
    response = requests.get(news_url)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])

        if articles:
            news_info = "Here are today's headlines:\n"
            for idx, article in enumerate(articles[:num_articles]):
                news_info += f"{idx + 1}. {article['title']}\n"
            return news_info
            bot_statement = "Bot -> " + news_info
            txt.insert(END, "\n" + bot_statement)
            Speak(news_info)
        else:
            return "Sorry, I couldn't fetch the latest news at the moment."
    else:
        return "Sorry, I couldn't fetch the latest news at the moment."

# Function to get today's sports news headlines
def get_sports_news(num_articles=5):
    sports_url = f'https://newsapi.org/v2/top-headlines?category=sports&apiKey={NEWS_API_KEY}'
    response = requests.get(sports_url)

    if response.status_code == 200:
        sports_data = response.json()
        articles = sports_data.get('articles', [])

        if articles:
            sports_headlines = [article['title'] for article in random.sample(articles, min(num_articles, len(articles)))]
            return f"Here are the latest sports updates:\n" + "\n".join(f"{idx + 1}. {headline}" for idx, headline in enumerate(sports_headlines))
        else:
            return "Sorry, I couldn't fetch the latest sports news at the moment."
    else:
        return "Sorry, I couldn't fetch the latest sports news at the moment."
def play_music():
     music_dir = "C:\\Users\\sejal\\Music"
     songs = os.listdir(music_dir)
     user_input = entry.get().lower()
     # Check if the provided song name is in the list of songs
     if user_input in songs:
         os.startfile(os.path.join(music_dir, user_input))
         Speak(f"Now playing {user_input}")
     else:
         pywhatkit.playonyt(user_input)
         Speak(f"Now playing {user_input} from YouTube.")

# Function to search YouTube
def youtube_search(query):
    query = query.replace("VERTIGO", "")
    query = query.replace("youtube search", "")
    web = 'https://www.youtube.com/results?search_query=' + query
    webbrowser.open(web)
    Speak("Done Sir!")

# Send function
def send():
    query = entry.get().lower()
    if query == "helo":
        statement="user=>"+query
        txt.insert(END, "\n" + statement)
        response = "Hi there, how can I help?"
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif query == "how are you":
        statement = "user=>"+query
        txt.insert(END, "\n" + statement)
        response = "I'm doing well, thank you!"
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'hello' in query or 'hey' in query or 'hii' in query:
        response = random.choice(
            ["Hello! How can I assist you?", "Hi there!", "Hey! What can I do for you?",

             "Good morning! How can I be of service?", "Good afternoon! What do you need assistance with?",
             "Good evening! How may I assist you?", "Hey there! How can I help?",
             "Hi! What's on your mind?",
             "Hello there! How can I assist you today?"])
        statement = "user=>"+query
        txt.insert(END, "\n" + statement)
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'how are you' in query:
        response = random.choice(["I'm doing well, thank you!", "I'm great! How can I assist you?",
                                  "I'm here and ready to help!", "I'm good, thanks for asking.",
                                  "I'm functioning at full capacity! How may I assist you today?"])
        statement = "user=>"+query
        txt.insert(END, "\n" + statement)
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'how was your day' in query:
        response = random.choice(["My day is going smoothly, thank you!", "It's been a good day so far.",
                                  "I'm having a productive day! How can I help you?",
                                  "Every day is a good day for assistance! What can I do for you?"])
        statement = "user=>"+query
        txt.insert(END, "\n" + statement)
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'what are you doing' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["I'm here, ready to assist you!", "I'm always at your service.",
                                  "Just here, waiting for your commands.",
                                  "I'm busy helping users like you!"])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)



    elif 'what is your favorite color' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "I love purple color."
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'what do you like to talk about' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "I enjoy talking about various topics! Feel free to ask me anything, and I'll do my best to assist you."
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'tell me something interesting' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "Sure! Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible."
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'do you have any hobbies' in query or 'your hobbies ' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "I don't have personal hobbies, but I'm here to help and engage in conversations with you!"
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif "what's your favorite book" in query or "favorite book" in query :
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "I don't have personal preferences for books. However, I can help you find information or recommend books based on your interests. What genre are you into?"
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif "what's your favorite movie" in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "I don't have personal movie preferences, but I can suggest movies based on your taste. What genre are you in the mood for?"
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'hi' in query or 'hey' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(
            ["Hey! How can I assist you?", "Hi there!", "Hello! What can I do for you?",
             "Howdy! What brings you here?", "Greetings! How may I help you?",
             "Hi! What's on your mind?", "Hello there! How can I assist you today?"])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'bye' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Goodbye!", "See you later!", "Have a great day!", "Farewell! Take care.",
                                  "Goodbye! Until next time.", "Take care! Have a wonderful day.",
                                  "Bye bye!",
                                  "Catch you later!", "Have a good one!", "So long!"])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'thank you' in query or 'thanks' in query or 'appreciate it' in query or 'thank you so much' in query or 'thanks a lot' in query or 'much appreciated' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["You're welcome!", "Happy to help!", "Glad I could assist.", "Anytime!",
                                  "You're welcome! Have a great day.", "No problem!"])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'sorry' in query or 'my apologies' in query or 'apologize' in query or 'I\'m sorry' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(
            ["No problem at all.", "It's alright.", "No need to apologize.", "That's okay.",
             "Don't worry about it.", "Apology accepted."])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'great job' in query or 'well done' in query or 'awesome' in query or 'fantastic' in query or 'amazing work' in query or 'excellent' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Thank you! I appreciate your feedback.", "Glad to hear that!",
                                  "Thank you for the compliment!",
                                  "I'm glad I could meet your expectations.", "Your words motivate me!",
                                  "Thank you for your kind words."])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'not good' in query or 'disappointed' in query or 'unsatisfied' in query or 'poor service' in query or 'needs improvement' in query or 'could be better' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(
            ["I'm sorry to hear that. Can you please provide more details so I can assist you better?",
             "I apologize for the inconvenience. Let me help resolve the issue.",
             "I'm sorry you're not satisfied. Please let me know how I can improve.",
             "Your feedback is valuable. I'll work on improving."])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'what\'s the weather like?' in query or 'weather forecast' in query or 'is it going to rain today?' in query or 'temperature today' in query or 'weather report' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        city_name = "Solan"  # Replace with your desired city
        weather_info = get_weather(city_name)
        response = Speak(weather_info)
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'help' in query or 'can you help me?' in query or 'I need assistance' in query or 'support' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Sure, I'll do my best to assist you.", "Of course, I'm here to help!",
                                  "How can I assist you?",
                                  "I'll help you with your query."])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'what\'s the time?' in query or 'current time' in query or 'time please' in query or 'what time is it?' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        time_info = get_current_time()
        response = Speak(time_info)
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'joke' in query or 'joke please' in query or 'got any jokes?' in query or 'make me laugh' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Why don't we ever tell secrets on a farm? Because the potatoes have eyes and the corn has ears!",
            "What do you get when you cross a snowman and a vampire? Frostbite!",
            "Why was the math book sad? Because it had too many problems!"])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)


    elif 'recommend restaurant' in query or 'food places nearby' in query or "what's good to eat?" in query or 'restaurant suggestion' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Sure, here are some recommended restaurants: ",
                                  "Hungry? Let me find some good food places for you!",
                                  "I can suggest some great places to eat nearby."])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
        city_name = "kandaghat"  # Replace with the desired city name
        location_query = f"restaurants in {city_name}"

        # Construct the Google Maps URL for the restaurant search
        maps_url = f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}"

        # Open the Google Maps URL in the default web browser
        webbrowser.open(maps_url)

        response = " I've opened Google Maps to show you nearby restaurants. Take a look!"
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'tourist places' in query or 'places to visit' in query or 'tourism places' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Certainly! Here are some popular tourist places: ",
                                  "Interested in sightseeing? I can recommend some great places to visit!",
                                  "Let me suggest some tourist attractions for you."])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
        city_name = "Solan"  # Replace with the desired city name
        location_query = f"tourist places in {city_name}"

        # Construct the Google Maps URL for the tourist places search
        maps_url = f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}"

        # Open the Google Maps URL in the default web browser
        webbrowser.open(maps_url)

        response = " I've opened Google Maps to show you nearby tourist places. Enjoy exploring!"
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'maps' in query or 'show me the map' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "Sure, I can show you the map. Opening Google Maps."
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
        # Open Google Maps in the default web browser
        webbrowser.open("https://www.google.com/maps/")
    elif 'latest news' in query or 'news updates' in query or 'what\'s happening?' in query or 'current events' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(
            ["Let me fetch the latest news for you.", "Here are the top headlines: [news_headlines]",
             "Stay updated with the latest news!"])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
        response = get_sports_news(num_articles=5)
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

        news_headlines = get_news(num_articles=5)
        for headline in news_headlines:
            bot_statement = "VERTIGO -> " + response
            txt.insert(END, "\n" + bot_statement)
            Speak(response)


    elif 'movie suggestions' in query or 'recommend a movie' in query or 'what should I watch' in query or 'best movies' in query:
        movie_suggestions = ["The Shawshank Redemption", "The Godfather", "Pulp Fiction", "Inception",
                             "The Dark Knight", "Forrest Gump", "The Matrix", "Schindler's List"]

        statement = "user=>" + query
        txt.insert(END, "\n" + statement)

        response = random.choice(["How about watching ?", "Here's a movie suggestion for you: .",
                                  "Let me recommend some great movies!"])
        movie_name = random.choice(movie_suggestions)
        response = Speak(response.format(movie_name))
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'sports news' in query or 'score updates' in query or 'latest sports events' in query or 'upcoming games' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(
            ["I'll get you the latest sports updates.", "Stay updated with the current sports events!",
             "Let me check the sports scores for you."])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
        response = get_sports_news(num_articles=5)
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)


    elif 'travel tips' in query or 'travelling tomorrow' in query or 'travel advice' in query or 'plan a trip' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = Speak(
            "Certainly! What type of travel tips are you looking for? Are you interested in packing tips or general travel advice?")
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

        travel_preference =entry.get().lower()

        if travel_preference:
            # Mapping user preferences to travel categories
            travel_category_mapping = {
                'packing tips': ['Pack versatile clothing', 'Don\'t forget essential documents',
                                 'Pack a portable charger'],
                'general travel advice': ['Research local customs', 'Stay hydrated during the journey',
                                          'Plan some downtime']
            }

            # Check if the user's preference is a valid travel category
            if travel_preference.lower() in travel_category_mapping:
                travel_tips = travel_category_mapping[travel_preference.lower()]
                statement = "user=>" + query
                txt.insert(END, "\n" + statement)
                response = Speak(
                    f"Great choice! Here are some {travel_preference.lower()} for your trip: {', '.join(travel_tips)}. Safe travels!")
                bot_statement = "VERTIGO-> " + response
                txt.insert(END, "\n" + bot_statement)
                Speak(response)
            else:
                statement = "user=>" + query
                txt.insert(END, "\n" + statement)
                response = Speak(
                    "I'm sorry, I couldn't find travel tips for that category. Please choose from the provided options.")
            bot_statement = "VERTIGO-> " + response
            txt.insert(END, "\n" + bot_statement)
            Speak(response)
        else:
            statement = "user=>" + query
            txt.insert(END, "\n" + statement)
            response = Speak(
                "I'm sorry, I didn't catch that. Can you please specify the type of travel tips you're looking for?")
            bot_statement = "VERTIGO-> " + response
            txt.insert(END, "\n" + bot_statement)
            Speak(response)
    elif 'fitness advice' in query or 'workout tips' in query or 'fitness tips' in query or 'exercise suggestions' in query or 'healthy habits' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = Speak("Staying fit is important! Here are some fitness tips:")

        # Fitness tips
        fitness_tips = [
            "Stay hydrated by drinking plenty of water throughout the day.",
            "Incorporate a mix of cardio and strength training exercises into your routine.",
            "Ensure you get an adequate amount of sleep for recovery.",
            "Eat a balanced diet with a variety of fruits, vegetables, lean proteins, and whole grains.",
            "Listen to your body and avoid pushing yourself too hard to prevent injuries.",
            "Take short breaks and stretch if you have a desk job to avoid sitting for long periods.",
            "Find physical activities you enjoy to make staying active more enjoyable.",
            "Set realistic fitness goals and celebrate your achievements along the way.",
            "Consider consulting with a fitness professional for personalized advice and guidance."
        ]

        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response += "\n".join(fitness_tips)

        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)


    elif 'learning resources' in query or 'study tips' in query or 'education advice' in query or 'academic help' in query:
        educational_websites = ["Khan Academy", "Coursera", "edX", "Quizlet", "Duolingo"]
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Let's explore learning resources together. Have you tried websites like {}?",
            "Tell me about your educational goals or questions. You might find {} helpful."
        ]).format(', '.join(educational_websites))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'pet care tips' in query or 'animal advice' in query or 'pet health' in query or 'taking care of pets' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Pets are wonderful! Here are some pet care tips: [pet_care_tips]",
                                  "I can provide advice on pet health and care.",
                                  "Let's talk about your pet and their well-being."])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'online shopping' in query or 'buying something' in query or 'shopping advice' in query or 'product recommendations' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "I can help you with online shopping",
            "Let's find the perfect website for you!",

        ])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

        # Ask about specific shopping websites
        websites = ['Amazon', 'Flipkart', 'Myntra', 'eBay', 'Walmart',
                    'Target']  # Add more websites as needed
        website_query = "Do you have a specific website in mind? You can choose from {}.".format(
            ', '.join(websites))

    elif 'mental health support' in query or 'coping strategies' in query or 'stress relief tips' in query or 'emotional well-being' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Mental health is important. How can I support you?",
                                  "I can provide guidance for managing stress and emotions.",
                                  "Let's talk about strategies for maintaining mental well-being."])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'language learning tips' in query or 'language practice' in query or 'learning new languages' in query or 'language study advice' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Learning a new language can be exciting! How can I assist you?",
                                  "I can help with language learning tips and practice.",
                                  "Tell me which language you're interested in learning."])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'financial planning help' in query or 'money management tips' in query or 'investment advice' in query or 'budgeting assistance' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "I can provide guidance on financial matters. What specific advice do you need?",
            "Let's discuss your financial goals and plans.",
            "Tell me about your financial situation or goals."
        ])

        # Add some actual financial tips
        financial_tips = [
            "Consider creating a budget to track your income and expenses.",
            "Diversify your investments to manage risk in your portfolio.",
            "Start an emergency fund to cover unexpected expenses.",
            "Review and update your financial goals regularly.",
            "Explore tax-saving investment options to optimize your returns."
        ]

        response += " Here are some financial tips for you: {}".format(', '.join(financial_tips))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'fun facts' in query or 'tell me something interesting' in query or 'another funfact' in query or 'interesting facts' in query or 'did you know' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Sure, did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
            "Here's an interesting fact: The world's largest desert is not the Sahara, but Antarctica!",
            "Did you know that a group of flamingos is called a 'flamboyance'?",
            "In Japan, there's a town called 'Nagoro' where dolls outnumber people. The dolls are placed throughout the town, and it creates a unique atmosphere.",
            "The shortest war in history was between Britain and Zanzibar in 1896. Zanzibar surrendered after 38 minutes!",
            "Bananas are berries, but strawberries aren't. In botanical terms, berries are fleshy fruits produced from a single ovary, and bananas fit the bill!",
            "Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body.",
            "The Eiffel Tower can be 15 cm taller during the summer. When a substance is heated up, its particles move more, and it takes up a larger volume.",
            "Cows have best friends and can become stressed when they are separated.",
            "The Great Wall of China is not visible from the Moon without aid, contrary to the popular belief.",
            "A 'jiffy' is an actual unit of time. It's defined as the time it takes for light to travel one centimeter in a vacuum, approximately 33.3564 picoseconds.",
            "Honeybees can recognize human faces.",
            "A group of crows is called a 'murder.'",
            "The longest English word without a vowel is 'rhythms.'",
            "The word 'nerd' was first coined by Dr. Seuss in 'If I Ran the Zoo' in 1950."
        ])
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'Technology trends' in query or 'another Trend' in query or 'latest gadgets' in query or 'innovations' in query or 'tech news' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Let me provide you with the latest technology trends.",
            "Here are some cutting-edge gadgets: [gadget_names]",
            "Stay updated on technological innovations with our tech news!",
            "Did you know that artificial intelligence is revolutionizing industries by automating tasks and enhancing decision-making processes?",
            "Quantum computing is making significant strides in solving complex problems that were once considered unsolvable by classical computers.",
            "The Internet of Things (IoT) is connecting everyday devices to the internet, enabling seamless communication and smart functionalities.",
            "Augmented Reality (AR) and Virtual Reality (VR) are transforming the way we experience and interact with the digital world.",
            "Blockchain technology is not just about cryptocurrencies; it's being used for secure and transparent transactions in various industries.",
            "5G technology is paving the way for faster and more reliable wireless communication, unlocking new possibilities for connectivity.",
            "Biometric authentication, such as fingerprint and facial recognition, is becoming increasingly common for securing devices and services.",
            "Robotics advancements are leading to the development of more sophisticated and versatile robots for various applications.",
            "Renewable energy technologies, like solar and wind power, continue to advance, contributing to a more sustainable and eco-friendly future.",
            "Edge computing is gaining prominence, allowing data processing to occur closer to the source, reducing latency and improving efficiency.",
            "Voice assistants and natural language processing are enhancing human-computer interaction, making devices more intuitive and user-friendly.",
            "Cybersecurity measures are evolving to address the growing threats in the digital landscape, ensuring the protection of sensitive information.",
            "The rise of remote work technologies is reshaping the way we work, collaborate, and communicate in the modern workplace.",
            "3D printing is revolutionizing manufacturing processes, enabling the creation of complex and customized objects with precision."
        ])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'coding tips' in query or 'programming advice' in query or 'coding challenges' in query or 'software development' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "I can provide coding tips and programming advice.",
            "Let's tackle some coding challenges together!",
            "Need advice on software development? Ask away!"
        ])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
        # Actual coding tips
        coding_tips = [
            "Always write clean and readable code. It makes collaboration and maintenance much easier.",
            "Break down complex problems into smaller, manageable tasks. It helps in solving problems step by step.",
            "Learn to use version control systems like Git. It's crucial for tracking changes and collaborating with others.",
            "Don't hesitate to ask for help or seek feedback. Learning from others is an essential part of growth.",
            "Practice regularly on coding platforms like LeetCode or HackerRank to sharpen your problem-solving skills.",
            "Understand the basics of algorithms and data structures. They are fundamental to efficient coding.",
            "Keep up with industry trends and advancements. Technology evolves quickly, and staying informed is key.",
            "Comment your code effectively. It helps not only others who might read your code but also your future self.",
            "Write test cases for your code. It ensures that your code works as intended and helps catch bugs early on.",
            "Take breaks and avoid burnout. Coding is a mentally demanding task, and breaks can improve productivity.",
            "Explore open-source projects to gain practical experience and contribute to the developer community.",
            "Consider pair programming with a colleague. It fosters collaboration and can lead to better solutions.",
            "Stay curious and embrace a lifelong learning mindset. The tech industry is constantly evolving.",
            "Document your code and projects. It's valuable for both yourself and others who may work on the same codebase.",
            "Master the art of debugging. Knowing how to troubleshoot issues efficiently is a crucial skill.",
        ]

        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response += "\nHere are some coding tips for you:\n{}".format('\n'.join(coding_tips))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)



    elif 'poetry' in query or 'write me a poem' in query or 'poem please' in query or 'poetry inspiration' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Sure, here's a short poem for you:\nRoses are red, violets are blue, life is an adventure, and so are you!",
            "In the quiet of the night, stars whisper their tales of light.",
            "A gentle breeze, a rustling tree, nature's poetry, forever free.",
            "Amidst the city's rhythmic hum, dreams dance until the morning comes.",
            "Moonlight paints the sky with grace, a tranquil scene, a quiet space.",
            "Silent whispers on the breeze, secrets told among the trees.",
            "Sunset hues, a canvas bright, nature's palette, pure delight.",
            "Echoes of the ocean's song, waves that gently drift along.",
            "In the meadow where dreams take flight, butterflies dance in golden light.",
            "Whispers of the autumn air, leaves descending with such flair.",
            "Misty morning, dewdrops gleam, a world wrapped in a tranquil dream.",
            "A solitary candle's flame, telling tales without a name.",
            "Raindrops on a window pane, a symphony of nature's refrain.",
            "Footprints in the sandy shore, memories of the tides before.",
            "Mountains standing tall and grand, reaching for the heavens, touching land."
        ])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'science facts' in query or 'scientific discoveries' in query or 'interesting science' in query or 'science trivia' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Did you know that a day on Venus is longer than a year on Venus?",
            "Discover recent scientific discoveries and interesting trivia with me!",
            "The world's largest desert is not covered in sand; it's Antarctica, covered in ice!",
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "The only planet in our solar system that rotates clockwise is Venus.",
            "A single rainforest can produce 20% of the Earth's oxygen.",
            "The Sun makes a full rotation once every 25 days, while it takes about 225 million years for our Sun to complete one orbit around the Milky Way.",
            "Bananas are berries, but strawberries aren't. In botanical terms, berries are fleshy fruits produced from a single ovary, and bananas fit the bill!",
            "A teaspoonful of a neutron star would weigh about six billion tons!",
            "There are more atoms in a single grain of sand than there are grains of sand on all the beaches on Earth.",
            "The shortest war in history was between Britain and Zanzibar in 1896. Zanzibar surrendered after 38 minutes!",
            "A group of flamingos is called a 'flamboyance'.",
            "Honeybees can recognize human faces.",
            "The Great Wall of China is not visible from the Moon without aid, contrary to popular belief.",
            "A 'jiffy' is an actual unit of time. It's defined as the time it takes for light to travel one centimeter in a vacuum, approximately 33.3564 picoseconds."
        ])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'quotes' in query or 'inspirational quotes' in query or 'motivational sayings' in query or 'quote of the day' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Embrace the journey, knowing that the destination is just a point on the map.",
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "The purpose of our lives is to be happy. - Dalai Lama",
            "Success is stumbling from failure to failure with no loss of enthusiasm. - Winston Churchill",
            "Do not wait to strike till the iron is hot, but make it hot by striking. - William Butler Yeats",
            "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
            "The only place where success comes before work is in the dictionary. - Vidal Sassoon"
        ])
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'DIY projects' in query or 'craft ideas' in query or 'creative hobbies' in query or 'homemade gifts' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Let's get crafty! Explore DIY projects and creative hobbies.",
            "DIY enthusiast? I've got project ideas for you.",
            "Discover the joy of creating with some exciting DIY projects."
        ])

        # Actual DIY project ideas
        diy_projects = [
            "Create your own personalized photo album with recycled materials.",
            "Design and paint custom mugs for unique, homemade gifts.",
            "Craft a handmade candle using your favorite scents and colors.",
            "Transform old t-shirts into trendy reusable tote bags.",
            "Build a birdhouse and add a touch of nature to your backyard.",
            "Craft a dreamcatcher with beads and feathers for a boho-inspired decor piece.",
            "Repurpose glass jars into stylish candle holders or storage containers.",
            "Make your own natural bath bombs for a spa-like experience at home.",
            "Create a personalized recipe book with your favorite dishes.",
            "Design and paint your own flower pots for a colorful garden display.",
            "Craft unique and personalized greeting cards for special occasions.",
            "Make homemade soap with customized scents and ingredients.",
            "Create a DIY terrarium with small plants for a touch of greenery indoors.",
            "Craft your own jewelry using beads, wire, and other materials.",
            "Transform a plain mirror into a decorative statement piece with a custom frame."
        ]

        response += "\nHere are some DIY project ideas for you:\n{}".format('\n'.join(diy_projects))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'philosophical questions' in query or 'deep thoughts' in query or 'existential pondering' in query or 'philosophy' in query:
        response = random.choice([
            "Contemplating life's mysteries? Let's delve into some philosophical questions.",
            "Explore the depths of philosophy and existential pondering together.",
            "Philosophy invites us to ask profound questions. What's on your mind?"
        ])

        # Actual philosophical questions
        philosophical_questions = [
            "What is the meaning of life?",
            "Is there such a thing as free will?",
            "What is the nature of reality?",
            "Can we truly know anything with certainty?",
            "What is the relationship between the mind and the body?",
            "Does God exist?",
            "What is the source of morality?",
            "Are we more influenced by nature or nurture?",
            "Is there an inherent purpose or meaning to the universe?",
            "Can we ever have objective knowledge?",
            "What is the nature of consciousness?",
            "Is there a difference between happiness and meaning in life?",
            "Do we have a moral obligation to help others?",
            "What is the role of art and beauty in our lives?",
            "Is time an absolute reality or a human construct?"
        ]

        response += "\nHere are some philosophical questions for contemplation:\n{}".format(
            '\n'.join(philosophical_questions))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)


    elif 'home gardening tips' in query or 'indoor plants care' in query or 'gardening advice' in query or 'grow herbs' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Green thumb alert! Let's talk about home gardening and plant care.",
            "Create a thriving indoor garden with helpful tips and gardening advice.",
            "Discover the joys of cultivating plants at home. Ready to get your hands dirty?"
        ])

        # Actual home gardening tips
        gardening_tips = [
            "Choose the right plants for your space and light conditions. Consider factors like sunlight and humidity.",
            "Ensure proper drainage for your plants by using well-draining soil and pots with drainage holes.",
            "Water your plants consistently, but be mindful not to overwater. Most plants prefer slightly moist soil, not soggy.",
            "Rotate your indoor plants periodically to ensure even exposure to sunlight and promote balanced growth.",
            "Fertilize your plants regularly during the growing season, following the recommended guidelines for each type of plant.",
            "Prune and trim your plants to encourage bushier growth and remove dead or yellowing leaves.",
            "Keep an eye out for pests. If you notice any, address the issue promptly with natural remedies or insecticidal soap.",
            "Consider companion planting – growing certain plants together to help each other thrive and deter pests.",
            "Group plants with similar water and light needs together to simplify care routines.",
            "Research the specific needs of the herbs you're growing. Some may prefer drier soil, while others thrive in more moisture.",
            "Experiment with container gardening to maximize limited space. Many herbs and small vegetables can be grown in pots.",
            "Invest in good-quality gardening tools to make your gardening tasks more enjoyable and efficient.",
            "Join a local gardening community or online forums to exchange tips and experiences with fellow gardeners.",
            "Explore eco-friendly gardening practices, such as composting kitchen scraps to create nutrient-rich soil.",
            "Remember that patience is key! Gardening is a journey, and your efforts will be rewarded over time."
        ]

        response += "\nHere are some home gardening tips for you:\n{}".format('\n'.join(gardening_tips))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)


    elif 'futuristic technology' in query or 'tech predictions' in query or 'future innovations' in query or 'next-gen gadgets' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Exciting times ahead! Let's explore futuristic technology and innovations.",
            "Curious about the future of tech? Dive into predictions and upcoming innovations.",
            "Stay ahead of the curve with insights into futuristic technology and gadgets."
        ])

        # Examples of futuristic technology
        futuristic_technology = [
            "Advancements in artificial intelligence leading to more personalized and efficient services.",
            "The widespread adoption of augmented reality (AR) and virtual reality (VR) in various industries.",
            "Development of smart cities with interconnected systems for better urban living and sustainability.",
            "Breakthroughs in quantum computing, revolutionizing data processing capabilities.",
            "Progress in biotechnology, including gene editing and personalized medicine.",
            "Enhancements in renewable energy technologies for a more sustainable future.",
            "Integration of 5G technology, enabling faster and more reliable wireless communication.",
            "Advances in space exploration, with potential manned missions to Mars and beyond.",
            "Innovations in transportation, such as hyperloop systems and autonomous vehicles.",
            "Emergence of wearable technology for health monitoring and improved user experiences.",
            "Growing use of blockchain technology for secure and transparent transactions.",
            "Development of brain-computer interfaces for seamless interaction between humans and machines.",
            "Exploration of new materials with unique properties, enabling innovative applications.",
            "Advancements in robotics for both industrial and personal use, enhancing automation and assistance.",
            "Integration of Internet of Things (IoT) in various aspects of daily life for enhanced connectivity."
        ]

        response += "\nHere are some glimpses of futuristic technology:\n{}".format(
            '\n'.join(futuristic_technology))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'coding projects' in query or 'programming challenges' in query or 'build software' in query or 'coding portfolio' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice([
            "Coding journey ahead! Let's discuss projects and challenges.",
            "Explore new coding projects and challenges to enhance your skills.",
            "Building a coding portfolio? Let's brainstorm ideas and discuss your next project."
        ])

        # Examples of coding projects and challenges
        coding_projects = [
            "Create a personal website or portfolio to showcase your coding skills and projects.",
            "Develop a mobile app that addresses a specific problem or provides a useful service.",
            "Contribute to an open-source project on platforms like GitHub to collaborate with other developers.",
            "Build a web application using a popular framework like Django, Flask, or Ruby on Rails.",
            "Implement a machine learning project, such as a sentiment analysis tool or image recognition system.",
            "Participate in coding competitions on platforms like LeetCode or HackerRank to sharpen your problem-solving skills.",
            "Design and develop a game, either for desktop or mobile platforms, to explore the realm of game development.",
            "Create a chatbot using natural language processing to assist users with common queries or tasks.",
            "Build a blog or content management system (CMS) from scratch to deepen your understanding of web development.",
            "Contribute to the development of a tool or library in your preferred programming language.",
            "Explore blockchain development by building a decentralized application (DApp) or smart contract.",
            "Develop a social media integration, such as a Twitter bot or Instagram photo downloader.",
            "Build a recommendation system that suggests content based on user preferences and behavior.",
            "Implement a data visualization project using libraries like D3.js or Matplotlib.",
            "Create a command-line tool or utility that automates a repetitive task you encounter frequently."
        ]

        response += "\nHere are some coding project ideas for you:\n{}".format('\n'.join(coding_projects))
        bot_statement = "VERTIGO-> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'bored' in query or 'boredom' in query or 'play a game' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = "Feeling bored? How about playing a game?"
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
        response = " Let's explore some online games. Opening a free online game website for you."
        Speak(response)
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        # You can replace the URL with the actual URL of a free online game website
        game_website_url = "https://poki.com/"  # Replace with the actual URL
        webbrowser.open(game_website_url)




    elif 'time' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        time_info = get_current_time()
        response = Speak(time_info)
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)
    elif 'news' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        news_info = get_news()
        response = Speak(news_info)
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'tell me a English joke' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        joke_info = get_english_joke()
        statement = Speak(joke_info)
        bot_statement = "VERTIGO-> " + statement
        txt.insert(END, "\n" + bot_statement)
        Speak(statement)

    elif 'you need a break' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        statement = Speak("Okay, sir. You can call me anytime.")
        bot_statement = "Bot -> " + statement
        txt.insert(END, "\n" + bot_statement)
        Speak(statement)

    elif 'kya hal hai' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        statement = Speak("Main badiya hoon, ap batao.")
        bot_statement = "Bot -> " + statement
        txt.insert(END, "\n" + bot_statement)
        Speak(statement)


    elif 'Google search' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        statement=Speak("This is what I found for your search")
        bot_statement = "Bot -> " + statement
        txt.insert(END, "\n" + bot_statement)
        Speak(statement)
        query = query.replace("jarvis", "").replace("google search", "")
        pywhatkit.search(query)
        Speak("Done Sir!")

    elif 'launch' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        statement=Speak("Tell me the name of the website!")
        bot_statement = "Bot -> " + statement
        txt.insert(END, "\n" + bot_statement)
        Speak(statement)
        name =entry.get().lower()
        web = 'https://www.' + name + '.com'
        webbrowser.open(web)
        Speak("Done sir")
    elif 'facebook' in query:
        Speak("ok sir!")
        webbrowser.open("https://www.facebook.com")


    elif 'play YouTube video' in query or "Youtube search" in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        statement = Speak("Tell me the Name of the video")
        bot_statement = "VERTIGO-> " + statement
        txt.insert(END, "\n" + bot_statement)
        Speak(statement)
        videoName =entry.get().lower()
        pywhatkit.playonyt(videoName)
        statement = Speak("Your video has been Started, Enjoy")
        bot_statement = "VERTIGO-> " + statement
        txt.insert(END, "\n" + bot_statement)
        Speak(statement)

    elif 'play music' in query or 'music please' in query or 'song recommendation' in query or 'music suggestion' in query:

        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response = random.choice(["Sure, playing some music for you!", "Let me play the song for you"])
        statement = Speak(response)
        print(statement)
        play_music()
    elif 'Wikipedia' in query or 'Wikipedia Search' in query:
        statement = "user=>" + query
        txt.insert(END, "\n" + statement)
        response=Speak("searching wikipedia.....")
        query = query.replace("jarvis", "")
        query = query.replace("wikipedia", "")
        wiki = wikipedia.summary(query, 2)
        response=Speak("According to wikipedia:" + wiki)
        bot_statement = "VERTIGO -> " + response
        txt.insert(END, "\n" + bot_statement)
        Speak(response)

    elif 'Chrome' in query:
        subprocess.run("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")


    elif 'edge' in query:
        subprocess.run("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")
    elif 'control panel' in query:
        subprocess.run("C:\\Windows\\System32\\control.exe")

    elif 'Facebook' in query:
        webbrowser.open('https://www.facebook.com/login/')
    elif 'Instagram' in query:
        webbrowser.open('https://www.instagram.com/accounts/login/')

    elif 'Netflix' in query:
        webbrowser.open('https://www.netflix.com/login/')
    elif 'netflix' in query or 'open netflix' in query:
        webbrowser.open('https://www.netflix.com/login/')
    elif 'date' in query:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        Speak(f"Today's date is {current_date}")

    elif 'calculator' in query:
        Speak("Sure, opening calculator.")
        subprocess.run("calc.exe")

    elif 'calendar' in query:
        Speak("Sure, checking today's date.")
        speak_date()




# GUI elements
BG_GRAY = "#B57EDC"
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Label using pack
label1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1)
label1.pack()

# Text widget using pack
txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.pack()

# Scrollbar using pack
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
txt.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=txt.yview)

# Entry widget using pack
# Create an Entry widget and pack it into the window
entry = tk.Entry(root)
entry.pack()

# Button using pack
send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send)
send_button.pack()

root.mainloop()


