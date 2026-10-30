import tkinter as tk
from tkinter import messagebox, filedialog, font, ttk
import sqlite3
import os

class AdvancedNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Notes Application - Pro Edition")
        self.root.geometry("950x650")

        # Theme configurations
        self.is_dark_mode = True
        self.themes = {
            "dark": {
                "bg": "#1e1e1e", "fg": "#d4d4d4", "text_bg": "#252526",
                "text_fg": "#d4d4d4", "btn_bg": "#333333", "btn_fg": "#ffffff",
                "sidebar_bg": "#2d2d2d", "accent": "#007acc"
            },
            "light": {
                "bg": "#f3f3f3", "fg": "#000000", "text_bg": "#ffffff",
                "text_fg": "#000000", "btn_bg": "#e1e1e1", "btn_fg": "#000000",
                "sidebar_bg": "#e5e5e5", "accent": "#005fb8"
            }
        }

        # Setup Database Backend
        self.init_db()

        # Build UI layout
        self.create_widgets()
        self.apply_theme()

        # Start Auto-Save background cycle (every 15 seconds)
        self.auto_save_trigger()

    # --- Database Setup ---
    def init_db(self):
        self.conn = sqlite3.connect("notes_database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()

    # --- UI Architecture ---
    def create_widgets(self):
        # Main Layout PanedWindow (Sidebar for DB notes + Notebook Workspace)
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar for Database Notes Management
        self.sidebar = tk.Frame(self.main_pane, width=220)
        self.main_pane.add(self.sidebar, weight=1)

        sidebar_label = tk.Label(self.sidebar, text="Saved Notes Database", font=("Arial", 10, "bold"))
        sidebar_label.pack(pady=10)

        self.notes_listbox = tk.Listbox(self.sidebar, font=("Arial", 9), selectmode=tk.SINGLE)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_listbox.bind('<<ListboxSelect>>', self.load_note_from_db)

        db_btn_frame = tk.Frame(self.sidebar)
        db_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_save_db = tk.Button(db_btn_frame, text="Save to DB", command=self.save_to_db)
        self.btn_save_db.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        self.btn_del_db = tk.Button(db_btn_frame, text="Delete DB Note", command=self.delete_from_db)
        self.btn_del_db.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)

        self.btn_refresh_db = tk.Button(self.sidebar, text="Refresh List", command=self.refresh_db_list)
        self.btn_refresh_db.pack(fill=tk.X, padx=5, pady=2)

        # Right Workspace Frame
        self.workspace = tk.Frame(self.main_pane)
        self.main_pane.add(self.workspace, weight=4)

        # Toolbar Frame
        self.toolbar = tk.Frame(self.workspace)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)

        # File Operation Buttons
        tk.Button(self.toolbar, text="📄 New Tab", command=self.new_tab).pack(side=tk.LEFT, padx=2)
        tk.Button(self.toolbar, text="📂 Open", command=self.open_file).pack(side=tk.LEFT, padx=2)
        tk.Button(self.toolbar, text="💾 Save File", command=self.save_file).pack(side=tk.LEFT, padx=2)
        tk.Button(self.toolbar, text="🗑 Clear", command=self.clear_note).pack(side=tk.LEFT, padx=2)
        tk.Button(self.toolbar, text="🔍 Find/Replace", command=self.open_find_replace_dialog).pack(side=tk.LEFT, padx=2)

        # Formatting Buttons
        tk.Button(self.toolbar, text="<b>B</b>", command=lambda: self.apply_style("bold")).pack(side=tk.LEFT, padx=1)
        tk.Button(self.toolbar, text="<i>I</i>", command=lambda: self.apply_style("italic")).pack(side=tk.LEFT, padx=1)
        tk.Button(self.toolbar, text="<u>U</u>", command=lambda: self.apply_style("underline")).pack(side=tk.LEFT, padx=1)
        tk.Button(self.toolbar, text="̅O̅", command=lambda: self.apply_style("overline")).pack(side=tk.LEFT, padx=1)
        tk.Button(self.toolbar, text="<s>T</s>", command=lambda: self.apply_style("overstrike")).pack(side=tk.LEFT, padx=1)
        tk.Button(self.toolbar, text="〰 Wavy", command=lambda: self.apply_style("wavy")).pack(side=tk.LEFT, padx=1)
        tk.Button(self.toolbar, text="`Code`", command=lambda: self.apply_style("code")).pack(side=tk.LEFT, padx=1)

        # Font Size Selector
        tk.Label(self.toolbar, text="Size:").pack(side=tk.LEFT, padx=(10, 2))
        self.font_size_var = tk.IntVar(value=11)
        size_cb = ttk.Combobox(self.toolbar, textvariable=self.font_size_var, values=[9, 11, 14, 18, 22, 26], width=3)
        size_cb.pack(side=tk.LEFT)
        size_cb.bind("<<ComboboxSelected>>", self.change_font_size)

        # Theme Toggle Switch
        self.theme_btn = tk.Button(self.toolbar, text="☀️/🌙 Theme", command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT, padx=5)

        # Tab Notebook Frame for Multi-Tab Support
        self.notebook = ttk.Notebook(self.workspace)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Status Bar for Word & Character Count
        self.status_bar = tk.Label(self.workspace, text="Words: 0 | Characters: 0", anchor=tk.W, font=("Arial", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

        # Initialize with one default tab
        self.new_tab("Untitled")
        self.refresh_db_list()

    # --- Tab Management ---
    def new_tab(self, title="Untitled"):
        tab_frame = tk.Frame(self.notebook)
        
        # Text Area with Scrollbar
        text_scroll = tk.Scrollbar(tab_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        current_theme = self.themes["dark" if self.is_dark_mode else "light"]
        text_area = tk.Text(
            tab_frame, wrap=tk.WORD, yscrollcommand=text_scroll.set,
            bg=current_theme["text_bg"], fg=current_theme["text_fg"],
            insertbackground=current_theme["fg"], font=("Consolas", 11)
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        text_scroll.config(command=text_area.yview)

        # Bind events for word counting
        text_area.bind("<KeyRelease>", self.update_status_bar)

        self.notebook.add(tab_frame, text=title)
        self.notebook.select(tab_frame)

    def get_current_text_widget(self):
        try:
            current_tab = self.notebook.nametowidget(self.notebook.select())
            for widget in current_tab.winfo_children():
                if isinstance(widget, tk.Text):
                    return widget
        except Exception:
            pass
        return None

    # --- Rich Text Styling Engine ---
    def apply_style(self, style_type):
        txt = self.get_current_text_widget()
        if not txt:
            return
        
        try:
            sel_start = txt.index(tk.SEL_FIRST)
            sel_end = txt.index(tk.SEL_LAST)
        except tk.TclError:
            return  # No text selected

        current_font = font.Font(font=txt.cget("font"))
        tag_name = f"style_{style_type}_{id(txt)}"

        # Configure tags dynamically based on style type
        if style_type == "bold":
            f = font.Font(family=current_font.actual("family"), size=current_font.actual("size"), weight="bold")
            txt.tag_config(tag_name, font=f)
        elif style_type == "italic":
            f = font.Font(family=current_font.actual("family"), size=current_font.actual("size"), slant="italic")
            txt.tag_config(tag_name, font=f)
        elif style_type == "underline":
            txt.tag_config(tag_name, underline=True)
        elif style_type == "overline":
            txt.tag_config(tag_name, overline=True)
        elif style_type == "overstrike":
            txt.tag_config(tag_name, overstrike=True)
        elif style_type == "wavy":
            txt.tag_config(tag_name, underline=True, underlinefg="red") # Simulated wavy indicator underline
        elif style_type == "code":
            txt.tag_config(tag_name, background="#333333" if self.is_dark_mode else "#e0e0e0", foreground="#ff79c6")

        txt.tag_add(tag_name, sel_start, sel_end)

    def change_font_size(self, event=None):
        txt = self.get_current_text_widget()
        if not txt:
            return
        new_size = self.font_size_var.get()
        current_font = font.Font(font=txt.cget("font"))
        current_font.config(size=new_size)
        txt.config(font=current_font)

    # --- Functional Enhancements (Clear, Status Bar, Auto-Save) ---
    def clear_note(self):
        txt = self.get_current_text_widget()
        if not txt:
            return
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the current workspace?"):
            txt.delete("1.0", tk.END)
            self.update_status_bar()

    def update_status_bar(self, event=None):
        txt = self.get_current_text_widget()
        if not txt:
            return
        content = txt.get("1.0", tk.END).strip()
        words = len(content.split()) if content else 0
        chars = len(content)
        self.status_bar.config(text=f"Words: {words} | Characters: {chars}")

    def on_tab_changed(self, event):
        self.update_status_bar()

    def auto_save_trigger(self):
        try:
            txt = self.get_current_text_widget()
            if txt:
                content = txt.get("1.0", tk.END)
                with open(".autosave.txt", "w", encoding="utf-8") as f:
                    f.write(content)
        except Exception:
            pass
        self.root.after(15000, self.auto_save_trigger)  # Runs every 15 seconds

    # --- File Management & Database Integration ---
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.new_tab(os.path.basename(file_path))
            txt = self.get_current_text_widget()
            txt.insert("1.0", content)
            self.update_status_bar()

    def save_file(self):
        txt = self.get_current_text_widget()
        if not txt:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(txt.get("1.0", tk.END))
            messagebox.showinfo("Success", "File saved successfully!")

    def save_to_db(self):
        txt = self.get_current_text_widget()
        if not txt:
            return
        content = txt.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Note is empty!")
            return
        
        note_title = content.split('\n')[0][:25] or "Untitled Note"
        self.cursor.execute("INSERT INTO saved_notes (title, content) VALUES (?, ?)", (note_title, content))
        self.conn.commit()
        self.refresh_db_list()
        messagebox.showinfo("Database", "Note successfully saved to SQLite database!")

    def refresh_db_list(self):
        self.notes_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, title FROM saved_notes")
        for row in self.cursor.fetchall():
            self.notes_listbox.insert(tk.END, f"{row[0]}: {row[1]}")

    def load_note_from_db(self, event):
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        item_text = self.notes_listbox.get(selection[0])
        note_id = item_text.split(":")[0]

        self.cursor.execute("SELECT title, content FROM saved_notes WHERE id = ?", (note_id,))
        row = self.cursor.fetchone()
        if row:
            self.new_tab(row[0])
            txt = self.get_current_text_widget()
            txt.insert("1.0", row[1])
            self.update_status_bar()

    def delete_from_db(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a note from the sidebar database list to delete.")
            return
        item_text = self.notes_listbox.get(selection[0])
        note_id = item_text.split(":")[0]

        if messagebox.askyesno("Confirm Delete", "Permanently remove this note from the database?"):
            self.cursor.execute("DELETE FROM saved_notes WHERE id = ?", (note_id,))
            self.conn.commit()
            self.refresh_db_list()

    # --- Find & Replace Modal Dialog ---
    def open_find_replace_dialog(self):
        fr_window = tk.Toplevel(self.root)
        fr_window.title("Find and Replace")
        fr_window.geometry("340x160")
        fr_window.resizable(False, False)

        tk.Label(fr_window, text="Find:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        find_entry = tk.Entry(fr_window, width=25)
        find_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(fr_window, text="Replace:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        replace_entry = tk.Entry(fr_window, width=25)
        replace_entry.grid(row=1, column=1, padx=10, pady=5)

        def perform_find():
            txt = self.get_current_text_widget()
            if not txt:
                return
            target = find_entry.get()
            txt.tag_remove("found", "1.0", tk.END)
            if target:
                idx = "1.0"
                while True:
                    idx = txt.search(target, idx, nocase=1, stopindex=tk.END)
                    if not idx:
                        break
                    end_idx = f"{idx}+{len(target)}c"
                    txt.tag_add("found", idx, end_idx)
                    idx = end_idx
                txt.tag_config("found", background="yellow", foreground="black")

        def perform_replace_single():
            txt = self.get_current_text_widget()
            if not txt:
                return
            target = find_entry.get()
            replacement = replace_entry.get()
            try:
                sel_start = txt.index(tk.SEL_FIRST)
                sel_end = txt.index(tk.SEL_LAST)
                selected_text = txt.get(sel_start, sel_end)
                if selected_text.lower() == target.lower():
                    txt.delete(sel_start, sel_end)
                    txt.insert(sel_start, replacement)
            except tk.TclError:
                pass

        def perform_replace_all():
            txt = self.get_current_text_widget()
            if not txt:
                return
            target = find_entry.get()
            replacement = replace_entry.get()
            content = txt.get("1.0", tk.END)
            new_content = content.replace(target, replacement)
            txt.delete("1.0", tk.END)
            txt.insert("1.0", new_content)

        btn_frame = tk.Frame(fr_window)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Find", command=perform_find).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Replace Next", command=perform_replace_single).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Replace All", command=perform_replace_all).pack(side=tk.LEFT, padx=5)

    # --- Theme Engine ---
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        t = self.themes["dark" if self.is_dark_mode else "light"]
        self.root.config(bg=t["bg"])
        self.sidebar.config(bg=t["sidebar_bg"])
        self.workspace.config(bg=t["bg"])
        self.toolbar.config(bg=t["bg"])
        
        # Apply style updates to open text areas
        for tab_id in self.notebook.tabs():
            tab_widget = self.notebook.nametowidget(tab_id)
            for widget in tab_widget.winfo_children():
                if isinstance(widget, tk.Text):
                    widget.config(
                        bg=t["text_bg"], fg=t["text_fg"],
                        insertbackground=t["fg"]
                    )

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedNotesApp(root)
    root.mainloop()