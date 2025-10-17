import tkinter as tk
import os
import json
import ctypes

# --- Windows API Fonksiyonları için Ayarlar ---
# Bu kısım, pencerenin varsayılan başlık çubuğunu kaldırmamızı sağlar.
try:
    GWL_STYLE = -16
    WS_CAPTION = 0x00C00000
    WS_THICKFRAME = 0x00040000
    WS_MINIMIZEBOX = 0x00020000
    WS_MAXIMIZEBOX = 0x00010000
    WS_SYSMENU = 0x00080000
    SWP_FRAMECHANGED = 0x0020
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
except Exception:
    pass # Windows dışı bir sistemde çalışırsa hata vermemesi için

# Not verilerinin kaydedileceği dosya
SAVE_FILE = "sticky_note_data.json"

class StickyNote:
    def __init__(self, root):
        self.root = root
        
        # --- Başlık Çubuğunu Kaldırma Sihri ---
        # Bu fonksiyon, pencere oluşturulduktan sonra başlık çubuğunu kaldırır.
        def remove_title_bar():
            try:
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
                style &= ~WS_CAPTION & ~WS_THICKFRAME & ~WS_MINIMIZEBOX & ~WS_MAXIMIZEBOX & ~WS_SYSMENU
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
                ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER)
            except Exception:
                # Windows'ta değilsek bu kısmı atla
                pass
        
        # Fonksiyonu çok kısa bir süre sonra çalıştırarak pencerenin hazır olmasını garantile
        self.root.after(10, remove_title_bar)
        
        # Pencereyi her zaman en üstte tutma özelliği
        self.root.wm_attributes("-topmost", 1)
        
        # Ana renk ve fontlar
        self.bg_color = "#FFFFAA"
        self.header_font = ("Calibri", 12, "bold")
        self.main_font = ("Calibri", 12)
        
        # Kendi özel başlık çubuğumuz
        self.header_frame = tk.Frame(self.root, bg=self.bg_color)
        self.header_frame.pack(side='top', fill='x')

        self.close_button = tk.Label(self.header_frame, text=" X ", bg=self.bg_color, fg="black", font=self.header_font, cursor="hand2")
        self.close_button.pack(side='right', padx=5)
        self.close_button.bind("<Button-1>", self.quit_application)

        self.minimize_button = tk.Label(self.header_frame, text=" ... ", bg=self.bg_color, fg="black", font=self.header_font, cursor="hand2")
        self.minimize_button.pack(side='right')
        self.minimize_button.bind("<Button-1>", self.minimize_window)

        self.title_entry = tk.Entry(self.header_frame, bg=self.bg_color, fg="black", font=self.header_font, justify='center', bd=0, highlightthickness=0, relief='flat', insertbackground="black")
        self.title_entry.pack(side='left', fill='x', expand=True, padx=10)

        # Butonların üzerine gelince renk değiştirme
        self.close_button.bind("<Enter>", lambda e: self.on_enter(self.close_button))
        self.close_button.bind("<Leave>", lambda e: self.on_leave(self.close_button))
        self.minimize_button.bind("<Enter>", lambda e: self.on_enter(self.minimize_button))
        self.minimize_button.bind("<Leave>", lambda e: self.on_leave(self.minimize_button))

        # Not Alanı
        self.text_widget = tk.Text(self.root, bg=self.bg_color, fg="black", font=self.main_font, padx=10, pady=10, bd=0, highlightthickness=0, insertbackground="black")
        self.text_widget.pack(expand=True, fill='both')

        self.load_note()

        # Pencereyi sürüklemek için
        for widget in [self.header_frame, self.title_entry]:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<ButtonRelease-1>", self.stop_move)
            widget.bind("<B1-Motion>", self.do_move)

    def minimize_window(self, event=None):
        self.root.iconify()

    def quit_application(self, event=None):
        self.save_note()
        self.root.destroy()

    def on_enter(self, widget): widget.config(bg="#E0E0E0")
    def on_leave(self, widget): widget.config(bg=self.bg_color)
    def start_move(self, event): self.x, self.y = event.x, event.y
    def stop_move(self, event): self.x, self.y = None, None
    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    def save_note(self):
        data = {"title": self.title_entry.get(), "content": self.text_widget.get("1.0", tk.END).strip()}
        with open(SAVE_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

    def load_note(self):
        default_title = "TO-DO LIST"
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f: data = json.load(f)
                self.title_entry.insert(0, data.get("title", default_title))
                self.text_widget.insert("1.0", data.get("content", ""))
            except Exception: self.title_entry.insert(0, default_title)
        else: self.title_entry.insert(0, default_title)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("320x280+150+150")
    # Pencereye varsayılan bir isim verelim, bu görev çubuğunda görünecek
    root.title("StickyPy") 
    app = StickyNote(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_application)
    root.mainloop()