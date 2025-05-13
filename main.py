import tkinter as tk
from tkinter import ttk, messagebox
from downloader import download_video
import threading

is_downloading = False
download_thread = None

def start_download():
    global is_downloading, download_thread
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Masukkan URL YouTube!")
        return

    # Reset UI
    log_text.delete(1.0, tk.END)
    progress_var.set(0)
    is_downloading = True
    button_download.config(text="Cancel", command=cancel_download)

    # Jalankan di thread agar UI tidak freeze
    selected_browser = browser_var.get()
    download_thread = threading.Thread(target=run_download, args=(url, selected_browser), daemon=True)
    download_thread.start()

def run_download(url, browser):
    global is_downloading

    def update_progress(pct):
        progress_var.set(pct)

    def log(msg):
        log_text.insert(tk.END, f"{msg}\n")
        log_text.see(tk.END)  # Scroll otomatis

    try:
        download_video(url, progress_callback=update_progress, log_callback=log, cancel_flag=lambda: not is_downloading, browser=browser)
        log("✅ Download selesai!")
        progress_var.set(0)
        messagebox.showinfo("Selesai", "Download selesai!")
    except Exception as e:
        log(f"❌ Error: {str(e)}")

    is_downloading = False
    button_download.config(text="Download", command=start_download)

def cancel_download():
    global is_downloading
    is_downloading = False
    progress_var.set(0)
    log_text.insert(tk.END, "⛔ Download dibatalkan oleh pengguna.\n")
    button_download.config(text="Download", command=start_download)

# GUI
root = tk.Tk()
root.title("YouTube Downloader")

tk.Label(root, text="Masukkan URL YouTube").pack(pady=10)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

browser_var = tk.StringVar(value='chrome')
tk.Label(root, text="Pilih Browser untuk Cookie").pack()
browser_dropdown = ttk.Combobox(root, textvariable=browser_var, state="readonly")
browser_dropdown['values'] = ('chrome', 'firefox')
browser_dropdown.pack(pady=5)

button_download = tk.Button(root, text="Download", command=start_download)
button_download.pack(pady=10)

progress_var = tk.DoubleVar()
progress = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
progress.pack(pady=5)

# Section log
log_text = tk.Text(root, height=10, width=60)
log_text.pack(pady=10)

root.mainloop()
