import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
import customtkinter
from PIL import Image, ImageTk, ImageSequence
import tkinter.font as tkFont

# Database functions
def create_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect('users.db')
    return conn

def create_table():
    """Creates the users table if it doesn't exist."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        security_question TEXT,
                        security_answer TEXT)''')
    conn.commit()
    conn.close()

create_table()

def display_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()
display_users()

def sign_up(username, password, email, security_question, security_answer):
    """Registers a new user."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists.")
        conn.close()
        return

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Email already exists.")
        conn.close()
        return

    try:
        cursor.execute('INSERT INTO users (username, password, email, security_question, security_answer) VALUES (?, ?, ?, ?, ?)',
                       (username, password, email, security_question, security_answer))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Failed to register user.")
    finally:
        conn.close()

def login(username, password):
    """Logs in an existing user."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    print(user)  # Add this line to see the user information retrieved
    conn.close()
    return user is not None

def reset_password(email, security_question, security_answer, new_password):
    """Resets the password for an existing user."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND security_question = ? AND security_answer = ?',
                   (email, security_question, security_answer))
    user = cursor.fetchone()
    if user:
        cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, email))
        conn.commit()
        messagebox.showinfo("Success", "Password updated successfully!")
    else:
        messagebox.showerror("Error", "Email, security question, or answer is incorrect.")
    conn.close()

# Custom tkinter setup
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

# Functions to launch tools
def launch_calculator():
    import subprocess
    subprocess.run(["python", "calu.py"])

def launch_Deskassist():
    import subprocess
    subprocess.run(["python", "vertigoai.py"])

def launch_paint():
    import subprocess
    subprocess.run(["python", "paint1.py"])

def launch_notepad():
    import subprocess
    subprocess.run(["python", "note.py"])

def launch_dodgethecar():
    import subprocess
    subprocess.run(["python", "dodge the car.py"])

def launch_dodgetheball():
    import subprocess
    subprocess.run(["python", "DodgeTheBall.py"])

def launch_Flappy():
    import subprocess
    subprocess.run(["python", "flappy.py"])

# Main Application Class
class UserManagementApp:

    def __init__(self, root):
        self.submit_sign_up = None
        self.root = root
        self.root.title("APPSPHERE")
        self.root.geometry("1924x1080")

        self.load_background_image("bg.jpg")

        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)
        self.submit_sign_up = sign_up
        self.submit_reset_password = reset_password
        self.create_main_menu()

    def load_background_image(self, image_path):
        """Loads and sets the background image."""
        background_image = Image.open(image_path)
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=background_photo)
        background_label.image = background_photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_main_menu(self):
        """Creates the main menu."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        gif_path = "APPSPHERE.gif"
        gif = Image.open(gif_path)
        photo_sequence = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
        gif_width, gif_height = gif.size

        def update_gif(label, index):
            label.configure(image=photo_sequence[index])
            self.root.after(100, update_gif, label, (index + 1) % len(photo_sequence))

        canvas_width = gif_width
        canvas_height = gif_height

        canvas = tk.Canvas(self.main_frame, width=canvas_width, height=canvas_height)
        canvas.pack()

        update_gif_label = tk.Label(canvas)
        update_gif(update_gif_label, 0)
        update_gif_label.pack()

        buttons_frame = tk.Frame(self.root, bg="white")
        buttons_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        button_font = tkFont.Font(family="Arial", size=12, weight="bold")

        tk.Button(buttons_frame, text="Sign Up", width=20, height=2, font=button_font, command=self.show_sign_up,
                  relief="raised").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(buttons_frame, text="Login", width=20, height=2, font=button_font, command=self.show_login,
                  relief="raised").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(buttons_frame, text="Forgot Password", width=20, height=2, font=button_font,
                  command=self.show_forgot_password, relief="raised").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(buttons_frame, text="Exit", width=20, height=2, font=button_font, command=self.root.quit,
                  relief="raised").pack(side=tk.LEFT, padx=10, pady=10)

    def show_sign_up(self):
        """Opens the Sign Up window."""
        self.new_window(self.sign_up_window, "  ", "back.png")

    def show_login(self):
        """Opens the Login window."""
        self.new_window(self.login_window, "   ", "back.png")

    def show_forgot_password(self):
        """Opens the Forgot Password window."""
        self.new_window(self.forgot_password_window, "      ", "new.jpg")

    def new_window(self, window_func, title, background_image):
        """Creates a new window."""
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry("1928x1080")
        self.load_window_background(new_window, background_image)
        window_func(new_window)

        self.current_window = new_window

    def load_window_background(self, window, image_path):
        """Loads and sets the background image for a specific window."""
        background_image = Image.open(image_path)
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(window, image=background_photo)
        background_label.image = background_photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def sign_up_window(self, window):
        """Creates the Sign Up window."""
        self.create_sign_up_form(window, "Sign Up", self.submit_sign_up, "SIGNUP1.gif")

    def login_window(self, window):
        """Creates the Login window."""
        self.create_login_form(window, "Login", self.submit_login, "login.gif")

    def forgot_password_window(self, window):
        """Creates the Forgot Password window."""
        self.create_forgot_password_form(window, "Forgot Password", self.submit_reset_password, "forget_password.gif")

    def create_sign_up_form(self, window, title, submit_command, gif_path):
        """Creates the Sign Up form with a GIF and form fields."""
        self.create_form(window, title, submit_command, gif_path, sign_up=True)

    def create_login_form(self, window, title, submit_command, gif_path):
        """Creates the Login form with a GIF and form fields."""
        self.create_form(window, title, submit_command, gif_path, login=True)

    def create_forgot_password_form(self, window, title, submit_command, gif_path):
        """Creates the Forgot Password form with a GIF and form fields."""
        self.create_form(window, title, submit_command, gif_path, forgot_password=True)

    def create_form(self, window, title, submit_command, gif_path, sign_up=False, login=False, forgot_password=False):
        """Creates a form with a GIF and form fields."""
        gif = Image.open(gif_path)
        photo_sequence = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

        def update_gif(label, index):
            label.configure(image=photo_sequence[index])
            window.after(100, update_gif, label, (index + 1) % len(photo_sequence))

        canvas = tk.Canvas(window, width=800, height=500)
        canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        update_gif_label = tk.Label(canvas)
        update_gif_label.pack(fill="both", expand=True)
        update_gif(update_gif_label, 0)

        form_frame = tk.Frame(canvas, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(form_frame, text=title, font=("Arial", 14), bg="white").pack(pady=10)

        tk.Label(form_frame, text="Username:", bg="white", font=("Arial", 14)).pack(pady=5)
        username_entry = tk.Entry(form_frame, width=20, font=("Arial", 14))
        username_entry.pack(pady=5)

        if sign_up:
            tk.Label(form_frame, text="Email:", bg="white", font=("Arial", 14)).pack(pady=5)
            email_entry = tk.Entry(form_frame, width=20, font=("Arial", 14))
            email_entry.pack(pady=5)

            tk.Label(form_frame, text="Security Question:", bg="white", font=("Arial", 14)).pack(pady=5)
            security_question_entry = tk.Entry(form_frame, width=20, font=("Arial", 14))
            security_question_entry.pack(pady=5)

            tk.Label(form_frame, text="Security Answer:", bg="white", font=("Arial", 14)).pack(pady=5)
            security_answer_entry = tk.Entry(form_frame, width=20, font=("Arial", 14))
            security_answer_entry.pack(pady=5)

        tk.Label(form_frame, text="Password:", bg="white", font=("Arial", 14)).pack(pady=5)
        password_frame = tk.Frame(form_frame, bg="white")
        password_frame.pack(pady=5)

        password_entry = tk.Entry(password_frame, show='*', width=20, font=("Arial", 14))
        password_entry.pack(side=tk.LEFT, padx=5)

        eye_image_path = "eye_icon.png"
        eye_image = Image.open(eye_image_path)
        eye_photo = ImageTk.PhotoImage(eye_image)

        def toggle_password():
            if show_password.get():
                password_entry.config(show="")
                eye_button.config(image=eye_photo)
            else:
                password_entry.config(show="*")
                eye_button.config(image=eye_photo)

            show_password.set(not show_password.get())

        show_password = tk.BooleanVar(value=False)

        eye_button = tk.Button(password_frame, image=eye_photo, command=toggle_password)
        eye_button.pack(side=tk.LEFT, padx=5)

        if sign_up:
            tk.Button(form_frame, text="Submit", font="Arial", bg="lightgreen",
                      command=lambda: submit_command(username_entry.get(), password_entry.get(), email_entry.get(),
                                                     security_question_entry.get(), security_answer_entry.get())).pack(pady=20)

        if login:
            tk.Button(form_frame, text="Submit", font="Arial", bg="lightgreen",
                      command=lambda: submit_command(username_entry.get(), password_entry.get())).pack(pady=20)

        if forgot_password:
            tk.Label(form_frame, text="Email:", bg="white", font=("Arial", 14)).pack(pady=5)
            email_entry = tk.Entry(form_frame, width=20, font=("Arial", 14))
            email_entry.pack(pady=5)

            tk.Label(form_frame, text="Security Question:", bg="white", font=("Arial", 14)).pack(pady=5)
            security_question_entry = tk.Entry(form_frame, width=20, font=("Arial", 14))
            security_question_entry.pack(pady=5)

            tk.Label(form_frame, text="Security Answer:", bg="white", font=("Arial", 14)).pack(pady=5)
            security_answer_entry = tk.Entry(form_frame, width=20, font=("Arial", 14))
            security_answer_entry.pack(pady=5)

            tk.Button(form_frame, text="Submit", font="Arial", bg="lightgreen",
                      command=lambda: submit_command(email_entry.get(), security_question_entry.get(),
                                                     security_answer_entry.get(), password_entry.get())).pack(pady=20)

        return window

    def submit_login(self, username, password):
        """Handles the submission of the Login form."""
        if login(username, password):
            self.open_welcome_window(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def submit_reset_password(self, email, security_question, security_answer, new_password):
        """Handles the submission of the Forgot Password form."""
        reset_password(email, security_question, security_answer, new_password)
    def open_welcome_window(self, username):
        """Opens the welcome window with a GIF background and clickable screenshots."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to AppSphere")
        welcome_window.geometry("1800x1000")

        # Load the GIF
        gif_path = "mm.gif"  # Replace with the path to your GIF file
        gif = Image.open(gif_path)
        photo_sequence = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

        def update_gif(label, index):
            label.configure(image=photo_sequence[index])
            welcome_window.after(100, update_gif, label, (index + 1) % len(photo_sequence))

        # Create a label to display the GIF and place it in the background
        gif_label = tk.Label(welcome_window)
        gif_label.place(x=0, y=0, relwidth=1, relheight=1)
        update_gif(gif_label, 0)

        # Display the welcome message on top of the GIF
        welcome_label = tk.Label(welcome_window, text=f"Welcome, {username}!", font=("Arial", 25), bg='white',
                                 fg='black')
        welcome_label.place(relx=0.5, y=50, anchor="center")

        # Sample screenshots for tools
        tools = {
            "Calculator": "calculator.jpeg",
            "Paint": "paint.jpg",
            "Notepad": "notepad.png",
            "Dodge The Car": "dodgethecar.jpeg",  # Replace with actual game screenshots
            "Dodge The Ball": "dodge theball.jpeg",
            "Flappy Bird": "flappy.jpeg",
            "DeskAssist": "vertigo.png"
        }

        # Create a frame for centering the buttons
        button_frame = tk.Frame(welcome_window, bg='white')
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create and place buttons for each tool
        for index, (tool, img_path) in enumerate(tools.items()):
            img = Image.open(img_path)
            img = img.resize((200, 200), Image.NEAREST)  # Resize the image
            photo = ImageTk.PhotoImage(img)

            # Create button and place it on top of the GIF
            btn = tk.Button(button_frame, image=photo, text=tool, compound="top",
                            command=lambda t=tool: self.launch_tool(t))
            btn.image = photo

            # Use grid to place buttons in a grid layout
            btn.grid(row=index // 3, column=index % 3, padx=10, pady=10)


    def launch_tool(self, tool_name):
        """Launches the corresponding tool based on the button clicked."""
        if tool_name == "Calculator":
            launch_calculator()
        elif tool_name == "Paint":
            launch_paint()
        elif tool_name == "Notepad":
            launch_notepad()
        elif tool_name == "Dodge The Ball":
            launch_dodgetheball()
        elif tool_name == "Dodge The Car":
            launch_dodgethecar()
        elif tool_name == "Flappy Bird":
            launch_Flappy()
        elif tool_name == "DeskAssist":
            launch_Deskassist()


if __name__ == '__main__':
    root = customtkinter.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")  # Set the window size to fill the screen
    app = UserManagementApp(root)
    root.mainloop()
