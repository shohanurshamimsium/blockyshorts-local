---
name: blocky-shorts
description: Creates vertical 9:16 blocky 3D animated story Shorts and delivers a finished MP4 with the user's uploaded voice-over accurately synced to animation, captions, sound effects and optional background music. Always begin with a short guided intake; never choose a topic or start production until the user has selected the source, format and length.
---

# Blocky Shorts — guided, voice-synced production

Create a polished vertical 9:16 blocky/toy-like animated Short. The finished deliverable should be one MP4 containing the animation, the user's actual voice-over, captions timed to that voice, sound effects, and (when available and approved) background music. Do not make the user manually sync audio in another editor.

The renderer is a custom Three.js blocky animation engine, not Roblox Studio and not an actual Roblox gameplay recorder. Describe it accurately as Roblox-style/blocky 3D animation. Use only sets, characters, actions, props and effects supported by `references/library.md`, extending the engine only when practical and testable.

## LANGUAGE RULE — IMPORTANT

**All workflow communication must be in English, regardless of the language the user types in.** This includes every question, numbered option, clarification, approval request, instruction, progress update, error message and delivery note. Never reply to the user in Hindi or Hinglish during the workflow.

The only exception is the creative narration/dialogue itself: at Stage 4, let the user choose Hindi, Hinglish or English (or another language they request). Write the actual voice-over script in that selected language, but keep all surrounding explanations, labels and workflow messages in English. Do not assume the target audience is Indian just because the user types in Hindi.

## NON-NEGOTIABLE INTERACTION RULES

1. **Do not start by inventing a topic.** First ask what the user already has. Do not interpret "go ahead", "start", or a one-word acknowledgement as permission to skip the intake stages.
2. **Ask one stage at a time.** Keep questions short and show numbered choices. Wait for the user's answer before moving to the next stage. Do not dump the whole questionnaire at once.
3. **Never silently choose the user's topic, format, duration, narration language or voice-over path.** If the user says "you decide" for a particular stage, choose only that stage and tell them what you chose.
4. **Script approval is required.** Show the full narration script and ask for approval/edits before building the storyboard.
5. **The user's uploaded voice-over is the timing master.** Do not render the final video using estimated timing when the user has said they will upload a voice-over. Wait for the actual audio file, align it, and use that timing for captions, cuts, actions, camera beats and sound cues.
6. **No separate manual syncing.** Perform alignment, timing corrections, mixing and final encoding in this workflow. If exact alignment cannot be achieved, explain the limitation and fix/retry; never tell the user to sync it manually in CapCut as the normal workflow.
7. **Never claim a final render is complete unless the MP4 exists and has been checked.**

## Guided intake — exact sequence

### Stage 1 — What does the user have?
Start every new project with this question and nothing else:

"First, what do you already have ready?
1. I have a topic/idea
2. I have a rough idea, but no script
3. I have a complete script
4. I have nothing yet — suggest a topic for me"

If the user chooses 1, ask them to send the topic. If 2, ask them to explain the rough idea in their own words. If 3, ask them to paste/upload the script. If 4, move to Stage 2 and suggest topic options only after learning the desired video format. Do not write the script yet.

### Stage 2 — What kind of blocky/Roblox-style Short?
Ask the user to choose one format (or say their own):

1. In This Town / weird rule comedy — one strange rule changes everyday life
2. School / classroom comedy — students, teachers, exams, school situations
3. Family / home comedy — parents, siblings, daily-life chaos
4. Superpower / fantasy — unusual powers, magic, impossible events
5. Mystery / suspense / light horror — strange event, clues, reveal
6. Survival / challenge — character faces a simple escalating challenge
7. Social experiment / city life — people react to an unusual situation
8. Other — user describes it

These are story formats, not promises of real Roblox gameplay. Pick locations and assets that the current engine supports. If a requested format needs unavailable mechanics, say so and offer the closest buildable version before proceeding.

If the user has an existing topic/script, preserve its core premise and adapt it to the selected format only with permission. If they have nothing, offer 3 distinct original topic pitches matching the selected format and let them choose. Never automatically select one of the three.

### Stage 3 — Video length
Ask:

"How long should the video be?
1. 20–30 seconds
2. 45–60 seconds
3. 60–90 seconds
4. 2–3 minutes"

Use the selected length. If the engine/session has a practical render limit, explain it before script approval; do not silently shorten the requested duration.

### Stage 4 — Language and narration
Ask in English: "Which language should the narration use? 1. Hindi 2. Hinglish 3. English 4. Another language (tell me which one)." Keep the narration natural and easy to speak. Confirm whether it is a single narrator or multiple character voices only if the story requires dialogue.

### Stage 5 — Write and approve script
Write a complete voice-over script suited to the chosen format and duration. Include a strong opening, clear escalation, visual beats and a satisfying ending. Avoid filler. Show:
- narration text, exactly as it should be spoken;
- estimated spoken duration;
- brief scene/visual premise.

Ask: "Do you approve this script? Reply 'Approve' or tell me what you want changed." Do not proceed until approval. If edits are requested, revise and show the full revised script.

### Stage 6 — Voice-over handoff (mandatory before final render)
After approval:
1. Generate `build/vo_script.txt`, `build/vo_script_v2_breaks.txt`, and `build/vo_transcript.txt` using `python3 scripts/bs.py script <PROJECT>`.
2. Give the user the correct ready-to-copy narration file/text and concise ElevenLabs instructions. The generated voice must speak the approved script exactly, in the same order. Tell the user to download MP3 and upload it in this chat.
3. Explicitly say: "Once you upload the voice-over, I will automatically sync it with the animation and render the final MP4. You will not need to sync it manually in CapCut."
4. **STOP and wait for the actual uploaded voice-over.** Do not use `bs.py estimate` to create a final deliverable. A silent preview may be made only if useful and clearly labelled as a temporary preview, never as final.

### Stage 7 — Align the uploaded voice-over
When the user uploads the VO:
1. Save/copy the uploaded audio to `<PROJECT>/audio/vo.mp3` (convert to a supported format only if needed; preserve the original).
2. Prefer exact timing from ElevenLabs character-level alignment/forced alignment if available. Use the helper only if credentials/network are already available and the user has authorized it. Never ask the user to expose an API key in chat.
3. Otherwise run `python3 scripts/bs.py align <PROJECT>` on the clean voice track. If an SRT/subtitle file is provided, use `--srt`; if alignment JSON is provided, use `--alignment`.
4. Inspect the printed alignment table and `build/timing.json`. Check that every approved narration line is present, in order, with plausible start/end times. If a line is missing, duplicated, or badly aligned, correct the timing or retry alignment. Do not add music/SFX to the voice track before alignment.
5. The VO duration is authoritative. Adapt shot lengths, camera moves, actions and visual beats to the real VO timing. Do not speed up, stretch or cut the user's voice unless they explicitly approve it.
6. If the uploaded VO text differs from the approved script, show the differences and ask whether to revise the script to match the VO or regenerate the VO. Do not silently rewrite spoken words.

### Stage 8 — Storyboard and visual plan
Read `references/storyboard.md`, `references/library.md`, and `references/qa-and-iteration.md`. Build the `story.json` around the approved script and actual VO timing. Use a fresh project folder, not the read-only skill folder. Keep the user's chosen format and duration. Plan a new visual beat for each narration phrase; vary sets, character framing, expressions, actions, props, camera movement and transitions. Avoid repetitive shots. Validate all names against the library; do not invent unsupported set/action/prop identifiers.

Show a compact storyboard/preview sheet only when the user needs to approve visual direction or when it is practical to catch issues before the expensive render. Do not ask for redundant approvals at every tiny implementation step. If a material creative choice is needed, ask one clear question; otherwise continue with the approved plan.

### Stage 9 — Sound design and music
1. Use the original built-in SFX pack and event system. Place SFX deliberately on meaningful actions, reveals, transitions and punchlines; do not put a loud sound on every cut. Keep SFX below the narration and avoid masking words.
2. Add an original or properly licensed background music track only when one is available in the workspace or supplied/approved by the user. Place it at `<PROJECT>/audio/music.mp3`; use ducking under narration. Never use copyrighted commercial songs. If no suitable music track is available, do not pretend one was added; deliver clean VO + SFX and tell the user that music was not included.
3. Default mix guidance: voice clear and dominant, SFX supportive, music subtle. Use the mixer's ducking and normalization. If SFX masks speech, reduce SFX gain and remix.

### Stage 10 — Render final MP4
Run the renderer's validation and preview checks. Fix warnings and visual defects before the final render. Render frames, then mix and encode with the real VO:

```bash
node scripts/render.mjs check <PROJECT>
node scripts/render.mjs preview <PROJECT>
node scripts/render.mjs frames <PROJECT> --budget 240
# repeat frames command until it reports DONE
python3 scripts/bs.py mix <PROJECT>
python3 scripts/bs.py encode <PROJECT>
```

Use the actual VO-derived `build/timing.json`; never substitute estimated timing. If there is no music file, the mix should still contain VO and SFX. Check the final MP4 exists, inspect representative frames, confirm duration is close to the VO duration, and listen/check that the audio contains the narration, SFX and any approved music. Ensure the first and last words are not clipped. Confirm captions follow the spoken words.

If rendering fails due to missing dependencies, browser/Chrome, FFmpeg, memory or time limits, report the exact blocker and what did complete. Do not claim success or invent a download path.

### Stage 11 — Delivery
Deliver the actual final MP4 file/link from the verified output path. State briefly:
- final duration and resolution;
- that the uploaded VO is synced;
- whether SFX and music are included;
- any known limitation.

The goal is a ready-to-upload Short. Do not tell the user to manually sync the voice in another editor. Optional final trims, platform upload and adding platform-native music can be mentioned only as optional finishing choices.

## Existing engine workflow references
- Story structure: `references/story-formula.md`
- Story JSON schema and shot construction: `references/storyboard.md`
- Available sets, cast, actions, props, camera and SFX: `references/library.md`
- Alignment, ElevenLabs instructions, SFX/music and mixing: `references/audio.md`
- Visual QA and iteration: `references/qa-and-iteration.md`

## Setup and working files
Use a writable project copy outside the skill folder. Check the environment once per session with `bash scripts/setup.sh`, then initialise a unique project with `python3 scripts/bs.py init <PROJECT>`. Preserve the bundled engine and original SFX assets. Do not overwrite the original skill files.
