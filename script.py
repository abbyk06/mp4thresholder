import tkinter as tk
from tkinter import filedialog
import cv2

THRESHOLD = 128

while True:
    raw = input("Enter a threshold (0–255): ").strip()
    if raw.isdigit() and 0 <= int(raw) <= 255:
        THRESHOLD = int(raw)
        break
    print("Invalid input. Please enter a whole number between 0 and 255.")

#file picker dialog
print("Select a video file")
root = tk.Tk()
root.withdraw()
INPUT = filedialog.askopenfilename(
    title="Select a video file",
    filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
)

if not INPUT:
    print("No file selected.")
    exit()

OUTPUT = INPUT.replace(".mp4", "_bw.mp4")

cap = cv2.VideoCapture(INPUT)
fps    = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(OUTPUT, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height), isColor=False)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, THRESHOLD, 255, cv2.THRESH_BINARY)
    out.write(bw)

cap.release()
out.release()
print(f"Done! Saved to: {OUTPUT}")