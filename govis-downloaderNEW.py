import customtkinter as ctk
from pytubefix import YouTube
from PIL import Image
import os
import shutil
import sys
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def get_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")
def return_to_menu():
    for widget in app.winfo_children():
        widget.destroy()
    main_menu()
def inputvideo(download_type="video"):
    for widget in app.winfo_children():
        widget.destroy()
    try:
        img_path = resource_path("g.png")
        image = Image.open(img_path)
        app.logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(120, 120))
        ctk.CTkLabel(app, text="", image=app.logo_image).pack(pady=10)
    except Exception as e:
        print("Nepodařilo se načíst obrázek:", e)
    ctk.CTkLabel(app, text="Zadej YouTube URL:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
    entry = ctk.CTkEntry(app, placeholder_text="https://www.youtube.com/...", width=300)
    entry.pack(pady=10)
    status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=13))
    status_label.pack(pady=10)
    button_style = {"fg_color": "#d32f2f", "hover_color": "#b71c1c"}
    ctk.CTkButton(app, text="⬇ Stáhnout", width=180, height=40, corner_radius=10, **button_style).pack(pady=10)
    ctk.CTkButton(app, text="↩ Zpět do menu", command=return_to_menu, width=150, **button_style).pack(pady=5)
def main_menu():
    try:
        img_path = resource_path("g.png")
        image = Image.open(img_path)
        app.logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(120, 120))
        ctk.CTkLabel(app, text="", image=app.logo_image).pack(pady=15)
    except Exception as e:
        print("Nepodařilo se načíst obrázek:", e)
    ctk.CTkLabel(app, text="Vyber si formát:", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=20)
    button_style = {"fg_color": "#d32f2f", "hover_color": "#b71c1c"}
    ctk.CTkButton(frame, text="🎞 MP4", width=120, height=40, corner_radius=10,
                  command=lambda: inputvideo("video"), **button_style).pack(side="left", padx=10)
    ctk.CTkButton(frame, text="🔊 MP3", width=120, height=40, corner_radius=10,
                  command=lambda: inputvideo("audio"), **button_style).pack(side="left", padx=10)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Govis YouTube Downloader")
app.geometry("420x420")
app.resizable(False, False)
main_menu()
app.mainloop()
