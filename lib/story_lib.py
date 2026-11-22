"""Tiny helper for writing a blocky-shorts storyboard (story.json) in Python.

Usage in a story file:
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
    from story_lib import Story
    S = Story("Title", "one-line logline")
    S.cast = {"hero": {"preset": "boy", "shirt": "#d9622b", "shirtDesign": "plain"}}
    S.shot("plaza", ["In this world,", "you get one", "*lie.*"], {"hero": {"spot": "front"}},
           {"on": "hero", "shot": "full", "move": "push"})
    S.save(project_dir)       # writes <project_dir>/story.json
Everything inside a shot follows the engine's references/storyboard.md and references/library.md.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cast_library import CAST_LIBRARY

class Story:
    def __init__(self, title, logline="", fps=30, width=720, height=1280, tail=0.8, style=None):
        self.title, self.logline = title, logline
        self.fps, self.width, self.height, self.tail = fps, width, height, tail
        self.style = style or {"caption": {"size": 50, "y": 0.725}, "clapBursts": False, "saturate": 1.18}
        self.cast, self.shots = {}, []

    def use(self, *names, **renamed):
        """Add ready-made characters: S.use("dad", "mom") or S.use(hero="narrator_boy", pal="friend_girl")."""
        for n in names: self.cast[n] = dict(CAST_LIBRARY[n])
        for n, src in renamed.items(): self.cast[n] = dict(CAST_LIBRARY[src])

    def shot(self, set, lines, cast=None, camera=None, mood="day", fx=None, extras=None, props=None, setOpts=None, **kw):
        s = {"set": set, "mood": mood, "lines": list(lines), "cast": cast or {}, "camera": camera or {}}
        if fx: s["fx"] = fx
        if extras: s["extras"] = extras
        if props: s["props"] = props
        if setOpts: s["setOpts"] = setOpts
        s.update(kw)
        self.shots.append(s)

    def words(self):
        return sum(len(l.replace('*', '').split()) for s in self.shots for l in s["lines"])

    def save(self, project):
        story = {"title": self.title, "logline": self.logline, "fps": self.fps, "width": self.width,
                 "height": self.height, "tail": self.tail, "style": self.style, "cast": self.cast, "shots": self.shots}
        os.makedirs(project, exist_ok=True)
        path = os.path.join(project, "story.json")
        with open(path, "w", encoding="utf-8") as f: json.dump(story, f, indent=1)
        print(f"wrote {path}: {len(self.shots)} shots, {self.words()} words")
        return path

def project_dir_from_argv():
    """Story files are run as: python story_x.py <project_dir>"""
    if len(sys.argv) < 2: sys.exit("usage: python <story file> <project folder>")
    return sys.argv[1]
