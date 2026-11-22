#!/usr/bin/env python3
"""Checks what the blocky-shorts pipeline needs. Installs nothing."""
import os, shutil, subprocess, sys
ok = True
def good(m): print("  OK  ", m)
def bad(m, tip):
    global ok; ok = False; print("  MISSING", m, "->", tip)
print("Blocky local workflow: setup check")
print("  Python", sys.version.split()[0]); 
try:
    import numpy; good("numpy " + numpy.__version__)
except Exception: bad("numpy", "run: pip install numpy")
n = shutil.which("node")
if n:
    v = subprocess.run([n, "-v"], capture_output=True, text=True).stdout.strip(); major = int(v.lstrip("v").split(".")[0])
    good("node " + v) if major >= 22 else bad("node " + v + " (need 22 or newer)", "install Node.js 22+ from nodejs.org")
else: bad("node", "install Node.js 22+ from nodejs.org")
for t in ("ffmpeg", "ffprobe"):
    good(t) if shutil.which(t) else bad(t, "install ffmpeg and add it to PATH (Windows: winget install ffmpeg)")
cands = [os.environ.get("CHROME_PATH"), shutil.which("google-chrome"), shutil.which("chrome"), shutil.which("chromium"),
 r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
 os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium"]
c = next((p for p in cands if p and os.path.exists(p)), None)
good("Chrome: " + c) if c else bad("Google Chrome", "install Chrome, or set CHROME_PATH to its chrome.exe")
print("\nReady." if ok else "\nFix the MISSING items above, then run this again.")
sys.exit(0 if ok else 1)
