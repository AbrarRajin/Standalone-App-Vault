import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# 🔧 Default FFmpeg location
DEFAULT_FFMPEG = r"D:\Movies\YTDL\EXE\ffmpeg.exe"

def process_video(mode):
    ffmpeg_path = ffmpeg_entry.get().strip()

    if not os.path.isfile(ffmpeg_path):
        messagebox.showerror("FFmpeg Error", f"ffmpeg.exe not found at:\n{ffmpeg_path}")
        return

    # Ask user to pick a video
    input_path = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[("Video files", "*.mp4;*.mov;*.mkv;*.avi;*.flv;*.wmv")]
    )

    if not input_path:
        return  # user cancelled

    # Decide filter and suffix based on mode
    if mode == "90":
        vf_filter = "transpose=1"
        suffix = "_90cw"
    elif mode == "180":
        vf_filter = "transpose=2,transpose=2"
        suffix = "_180"
    elif mode == "270":
        vf_filter = "transpose=2"
        suffix = "_270"
    elif mode == "flip":
        vf_filter = "hflip"
        suffix = "_flip"
    else:
        messagebox.showerror("Error", "Unknown mode.")
        return

    base, ext = os.path.splitext(input_path)
    output_path = base + suffix + ext

    # FFmpeg command
    cmd = [
        ffmpeg_path,
        "-i", input_path,
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "veryfast",
        "-c:a", "copy",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Done!\nSaved as:\n{output_path}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "FFmpeg failed while processing the video.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

# ---------- GUI ----------
root = tk.Tk()
root.title("FFmpeg Video Rotator")
root.geometry("460x300")

# FFmpeg path label
tk.Label(root, text="FFmpeg Location:", pady=5).pack()

# Editable FFmpeg path field
ffmpeg_entry = tk.Entry(root, width=60)
ffmpeg_entry.insert(0, DEFAULT_FFMPEG)
ffmpeg_entry.pack(pady=5)

# Buttons
tk.Label(root, text="Choose rotation:", pady=10).pack()

tk.Button(root, text="Rotate 90° clockwise", width=35, command=lambda: process_video("90")).pack(pady=5)
tk.Button(root, text="Rotate 180°", width=35, command=lambda: process_video("180")).pack(pady=5)
tk.Button(root, text="Rotate 270° (90° CCW)", width=35, command=lambda: process_video("270")).pack(pady=5)
tk.Button(root, text="Flip horizontally (mirror)", width=35, command=lambda: process_video("flip")).pack(pady=5)

root.mainloop()
