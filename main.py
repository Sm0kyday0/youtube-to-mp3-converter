# pip install yt-dlp imageio-ffmpeg

import os
import yt_dlp
import imageio_ffmpeg as ffmpeg

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

if __name__ == "__main__":
    url = input("YouTubeのURLを入力してください: ")

    print("音質を選択してください:")
    print("1: 128kbps")
    print("2: 192kbps")
    print("3: 256kbps")
    print("4: 320kbps")

    choice = input("番号を入力: ")
    quality_map = {
        "1": "128",
        "2": "192",
        "3": "256",
        "4": "320",
    }
    quality = quality_map.get(choice, "192")

    filename = input("MP3の名前を入力してください（指定しないなら動画タイトル）: ")

    try:
        download_youtube_mp3(url, quality, filename)
        print(f"ダウンロード完了（音質: {quality}kbps）")
    except Exception as e:
        print("ダウンロードに失敗しました:", e)
