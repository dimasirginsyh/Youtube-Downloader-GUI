from yt_dlp import YoutubeDL
from platformdirs import user_downloads_dir
from pathlib import Path

output_dir = Path(user_downloads_dir())

def download_video(url, progress_callback=None, log_callback=None, cancel_flag=None, browser='chrome'):
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
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]',
        'cookiesfrombrowser': (browser,),
        '-o': str(output_dir / '%(title)s.%(ext)s'),
        'progress_hooks': [hook],
        'quiet': True,
        'noprogress': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        if cancel_flag and cancel_flag():
            if log_callback:
                log_callback("⚠️ Download dibatalkan sebelum mulai.")
            return
        ydl.download([url])
