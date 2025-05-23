from yt_dlp import YoutubeDL
from platformdirs import user_downloads_dir
from pathlib import Path
import sys
import platform
import shutil

output_dir = Path(user_downloads_dir())

def download_video(url, progress_callback=None, log_callback=None, cancel_flag=None, browser='chrome'):
    def get_ffmpeg_path():
        system = platform.system().lower()

        if system == 'windows':
            if getattr(sys, 'frozen', False):
                # saat sudah dibundle pakai PyInstaller
                return str(Path(sys._MEIPASS) / "ffmpeg" / "ffmpeg.exe")
            else:
                return str(Path("ffmpeg") / "ffmpeg.exe")
        else:
            # Untuk Linux & macOS, asumsikan ffmpeg ada di PATH
            ffmpeg_path = shutil.which("ffmpeg")
            if ffmpeg_path:
                return ffmpeg_path
            else:
                raise FileNotFoundError("⚠️ FFmpeg tidak ditemukan di PATH. Silakan install ffmpeg.")

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
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'progress_hooks': [hook],
        'ffmpeg_location': get_ffmpeg_path(),
        'quiet': True,
        'noprogress': True,
        'allow_plugins': True,
        'plugin_paths': [get_plugin_path()],
    }

    try:
        import importlib.metadata
        plugins = importlib.metadata.entry_points().get('yt_dlp_plugins', [])
        if any('chrome_cookie_unlock' in str(p) for p in plugins):
            ydl_opts['cookiesfrombrowser'] = (browser,)
            ydl_opts['--plugin'] = 'extractor:chrome_cookie_unlock'
            if log_callback:
                log_callback("🍪 Mengambil cookie dari browser...")
    except Exception as e:
        if log_callback:
            log_callback(f"⚠️ Tidak bisa ambil cookie browser: {e}")

    with YoutubeDL(ydl_opts) as ydl:
        if cancel_flag and cancel_flag():
            if log_callback:
                log_callback("⚠️ Download dibatalkan sebelum mulai.")
            return
        ydl.download([url])
