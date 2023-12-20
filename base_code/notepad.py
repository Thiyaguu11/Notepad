import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("600x400")

        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Track changes
        self.file_path = None
        self.text_changed = False

        self.text_widget = tk.Text(self.root, wrap="word", undo=True)
        self.text_widget.pack(expand=True, fill="both")

        # Bind the event after creating self.text_widget
        self.text_widget.bind("<Key>", self.on_text_change)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Zoom In", command=lambda: self.zoom_text(2))
        edit_menu.add_command(label="Zoom Out", command=lambda: self.zoom_text(0.5))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", command=self.replace_text)

        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_separator()
        view_menu.add_command(label="Word Count", command=self.word_count)

        # Variable to track whether the content is modified
        self.modified = False

        # Binding to track modifications
        self.text_widget.bind("<Key>", self.set_modified)

    def word_count(self):
        content = self.text_widget.get("1.0", tk.END)
        words = content.split()
        lines = content.splitlines()

        word_count = len(words)
        character_count = len(content)
        line_count = len(lines)

        count_message = f"Word Count: {word_count}\nCharacter Count: {character_count}\nLine Count: {line_count}"

        messagebox.showinfo("Word Count", count_message)

    def find_text(self):
        find_dialog = tk.Toplevel(self.root)
        find_dialog.title("Find Text")

        find_label = tk.Label(find_dialog, text="Find:")
        find_label.grid(row=0, column=0, padx=10, pady=10)

        find_entry = tk.Entry(find_dialog)
        find_entry.grid(row=0, column=1, padx=10, pady=10)

        find_button = tk.Button(find_dialog, text="Find", command=lambda: self.find_occurrences(find_entry.get()))
        find_button.grid(row=0, column=2, padx=10, pady=10)

        def on_close():
            find_dialog.destroy()

        find_dialog.protocol("WM_DELETE_WINDOW", on_close)

    def find_occurrences(self, search_term):
        start_index = "1.0"
        count = tk.IntVar()
        content = self.text_widget.get(start_index, tk.END)
        index = content.find(search_term, count.get())

        while index != -1:
            end_index = f"{start_index}+{index}c"
            self.text_widget.tag_add(tk.SEL, start_index, end_index)
            start_index = end_index
            content = self.text_widget.get(start_index, tk.END)
            index = content.find(search_term, count.get())

        if tk.SEL not in self.text_widget.tag_ranges(tk.SEL):
            messagebox.showinfo("Find", "No more occurrences found.")
            self.text_widget.tag_remove(tk.SEL, "1.0", tk.END)
        else:
            self.text_widget.mark_set(tk.SEL_FIRST, self.text_widget.index(tk.SEL_FIRST))
            self.text_widget.mark_set(tk.SEL_LAST, self.text_widget.index(tk.SEL_LAST))
            self.text_widget.see(tk.SEL_FIRST)


    def replace_text(self):
        replace_dialog = tk.Toplevel(self.root)
        replace_dialog.title("Replace Text")

        find_label = tk.Label(replace_dialog, text="Find:")
        find_label.grid(row=0, column=0, padx=10, pady=10)

        find_entry = tk.Entry(replace_dialog)
        find_entry.grid(row=0, column=1, padx=10, pady=10)

        replace_label = tk.Label(replace_dialog, text="Replace with:")
        replace_label.grid(row=1, column=0, padx=10, pady=10)

        replace_entry = tk.Entry(replace_dialog)
        replace_entry.grid(row=1, column=1, padx=10, pady=10)

        replace_button = tk.Button(replace_dialog, text="Replace", command=lambda: self.replace_occurrences(find_entry.get(), replace_entry.get()))
        replace_button.grid(row=0, column=2, padx=10, pady=10)

    def replace_occurrences(self, search_term, replace_term):
        start_index = self.text_widget.search(search_term, 1.0, tk.END)

        while start_index:
            end_index = f"{start_index}+{len(search_term)}c"
            self.text_widget.delete(start_index, end_index)
            self.text_widget.insert(start_index, replace_term)

            start_index = self.text_widget.search(search_term, end_index, tk.END)

    def set_modified(self, event):
        self.modified = True

    def on_text_change(self, event):
        self.text_changed = True
        self.update_status_bar()

    def update_status_bar(self):
        if self.text_changed:
            self.status_bar.config(text="Unsaved Changes")
        else:
            self.status_bar.config(text="Ready")

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)
        if self.modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before creating a new file?")
            if response is None:
                return
            elif response:
                self.save_file()

        self.text_widget.delete(1.0, tk.END)
        self.modified = False

    def open_file(self):
        if self.modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before opening a new file?")
            if response is None:
                return
            elif response:
                self.save_file()

        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
            self.root.title(f"Notepad - {file_path}")
            self.modified = False

    def save_file(self):
        if not self.modified:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"Notepad - {file_path}")

    def save_as_file(self):
        self.save_file()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"Notepad - {file_path}")
            self.modified = False
    
    def exit_application(self):
        if self.modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before exiting?")
            if response is None:
                return
            elif response:
                self.save_file()
        self.root.destroy()

    def undo(self):
        try:
            self.text_widget.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")
    
    def zoom_text(self, factor):
            current_font = self.text_widget.cget("font")
            font_size = int(current_font.split(" ")[-1])
            new_font_size = max(8, min(48, int(font_size * factor)))
            new_font = current_font.replace(str(font_size), str(new_font_size))
            self.text_widget.configure(font=new_font)

    def select_all(self):
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.SEL_FIRST, "1.0")
        self.text_widget.mark_set(tk.SEL_LAST, tk.END)
        self.text_widget.see(tk.SEL_FIRST)


if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
