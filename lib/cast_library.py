"""Ready-made recoloured characters for any story. Pull them in with  S.use("dad", "mom")  or  S.use(hero="narrator_boy").
Colours are tuned so faces stay readable. Add your own freely (see the engine's references/library.md for every option)."""
CAST_LIBRARY = {
 "narrator_boy":  {"preset": "boy",  "shirt": "#d9622b", "shirtDesign": "plain", "pants": "#2b4fb8", "hair": "short", "hairColor": "#5a3a1e"},
 "narrator_girl": {"preset": "girl", "shirt": "#7b3fe4", "shirtDesign": "plain", "pants": "#2b2b3a", "hair": "pony",  "hairColor": "#3a2415"},
 "dad":     {"preset": "dad",  "shirt": "#7a4a2a", "sleeves": "long", "pants": "#2e2e3a", "hair": "short", "hairColor": "#8a8a8a"},
 "mom":     {"preset": "mom",  "shirt": "#f2e6c9", "hair": "long", "hairColor": "#2a1a0e"},
 "grandma": {"preset": "grandma", "shirt": "#d9a521", "extras": ["glasses"]},
 "grandpa": {"preset": "grandpa", "shirt": "#4a6f8a"},
 "boss":    {"preset": "boss"},
 "teacher": {"preset": "teacher"},
 "friend_boy":  {"preset": "boy",  "shirt": "#2a9d6f", "shirtDesign": "plain", "hair": "spiky", "hairColor": "#e8c84a"},
 "friend_girl": {"preset": "girl", "shirt": "#e84a8a", "shirtDesign": "plain", "hair": "bob", "hairColor": "#1a1a1a"},
 "coworker": {"preset": "boy", "shirt": "#9ec9f0", "shirtDesign": "tie", "accent": "#222222", "hair": "spiky", "hairColor": "#e8c84a"},
 "landlord": {"preset": "worker", "hair": "bald"},
 "cop":     {"preset": "cop"}, "doctor": {"preset": "doctor"}, "chef": {"preset": "chef"}, "mayor": {"preset": "mayor"},
 "kid":     {"preset": "kid"}, "villain": {"preset": "villain"}, "king": {"preset": "king"}, "robot": {"preset": "robot"},
}
