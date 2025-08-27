# pip install yt-dlp imageio-ffmpeg pyinstaller
import os
import threading
import yt_dlp
import imageio_ffmpeg as ffmpeg
import tkinter as tk
from tkinter import messagebox


def download_youtube_mp3(url, quality, filename=None):
    save_path = os.path.join(os.path.expanduser("~"), "Desktop", "mp3DL")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ffmpeg_path = ffmpeg.get_ffmpeg_exe()

    if filename and filename.strip() != "":
        out_template = os.path.join(save_path, f"{filename}.%(ext)s")
    else:
        out_template = os.path.join(save_path, "%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': out_template,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def reset_gui():
    url_entry.delete(0, tk.END)
    filename_entry.delete(0, tk.END)
    quality_var.set("192")


def start_download_thread():
    url = url_entry.get().strip()
    quality = quality_var.get()
    filename = filename_entry.get().strip()

    if not url:
        messagebox.showerror("エラー", "YouTubeのURLを入力してください")
        return

    def download_task():
        try:
            download_youtube_mp3(url, quality, filename)
            root.after(0, lambda: messagebox.showinfo("完了", f"ダウンロード完了（音質: {quality}kbps）"))
            root.after(0, reset_gui)
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("失敗", f"ダウンロードに失敗しました:\n{e}"))

    threading.Thread(target=download_task, daemon=True).start()

root = tk.Tk()
root.title("YouTube MP3ダウンローダー")
root.configure(bg='black')
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="YouTube URL:", bg='black', fg='white').pack(pady=(10, 0))
url_entry = tk.Entry(root, width=50, bg='white', fg='black')
url_entry.pack(pady=5)

tk.Label(root, text="音質を選択:", bg='black', fg='white').pack(pady=(10, 0))
quality_var = tk.StringVar(value="192")
qualities = [("128kbps", "128"), ("192kbps", "192"), ("256kbps", "256"), ("320kbps", "320")]
for text, value in qualities:
    tk.Radiobutton(root, text=text, variable=quality_var, value=value,
                   bg='black', fg='white', selectcolor='blue').pack(anchor='center')

tk.Label(root, text="MP3の名前（省略可）:", bg='black', fg='white').pack(pady=(10, 0))
filename_entry = tk.Entry(root, width=50, bg='white', fg='black')
filename_entry.pack(pady=5)

download_btn = tk.Button(root, text="ダウンロード", command=start_download_thread, bg='blue', fg='white')
download_btn.pack(pady=10)

root.mainloop()
