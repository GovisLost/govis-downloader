import customtkinter as ctk
from pytubefix import YouTube
from PIL import Image
import shutil
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def video_download(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        download_folder = get_download_path()
        stream.download(output_path=download_folder)
        status_label.configure(text=f"🎬 Video staženo do: {download_folder}", text_color="green")
    except Exception as e:
        status_label.configure(text=f"❌ Chyba při stahování videa!", text_color="red")

def audio_download(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        download_folder = get_download_path()
        out_file = stream.download(output_path=download_folder)
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        shutil.move(out_file, new_file)
        status_label.configure(text=f"🎵 MP3 staženo do: {download_folder}", text_color="green")
    except Exception as e:
        status_label.configure(text=f"❌ Chyba při stahování audia!", text_color="red")

def return_to_menu():
    for widget in app.winfo_children():
        widget.destroy()
    main_menu()

def input_video(download_type="video"):
    for widget in app.winfo_children():
        widget.destroy()

    img_path = resource_path("g.png")
    image = Image.open(img_path)
    logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(120, 120))
    ctk.CTkLabel(app, image=logo_image, text="").pack(pady=10)
    app.logo_image = logo_image

    ctk.CTkLabel(app, text="Zadej YouTube URL:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 10))

    global entry, status_label
    entry = ctk.CTkEntry(app, placeholder_text="https://www.youtube.com/...", width=300)
    entry.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=13))
    status_label.pack(pady=10)

    button_style = {"width": 180, "height": 40, "corner_radius": 10, "fg_color": "#d32f2f", "hover_color": "#b71c1c"}

    if download_type == "video":
        ctk.CTkButton(app, text="⬇ Stáhnout MP4", command=lambda: video_download(entry.get()), **button_style).pack(pady=10)
    else:
        ctk.CTkButton(app, text="⬇ Stáhnout MP3", command=lambda: audio_download(entry.get()), **button_style).pack(pady=10)

    ctk.CTkButton(app, text="↩ Zpět do menu", command=return_to_menu, **button_style).pack(pady=5)

def main_menu():
    for widget in app.winfo_children():
        widget.destroy()

    img_path = resource_path("g.png")
    image = Image.open(img_path)
    logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(120, 120))
    ctk.CTkLabel(app, image=logo_image, text="").pack(pady=10)
    app.logo_image = logo_image

    ctk.CTkLabel(app, text="Govis YouTube Downloader", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
    ctk.CTkLabel(app, text="Vyber si formát:", font=ctk.CTkFont(size=16)).pack(pady=(5, 15))

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=10)

    button_style = {"width": 120, "height": 40, "corner_radius": 10, "fg_color": "#d32f2f", "hover_color": "#b71c1c"}

    ctk.CTkButton(frame, text="🎞 MP4", command=lambda: input_video("video"), **button_style).pack(side="left", padx=10)
    ctk.CTkButton(frame, text="🔊 MP3", command=lambda: input_video("audio"), **button_style).pack(side="left", padx=10)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("420x420")
app.title("Govis YouTube Downloader")
app.resizable(False, False)

main_menu()
app.mainloop()

