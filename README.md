# StickyPy - A Desktop Sticky Notes App

A modern and lightweight sticky notes application for Windows, built with Python and Tkinter. It allows you to keep your notes always visible on your desktop, thanks to a custom borderless window.

![Application Screenshot]

## 🚀 Features

-   **Borderless UI:** Features a sleek, modern look without the default Windows title bar.
-   **Always on Top:** Notes stay on top of other windows, ensuring they are always visible.
-   **Taskbar Integration:** Minimizes to the taskbar and can be restored just like a standard application.
-   **Automatic Saving:** The note's title and content are automatically saved to a `json` file on close and reloaded on launch.
-   **Drag to Move:** Easily move the note anywhere on the screen by dragging its header.
-   **Editable Title:** Simply click on the title to change it.

## 🛠️ Technologies Used

-   **Python 3:** The core programming language.
-   **Tkinter:** Python's standard library for the graphical user interface (GUI).
-   **ctypes:** Used for UI customization by accessing the Windows API to remove the default title bar while keeping the app on the taskbar.

## 🏃‍♀️ How to Run

1.  Clone this repository or download it as a ZIP file.
2.  No external libraries are needed as it only uses Python's standard library.
3.  Run the application with the following command:
    ```bash
    python sticky_note.pyw
    ```

### Building an Executable (Optional)

To convert the application into a standalone `.exe` file, you can use `pyinstaller`:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --noconsole sticky_note.pyw
```

This will create a `dist` folder containing the final executable file.
