import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import os

def prompt_hex(label):
    while True:
        raw = input(f"{label} hex color (e.g. #121212 or 121212): ").strip().lstrip("#")
        if len(raw) == 6 and all(c in "0123456789abcdefABCDEF" for c in raw):
            r = int(raw[0:2], 16)
            g = int(raw[2:4], 16)
            b = int(raw[4:6], 16)
            return (r, g, b, 255)
        if len(raw) == 8 and all(c in "0123456789abcdefABCDEF" for c in raw):
            r = int(raw[0:2], 16)
            g = int(raw[2:4], 16)
            b = int(raw[4:6], 16)
            a = int(raw[6:8], 16)
            return (r, g, b, a)
        print("Invalid input. Enter a 6-digit hex code (e.g. #121212) or 8-digit with alpha (e.g. #121212FF).")

while True:
    raw = input("Enter a threshold (0–255): ").strip()
    if raw.isdigit() and 0 <= int(raw) <= 255:
        THRESHOLD = int(raw)
        break
    print("Invalid input. Please enter a whole number between 0 and 255.")

while True:
    raw = input("Invert colors? (y/n): ").strip().lower()
    if raw in ("y", "n"):
        INVERT = raw == "y"
        break
    print("Invalid input. Please enter y or n.")

while True:
    raw = input("Custom black/white colors? (y/n): ").strip().lower()
    if raw in ("y", "n"):
        CUSTOM_COLORS = raw == "y"
        break
    print("Invalid input. Please enter y or n.")

if CUSTOM_COLORS:
    COLOR_BLACK = prompt_hex("'Black' color")
    COLOR_WHITE = prompt_hex("'White' color")
else:
    COLOR_BLACK = (0, 0, 0, 255)
    COLOR_WHITE = (255, 255, 255, 255)

while True:
    raw = input("Save last frame as PNG? (y/n): ").strip().lower()
    if raw in ("y", "n"):
        SAVE_PNG = raw == "y"
        break
    print("Invalid input. Please enter y or n.")

print("Select a video file")
root = tk.Tk()
root.withdraw()
root.lift()
root.attributes('-topmost', True)
root.update()
INPUT = filedialog.askopenfilename(
    title="Select a video file",
    filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
)

if not INPUT:
    print("No file selected.")
    exit()

name = input("Enter output file name (without extension): ").strip()
if not name:
    name = "output"
OUTPUT     = os.path.join(os.path.dirname(INPUT), f"{name}.mp4")
OUTPUT_PNG = os.path.join(os.path.dirname(INPUT), f"{name}.png")

cap    = cv2.VideoCapture(INPUT)
fps    = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

IS_COLOR = CUSTOM_COLORS
out = cv2.VideoWriter(OUTPUT, cv2.VideoWriter_fourcc(*"avc1"), fps, (width, height), isColor=IS_COLOR)

last_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, THRESHOLD, 255, cv2.THRESH_BINARY)
    if INVERT:
        bw = cv2.bitwise_not(bw)

    if CUSTOM_COLORS:
        colored = np.zeros((height, width, 3), dtype=np.uint8)
        colored[bw == 0]   = (COLOR_BLACK[2], COLOR_BLACK[1], COLOR_BLACK[0])
        colored[bw == 255] = (COLOR_WHITE[2], COLOR_WHITE[1], COLOR_WHITE[0])
        out.write(colored)
        last_frame = colored
    else:
        out.write(bw)
        last_frame = bw

cap.release()
out.release()
print(f"Done! Saved to: {OUTPUT}")

if SAVE_PNG and last_frame is not None:
    cv2.imwrite(OUTPUT_PNG, last_frame)
    print(f"Last frame saved to: {OUTPUT_PNG}")