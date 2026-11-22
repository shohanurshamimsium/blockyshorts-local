#!/usr/bin/env python3
"""Blocky Video Maker - local web app. Run: python app.py  then open http://127.0.0.1:8765
Uses only the Python standard library. Drives run_video.py as a background job."""
import json, os, re, shutil, subprocess, sys, threading, time, glob, mimetypes, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECTS = os.path.join(HERE, "projects")
STORIES = os.path.join(HERE, "stories")
OUTPUTS = os.path.join(HERE, "outputs")
CONFIG = os.path.join(HERE, "app_config.json")
PORT = int(os.environ.get("BLOCKY_PORT", "8765"))
os.makedirs(PROJECTS, exist_ok=True); os.makedirs(STORIES, exist_ok=True); os.makedirs(OUTPUTS, exist_ok=True)

def load_cfg():
    try: return json.load(open(CONFIG, encoding="utf-8"))
    except Exception: return {}
def save_cfg(c): json.dump(c, open(CONFIG, "w", encoding="utf-8"), indent=1)

def guess_engine():
    for c in [load_cfg().get("engine"), os.path.join(HERE, "blocky-shorts"), os.path.join(HERE, "..", "blocky-shorts")]:
        if c and os.path.isfile(os.path.join(c, "scripts", "bs.py")): return os.path.abspath(c)
    return load_cfg().get("engine") or os.path.join(HERE, "blocky-shorts")
def engine_ok(e): return os.path.isfile(os.path.join(e, "scripts", "bs.py")) if e else False

def safe(name):
    n = re.sub(r"[^A-Za-z0-9_\-]", "_", (name or "").strip())[:60]
    return n or "my_video"

def list_stories():
    out = []
    for p in sorted(glob.glob(os.path.join(STORIES, "*.py"))): out.append({"label": "stories/" + os.path.basename(p), "path": p})
    for p in sorted(glob.glob(os.path.join(HERE, "examples", "*", "story_*.py"))):
        out.append({"label": "example: " + os.path.relpath(p, HERE).replace("\\", "/"), "path": p})
    t = os.path.join(HERE, "templates", "story_template.py")
    if os.path.isfile(t): out.append({"label": "template (blank starter)", "path": t})
    return out

def videos_for(name):
    vs = []
    for p in glob.glob(os.path.join(OUTPUTS, name + "_*.mp4")) + glob.glob(os.path.join(OUTPUTS, name + ".mp4")):
        vs.append({"name": os.path.basename(p), "url": "/out/" + os.path.basename(p), "mtime": os.path.getmtime(p), "mb": round(os.path.getsize(p) / 1e6, 1)})
    return sorted(vs, key=lambda v: -v["mtime"])

def project_info(name):
    d = os.path.join(PROJECTS, name)
    audio = [f for f in glob.glob(os.path.join(d, "audio", "vo.*")) if not f.endswith(".srt")]
    return {"name": name, "audio": bool(audio), "srt": os.path.isfile(os.path.join(d, "audio", "vo.srt")),
            "preview": os.path.isfile(os.path.join(d, "build", "preview", "sheet.jpg")),
            "videos": videos_for(name)}

def list_projects():
    return [project_info(n) for n in sorted(os.listdir(PROJECTS)) if os.path.isdir(os.path.join(PROJECTS, n))]

JOB = {"running": False, "project": None, "mode": None, "log": [], "progress": None, "status": "idle", "started": 0, "proc": None, "pct": 0, "nxt": 0, "label": "", "stage_t": 0, "result": None}
LOCK = threading.Lock()

def run_job(project, story, mode, gpu, fresh, quality):
    eng = guess_engine()
    cmd = [sys.executable, "-u", os.path.join(HERE, "run_video.py"), "--engine", eng,
           "--project", os.path.join(PROJECTS, project), "--story", story]
    if mode == "preview": cmd.append("--preview-only")
    if gpu: cmd.append("--gpu")
    if fresh: cmd.append("--fresh")
    cmd += ["--quality", quality]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        p = subprocess.Popen(cmd, cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                             encoding="utf-8", errors="replace", env=env)
        JOB["proc"] = p
        for line in p.stdout:
            line = line.rstrip()
            with LOCK:
                if line.startswith("PROGRESS "): JOB["progress"] = line[9:]
                elif line.startswith("PCT "):
                    try:
                        a, b, lab = line[4:].split("|", 2)
                        JOB.update(pct=int(a), nxt=int(b), label=lab, stage_t=time.time())
                    except ValueError: pass
                else:
                    JOB["log"].append(line)
                    if len(JOB["log"]) > 400: JOB["log"] = JOB["log"][-300:]
        rc = p.wait()
        JOB["status"] = "done" if rc == 0 else ("stopped" if rc < 0 else "failed")
        if rc == 0 and mode == "video":
            src = os.path.join(PROJECTS, project, "out", "video.mp4")
            if os.path.isfile(src):
                dst = os.path.join(OUTPUTS, "%s_%s.mp4" % (project, quality))
                shutil.copy2(src, dst); JOB["result"] = dst
                JOB["log"].append("Saved: " + dst)
        if rc == 0: JOB["pct"] = 100; JOB["nxt"] = 100
    except Exception as e:
        JOB["log"].append("ERROR: %s" % e); JOB["status"] = "failed"
    finally:
        JOB["running"] = False; JOB["proc"] = None

def start_job(project, story, mode, gpu, fresh, quality):
    with LOCK:
        if JOB["running"]: return False, "A job is already running."
        JOB.update(running=True, project=project, mode=mode, log=[], progress=None, status="running", started=time.time(), pct=0, nxt=3, label="Starting", stage_t=time.time(), result=None)
    threading.Thread(target=run_job, args=(project, story, mode, gpu, fresh, quality), daemon=True).start()
    return True, "started"

def state():
    e = guess_engine()
    with LOCK:
        job = {k: JOB[k] for k in ("running", "project", "mode", "progress", "status", "started", "pct", "nxt", "label", "stage_t", "result")}
        job["log"] = JOB["log"][-80:]
    return {"outputs": OUTPUTS, "engine": e, "engine_ok": engine_ok(e), "stories": list_stories(), "projects": list_projects(), "job": job}

PAGE = open(os.path.join(HERE, "app_page.html"), encoding="utf-8").read() if os.path.isfile(os.path.join(HERE, "app_page.html")) else "<h1>app_page.html missing</h1>"

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _json(self, obj, code=200):
        b = json.dumps(obj).encode(); self.send_response(code)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            b = open(os.path.join(HERE, "app_page.html"), "rb").read()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        elif u.path == "/api/state": self._json(state())
        elif u.path.startswith("/file/"): self.serve_file(unquote(u.path[6:]), parse_qs(u.query))
        elif u.path.startswith("/out/"): self.serve_file(unquote(u.path[5:]), parse_qs(u.query), OUTPUTS)
        else: self._json({"error": "not found"}, 404)
    def serve_file(self, rel, q, base=None):
        base = base or PROJECTS
        full = os.path.abspath(os.path.join(base, rel))
        if not full.startswith(base + os.sep) or not os.path.isfile(full): return self._json({"error": "not found"}, 404)
        size = os.path.getsize(full); ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        start, end, code = 0, size - 1, 200
        rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):
            a, _, b = rng[6:].partition("-")
            try:
                start = int(a) if a else 0; end = int(b) if b else size - 1; code = 206
            except ValueError: pass
        end = min(end, size - 1)
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        if code == 206: self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        if q.get("dl"): self.send_header("Content-Disposition", 'attachment; filename="%s"' % os.path.basename(full))
        self.send_header("Cache-Control", "no-store"); self.end_headers()
        try:
            with open(full, "rb") as f:
                f.seek(start); left = end - start + 1
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk: break
                    self.wfile.write(chunk); left -= len(chunk)
        except (BrokenPipeError, ConnectionResetError): pass
    def body(self):
        n = int(self.headers.get("Content-Length", 0)); return self.rfile.read(n) if n else b""
    def do_PUT(self):
        u = urlparse(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path != "/api/upload": return self._json({"error": "not found"}, 404)
        proj, kind, name = safe(q.get("project")), q.get("kind"), os.path.basename(q.get("name", "file"))
        data = self.body()
        if kind == "audio":
            ext = os.path.splitext(name)[1].lower()
            if ext not in (".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"): return self._json({"error": "audio must be mp3/wav/m4a/ogg/flac"}, 400)
            d = os.path.join(PROJECTS, proj, "audio"); os.makedirs(d, exist_ok=True)
            for old in glob.glob(os.path.join(d, "vo.*")):
                if not old.endswith(".srt"): os.remove(old)
            open(os.path.join(d, "vo" + ext), "wb").write(data)
        elif kind == "srt":
            d = os.path.join(PROJECTS, proj, "audio"); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "vo.srt"), "wb").write(data)
        elif kind == "story":
            if not name.lower().endswith(".py"): return self._json({"error": "story file must be .py"}, 400)
            open(os.path.join(STORIES, safe(os.path.splitext(name)[0]) + ".py"), "wb").write(data)
        else: return self._json({"error": "bad kind"}, 400)
        self._json({"ok": True, "project": proj, "info": project_info(proj)})
    def do_POST(self):
        u = urlparse(self.path)
        try: d = json.loads(self.body() or b"{}")
        except Exception: d = {}
        if u.path == "/api/config":
            e = (d.get("engine") or "").strip().strip('"')
            if not engine_ok(e): return self._json({"error": "That folder has no scripts/bs.py - pick the blocky-shorts folder."}, 400)
            c = load_cfg(); c["engine"] = e; save_cfg(c); self._json({"ok": True})
        elif u.path == "/api/run":
            proj = safe(d.get("project")); info = project_info(proj)
            if not engine_ok(guess_engine()): return self._json({"error": "Engine folder not set."}, 400)
            if not info["audio"] or not info["srt"]: return self._json({"error": "Upload both the audio and the SRT first."}, 400)
            story = d.get("story")
            if not story or not os.path.isfile(story): return self._json({"error": "Pick a story file."}, 400)
            q = d.get("quality") if d.get("quality") in ("draft", "standard", "max") else "standard"
            ok, msg = start_job(proj, story, d.get("mode", "preview"), bool(d.get("gpu")), bool(d.get("fresh")), q)
            self._json({"ok": ok, "message": msg}, 200 if ok else 409)
        elif u.path == "/api/open":
            try:
                if os.name == "nt": os.startfile(OUTPUTS)
                elif sys.platform == "darwin": subprocess.Popen(["open", OUTPUTS])
                else: subprocess.Popen(["xdg-open", OUTPUTS])
            except Exception: pass
            self._json({"ok": True})
        elif u.path == "/api/stop":
            p = JOB.get("proc")
            if p:
                try: p.terminate()
                except Exception: pass
            self._json({"ok": True})
        else: self._json({"error": "not found"}, 404)

if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = "http://127.0.0.1:%d" % PORT
    print("Blocky Video Maker running at " + url + "  (close this window to stop)")
    print("Finished videos are saved in: " + OUTPUTS)
    if "--no-browser" not in sys.argv:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
