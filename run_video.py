#!/usr/bin/env python3
"""One-command local pipeline for the blocky-shorts engine (no AI model, no internet needed).

  python run_video.py --engine <path to blocky-shorts folder> --project <project folder> \
                      [--story story_x.py] [--preview-only] [--fresh] [--gpu] [--workers 2]

Project folder must contain  audio/vo.mp3  (your voiceover)  and  audio/vo.srt  (its subtitles).
Steps: build story.json (if --story) -> align audio -> validate -> preview sheet -> render frames -> mix -> encode.
Always run once with --preview-only first, look at build/preview/sheet.jpg, then run again without it.
"""
import argparse, os, shutil, subprocess, sys, glob

import re
QUALITY = {  # scale on the 720x1280 base, x264 crf, x264 preset
    "draft":    (1.0, 20, "veryfast"),
    "standard": (1.5, 16, "medium"),
    "max":      (1.5, 14, "slow"),
}
def pct(p, nxt, label):
    print("PCT %d|%d|%s" % (p, nxt, label), flush=True)

def run(cmd, cwd, stream=True, progress=False, frames_cb=None):
    print("\n$ " + " ".join(cmd), flush=True)
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    lines = []
    for line in p.stdout:
        lines.append(line)
        if progress and re.match(r"^\s*\d+/\d+", line):
            print("PROGRESS " + line.strip(), flush=True)
            if frames_cb: frames_cb(line)
        elif stream and (len(lines) < 60 or not line.startswith("  ")): print(line.rstrip(), flush=True)
    p.wait()
    return p.returncode, "".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default=os.environ.get("BLOCKY_ENGINE"), help="folder named blocky-shorts (unzipped skill)")
    ap.add_argument("--project", required=True)
    ap.add_argument("--story", help="python story file that writes story.json into the project")
    ap.add_argument("--auto", action="store_true", help="build the scenes automatically from the SRT (no story file)")
    ap.add_argument("--narrator", choices=["boy", "girl"], default="boy", help="narrator look for --auto")
    ap.add_argument("--preview-only", action="store_true")
    ap.add_argument("--fresh", action="store_true", help="delete old frames (use after any change to lines or timing)")
    ap.add_argument("--gpu", action="store_true"); ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--budget", type=int, default=500); ap.add_argument("--out")
    ap.add_argument("--quality", choices=list(QUALITY), default="standard", help="draft=720p fast, standard=1080p, max=1080p best encode")
    a = ap.parse_args()
    if not a.engine or not os.path.isfile(os.path.join(a.engine, "scripts", "bs.py")):
        sys.exit("--engine must point to the unzipped blocky-shorts folder (it contains scripts/bs.py)")
    eng, proj = os.path.abspath(a.engine), os.path.abspath(a.project)
    py = sys.executable
    scale, crf, preset = QUALITY[a.quality]
    pct(1, 4, "Building story")
    if not os.path.isdir(proj):
        run([py, "scripts/bs.py", "init", proj], eng)
    os.makedirs(os.path.join(proj, "audio"), exist_ok=True)
    vo = [f for f in glob.glob(os.path.join(proj, "audio", "vo.*")) if f.lower().endswith((".mp3", ".wav", ".m4a"))]
    srt = os.path.join(proj, "audio", "vo.srt")
    if not vo: sys.exit(f"Put your voiceover at {os.path.join(proj,'audio','vo.mp3')} first.")
    if a.auto:
        if not os.path.isfile(srt): sys.exit("Auto mode needs the SRT (audio/vo.srt).")
        here = os.path.dirname(os.path.abspath(__file__))
        rc, _ = run([py, os.path.join(here, "lib", "auto_story.py"), proj, "--srt", srt, "--narrator", a.narrator], eng)
        if rc: sys.exit("Auto story builder failed (see message above).")
    elif a.story:
        rc, _ = run([py, os.path.abspath(a.story), proj], eng)
        if rc: sys.exit("Story file failed (see message above).")
    if not os.path.isfile(os.path.join(proj, "story.json")): sys.exit("No story.json: pass --story or put one in the project folder.")
    if a.fresh: shutil.rmtree(os.path.join(proj, "build", "frames"), ignore_errors=True)
    # 1 align
    pct(5, 9, "Aligning voiceover to captions")
    cmd = [py, "scripts/bs.py", "align", proj] + (["--srt", srt] if os.path.isfile(srt) else [])
    if not os.path.isfile(srt): print("No audio/vo.srt found: using slower, less exact pause-based alignment.")
    rc, out = run(cmd, eng, stream=False)
    print("\n".join(out.splitlines()[-6:]))
    if rc: sys.exit("Alignment failed. The voiceover must say exactly the words in story.json lines.")
    # 2 check
    pct(10, 30, "Checking story (starting the hidden Chrome)")
    rc, out = run(["node", "scripts/render.mjs", "check", proj], eng, stream=False)
    print("\n".join(out.splitlines()[-4:]))
    if rc or "No warnings" not in out: sys.exit("Fix the warnings above in your story file, then run again.")
    # 3 preview (skipped when making the video if a sheet already exists)
    sheet = os.path.join(proj, "build", "preview", "sheet.jpg")
    if a.preview_only or not os.path.isfile(sheet):
        pct(32, 97, "Making preview sheet")
        rc, out = run(["node", "scripts/render.mjs", "preview", proj], eng, stream=False)
        print(out.strip().splitlines()[-1] if out.strip() else "")
        if rc: sys.exit("Preview failed: see message above (is Chrome installed? set CHROME_PATH).")
        print("\nOpen this and look at it:", sheet)
    if a.preview_only: pct(100, 100, "Preview ready"); print("Preview only. Run again without --preview-only to render the video."); return
    # frames from another quality have another size: start clean
    import hashlib
    h = hashlib.md5(str(scale).encode())
    for f in (os.path.join(proj, "story.json"), os.path.join(proj, "build", "timing.json")):
        if os.path.isfile(f): h.update(open(f, "rb").read())
    sig = h.hexdigest()
    marker = os.path.join(proj, "build", "frames_sig.txt"); os.makedirs(os.path.dirname(marker), exist_ok=True)
    old = open(marker).read().strip() if os.path.isfile(marker) else None
    if old != sig:
        if old is not None: print("Story, audio timing or quality changed: re-rendering all frames.", flush=True)
        shutil.rmtree(os.path.join(proj, "build", "frames"), ignore_errors=True)
    open(marker, "w").write(sig)
    pct(15, 15, "Rendering frames")
    def fcb(line):
        m = re.match(r"^\s*(\d+)/(\d+)\s+(\d+)s elapsed, ~(\d+)s left", line)
        if m:
            n, t, left = int(m.group(1)), int(m.group(2)), int(m.group(4))
            pct(15 + int(75 * n / max(t, 1)), 15 + int(75 * (n + 30) / max(t, 1)), "Rendering frames %d/%d  (about %d:%02d left)" % (n, t, left // 60, left % 60))
    # 4 frames (resumable; repeat until DONE)
    for i in range(200):
        cmd = ["node", "scripts/render.mjs", "frames", proj, "--budget", str(a.budget), "--workers", str(a.workers)] + (["--gpu"] if a.gpu else []) + ["--scale", str(scale)]
        rc, out = run(cmd, eng, stream=False, progress=True, frames_cb=fcb)
        print("\n".join(out.splitlines()[-2:]))
        if rc: sys.exit("Frame rendering failed: see message above.")
        if "DONE" in out: break
    else: sys.exit("Rendering did not finish.")
    # 5 mix + encode
    pct(91, 93, "Mixing audio")
    rc, out = run([py, "scripts/bs.py", "mix", proj], eng, stream=False); print("\n".join(out.splitlines()[-3:]))
    if rc: sys.exit("Mix failed.")
    final = os.path.abspath(a.out) if a.out else os.path.join(proj, "out", "video.mp4")
    os.makedirs(os.path.dirname(final), exist_ok=True)
    pct(94, 99, "Encoding video (%s quality)" % a.quality)
    rc, out = run([py, "scripts/bs.py", "encode", proj, "--out", final, "--crf", str(crf), "--preset", preset], eng, stream=False); print("\n".join(out.splitlines()[-2:]))
    if rc or not os.path.isfile(final): sys.exit("Encode failed.")
    pct(100, 100, "Done")
    print("\nDONE:", final)

if __name__ == "__main__": main()
