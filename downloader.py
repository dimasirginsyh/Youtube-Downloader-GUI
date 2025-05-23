from yt_dlp import YoutubeDL
from platformdirs import user_downloads_dir
from pathlib import Path
import sys

output_dir = Path(user_downloads_dir())

def download_video(url, progress_callback=None, log_callback=None, cancel_flag=None, browser='chrome'):
    def get_ffmpeg_path():
        if getattr(sys, 'frozen', False):
            return str(Path(sys._MEIPASS) / 'ffmpeg' / 'ffmpeg.exe')
        return str(Path('ffmpeg') / 'ffmpeg.exe')

    def get_plugin_path():
        if getattr(sys, 'frozen', False):
            return str(Path(sys._MEIPASS) / 'plugins')
        return str(Path('plugins'))

    def hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
            downloaded = d.get('downloaded_bytes', 0)
            percentage = downloaded / total_bytes * 100
            if progress_callback:
                progress_callback(percentage)
        if d['status'] == 'finished':
            if log_callback:
                log_callback("📦 File telah disimpan: " + str(output_dir) + "/" + d['filename'])

    if log_callback:
        log_callback("📡 Mengambil info video...")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'cookiesfrombrowser': (browser,),  # ini tetap benar
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),  # gunakan 'outtmpl', bukan '-o'
        'progress_hooks': [hook],
        'ffmpeg_location': get_ffmpeg_path(),  # key benar: 'ffmpeg_location'
        'quiet': True,
        'noprogress': True,
        'allow_plugins': True,  # aktifkan plugin
        'plugin_paths': [get_plugin_path()],  # arahkan ke folder plugin
    }

    with YoutubeDL(ydl_opts) as ydl:
        if cancel_flag and cancel_flag():
            if log_callback:
                log_callback("⚠️ Download dibatalkan sebelum mulai.")
            return
        ydl.download([url])
