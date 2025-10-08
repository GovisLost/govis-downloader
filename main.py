import tkinter as tk
from pytubefix import YouTube
import os
import shutil
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
        status_label.config(text=f"🎬 Video staženo do: {download_folder}")
    except Exception as e:
        status_label.config(text="Chyba při stahování videa!")
def audio_download(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only()
        download_folder = get_download_path()
        out_file = stream.download(output_path=download_folder)
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        shutil.move(out_file, new_file)

        status_label.config(text=f"🎵 MP3 staženo do: {download_folder}")
    except Exception as e:
        status_label.config(text="Chyba při stahování audia!")
def return_to_menu():
    for widget in win.winfo_children():
        widget.destroy()
    main_menu()
def inputvideo(download_type="video"):
    for widget in win.winfo_children():
        widget.destroy()
    global entry, status_label
    status_label = tk.Label(win, text="", font=("Comic Sans MS", 12), bg="black", fg="white")
    status_label.pack(pady=5)
    label = tk.Label(win, text="Zadej YouTube URL:", font=("Comic Sans MS", 14), bg="black", fg="red")
    label.pack(pady=20)
    entry = tk.Entry(win, font=("Comic Sans MS", 14), width=30)
    entry.pack(pady=10)
    if download_type == "video":
        btn_text = "Stáhnout v MP4"
        command = lambda: video_download(entry.get())
    else:
        btn_text = "Stáhnout v MP3"
        command = lambda: audio_download(entry.get())
    btn = tk.Button(
        win,
        text=btn_text,
        command=command,
        font=("Comic Sans MS", 14),
        bg="black",
        fg="red"
    )
    btn.pack(pady=10)
    back_btn = tk.Button(
        win,
        text="↩ Zpět do menu",
        command=return_to_menu,
        font=("Comic Sans MS", 12),
        bg="black",
        fg="red"
    )
    back_btn.pack(pady=10)
def main_menu():
    img_label = tk.Label(win, image=img, bg="black", bd=0, highlightthickness=0)
    img_label.pack(pady=10)
    nadpis = tk.Label(win, text="Vyber si formát:", font=("Comic Sans MS", 14),
                      bg="black", fg="red")
    nadpis.pack(pady=10)
    button_frame = tk.Frame(win, bg="black")
    button_frame.pack(pady=20)
    btn_1 = tk.Button(
        button_frame,
        text="🎞MP4",
        width=8,
        font=("Comic Sans MS", 14),
        bg="black",
        fg="red",
        command=lambda: inputvideo("video")
    )
    btn_1.pack(side="left", padx=10)

    btn_2 = tk.Button(
        button_frame,
        text="🔊MP3",
        width=8,
        font=("Comic Sans MS", 14),
        bg="black",
        fg="red",
        command=lambda: inputvideo("audio")
    )
    btn_2.pack(side="left", padx=10)
win = tk.Tk()
win.geometry("400x400")
win.title("Govis yt downloader")
win.configure(background="black")
img = tk.PhotoImage(file=resource_path("g.png"))
img = img.subsample(2, 2)
main_menu()
win.mainloop()
