# EASIEST WAY: the web app
1. Double-click `start_app.bat` (browser opens at http://127.0.0.1:8765; keep the black window open).
2. First time only: paste the engine folder path (e.g. `I:\blocky-local\blocky-shorts`) and Save.
3. Type a project name, pick the story file (or drop a new story .py I give you), drop the voiceover mp3 and the SRT.
4. Press **Preview sheet**, check it, then **Make video**. Tick "Use GPU" for your RTX 3060. Video appears on the page with a Download button.
Files live in `projects\<name>\` next to the app. The PowerShell steps below still work as a backup.

---
# Blocky story videos: local workflow (no AI model, no internet while rendering)

You write nothing by hand. The split is:

| Who | Does what |
|---|---|
| Claude (chat) | Writes the script, the voiceover text, and the **story file** (`story_<name>.py`) that matches the script word for word |
| You (ai33) | Make the voiceover MP3 and the SRT from the voiceover text |
| Your PC | Builds, checks, renders and encodes the video with one command |

Because the story file only needs the script, Claude can give you the script, the voiceover text and the story file **in the same chat turn**, before any audio exists. Then you never need to come back to Claude for the render.

## One-time setup (Windows)
1. Install Node.js 22 or newer (nodejs.org), Google Chrome, Python 3, and ffmpeg (`winget install ffmpeg`, then reopen the terminal).
2. In a terminal: `pip install numpy`
3. Unzip your **Roblox_Blocky.zip** somewhere, for example `D:\blocky\blocky-shorts` (the folder that contains `SKILL.md` and `scripts`).
4. Unzip this workflow package, for example to `D:\blocky\local`.
5. Check everything: `python D:\blocky\local\setup_check.py` (it installs nothing; it tells you what is missing).

## Every video
1. **In chat:** ask Claude for a script ("write a new In this world script about ..."). You get three things: the script, `voiceover.txt`, and `story_<name>.py`. Save the story file in `D:\blocky\local\stories\`.
2. **ai33:** paste `voiceover.txt` (Eleven v3), generate, download the MP3. Get the SRT of that audio from ai33 (or any tool that gives an SRT).
3. **Make a project folder** and put the two files in an `audio` subfolder, named exactly:
   `D:\blocky\projects\my_video\audio\vo.mp3` and `...\audio\vo.srt`
4. **Preview first** (about 30 seconds):
   `python D:\blocky\local\run_video.py --engine D:\blocky\blocky-shorts --project D:\blocky\projects\my_video --story D:\blocky\local\stories\story_<name>.py --preview-only`
   Open `D:\blocky\projects\my_video\build\preview\sheet.jpg` and look at every shot: faces visible, nobody hidden, nothing too dark.
5. **Render** (same command without `--preview-only`; add `--gpu` to use your graphics card, and `--fresh` if you changed anything since the last render):
   `python D:\blocky\local\run_video.py --engine D:\blocky\blocky-shorts --project D:\blocky\projects\my_video --story D:\blocky\local\stories\story_<name>.py --fresh --gpu`
6. The video is saved at `D:\blocky\projects\my_video\out\video.mp4`. The runner prints `DONE: <path>` when it finishes.

## If something looks wrong
- Tell Claude the **time stamp or shot number** and what is wrong ("0:41 Mom is too dark", "shot 12 cut off"). Claude gives you a corrected story file; run it again with `--fresh`.
- Captions slightly early or late: they come from the SRT, spread across each cue's words, so single words can be 0.1 to 0.2 seconds off. A better SRT (word-level) fixes it.
- `Alignment failed`: the voiceover must say exactly the words in the story file (no extra words, no tags read aloud). Regenerate that line or change the story file text to match.
- `Preview failed` or black frames: set `CHROME_PATH` to your chrome.exe, or run without `--gpu`.
- Render slow: add `--gpu`, or `--workers 4` if your CPU has many cores.

## Files in this package
- `run_video.py` the one command pipeline (align, check, preview, render, mix, encode)
- `setup_check.py` checks requirements
- `lib/story_lib.py` small helper used by story files
- `lib/cast_library.py` ready-made characters for any story
- `templates/story_template.py` empty story to copy
- `STORY_FILE_GUIDE.md` the rules for writing a story file (paste to Claude in any new chat)
- `examples/one_lie/` the finished example (story file, voiceover text, SRT)

## What this cannot do
Characters are the engine's blocky presets, recoloured. There is no snow, kitchen or hospital corridor; substitutes are listed in the engine's `references/library.md`. No background music is included: add platform music when you upload.

---

## Engine patches (blocky-shorts/scripts/render.mjs)
The bundled `blocky-shorts/scripts/render.mjs` has two changes from the original skill:
1. Windows fix: the engine folder is found with `fileURLToPath(import.meta.url)` instead of `new URL(import.meta.url).pathname`, which breaks on Windows.
2. `--scale` option for `frames`, used by the app's quality setting (1.0 = 720p, 1.5 = 1080p).
If you use a fresh copy of the engine, re-apply both.
