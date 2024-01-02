import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad")
        self.root.geometry("600x400")

        # Set the default indentation level (customize as needed)
        self.default_indentation = 4

        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Track changes
        self.file_path = None
        self.text_changed = False

        # Main text and line number bar
        self.text_widget = tk.Text(self.root, wrap="word", undo=True)
        self.text_widget.pack(expand=True, fill="both", side=tk.RIGHT)

        self.line_number_bar = tk.Text(self.root, width=4, wrap="none", takefocus=0, border=0, background="#f0f0f0", state="disabled")
        self.line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

        # Bind the event after creating self.text_widget
        self.text_widget.bind("<Key>", self.on_text_change)
        self.text_widget.bind("<Configure>", self.on_text_configure)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

       # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application, accelerator="Alt+F4")

        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Zoom In", command=lambda: self.zoom_text(2), accelerator="Ctrl++")
        edit_menu.add_command(label="Zoom Out", command=lambda: self.zoom_text(0.5), accelerator="Ctrl+-")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", command=self.replace_text, accelerator="Ctrl+F")

        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_separator()
        view_menu.add_command(label="Word Count", command=self.word_count, accelerator="Ctrl+W")

        # Bind keyboard shortcuts
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-Shift-s>", self.save_as_file)
        self.root.bind("<Alt-F4>", self.exit_application)
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<Control-y>", self.redo)
        self.root.bind("<Control-x>", self.cut)
        self.root.bind("<Control-c>", self.copy)
        self.root.bind("<Control-v>", self.paste)
        self.root.bind("<Control-a>", self.select_all)
        self.root.bind("<Control-w>", self.word_count)
        self.root.bind("<Control-f>", self.replace_text)
        self.root.bind("<Control-plus>", lambda event: self.zoom_text(2))
        self.root.bind("<Control-minus>", lambda event: self.zoom_text(0.5))

        # Variable to track whether the content is modified
        self.modified = False

        # Binding to track modifications
        self.text_widget.bind("<Key>", self.set_modified)

        # Bind the "Return" key event for auto-indentation
        self.text_widget.bind("<Return>", self.on_return_key)

    # ===================================== End of Function =====================================

    # ======================= Function for word count =======================
    def word_count(self, event=None):
        content = self.text_widget.get("1.0", tk.END)
        words = content.split()
        lines = content.splitlines()

        word_count = len(words)
        character_count = len(content)
        line_count = len(lines)

        count_message = f"Word Count: {word_count}\nCharacter Count: {character_count}\nLine Count: {line_count}"

        messagebox.showinfo("Word Count", count_message)
    # ===================================== End of Function =====================================

    # ======================= Function for find text =======================
    def find_text(self, event=None):
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
    # ===================================== End of Function =====================================

    # ======================= Function for find occurrences ======================
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
    # ===================================== End of Function =====================================

    # ======================= Function for replace text ======================
    def replace_text(self, event=None):
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
    # ===================================== End of Function =====================================

    # ======================= Function for replace occurrences ======================
    def replace_occurrences(self, search_term, replace_term):
        start_index = self.text_widget.search(search_term, 1.0, tk.END)

        while start_index:
            end_index = f"{start_index}+{len(search_term)}c"
            self.text_widget.delete(start_index, end_index)
            self.text_widget.insert(start_index, replace_term)

            start_index = self.text_widget.search(search_term, end_index, tk.END)
    # ===================================== End of Function =====================================

    # ======================= Function to check if text is modified or not ======================
    def set_modified(self, event):
        self.modified = True

    def on_text_change(self, event):
        self.text_changed = True
        self.update_status_bar()
        self.update_line_numbers()

    def on_text_configure(self, event):
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        lines = self.text_widget.get("1.0", tk.END).split("\n")
        line_count = len(lines)
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_number_bar.config(state="normal")
        self.line_number_bar.delete("1.0", tk.END)
        self.line_number_bar.insert(tk.END, line_numbers_text)
        self.line_number_bar.config(state="disabled")
    # ===================================== End of Function =====================================

    def on_return_key(self, event):
        current_line = self.text_widget.get("insert linestart", "insert lineend")
        leading_spaces = len(current_line) - len(current_line.lstrip())

        # Check if the previous line ends with ":"
        prev_line_number = int(self.text_widget.index("insert").split(".")[0]) - 1
        prev_line = self.text_widget.get(f"{prev_line_number}.0", f"{prev_line_number}.end").strip()
        indent_char = " " * self.default_indentation

        # Not sure why when ';' is used it is recognised ad ':', so used ';' below
        if prev_line.endswith(";"):
            # Use the default_indentation if the current line has no leading spaces
            indentation = leading_spaces + self.default_indentation
        else:
            # Use the same indentation as the previous line if it doesn't end with ":"
            indentation = leading_spaces

        # Insert a new line with the specified indentation
        self.text_widget.insert("insert", "\n" + " " * indentation)

        # Call the on_text_change function after auto-indentation
        self.on_text_change(event)

        # Prevent default behavior (new line insertion) from occurring
        return "break"
    # ===================================== End of Function =====================================

    def update_status_bar(self, event=None):
        if self.text_changed:
            self.status_bar.config(text="Unsaved Changes")
        else:
            self.status_bar.config(text="Ready")
    # ===================================== End of Function =====================================

    # ======================= Function to create new file  ======================
    def new_file(self, event=None):
        self.text_widget.delete(1.0, tk.END)
        if self.modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before creating a new file?")
            if response is None:
                return
            elif response:
                self.save_file()

        self.text_widget.delete(1.0, tk.END)
        self.modified = False
    # ===================================== End of Function =====================================

    # ======================= Function to open a file ======================
    def open_file(self, event=None):
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
    # ===================================== End of Function =====================================

    # ======================= Function to save a saved file ======================
    def save_file(self, event=None):
        if not self.modified:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"Notepad - {file_path}")
    # ===================================== End of Function =====================================
    
    # ======================= Function to save a new file ======================
    def save_as_file(self, event=None):
        self.save_file()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.root.title(f"Notepad - {file_path}")
            self.modified = False
    # ===================================== End of Function =====================================

    # ======================= Function to close notepad  ======================
    def exit_application(self, event=None):
        if self.modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before exiting?")
            if response is None:
                return
            elif response:
                self.save_file()
        self.root.destroy()
    # ===================================== End of Function =====================================

    # ======================= Function to undo  ======================
    def undo(self, event=None):
        try:
            self.text_widget.edit_undo()
        except tk.TclError:
            pass
    # ===================================== End of Function =====================================

    # ======================= Function to redo ======================
    def redo(self):
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass
    # ===================================== End of Function =====================================

    # ======================= Function to cut ======================
    def cut(self, event=None):
        self.text_widget.event_generate("<<Cut>>")
    # ===================================== End of Function =====================================

    # ======================= Function to copy  ======================
    def copy(self, event=None):
        self.text_widget.event_generate("<<Copy>>")
    # ===================================== End of Function =====================================

    # ======================= Function to paste ======================
    def paste(self, event=None):
        self.text_widget.event_generate("<<Paste>>")
    # ===================================== End of Function =====================================

    def zoom_text(self, factor):
            current_font = self.text_widget.cget("font")
            font_size = int(current_font.split(" ")[-1])
            new_font_size = max(8, min(48, int(font_size * factor)))
            new_font = current_font.replace(str(font_size), str(new_font_size))
            self.text_widget.configure(font=new_font)
    # ===================================== End of Function =====================================

    def select_all(self, event=None):
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.SEL_FIRST, "1.0")
        self.text_widget.mark_set(tk.SEL_LAST, tk.END)
        self.text_widget.see(tk.SEL_FIRST)
    # ===================================== End of Function =====================================

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
