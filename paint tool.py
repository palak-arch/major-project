import tkinter as tk
from tkinter import colorchooser, filedialog
from tkinter import Button

class PaintApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint Application")
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both")

        self.color = "black"
        self.selected_item = None
        self.eraser_mode = False
        self.current_shape = None  

        self.create_menu()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        shape_menu = tk.Menu(menubar, tearoff=0)
        shape_menu.add_command(label="Line", command=lambda: self.select_shape("line"))
        shape_menu.add_command(label="Oval", command=lambda: self.select_shape("oval"))
        shape_menu.add_command(label="Rectangle", command=lambda: self.select_shape("rectangle"))
        shape_menu.add_command(label="Triangle", command=lambda: self.select_shape("triangle"))
        shape_menu.add_command(label="Circle", command=lambda: self.select_shape("circle"))
        menubar.add_cascade(label="Shapes", menu=shape_menu)

        color_menu = tk.Menu(menubar, tearoff=0)
        color_menu.add_command(label="Select Color", command=self.select_color)
        menubar.add_cascade(label="Color", menu=color_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Eraser", command=self.toggle_eraser)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        self.master.config(menu=menubar)

    def new_file(self):
        self.canvas.delete("all")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.canvas.postscript(file=file_path, colormode='color')

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.color = "white"
            self.canvas["cursor"] = "dotbox"
        else:
            self.color = "black"
            self.canvas["cursor"] = ""  

    def select_color(self):
        color = colorchooser.askcolor(title="Select Color")
        if color[1]:
            self.color = color[1]

    def select_shape(self, shape):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.current_shape = shape

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        pass

    def on_release(self, event):
        if self.current_shape == "line":
            if not self.eraser_mode:
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color)
        elif self.current_shape == "oval":
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.color)
        elif self.current_shape == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color)
        elif self.current_shape == "triangle":
            self.draw_triangle(self.start_x, self.start_y, event.x, event.y)
        elif self.current_shape == "circle":
            self.draw_circle(self.start_x, self.start_y, event.x, event.y)

    def draw_triangle(self, x1, y1, x2, y2):
        self.canvas.create_polygon(x1, y1, (x1 + x2) / 2, y2, x2, y1, fill=self.color, outline=self.color)

    def draw_circle(self, x1, y1, x2, y2):
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
