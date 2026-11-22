"""Template. Copy, rename (story_<name>.py), fill in. Run: python story_<name>.py <project folder>
Rules: every line is a caption chunk (1-3 words); the voiceover must say the lines exactly, in order.
Wrap a key word in *asterisks* to highlight it. 1-3 lines per shot. See the engine's references/library.md for every set,
preset, action and effect name."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib'))
from story_lib import Story, project_dir_from_argv

S = Story("Title", "one-line logline")
S.use(hero="narrator_boy")            # ready-made characters; or write your own in S.cast = {...}
S.use("dad", "mom")
S.shot("plaza", ["In this world,", "you get one", "*thing.*"],
       {"hero": {"at": [-1, 0, 6.5], "expr": "smile", "do": [{"do": "walk", "at": 0, "to": [-1, 0, 8.8], "dur": 1.0}]}},
       {"on": "hero", "shot": "full", "move": "push"}, extras={"walkers": 6})
# ... more shots ...
S.save(project_dir_from_argv())
