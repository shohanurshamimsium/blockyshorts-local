# blockyshorts-local

Offline web app that turns a **voiceover (mp3) + subtitles (SRT)** into a finished blocky 3D "In this world..." story short (9:16, up to 1080x1920) on your own PC. No AI model, no cloud, no per-video cost.

You give it three things: a voiceover, its SRT, and a *story file* (a small Python file describing the scenes, characters, camera and captions for that script). The app aligns the captions to the audio, renders every frame in headless Chrome (Three.js), and encodes the video with ffmpeg. Quality presets: Draft (720p), Standard (1080p), Max (1080p, best encode).

**Requirements (Windows):** Python 3.10+ (with `numpy`), Node.js 22+, ffmpeg, Google Chrome. A GPU is optional but makes rendering much faster. Run `install_windows.bat` to install them with winget, then `python setup_check.py` to verify.

**Engine credit:** the `blocky-shorts/` folder is the blocky-shorts renderer taken from the "Roblox Blocky" skill package, with two small patches (see the last section). The rest of this repo (web app, pipeline, story library, cast library) is the local workflow around it.

**Layout:** `start_app.bat` (launch), `app.py` + `app_page.html` (web app), `run_video.py` (pipeline), `lib/` (story + cast library), `examples/` (a working example), `templates/` (blank story starter), `stories/` (your story files), `projects/` and `outputs/` (created at run time, git-ignored).

---

## Quick start: the web app
1. Double-click `start_app.bat` (browser opens at http://127.0.0.1:8765; keep the black window open).
2. The app finds the `blocky-shorts` engine folder next to it automatically. If it asks, paste the full path of that folder and press Save.
3. Type a project name, pick the story file (or drop in a new story .py), drop the voiceover mp3 and the SRT.
4. Press **Preview sheet**, check it, then **Make video**. Tick "Use GPU" if you have one. Video appears on the page with a Download button.
**Two ways to get scenes:**
- **Manual (best quality):** drop a story `.py` file onto the page. It is added to the list and selected.
- **Auto:** choose "Auto: build the scenes from the SRT" in the story list. No story file needed: it picks sets, characters, expressions and camera moves from keywords in the SRT (boss/work -> office, mom/dad -> those characters, and so on). Faster but more generic than a hand-written story. You can pick a boy or girl narrator.

Files live in `projects\<name>\` next to the app. The PowerShell steps below still work as a backup.

---
## Workflow details: Blocky story videos, local workflow (no AI model, no internet while rendering)

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


---

## Master prompt: have any AI write the story file

The app needs one **story file** (`story_<name>.py`) per video, unless you use Auto mode. Any AI (Claude, ChatGPT, Gemini...) can write it if you paste the prompt below, followed by your script. Save its answer as `story_<name>.py` and drop it onto the app page.

**How to use:** copy everything inside the box, paste it into the AI, then add your script (or the voiceover text) after the line `SCRIPT:`. Always run **Preview sheet** first and send the AI any warnings the app shows, so it can fix them.

````text
You are writing ONE Python "story file" for blockyshorts-local, a tool that renders Roblox-style blocky 3D animated vertical shorts (9:16) from a voiceover. The voiceover audio and its SRT are made separately; your file only describes the scenes. Reply with ONE Python code block (the complete file) and nothing else.

FILE SKELETON (keep exactly; works from the stories/ folder):
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for up in ("..", os.path.join("..", "..")):
    p = os.path.join(HERE, up, "lib")
    if os.path.isdir(p): sys.path.insert(0, p); break
from story_lib import Story, project_dir_from_argv

S = Story("Title", "one-line logline")
S.use(narrator="narrator_boy")        # ready-made look, renamed to the key "narrator"
S.use("dad", "mom")                   # library characters keep their own names
S.cast["boss"] = {"preset": "boss"}   # or define a brand-new character
S.shot("plaza", ["In this world,", "you get one", "*lie.*"],
       {"narrator": {"at": [-1, 0, 6.5], "expr": "smile",
                     "do": [{"do": "walk", "at": 0, "to": [-1, 0, 8.8], "dur": 1.0}]}},
       {"on": "narrator", "shot": "full", "move": "push"}, extras={"walkers": 6})
S.shot("office", ["My boss", "believed it."], {"boss": {"spot": "center", "expr": "proud"}},
       {"on": "boss", "shot": "medium", "angle": "low", "move": "push"}, fx=[{"punch": 0.15, "at": "believed"}])
S.save(project_dir_from_argv())

S.shot(set, lines, cast, camera, mood="day", fx=None, extras=None, props=None, setOpts=None)

THE MOST IMPORTANT RULE: the shots' "lines", read in order, must be EXACTLY the words the narrator says (same words, same order). Each line is one caption chunk of 1-3 words (never more than 4). Drop any [tags] like [pause]. Punctuation stays. Wrap ONE key word per sentence in *asterisks* to highlight it yellow ("*lie.*" or "was *paid.*"). If the script is changed later, the lines must change with it.

PACING: one shot per 1-3 lines, about 1.5-2 seconds each (narration runs about 3.2 words per second, so a 230-word script is about 70 s and about 40 shots). Cut on almost every line or two; never put a whole paragraph in one shot. Vary shot sizes and sets; "push" is the default camera move (use it on most shots). Do not use digits in lines unless the narrator says digits.

STRUCTURE: every shot needs: a set, lines, the characters on screen (cast), and a camera. Cast entries use the shot-level key names you defined in S.cast / S.use (the same name = the same look in every shot). Positions change per shot, so move actors freely between shots.

CHARACTERS
- Ready-made (S.use("dad","mom") or S.use(hero="narrator_boy")): narrator_boy, narrator_girl, dad, mom, grandma, grandpa, boss, teacher, friend_boy, friend_girl, coworker, landlord, cop, doctor, chef, mayor, kid, villain, king, robot.
- Custom: S.cast["name"] = {"preset":"boy","shirt":"#d9622b","shirtDesign":"plain","pants":"#2b4fb8","hair":"short","hairColor":"#5a3a1e"}
  presets: kid girl boy dad mom grandma grandpa teacher mayor boss worker chef doctor dentist cop farmer gamer noob king robot villain
  options: skin, shirt, shirtDesign (plain stripe stripes star heart suit hoodie overalls coat police chef tie skull tank), accent, pants, shoes, sleeves (long short none), bottom (pants shorts skirt), hat (cap cap_back beanie top fedora hard crown chef police cowboy party bunny), hatColor, hair (short spiky bob pony long buns bun afro mohawk bald), hairColor, extras (["glasses"] shades stache blush freckles), beard (color), bowtie, suspenders, backpack, cape, headphones.
- IMPORTANT: for the "boy" preset always set "shirtDesign":"plain" (otherwise a "7" is printed on the shirt).
- Any cast name not defined gets a random consistent look (handy for extras: "s1", "s2").

SETS AND SPOTS (spot names are exact)
plaza: center front left right fountain bench(seat) podium far | street: sidewalk center road left right door crosswalk | living_room: sofa(seat) sofa2(seat) center tv window door | bedroom: bed bedside center window door | classroom: desk1..desk6(seat) teacher board center | office: desk1..desk6(seat) center cooler window | farm: barn field center post fence | clinic: chair(seat,reclined) doctor center door | studio: center left right (setOpts {"color":"#3a7bd5"}).
Or place directly: "at": [x, y, z]. In the plaza the fountain is the origin and the camera side is +z; actors usually stand at z = 6-10.
Not available: snow, kitchen, hospital corridor. Substitutes: street at sunset for winter, bedroom for a hospital room, a night street for a corridor.

CAST ENTRY KEYS: spot or at; face ("front", "back", "left", "right", degrees, or another actor's name); base ("idle","sit","lie"); seat; expr; hold ("phone", "paper", "cup", "cake", or {"type":"gavel","arm":"R"}); hidden (true, then {"do":"appear"}); do (timeline list).
EXPRESSIONS: smile grin happy laugh smirk surprised shock scared sad cry angry furious sleepy asleep yawn strain sus love dead wink nervous blank evil cool disgust proud dizzy cringe talk.
ACTIONS (in "do": {"do": name, "at": time, "dur": seconds}; or {"expr":"shock","at":time}): walk run sneak slide (each with "to": spot or [x,y,z]), turn, sit, stand, lie, appear, vanish, clap, wave, point (dir: up/left/right/forward), cheer, jump, dance, bow, slam, facepalm, shrug, think, salute, flex, hug, kneel, yawn, stretch, tremble, shake, scared, cry, laugh, nod, headshake, look (yaw), talk, type, eat, fall, faint, spin, panic.
TIME REFERENCES ("at"/"until"): a number of seconds from the shot start; a line's text or a partial match ("believed"); "#2" (third line); "start", "mid", "end", "end-0.3"; "believed+0.1".

CAMERA: {"on": actor | [actor, actor] | "crowd" | spot, "shot": extreme|close|medium|cowboy|full|wide|establishing, "angle": eye|low|high|top, "from": front|front-left|front-right|left|right|behind, "move": push|pull|static|zoom-in|zoom-out|crane-up|crane-down|track-left|track-right|orbit-left|orbit-right|handheld}.
Vertical video is narrow: two people side by side need "full" or "wide"; three people need "wide". If a shot looks cramped, go one size wider.
Use "close"/"extreme" on emotional beats and reveals, "wide" for establishing and group shots, "low" angle for authority.

MOOD: "day" (default), "sunset" for flashbacks, evenings, sad or later scenes. Avoid "night": faces become too dark.

FX (in the shot's fx list, each with optional "at"): {"punch":0.15} fast zoom-in for emphasis; {"shake":0.12,"dur":0.28}; {"sparkle":"hero"}; {"glint":"hero"} (great for the last beat); {"bulb":"hero"}; {"icon":"sweat"|"question"|"exclaim"|"heart"|"clock"|"zzz"|"dots"|"anger"|"dollar"|"phone","on":"hero","dur":1.2}; {"stamp":"PAID!"}; {"title":"TEN YEARS LATER","dur":1.2,"style":"banner"}; {"say":"Hello?","on":"hero","dur":1.4}; {"sign":{"text":"NO\nYAWNING","icon":"yawn"},"until":"end"}.
Props (shot level "props": [{"type":"money","at":[x,y,z]}]): bulb phone book paper cup pizza trophy money gavel mic balloon cake alarm laptop sign box ball car chicken rooster dog cat tv table chair podium tree rock sword.
Extras: extras={"walkers":6} (people strolling in plaza/street) or a crowd: {"crowd":{"n":14,"rows":2,"center":[0,0,12],"yaw":180,"spacing":2.6,"expr":"smile"}}.

KNOWN PITFALLS (avoid these)
- A shot with two actors where one stands directly in front of the other hides one. In the office use desk2 + cooler with a "wide" shot; in living_room use sofa + center with "full".
- bedroom: never use the "bed" spot (the actor lies down and the camera ends in pillows). Prop the person up instead: {"at":[-2.5,0,-3.1],"base":"sit","seat":1.95,"face":"front"}; a visitor sits at {"at":[-0.4,0,-1.2],"base":"sit","seat":1.38,"face":"<other actor>"}; use a normal "medium"/"wide" camera from "front" and mood "day" or "sunset".
- "track-left"/"track-right" on a walking actor can leave them out of frame: keep walks short or use a wider shot.
- Signs ("sign" fx) cover the top quarter of the frame: never use one on an extreme close-up.
- Never hide the narrator by accident: every shot's cast must contain whoever the camera is "on".
- Do not invent names. Unknown set, spot, preset, expression, action or prop names are ignored and shown as warnings.

STYLE ("version 1 look", loved by the author): captions of 2-3 words with one yellow highlight per sentence; mostly "push" moves; a hook shot of the narrator in the plaza; emotional beats on close-ups; final shot a close-up with {"glint": narrator}. Keep one fixed narrator look across the whole file.

BEFORE ANSWERING check: (1) lines concatenated equal the script's spoken words exactly; (2) every cast name used in a shot exists in S.cast/S.use (or is an intentional extra); (3) every spot belongs to that set; (4) no shot is longer than about 2.5 seconds of narration; (5) the file ends with S.save(project_dir_from_argv()).

SCRIPT:
(paste the voiceover text here, tags removed)
````

If the app's check shows warnings (for example `time ref "..." not found` or an unknown spot), paste the warning text back to the AI and ask it to fix only those lines.
