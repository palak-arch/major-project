import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import threading
import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import os
import subprocess
import webbrowser
import datetime
from pyowm import OWM
import requests
import random
# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
Assistant = pyttsx3.init('sapi5')
voices = Assistant.getProperty('voices')
Assistant.setProperty('voice', voices[1].id)
window = tk.Tk()
window.title("Vertigo Assistant")  # Set the window title
# Load the initial GIF
gif_path = "X:\\python project\\vertigo.gif"
gif = Image.open(gif_path)
# Convert the GIF to a sequence of PhotoImage objects
photo_sequence = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
# Function to update the GIF displayed
def update_gif(index):
    label.configure(image=photo_sequence[index])
    window.after(100, update_gif, (index + 1) % len(photo_sequence))
# Create a label to display the GIF
label = tk.Label(window)
label.pack()
# Create a label to display the assistant's reply
reply_label = tk.Label(window, text="", font=("Helvetica", 12), fg="black")  # Change text color to black
reply_label.pack()
# Create a label to display the listening status
listening_label = tk.Label(window, text="", font=("Helvetica", 12), fg="black")
listening_label.pack()
# Start the animation with the initial GIF
window.after(0, update_gif, 0)
# Create an entry widget for user input
user_input = tk.StringVar()
entry = ttk.Entry(window, textvariable=user_input, font=("Helvetica", 12))
entry.pack(pady=10, padx=20, fill=tk.X, ipady=5)
# Function to handle window closing
def on_close():
    window.destroy()
# Set the close event handler for the window
window.protocol("WM_DELETE_WINDOW", on_close)
# Function to update the reply label in the Tkinter window
def update_reply_label(text):
    reply_label.config(text=text)
# Function to update the listening status label
def update_listening_label(text):
    listening_label.config(text=text)
# Function to capture voice command
def takecommand():
    microphone = sr.Microphone()
    with microphone as source:
        statement = "Listening for a command ..."
        print(statement)
        # Update the listening status label
        update_listening_label(statement)
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        recognizer.energy_threshold = 4000
    try:
        command = recognizer.recognize_google(audio)
        statement = f"Recognized online command: {command}"
        print(statement)
        # Update the reply label with the recognized command
        update_reply_label(statement)
        return command  # Return the recognized command
    except sr.UnknownValueError:
        statement = Speak("Sorry, I couldn't understand the audio.")
        print(statement)
        # Update the reply label with the error message
        update_reply_label(statement)
        return None  # Return None when the command is not understood
# Function to wish based on the time
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        Speak("Good Morning!")
    elif 12 <= hour < 18:
        Speak("Good Afternoon!")
    else:
        Speak("Good Evening!")

def speak_date():
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    Speak(f"Today is {today}")
# Function to speak a message
def Speak(audio):
    statement = "Assistant: " + audio
    reply_label.config(text=statement)  # Update reply_label with the spoken statement
    print(statement)  # Print the statement

    # Stop the TTS engine if it's already running
    Assistant.stop()

    Assistant.say(audio)  # Speak the message
    Assistant.runAndWait()
    return statement  # Return the spoken statement
def get_weather(city_name):
    owm = OWM('3b91764244d706e6dceab2dc46490cb5')  # Replace with your OpenWeatherMap API key
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(city_name)
    w = observation.weather

    weather_info = f"The weather in {city_name} is {w.detailed_status}. "
    weather_info += f"The temperature is {w.temperature('celsius')['temp']}°C."

    return weather_info
# Function to get current time
def get_current_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"The current time is {current_time}."
# Function to fetch a random English joke
def get_english_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a rose that wants to go to moon       Gulab ja moon",
        "What do you call a labrador that becames a magician           Labracadabrador",
        "What is the most shocking city in the world?            Electricity",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "I told my wife she should embrace her mistakes. She gave me a hug.",
        # Add more English jokes as needed
    ]
    joke = random.choice(jokes)
    statement = Speak(joke)
    print(statement)
    return statement
# Function to fetch a random Hindi joke
def get_hindi_joke():
    jokes = [
        "Ek dost ne poocha: Teri girlfriend tere saath kaise rehti hai? \nMaine kaha: Bilkul nayi baat hai, main uske saath rehta hoon!",
        "Baccha: Papa, tum shaadi ke liye kaunsi baatein dekhte ho? \nPapa: Yahi ki kahin teri maa mujhse kam umar ki na ho!",
        "Mohabbat aur bank loot ek hi baat hai,\nbas fark itna hai ki\nek mein paisa lootte hain aur doosre mein dil!"


    ]
    joke = random.choice(jokes)
    statement = Speak(joke)
    print(statement)
    return Speak(joke)


# Function to play a song on Spotify

def play_music():
    music_dir = "C:\\Users\\sejal\\Music"
    songs = os.listdir(music_dir)

    if songs:
        Speak("Please provide the song name.")
        user_input = takecommand()

        # Check if the provided song name is in the list of songs
        if user_input in songs:
            os.startfile(os.path.join(music_dir, user_input))
            Speak(f"Now playing {user_input}")
        else:
            Speak("Song not found in the specified directory. Searching on YouTube...")
            pywhatkit.playonyt(user_input)
            Speak(f"Now playing {user_input} from YouTube.")

# Replace 'YOUR_NEWS_API_KEY' with the actual API key you obtained from News API
NEWS_API_KEY = 'c099a32bdc704307a93c846fc0edbf06'
# Function to get today's news headlines
def get_news(num_articles=5):
    news_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'  # Adjust the country code if needed
    response = requests.get(news_url)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        if articles:
            news_info = "Here are today's headlines:\n"
            for idx, article in enumerate(articles[:num_articles]):
                news_info += f"{idx + 1}. {article['title']}\n"
            return news_info
        else:
            return "Sorry, I couldn't fetch the latest news at the moment."
    else:
        return "Sorry, I couldn't fetch the latest news at the moment."
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
def youtubeSearch(query):
    query = query.replace("VERTIGO", "")
    query = query.replace("youtube search", "")
    web = 'https://www.youtube.com/results?search_query=' + query
    webbrowser.open(web)
    Speak("Done Sir!")
# Main function to execute the assistant
def TaskExe():
    try:
        statement = Speak("Hello, I am VERTIGO, your Personal Assistant.")
        print(statement)
        wish_me()
        time_info = get_current_time()
        statement = Speak(time_info)
        print(statement)
        city_name = "Shimla"  # Replace with your desired city
        weather_info = get_weather(city_name)
        statement = Speak(weather_info)
        print(statement)
        statement = Speak("I am ready to assist you how can i help you?")
        print(statement)
        statement=speak_date()
        print(statement)
        try:
            # Check if the internet is available by making a simple request
            response = requests.get("https://www.google.com")
        except requests.ConnectionError:
            statement = Speak("Please check your internet connection. Sorry for the inconvenience.")
            print(statement)  # Print the spoken statement
        while True:
            query = takecommand()
            if query is not None:
                if 'tell me Hindi joke' in query:
                    joke_info = get_hindi_joke()
                    statement = Speak(joke_info)
                    print(statement)

                elif 'exit' in query or 'bye' in query or 'dfa ho' in query:
                    statement = Speak("byee have a nice day")
                    print(statement)
                    break
                elif 'hello' in query or 'hey' in query or 'hii' in query:
                    response = random.choice(
                        ["Hello! How can I assist you?", "Hi there!", "Hey! What can I do for you?",
                         "Howdy! What brings you here?", "Greetings! How may I help you?",
                         "Good morning! How can I be of service?", "Good afternoon! What do you need assistance with?",
                         "Good evening! How may I assist you?", "Hey there! How can I help?",
                         "Hi! What's on your mind?",
                         "Hello there! How can I assist you today?"])
                    statement=Speak(response)
                    print (statement)
                elif 'how are you' in query or 'h r u' in query:
                    response = random.choice(["I'm doing well, thank you!", "I'm great! How can I assist you?",
                                              "I'm here and ready to help!", "I'm good, thanks for asking.",
                                              "I'm functioning at full capacity! How may I assist you today?"])
                    statement = Speak(response)
                    print(statement)

                elif 'how was your day' in query:
                    response = random.choice(["My day is going smoothly, thank you!", "It's been a good day so far.",
                                              "I'm having a productive day! How can I help you?",
                                              "Every day is a good day for assistance! What can I do for you?"])
                    statement = Speak(response)
                    print(statement)
                elif 'what are you doing' in query:
                    response = random.choice(["I'm here, ready to assist you!", "I'm always at your service.",
                                              "Just here, waiting for your commands.",
                                              "I'm busy helping users like you!"])
                    statement = Speak(response)
                    print(statement)


                elif 'what is your favorite color' in query:
                    response = "I love purple color."
                    statement = Speak(response)
                    print(statement)
                elif 'what do you like to talk about' in query:
                    response = "I enjoy talking about various topics! Feel free to ask me anything, and I'll do my best to assist you."
                    statement = Speak(response)
                    print(statement)

                elif 'tell me something interesting' in query:
                    response = "Sure! Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible."
                    statement = Speak(response)
                    print(statement)

                elif 'do you have any hobbies' in query or 'your hobbies ' in query:
                    response = "I don't have personal hobbies, but I'm here to help and engage in conversations with you!"
                    statement = Speak(response)
                    print(statement)

                elif "what's your favorite book" in query or  "recommend books" in query or  "famous books" in query:
                    response = "I don't have personal preferences for books. However, I can help you find information or recommend books based on your interests. What genre are you into?"
                    statement = Speak(response)
                    print(statement)

                elif "what's your favorite movie" in query:
                    response = "I don't have personal movie preferences, but I can suggest movies based on your taste. What genre are you in the mood for?"
                    statement = Speak(response)
                    print(statement)

                elif 'hi' in query or 'hey' in query:
                    response = random.choice(
                        ["Hey! How can I assist you?", "Hi there!", "Hello! What can I do for you?",
                         "Howdy! What brings you here?", "Greetings! How may I help you?",
                         "Hi! What's on your mind?", "Hello there! How can I assist you today?"])
                    statement = Speak(response)
                    print(statement)

                elif 'bye' in query:
                    response = random.choice(["Goodbye!", "See you later!", "Have a great day!", "Farewell! Take care.",
                                              "Goodbye! Until next time.", "Take care! Have a wonderful day.",
                                              "Bye bye!",
                                              "Catch you later!", "Have a good one!", "So long!"])
                    statement = Speak(response)
                    print(statement)
                elif 'thank you' in query or 'thanks' in query or 'appreciate it' in query or 'thank you so much' in query or 'thanks a lot' in query or 'much appreciated' in query:
                    response = random.choice(["You're welcome!", "Happy to help!", "Glad I could assist.", "Anytime!",
                                              "You're welcome! Have a great day.", "No problem!"])
                    statement = Speak(response)
                    print(statement)
                elif 'sorry' in query or 'my apologies' in query or 'apologize' in query or 'I\'m sorry' in query:
                    response = random.choice(
                        ["No problem at all.", "It's alright.", "No need to apologize.", "That's okay.",
                         "Don't worry about it.", "Apology accepted."])
                    statement = Speak(response)
                    print(statement)
                elif 'great job' in query or 'well done' in query or 'awesome' in query or 'fantastic' in query or 'amazing work' in query or 'excellent' in query:
                    response = random.choice(["Thank you! I appreciate your feedback.", "Glad to hear that!",
                                              "Thank you for the compliment!",
                                              "I'm glad I could meet your expectations.", "Your words motivate me!",
                                              "Thank you for your kind words."])
                    statement = Speak(response)
                    print(statement)
                elif 'not good' in query or 'disappointed' in query or 'unsatisfied' in query or 'poor service' in query or 'needs improvement' in query or 'could be better' in query:
                    response = random.choice(
                        ["I'm sorry to hear that. Can you please provide more details so I can assist you better?",
                         "I apologize for the inconvenience. Let me help resolve the issue.",
                         "I'm sorry you're not satisfied. Please let me know how I can improve.",
                         "Your feedback is valuable. I'll work on improving."])
                    statement = Speak(response)
                    print(statement)
                elif 'what\'s the weather like?' in query or 'weather forecast' in query or 'is it going to rain today?' in query or 'temperature today' in query or 'weather report' in query:
                    city_name = "Shimla"  # Replace with your desired city
                    weather_info = get_weather(city_name)
                    statement = Speak(weather_info)
                    print(statement)
                elif 'help' in query or 'can you help me?' in query or 'I need assistance' in query or 'support' in query:
                    response = random.choice(["Sure, I'll do my best to assist you.", "Of course, I'm here to help!",
                                              "How can I assist you?",
                                              "I'll help you with your query."])
                    statement = Speak(response)
                    print(statement)
                elif 'what\'s the time?' in query or 'current time' in query or 'time please' in query or 'what time is it?' in query:
                    time_info = get_current_time()
                    statement = Speak("It's " + time_info)
                    print(statement)
                elif 'joke' in query or 'joke please' in query or 'got any jokes?' in query or 'make me laugh' in query:
                    response = random.choice([
                                                 "Why don't we ever tell secrets on a farm? Because the potatoes have eyes and the corn has ears!",
                                                 "What do you get when you cross a snowman and a vampire? Frostbite!",
                                                 "Why was the math book sad? Because it had too many problems!"])
                    statement = Speak(response)
                    print(statement)
                elif 'play music' in query or 'music please' in query or 'song recommendation' in query or 'music suggestion' in query:
                    response = random.choice(["Sure, playing some music for you!", "Let me play the song for you"])
                    statement = Speak(response)
                    print(statement)
                    play_music()

                elif 'recommend restaurant' in query or 'food places nearby' in query or "what's good to eat?" in query or 'restaurant suggestion' in query:
                    response = random.choice(["Sure, here are some recommended restaurants: ",
                                              "Hungry? Let me find some good food places for you!",
                                              "I can suggest some great places to eat nearby."])
                    statement = Speak(response)
                    print(statement)
                    city_name = "kandaghat"  # Replace with the desired city name
                    location_query = f"restaurants in {city_name}"

                    # Construct the Google Maps URL for the restaurant search
                    maps_url = f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}"

                    # Open the Google Maps URL in the default web browser
                    webbrowser.open(maps_url)

                    response = " I've opened Google Maps to show you nearby restaurants. Take a look!"
                    statement = Speak(response)
                    print(statement)
                elif 'tourist places' in query or 'places to visit' in query or 'tourism places' in query:
                    response = random.choice(["Certainly! Here are some popular tourist places: ",
                                              "Interested in sightseeing? I can recommend some great places to visit!",
                                              "Let me suggest some tourist attractions for you."])
                    statement = Speak(response)
                    print(statement)
                    city_name = "Solan"  # Replace with the desired city name
                    location_query = f"tourist places in {city_name}"

                    # Construct the Google Maps URL for the tourist places search
                    maps_url = f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}"

                    # Open the Google Maps URL in the default web browser
                    webbrowser.open(maps_url)

                    response = " I've opened Google Maps to show you nearby tourist places. Enjoy exploring!"
                    statement = Speak(response)
                    print(statement)

                elif 'maps' in query or 'show me the map' in query:
                    response = "Sure, I can show you the map. Opening Google Maps."
                    statement = Speak(response)
                    print(statement)
                    # Open Google Maps in the default web browser
                    webbrowser.open("https://www.google.com/maps/")

                elif 'latest news' in query or 'news updates' in query or 'what\'s happening?' in query or 'current events' in query:
                    response = random.choice(
                        ["Let me fetch the latest news for you.", "Here are the top headlines: [news_headlines]",
                         "Stay updated with the latest news!"])
                    response = get_sports_news(num_articles=5)
                    statement = Speak(response)
                    print(statement)

                    news_headlines = get_news(num_articles=5)
                    for headline in news_headlines:
                        statement = Speak(headline)
                        print(statement)

                        # Check if the user wants to stop after each headline
                        query = takecommand().lower()
                        if 'stop' in query or 'that\'s enough' in query or 'enough' in query:
                            break
                elif 'movie suggestions' in query or 'recommend a movie' in query or 'what should I watch' in query or 'best movies' in query:
                    movie_suggestions = ["The Shawshank Redemption", "The Godfather", "Pulp Fiction", "Inception",
                                         "The Dark Knight", "Forrest Gump", "The Matrix", "Schindler's List"]

                    response = random.choice(["How about watching ?", "Here's a movie suggestion for you: .",
                                              "Let me recommend some great movies!"])
                    movie_name = random.choice(movie_suggestions)
                    statement = Speak(response.format(movie_name))
                    print(statement)
                elif 'sports news' in query or 'score updates' in query or 'latest sports events' in query or 'upcoming games' in query:
                    response = random.choice(
                        ["I'll get you the latest sports updates.", "Stay updated with the current sports events!",
                         "Let me check the sports scores for you."])
                    statement = Speak(response)
                    print(statement)
                    response = get_sports_news(num_articles=5)
                    statement = Speak(response)
                    print(statement)


                elif 'travel tips' in query or 'travelling tomorrow' in query or 'travel advice' in query or 'plan a trip' in query:
                    response = Speak("Certainly! What type of travel tips are you looking for? Are you interested in packing tips or general travel advice?")
                    print(response)

                    travel_preference = takecommand()

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
                            response = Speak(
                                f"Great choice! Here are some {travel_preference.lower()} for your trip: {', '.join(travel_tips)}. Safe travels!")
                            print(response)
                        else:
                            response = Speak(
                                "I'm sorry, I couldn't find travel tips for that category. Please choose from the provided options.")
                            print(response)
                    else:
                        response = Speak(
                            "I'm sorry, I didn't catch that. Can you please specify the type of travel tips you're looking for?")
                        print(response)

                        # Check if the user's preference is a valid travel category



                elif 'fitness advice' in query or 'workout tips' in query or 'fitness tips' in query or 'exercise suggestions' in query or 'healthy habits' in query:
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

                    response += "\n".join(fitness_tips)

                    statement = Speak(response)
                    print(statement)


                elif 'learning resources' in query or 'study tips' in query or 'education advice' in query or 'academic help' in query:
                    educational_websites = ["Khan Academy", "Coursera", "edX", "Quizlet", "Duolingo"]
                    response = random.choice([
                        "Let's explore learning resources together. Have you tried websites like {}?",
                        "Tell me about your educational goals or questions. You might find {} helpful."
                    ]).format(', '.join(educational_websites))
                    statement = Speak(response)
                    print(statement)

                elif 'pet care tips' in query or 'animal advice' in query or 'pet health' in query or 'taking care of pets' in query:
                    response = random.choice(["Pets are wonderful! Here are some pet care tips: [pet_care_tips]",
                                              "I can provide advice on pet health and care.",
                                              "Let's talk about your pet and their well-being."])
                    statement = Speak(response)
                    print(statement)
                elif 'online shopping' in query or 'buying something' in query or 'shopping advice' in query or 'product recommendations' in query:
                    response = random.choice([
                        "I can help you with online shopping",
                        "Let's find the perfect website for you!",
                        "Tell me what you're interested in purchasing."
                    ])
                    statement = Speak(response)
                    print(statement)

                    # Ask about specific shopping websites
                    websites = ['Amazon', 'Flipkart', 'Myntra', 'eBay', 'Walmart',
                                'Target']  # Add more websites as needed
                    website_query = "Do you have a specific website in mind? You can choose from {}.".format(
                        ', '.join(websites))

                    # Assuming you have a function to get user input, replace input() with your function
                    user_choice = input(website_query).lower()

                    if user_choice in websites:
                        print("Great choice! Let me know if there's anything specific you're looking for on {}.".format(
                            user_choice))
                    else:
                        print("Alright, if you have any specific preferences, feel free to let me know!")


                elif 'mental health support' in query or 'coping strategies' in query or 'stress relief tips' in query or 'emotional well-being' in query:
                    response = random.choice(["Mental health is important. How can I support you?",
                                              "I can provide guidance for managing stress and emotions.",
                                              "Let's talk about strategies for maintaining mental well-being."])
                    statement = Speak(response)
                    print(statement)
                elif 'language learning tips' in query or 'language practice' in query or 'learning new languages' in query or 'language study advice' in query:
                    response = random.choice(["Learning a new language can be exciting! How can I assist you?",
                                              "I can help with language learning tips and practice.",
                                              "Tell me which language you're interested in learning."])
                    statement = Speak(response)
                    print(statement)
                elif 'financial planning help' in query or 'money management tips' in query or 'investment advice' in query or 'budgeting assistance' in query:
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
                    statement = Speak(response)
                    print(statement)

                elif 'fun facts' in query or 'tell me something interesting' in query or  'another funfact' in query or 'interesting facts' in query or 'did you know' in query:
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

                    statement = Speak(response)
                    print(statement)


                elif 'Technology trends' in query or 'another Trend' in query or 'latest gadgets' in query or 'innovations' in query or 'tech news' in query:
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

                    statement = Speak(response)
                    print(statement)



                elif 'coding tips' in query or 'programming advice' in query or 'coding challenges' in query or 'software development' in query:
                    response = random.choice([
                        "I can provide coding tips and programming advice.",
                        "Let's tackle some coding challenges together!",
                        "Need advice on software development? Ask away!"
                    ])

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

                    response += "\nHere are some coding tips for you:\n{}".format('\n'.join(coding_tips))
                    statement = Speak(response)
                    print(statement)



                elif 'poetry' in query or 'write me a poem' in query or 'poem please' in query or 'poetry inspiration' in query:
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

                    statement = Speak(response)
                    print(statement)


                elif 'science facts' in query or 'scientific discoveries' in query or 'interesting science' in query or 'science trivia' in query:
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

                    statement = Speak(response)
                    print(statement)



                elif 'quotes' in query or 'inspirational quotes' in query or 'motivational sayings' in query or 'quote of the day' in query:
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

                    statement = Speak(response)
                    print(statement)

                elif 'DIY projects' in query or 'craft ideas' in query or 'creative hobbies' in query or 'homemade gifts' in query:
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
                    statement = Speak(response)
                    print(statement)


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
                    statement = Speak(response)
                    print(statement)


                elif 'home gardening tips' in query or 'indoor plants care' in query or 'gardening advice' in query or 'grow herbs' in query:
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
                    statement = Speak(response)
                    print(statement)


                elif 'futuristic technology' in query or 'tech predictions' in query or 'future innovations' in query or 'next-gen gadgets' in query:
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
                    statement = Speak(response)
                    print(statement)




                elif 'coding projects' in query or 'programming challenges' in query or 'build software' in query or 'coding portfolio' in query:
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
                    statement = Speak(response)
                    print(statement)
                if 'bored' in query or 'boredom' in query or 'play a game' in query:
                    response = "Feeling bored? How about playing a game?"

                    Speak(response)

                    user_response = takecommand()

                    if user_response and 'yes' in user_response:
                        response = "Great! Let's explore some online games. Opening a free online game website for you."
                        Speak(response)

                        # You can replace the URL with the actual URL of a free online game website
                        game_website_url = "https://poki.com/"  # Replace with the actual URL
                        webbrowser.open(game_website_url)
                    else:
                        response = "No worries! If you have any other requests or need information, feel free to ask."
                        Speak(response)



                elif 'time' in query:
                    time_info = get_current_time()
                    statement = Speak(time_info)
                    print(statement)
                elif 'news' in query:
                    news_info = get_news()
                    statement = Speak(news_info)
                    print(statement)

                elif 'tell me a English joke' in query:
                    joke_info = get_english_joke()
                    statement = Speak(joke_info)
                    print(statement)

                elif 'you need a break' in query:
                    statement = Speak("Okay, sir. You can call me anytime.")
                    print(statement)
                    break
                elif 'kya hal hai' in query:
                    statement = Speak("Main badiya hoon, ap batao.")
                    print(statement)


                elif 'Google search' in query :
                    Speak("This is what I found for your search")
                    query = query.replace("jarvis", "").replace("google search", "")
                    pywhatkit.search(query)
                    Speak("Done Sir!")

                elif 'launch' in query:
                    Speak("Tell me the name of the website!")
                    name = takecommand()
                    web = 'https://www.' + name + '.com'
                    webbrowser.open(web)
                    Speak("Done sir")
                elif 'facebook' in query:
                    Speak("ok sir!")
                    webbrowser.open("https://www.facebook.com")
                    Speak("Done Sir!")

                elif 'play YouTube video' in query or "Youtube search" in query:
                    statement = Speak("Tell me the Name of the video")
                    print(statement)
                    videoName = takecommand()
                    pywhatkit.playonyt(videoName)
                    statement = Speak("Your video has been Started, Enjoy")
                    print(statement)


                elif 'Wikipedia' in query or 'Wikipedia Search' in query :
                    Speak("searching wikipedia.....")
                    query = query.replace("jarvis", "")
                    query = query.replace("wikipedia", "")
                    wiki = wikipedia.summary(query, 2)
                    Speak("According to wikipedia:" + wiki)


                elif 'Chrome' in query:
                    subprocess.run("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")

                elif 'edge' in query or 'open edge' in query:
                    subprocess.run("C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")
                elif 'control panel' in query:
                    subprocess.run("C:\\Windows\\System32\\control.exe")

                elif 'Facebook' in query or 'open Facebook' in query:
                    webbrowser.open('https://www.facebook.com/login/')
                elif 'Instagram' in query or 'open Instagram' in query:
                    webbrowser.open('https://www.instagram.com/accounts/login/')

                elif 'Netflix' in query or 'open Netflix' in query:
                    webbrowser.open('https://www.netflix.com/login/')
                elif 'whatsapp' in query or 'open whatsapp' in query:
                    webbrowser.open('https://web.whatsapp.com/')
                elif 'date' in query:
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    Speak(f"Today's date is {current_date}")

                elif 'calculator' in query:
                    Speak("Sure, opening calculator.")
                    subprocess.run("calc.exe")

                elif 'calendar' in query:
                    Speak("Sure, checking today's date.")
                    speak_date()
                else:
                    print("sorry my functions are limited ")
            else:
                print("I can't hear you kindly speak again")



    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        Speak("My functions are limited kindly say something that is not beyond my limits how can i help you ")


def open_manual_input_file():
    try:
        import manual_input_file
        with open("manual_input_file.py", "r") as file:
            script_content = file.read()
        exec(script_content)
    except Exception as e:
        print(f"Error: {e}")
# Create a frame to contain the buttons and align them horizontally
button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

# Create a button in the Tkinter window to start the assistant task
assistant_button = ttk.Button(button_frame, text="Start Assistant", command=lambda: threading.Thread(target=TaskExe).start(), style='TButton')
assistant_button.pack(side=tk.LEFT, padx=5)
# Create a button to open the manual input filE
manual_input_button = ttk.Button(button_frame, text="Chat Bot", command=open_manual_input_file, style='TButton')
manual_input_button.pack(side=tk.LEFT, padx=5)

# Create an "Exit" button
exit_button = ttk.Button(button_frame, text="Exit", command=window.destroy, style='Exit.TButton')
exit_button.pack(side=tk.LEFT, padx=5)


# Function to handle window closing
def on_close():
    window.destroy()

# Set the close event handler for the window
window.protocol("WM_DELETE_WINDOW", on_close)

# Configure styles for the buttons with dark green background
style = ttk.Style()
style.configure('TButton', font=("Helvetica", 12), background='#006400', foreground='green')  # Dark green background
style.configure('Exit.TButton', font=("Helvetica", 12), background='#006400', foreground='green')  # Dark green background

# Run the Tkinter event loop
window.mainloop()