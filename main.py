import customtkinter as ctk
import yt_dlp
import os
import threading
import imageio_ffmpeg as iio
from PIL import Image
import sys
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")
total_bytes_expected = 0
downloaded_bytes_total = 0
merging = False
def progress_hook(d):
    global total_bytes_expected, downloaded_bytes_total, merging
    status = d.get('status')
    if status == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes_expected = max(total_bytes_expected, total_bytes)
        downloaded_bytes_total = downloaded_bytes_total + downloaded_bytes
        if total_bytes_expected:
            percent = min(downloaded_bytes_total / total_bytes_expected * 100, 100)
            progress_bar.set(percent / 100)
            progress_label.configure(text=f"{percent:.1f}% ({downloaded_bytes_total//1024//1024}MB / {total_bytes_expected//1024//1024}MB)")
    elif status == 'finished':
        merging = True
        progress_label.configure(text="Merging video and audio…")
        app.update_idletasks()
    elif status == 'error':
        merging = False
def download_worker(fmt, url):
    global total_bytes_expected, downloaded_bytes_total, merging
    total_bytes_expected = 0
    downloaded_bytes_total = 0
    merging = False
    download_folder = get_download_path()
    ffmpeg_path = iio.get_ffmpeg_exe()
    opts = {
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "ffmpeg_location": ffmpeg_path,
        "progress_hooks": [progress_hook],
        "merge_output_format": "mp4" if fmt=="MP4" else None,
        "noplaylist": True,
    }
    if fmt == "MP4":
        res = resolution_var.get()
        opts["format"] = f"bestvideo[height<={res}]+bestaudio/best"
    else:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        status_label.configure(text=f"✅ Stáhnuto do: {download_folder}", text_color="white")
    except Exception as e:
        status_label.configure(text=f"❌ Chyba při stahování!\n{e}", text_color="white")
    finally:
        app.after(2000, hide_progress_bar)
        download_button.configure(state="normal")
def start_download():
    url = entry.get()
    fmt = format_var.get()
    status_label.configure(text="", text_color="white")
    if not url.strip():
        status_label.configure(text="❌ Zadej URL!", text_color="white")
        return
    download_button.configure(state="disabled")
    progress_bar.pack(pady=10)
    progress_label.pack(pady=5)
    progress_bar.set(0)
    progress_label.configure(text="0%")
    threading.Thread(target=download_worker, args=(fmt, url), daemon=True).start()
def hide_progress_bar():
    progress_bar.pack_forget()
    progress_label.pack_forget()
def toggle_resolution():
    if format_var.get() == "MP4":
        resolution_frame.pack(before=download_button, pady=5)
    else:
        resolution_frame.pack_forget()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Govis YT Downloader")
app.geometry("500x550")
app.resizable(False, False)
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(pady=20)
img_path = resource_path("g.png")
image = Image.open(img_path)
image = image.resize((60, 60))
app.logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(60, 60))
ctk.CTkLabel(header_frame, image=app.logo_image, text="").pack(side="left", padx=10)
ctk.CTkLabel(header_frame, text="Govis YouTube Downloader", 
             font=ctk.CTkFont(size=22, weight="bold")).pack(side="left", padx=10)
ctk.CTkLabel(app, text="Zadej YouTube URL:", font=ctk.CTkFont(size=14)).pack(pady=5)
entry = ctk.CTkEntry(app, placeholder_text="https://www.youtube.com/...", width=400)
entry.pack(pady=5)
ctk.CTkLabel(app, text="Vyber formát:", font=ctk.CTkFont(size=14)).pack(pady=10)
format_var = ctk.StringVar(value="MP4")
format_frame = ctk.CTkFrame(app, fg_color="transparent")
format_frame.pack(pady=5)
ctk.CTkRadioButton(format_frame, text="MP4", variable=format_var, value="MP4", command=toggle_resolution,
                   fg_color="#d32f2f", hover_color="#b71c1c", text_color="white").pack(side="left", padx=20)
ctk.CTkRadioButton(format_frame, text="MP3", variable=format_var, value="MP3", command=toggle_resolution,
                   fg_color="#d32f2f", hover_color="#b71c1c", text_color="white").pack(side="left", padx=20)
resolutions = ["1080", "720", "480", "360"]
resolution_var = ctk.StringVar(value="1080")
resolution_frame = ctk.CTkFrame(app, fg_color="transparent")
resolution_label = ctk.CTkLabel(resolution_frame, text="Vyber rozlišení (MP4):", font=ctk.CTkFont(size=14))
resolution_label.pack(pady=5)
resolution_optionmenu = ctk.CTkOptionMenu(resolution_frame, values=resolutions, variable=resolution_var,
                                          fg_color="#7a1f1f", button_color="#a32b2b", text_color="white", width=150)
resolution_optionmenu.pack(pady=5)
download_button = ctk.CTkButton(app, text="⬇ Stáhnout", width=200, height=40,
                                fg_color="#d32f2f", hover_color="#b71c1c", command=start_download)
download_button.pack(pady=15)
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_label = ctk.CTkLabel(app, text="0%", font=ctk.CTkFont(size=13))
status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=13))
status_label.pack(pady=10)
toggle_resolution()
app.mainloop()
