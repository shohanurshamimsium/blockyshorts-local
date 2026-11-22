#!/usr/bin/env python3
"""AUTO mode: build a story.json from the voiceover SRT alone (no AI, simple rules).

    python auto_story.py <project folder> [--srt <file>] [--narrator boy|girl] [--seed N]

What it does
- Splits the spoken text into 2-3 word caption chunks and groups them into shots (about 1.5-2 s each).
- Picks the set from keywords (boss/work -> office, school -> classroom, bed/sick -> bedroom, ...).
- Brings in supporting characters when they are mentioned (mom, dad, boss, teacher, doctor, cop, ...).
- Picks expressions from keywords (sad, scared, angry, happy, shock) and varies shot size, side and camera move.
- Highlights one key word per sentence in yellow, adds a title card for "years later", a glint on the last shot.
A hand-written story file will always look better; Auto is the fast, no-effort option.
"""
import os, re, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_lib import Story
from cast_library import CAST_LIBRARY

# ------------------------------------------------------------------ text
def read_srt_text(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read().replace("\r", "")
    out = []
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = [l for l in block.split("\n") if l.strip()]
        lines = [l for l in lines if not re.match(r"^\d+$", l.strip()) and "-->" not in l]
        out.append(" ".join(lines))
    t = " ".join(out)
    t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"\[[^\]]*\]", " ", t); t = re.sub(r"\{[^}]*\}", " ", t)
    return re.sub(r"\s+", " ", t).strip()

END = (".", "?", "!", "…")
SOFT = (",", ";", ":", "—", "-")
def endswith(w, marks): return w.rstrip("\"'”’)").endswith(marks)

def chunk_sentences(text):
    """-> list of sentences, each a list of chunks (strings)."""
    words = text.split(" ")
    sentences, cur = [], []
    for w in words:
        cur.append(w)
        if endswith(w, END): sentences.append(cur); cur = []
    if cur: sentences.append(cur)
    result = []
    for sw in sentences:
        chunks, c = [], []
        for i, w in enumerate(sw):
            c.append(w)
            last = i == len(sw) - 1
            if last or len(c) >= 3 or (endswith(w, SOFT) and len(c) >= 2) or (endswith(w, SOFT) and len(c) == 1 and len(w) <= 6):
                chunks.append(c); c = []
        # no orphan one-word ending chunk when it can join the previous one
        if len(chunks) >= 2 and len(chunks[-1]) == 1 and len(chunks[-2]) <= 2 and not endswith(chunks[-2][-1], SOFT):
            chunks[-2] += chunks.pop()
        result.append([" ".join(c) for c in chunks])
    return result

# ------------------------------------------------------------------ keywords
CHAR_WORDS = {
    "mom": ["mom", "mother", "mama", "mum", "mommy"], "dad": ["dad", "father", "papa", "daddy"],
    "grandma": ["grandma", "grandmother", "nana", "granny", "aunt", "grandmom"], "grandpa": ["grandpa", "grandfather", "grandad", "uncle", "grandpapa"],
    "boss": ["boss", "manager", "supervisor"], "teacher": ["teacher", "professor", "principal"],
    "doctor": ["doctor", "nurse", "dentist", "surgeon"], "cop": ["cop", "police", "officer", "detective"],
    "landlord": ["landlord", "neighbor", "neighbour"], "coworker": ["coworker", "colleague", "intern"],
    "friend": ["friend", "bestie", "buddy", "classmate", "roommate"], "chef": ["chef", "cook", "waiter"],
    "mayor": ["mayor", "president", "senator"], "kid": ["kid", "child", "son", "daughter", "baby", "boy", "girl", "brother", "sister"],
    "king": ["king", "queen", "prince", "princess"], "villain": ["thief", "robber", "villain", "stranger", "liar"],
    "robot": ["robot", "machine", "ai"],
}
SET_WORDS = {
    "office": ["office", "work", "boss", "report", "job", "desk", "meeting", "coworker", "colleague", "manager", "email", "salary", "company", "client", "deadline", "promotion", "fired", "intern"],
    "classroom": ["school", "class", "teacher", "exam", "homework", "student", "lesson", "grade", "test", "professor", "classmate", "university"],
    "bedroom": ["bed", "sleep", "slept", "asleep", "pillow", "dream", "nightmare", "wake", "woke", "sick", "ill", "alarm"],
    "clinic": ["doctor", "hospital", "clinic", "dentist", "nurse", "surgery", "diagnosis", "patient", "medicine"],
    "street": ["street", "road", "car", "drive", "driving", "city", "town", "store", "shop", "bus", "walk", "walked", "neighbor", "neighbour", "rent", "landlord", "door", "knocked", "outside", "traffic", "corner"],
    "farm": ["farm", "barn", "chicken", "rooster", "field", "cow", "animal", "harvest", "village"],
    "living_room": ["home", "house", "couch", "sofa", "tv", "television", "dinner", "family", "living", "kitchen", "table", "evening", "phone", "call", "called", "inside"],
    "plaza": ["park", "square", "crowd", "world", "everyone", "people", "stage", "speech", "festival", "town square", "fountain", "city hall"],
}
SAD = {"died", "dead", "death", "funeral", "cry", "cried", "crying", "tears", "alone", "lonely", "lost", "miss", "missed", "sorry", "goodbye", "hurt", "sick", "gone", "grief", "sad", "broke", "broken", "empty"}
SCARED = {"scared", "afraid", "fear", "terrified", "panic", "nervous", "worried", "trembling", "shaking", "nightmare", "hide", "danger"}
ANGRY = {"angry", "mad", "furious", "yelled", "screamed", "hate", "hated", "fight", "fought", "rage", "shouted", "stole", "lied", "cheated"}
HAPPY = {"happy", "love", "loved", "smile", "smiled", "laugh", "laughed", "won", "best", "proud", "birthday", "free", "finally", "wonderful", "thanks", "thank", "hug", "hugged"}
SHOCK = {"suddenly", "shock", "shocked", "wow", "impossible", "unbelievable", "gasped", "realized", "discovered", "found", "twist", "secret", "truth", "never expected"}
HILITE = ["never", "only", "nobody", "everyone", "forever", "always", "alone", "love", "free", "secret", "truth", "money", "lie", "wish", "last", "first", "except", "one", "call", "home", "wasted", "waste", "dead", "gone", "stay", "sorry", "thank", "mine", "yours", "yours."]
SUNSET = {"night", "midnight", "evening", "dusk", "funeral", "died", "memories", "childhood", "sunset"}  # strong cues only; lasts a few shots
DAY_RESET = {"morning", "today", "now", "tonight?", "sunrise", "noon", "right now"}
TIME_TITLE = re.compile(r"\b((?:\w+[\s-]){0,2}?(?:years?|months?|weeks?|days?|hours?|minutes?)\s+later|the next (?:day|morning|week|year)|next (?:day|morning|week|year))\b", re.I)

def tokens(s): return re.findall(r"[a-z']+", s.lower())
def has(words, vocab): return any(w in vocab for w in words)

def pick_set(text, prev):
    t = " " + " ".join(tokens(text)) + " "
    best, score = None, 0
    for st, kws in SET_WORDS.items():
        sc = sum(1 for k in kws if f" {k} " in t)
        if sc > score: best, score = st, sc
    return best if best and score >= 1 else prev

def mentioned_chars(text):
    t = tokens(text); found = []
    for ch, kws in CHAR_WORDS.items():
        if any(k in t for k in kws): found.append(ch)
    return found

# ------------------------------------------------------------------ layout per set
SOLO = {
    "plaza": {"at": [0, 0, 8.5]}, "street": {"spot": "center"}, "living_room": {"spot": "center"},
    "office": {"spot": "center"}, "classroom": {"spot": "desk3"}, "clinic": {"spot": "chair"},
    "farm": {"spot": "center"}, "studio": {"spot": "center"},
}
# (narrator, other) placements that were checked in earlier previews
DUO = {
    "plaza": ({"at": [-1.6, 0, 8.5]}, {"at": [1.6, 0, 8.5]}),
    "street": ({"spot": "sidewalk"}, {"spot": "door"}),
    "living_room": ({"spot": "sofa"}, {"spot": "center"}),
    "office": ({"spot": "desk2"}, {"spot": "cooler"}),
    "classroom": ({"spot": "desk3"}, {"spot": "teacher"}),
    "clinic": ({"spot": "chair"}, {"spot": "doctor"}),
    "farm": ({"spot": "center"}, {"spot": "barn"}),
    "studio": ({"spot": "left"}, {"spot": "right"}),
}
BED_MAIN = {"at": [-2.5, 0, -3.1], "base": "sit", "seat": 1.95, "face": "front"}
BED_VISITOR = {"at": [-0.4, 0, -1.2], "base": "sit", "seat": 1.38}
SIZES = ["medium", "close", "full", "medium", "medium", "close", "full", "medium"]
SIDES = ["front", "front-left", "front-right", "front", "front-right", "front-left"]

def build(project, srt, narrator="boy", seed=0, title="Auto story"):
    rnd = random.Random(seed)
    text = read_srt_text(srt)
    if not text: sys.exit("The SRT has no text.")
    sentences = chunk_sentences(text)
    # ---- group chunks into shots
    shots, cur, cur_words = [], [], 0
    for si, chunks in enumerate(sentences):
        for ci, ch in enumerate(chunks):
            cur.append((si, ch)); cur_words += len(ch.split())
            sentence_end = ci == len(chunks) - 1
            if len(cur) >= 3 or cur_words >= 7 or (sentence_end and (len(cur) >= 2 or cur_words >= 4)):
                shots.append(cur); cur, cur_words = [], 0
    if cur:
        if shots and len(cur) == 1 and len(shots[-1]) < 3: shots[-1] += cur
        else: shots.append(cur)
    # ---- one highlighted word per sentence
    hl = {}
    for si, chunks in enumerate(sentences):
        flat = [(ci, wi, w) for ci, ch in enumerate(chunks) for wi, w in enumerate(ch.split())]
        choice = None
        for ci, wi, w in flat:
            if re.sub(r"[^a-z']", "", w.lower()) in HILITE: choice = (ci, wi)
        if not choice and flat: choice = (flat[-1][0], flat[-1][1])
        hl[si] = choice
    chunk_pos = {}  # (sentence, chunk text order) -> index to apply
    seen = {}
    def render_line(si, ci_in_sentence, ch):
        c = hl.get(si)
        if c and c[0] == ci_in_sentence:
            ws = ch.split(); i = min(c[1], len(ws) - 1)
            if len(ws) == 1: return "*" + ws[0] + "*"
            ws[i] = "*" + ws[i] + "*"; return " ".join(ws)
        return ch
    # chunk index inside its sentence
    counters = {}
    shot_lines = []
    for sh in shots:
        ls = []
        for si, ch in sh:
            k = counters.get(si, 0); counters[si] = k + 1
            ls.append(render_line(si, k, ch))
        shot_lines.append(ls)

    # ---- story
    S = Story(title, "Auto-built from the SRT")
    nkey = "narrator"
    S.use(**{nkey: "narrator_girl" if narrator == "girl" else "narrator_boy"})
    used = {}
    def cast_key(ch):
        if ch == "friend":
            ch = "friend_girl" if narrator == "boy" else "friend_boy"
        if ch not in used:
            S.use(**{ch: ch}); used[ch] = ch
        return ch

    cur_set, mood, ctx_char, ctx_age, sunset_left = "plaza", "day", None, 99, 0
    n = len(shots)
    for idx, sh in enumerate(shots):
        plain = " ".join(c for _, c in sh)
        tk = tokens(plain)
        # set + mood
        cur_set = pick_set(plain, cur_set)
        if has(tk, SUNSET) or TIME_TITLE.search(plain): sunset_left = 5
        elif has(tk, DAY_RESET): sunset_left = 0
        mood = "sunset" if sunset_left > 0 else "day"
        sunset_left = max(0, sunset_left - 1)
        # characters
        ments = [c for c in mentioned_chars(plain) if c not in ("kid",) or True]
        if ments: ctx_char, ctx_age = ments[0], 0
        else: ctx_age += 1
        other = ctx_char if ctx_char and ctx_age <= 3 else None
        okey = cast_key(other) if other else None
        # expression
        if has(tk, SAD): expr = "sad"
        elif has(tk, SCARED): expr = "scared"
        elif has(tk, ANGRY): expr = "angry"
        elif has(tk, SHOCK) or plain.rstrip().endswith("!"): expr = "shock"
        elif has(tk, HAPPY): expr = "happy"
        elif plain.rstrip().endswith("?"): expr = "surprised"
        else: expr = "talk"
        other_expr = "sad" if expr == "sad" else ("scared" if expr == "scared" else ("angry" if expr == "angry" else "smile"))
        # who is on screen
        duo_turn = okey is not None and idx % 3 == 1
        other_only = okey is not None and not duo_turn and (idx % 2 == 0 or ctx_age == 0)
        size = SIZES[idx % len(SIZES)]
        side = SIDES[idx % len(SIDES)]
        move = "push"
        cast, camera, extras, fx = {}, {}, None, []
        last = idx == n - 1
        if cur_set == "bedroom":
            if okey and not other_only or duo_turn:
                cast[nkey] = dict(BED_VISITOR, face=okey or "front", expr=expr)
                cast[okey] = dict(BED_MAIN, expr=other_expr)
                camera = {"on": [nkey, okey], "shot": "wide", "from": "front", "move": "push"}
            elif okey:
                cast[okey] = dict(BED_MAIN, expr=other_expr)
                camera = {"on": okey, "shot": "medium", "from": "front", "move": "push"}
            else:
                cast[nkey] = dict(BED_MAIN, expr=expr)
                camera = {"on": nkey, "shot": "medium", "from": "front", "move": "push"}
            if mood == "night": mood = "sunset"
        elif duo_turn and okey:
            a, b = DUO.get(cur_set, DUO["plaza"])
            cast[nkey] = dict(a, expr=expr, face=okey); cast[okey] = dict(b, expr=other_expr, face=nkey)
            camera = {"on": [nkey, okey], "shot": "wide" if cur_set in ("office", "classroom", "clinic") else "full", "from": "front", "move": "pull" if idx % 2 else "push"}
        elif other_only and okey:
            a, b = DUO.get(cur_set, DUO["plaza"])
            cast[okey] = dict(b, expr=other_expr if other_expr != "smile" else "blank", do=[{"do": "talk", "at": 0, "until": "end"}])
            camera = {"on": okey, "shot": size if size != "full" else "medium", "from": side, "move": move}
        else:
            cast[nkey] = dict(SOLO.get(cur_set, SOLO["plaza"]), expr=expr)
            if expr == "talk": cast[nkey]["do"] = [{"do": "talk", "at": 0, "until": "end"}]
            elif expr == "sad" and rnd.random() < 0.3: cast[nkey]["do"] = [{"do": "cry", "at": 0.3, "until": "end"}]
            if idx == 0: size, move = "full", "push"
            camera = {"on": nkey, "shot": size, "from": side, "move": move}
        if cur_set in ("plaza", "street") and idx % 2 == 0: extras = {"walkers": 5}
        # emphasis on questions, exclamations and the last shot
        if last:
            camera = {"on": nkey if nkey in cast else list(cast)[0], "shot": "close", "from": "front", "move": "push"}
            fx.append({"glint": nkey if nkey in cast else list(cast)[0], "at": "end-0.6"})
        elif plain.rstrip().endswith(("!", "?")):
            fx.append({"punch": 0.15, "at": 0.15})
        m = TIME_TITLE.search(plain)
        if m and idx > 0:
            fx.append({"title": m.group(1).upper(), "dur": 1.2, "style": "banner", "at": 0})
        S.shot(cur_set, shot_lines[idx], cast, camera, mood=mood, fx=fx or None, extras=extras)
    return S.save(project)

def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    project = a[0]; opt = {}
    for i, x in enumerate(a[1:], 1):
        if x.startswith("--") and i + 1 < len(a): opt[x[2:]] = a[i + 1]
    srt = opt.get("srt") or os.path.join(project, "audio", "vo.srt")
    if not os.path.isfile(srt): sys.exit(f"SRT not found: {srt}")
    build(project, srt, narrator=opt.get("narrator", "boy"), seed=int(opt.get("seed", 0)))

if __name__ == "__main__": main()
