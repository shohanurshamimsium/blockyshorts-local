# How a story file is written (paste this to Claude in any new chat)

Goal: for ANY approved script, produce `story_<name>.py` for this workflow, so the user can render offline.

1. The script's words are split into **caption lines** of 2 to 3 words, grouped 1 to 3 lines per shot. About 1 shot per 1.5 to 2 seconds (a 70 s video is about 40 shots; 226 words). The voiceover must say these lines exactly, in order; no audio tags in the lines. Highlight one hinge word per shot with `*word*`.
2. Characters: TWO MODES, the user chooses per video (ask once, default to the one used last time).
   - **Fixed cast:** pull the channel's recurring characters from `lib/cast_library.py` by name, e.g. `S.use("dad","mom",hero="narrator_boy")`. Never change a library entry's look, so the same person looks identical in every video. Add a brand-new recurring character as a new library entry.
   - **New characters:** write fresh looks for this video in `S.cast = {...}` (preset plus shirt, pants, hair, hairColor, extras), so every story can have a new cast. You can mix: `S.use("dad")` for one fixed character and define the rest.
   In both modes one cast name = the same look in every shot of the video. Give every `boy`/`girl` preset `"shirtDesign":"plain"` (the default shirt has a number print).
3. Each shot: `S.shot(set, lines, cast_dict, camera_dict, mood=..., fx=[...], extras=..., props=...)`. Sets: plaza, street, living_room, bedroom, classroom, office, farm, clinic, studio. Moods: day, sunset, night. Use only names from the engine's `references/library.md`; `render.mjs check` reports unknown names.
4. Vary shot sizes (wide, medium, close), mostly `push` camera moves, a few others. Frame two actors with `"on":["a","b"]` and a `wide`/`full` shot.
5. Time references (`at`) match a line's text: use short fragments (`"report."`, `"fell"`).
6. Known pitfalls: bedroom `bed` spot hides the actor and breaks the camera (seat a person in bed with `{"at":[-2.5,0,-3.1],"base":"sit","seat":1.95,"face":"front"}`); `night` is very dark indoors (use `sunset`); two actors one in front of the other hide each other; `fx sign` covers the top of the frame so skip it on extreme close-ups; no snow, kitchen or hospital corridor.
7. Deliver three things together: the script, `voiceover.txt` (narration only, numbers as words, at most two tags), and the story file. Count the words with Python and say the estimated length (words / 3.2 = seconds).
8. Style versions: the user prefers the "version 1" look (2 to 3 word chunks, yellow highlights, mostly push moves). Use one-word red captions and sign graphics only if asked.
