
#pip install yt-dlp imageio-ffmpeg

import os
import yt_dlp
import imageio_ffmpeg as ffmpeg

def download_youtube_mp3(url):

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_folder = os.path.join(desktop, "mp3DL")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ffmpeg_path = ffmpeg.get_ffmpeg_exe()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("YouTubeのURLを入力してください: ")
    try:
        download_youtube_mp3(url)
        print("ダウンロード完了")
    except Exception as e:
        print("ダウンロードに失敗しました:", e)
