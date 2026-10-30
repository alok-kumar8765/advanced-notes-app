<div align="center">

# 📝 Advanced Notes Application - Pro Edition

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A feature-rich, desktop-based rich text notes manager built with Python, featuring multi-tab support, local SQLite database storage, dynamic find & replace, auto-saving, and customizable styling.*

</div>

---

## 📖 Table of Contents
1. [Purpose of This Project](#-purpose-of-this-project)
2. [Features](#-features)
3. [File Structure](#-file-structure)
4. [System Architecture & Diagrams](#-system-architecture--diagrams)
   - [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
   - [Entity-Relationship (ER) Schema Diagram](#entity-relationship-er-schema-diagram)
5. [Requirements](#-requirements)
6. [Installation & Setup](#-installation--setup)
7. [Usage / Instructions](#-usage--instructions)
8. [Pros & Cons](#-pros--cons)
9. [Limitations](#-limitations)
10. [Bugs & Vulnerabilities](#-bugs--vulnerabilities)
11. [Future Updates](#-future-updates)
12. [Contributing](#-contributing)
13. [Support & Star](#-support--star)

---

## 🎯 Purpose of This Project
Basic text editors and standard tutorial applications often lack modern productivity features like multi-tab workspace support, persistent database records, and advanced styling options. The purpose of this project is to provide a robust, production-grade desktop notes application that bridges simple text storage with advanced user-facing features—all contained within a lightweight Python script using standard and native libraries.

---

## ✨ Features
* **Multi-Tab Workspace (`ttk.Notebook`):** Open, edit, and manage multiple notes simultaneously across separate tabs.
* **SQLite Database Backend:** Save notes directly into a local SQLite database, browse them via a dedicated sidebar list, and load or delete them instantly.
* **Rich Text Formatting Engine:** Format selected text chunks with **Bold**, *Italic*, <u>Underline</u>, ̅O̅verline, <s>Strikethrough</s>, Wavy Underline simulation, and `Inline Code` blocks.
* **Dynamic Font Scaling:** Adjust font sizes on the fly via a quick selection dropdown.
* **Find & Replace Engine:** Search keywords with yellow text highlighting, replace matches individually, or execute a global **Replace All**.
* **Dark / Light Mode Toggle:** Seamlessly switch themes between a sleek dark mode and a clean light mode.
* **Auto-Save Protection:** Automatically creates a background `.autosave.txt` backup every 15 seconds to prevent data loss.
* **Dynamic Status Bar:** Real-time character and word count updates as you type.

---

## 📁 File Structure
```text
advanced-notes-app/
│
├── notes_database.db         # Local SQLite database (auto-generated)
├── .autosave.txt             # Background auto-save cache file
├── app.py                    # Main application script
└── README.md                 # Project documentation

```

---

## 📊 System Architecture & Diagrams

### Data Flow Diagram (DFD)

```text
 [ User Input (Keyboard / Mouse) ]
                │
                ▼
      [ Active Tab Widget ]
                │
                ├──────────────────────────────────────────────┐
                ▼                                              ▼
    [ Formatting Engine ]                         [ File / DB Manager ]
    - Bold, Italic, Underline                     - Open / Save Flat Files (.txt)
    - Font Scaling & Themes                       - SQLite DB (Save, Load, Delete)
                │                                              │
                └──────────────────────┬───────────────────────┘
                                       │
                                       ▼
                       [ Status Bar & Auto-Save Backup ]

```

### Entity-Relationship (ER) Schema Diagram

*(Database structure for stored notes)*

```text
+-------------------------------------------------------+
|                       saved_notes                     |
+-------------------------------------------------------+
| PK | id      | INTEGER (Auto-increment, Primary Key)  |
|    | title   | TEXT    (Extracted first line or title)|
|    | content | TEXT    (Full formatted note body)     |
+-------------------------------------------------------+

```

---

## ⚙️ Requirements

* **Operating System:** Windows 10/11, macOS, or Linux
* **Python Version:** Python 3.8 or higher
* **Dependencies:** Uses Python built-in standard libraries (`tkinter`, `sqlite3`, `os`, `font`) requiring no external pip installations.

---

## 📦 Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/alok--kumar8765/advanced-notes-app.git](https://github.com/alok--kumar8765/advanced-notes-app.git)
cd advanced-notes-app

```


2. **Run the application:**
```bash
python app.py

```



---

## 🕹️ Usage/Instructions

* **Creating Notes:** Click **📄 New Tab** to open a fresh workspace tab.
* **Saving to Database:** Click **Save to DB** to store your note permanently in the local SQLite database.
* **Browsing Saved Notes:** Click any entry in the left sidebar listbox to load it into a new tab instantly.
* **Find & Replace:** Click **🔍 Find/Replace** to open the modal dialog for searching and replacing text.
* **Formatting Text:** Highlight any text inside your editor and click the formatting buttons (`<b>B</b>`, `<i>I</i>`, `<u>U</u>`, etc.) to apply styles.
* **Theme Toggle:** Click the **☀️/🌙 Theme** button in the toolbar to switch between dark and light modes.

---

## ⚖️ Pros & Cons

### Pros

* Zero external package dependencies required (runs natively with Python).
* Fast, responsive interface with persistent offline database storage.
* Multi-tab capability allows multitasking across multiple documents.

### Cons

* Tkinter UI components look native/standard depending on the OS styling engine.
* Rich text styles are applied via local tags and do not export into complex formats like PDF or docx natively without third-party libraries.

---

## ⚠️ Limitations

* SQLite database file is stored locally in the root directory; migrating notes across computers requires copying the `.db` file or exporting to `.txt`.

---

## 🐛 Bugs & Vulnerabilities

* **Overlapping Tag Styling:** Applying multiple conflicting font-family tags on the exact same text selection can occasionally override previous styles unless handled sequentially.
* **Find/Replace Focus:** Modal dialog searches require the active tab window to maintain focus.

---

## 🔮 Future Updates

* [ ] Export notes directly to PDF and Markdown (`.md`) formats.
* [ ] Add cloud synchronization support via Firebase or Supabase.
* [ ] Implement tag-based categorization and search filters for the SQLite database.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the Project (`https://github.com/alok--kumar8765/advanced-notes-app/fork`)
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⭐ Support

If you found this project useful, please give it a **star** on GitHub!