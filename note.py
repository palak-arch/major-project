import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notepad")

        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(expand=tk.YES, fill=tk.BOTH)

        self.setup_menu()

    def setup_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="Font Size", command=self.change_font_size)
        format_menu.add_command(label="Text Color", command=self.change_text_color)
        format_menu.add_command(label="Text Font", command=self.change_text_font)
        menubar.add_cascade(label="Format", menu=format_menu)

        self.root.config(menu=menubar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = getattr(self, "file_path", None)
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
                self.file_path = file_path

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def change_font_size(self):
        font_size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=self.text_area["font"][1])
        if font_size:
            self.text_area.configure(font=("Helvetica", font_size))

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.configure(fg=color)

    def change_text_font(self):
        font_info = self.text_area["font"]
        font_info_parts = font_info.split()
        font_name = font_info_parts[0]
        font_size = font_info_parts[1] if len(font_info_parts) > 1 else "32"  # Default font size is 12
        font_style = "" if len(font_info_parts) < 3 else font_info_parts[2]

        font = simpledialog.askstring("Font", "Enter font name:", initialvalue=int(font_size))
    
        if font_size:
            font_style = simpledialog.askstring("Font Style", "Enter font style (italic, bold,):", initialvalue=font_style)
            if font_style:
                font_tuple = (font, font_size, font_style)
                self.text_area.configure(font=font_tuple)


def main():
    root = tk.Tk()
    notepad_app = NotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
