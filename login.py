import tkinter as tk
import customtkinter
from PIL import Image, ImageTk, ImageSequence
import os
# Setting up the appearance mode and default color theme
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

# Dummy user credentials
valid_username = "user"
valid_password = "password"

def forget_password():
    try:
        import createaccount
        with open("createaccount.py", "r") as file:
            script_content = file.read()
        exec(script_content)
    except Exception as e:
        print(f"Error: {e}")




# Function to handle create account action
def create_account():
    pass  # Your implementation here

# Function to authenticate the user
def authenticate(username, password):
    return username == valid_username and password == valid_password

# Function to handle login action
def login():
    username = entry1.get()
    password = entry2.get()

    if authenticate(username, password):
        app.destroy()  # Destroy login window
        welcome_window()
    else:
        # Display error message
        error_label.configure(text="Invalid username or password")

# Function to display the welcome window
def welcome_window():
    w = customtkinter.CTk()
    w.geometry("1280x720")
    w.title('Welcome')
    l1 = customtkinter.CTkLabel(master=w, text="Home Page", font=('Century Gothic', 60))
    l1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    w.mainloop()

# Creating the main login window
app = customtkinter.CTk()
app.geometry("900x700")
app.title('Login')

# Load the background image
background_image = Image.open("black.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a label with the background image and place it at the back
background_label = tk.Label(app, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Loading the GIF
gif_path = "login.gif"  # Replace with your GIF path
gif = Image.open(gif_path)
# Convert the GIF to a sequence of PhotoImage objects
photo_sequence = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

# Function to update the GIF displayed
def update_gif(label, index):
    label.configure(image=photo_sequence[index])
    app.after(100, update_gif, label, (index + 1) % len(photo_sequence))

# Create your custom frame
frame = customtkinter.CTkFrame(master=app, width=900, height=700, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Start the animation
update_gif_label = tk.Label(frame)
update_gif(update_gif_label, 0)
update_gif_label.pack(fill="both", expand=True)

# Other GUI elements



entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
entry1.place(x=290, y=220)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry2.place(x=290, y=255)

button1 = customtkinter.CTkButton(master=frame,  text="create an account", width=130, height=30, compound="left",
                                  fg_color='white', text_color='black', hover_color='#AFAFAF', command=create_account)
button1.place(x=320, y=350)

button2 = customtkinter.CTkButton(master=frame, text="Forget password", width=130, height=30, compound="left",
                                  fg_color='white', text_color='black', hover_color='#AFAFAF', command=forget_password)
button2.place(x=320, y=400)

# Error message label
error_label = customtkinter.CTkLabel(master=frame, text="", font=('Century Gotzhic', 12), text_color="red")
error_label.place(x=200, y=215)

# Create login button
button3 = customtkinter.CTkButton(master=frame, width=160, text="Login", command=login, corner_radius=6)
button3.place(x=310, y=310)



app.mainloop()
