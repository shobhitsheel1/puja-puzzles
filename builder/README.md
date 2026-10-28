# Festival puzzle builder

Builds a tap-to-play rebus picture quiz for a family festival party, made to be mirrored from a phone to a TV:
warm-ups, then easy → medium → hard picture puzzles, Right / Wrong buttons, a festival cartoon (deity or mascot)
who reacts with funny lines in a natural Hindi voice with lip sync, a welcome screen naming the hosts, scores,
and an installable web app that works offline.

The first event, `events/satyanarayan-2026` (Satyanarayan Puja hosted by Reshma and Shobhit), is live at
https://shobhitsheel1.github.io/puja-puzzles/ and is the worked example for every new event.

## Quick start

```bash
bash setup.sh                                   # once per machine: fonts, emoji, voices, lip-sync tool (~1 GB)
python3 build.py events/satyanarayan-2026       # -> build/satyanarayan-2026/app and build/satyanarayan-2026/site
python3 checks/check.py events/satyanarayan-2026
```

## A new event

1. Copy `events/satyanarayan-2026` to `events/<festival>-<year>` and delete its `voice/` folder and `lips.json`.
2. `config.json`: app title, festival names (English, Hindi), banner, hosts (English, Hindi, gender), the cartoon's
   name, pronoun, gender and voices (`rohan`, `pratham` male; `priyamvada` female), a new `storage_key` and
   `cache_prefix` (apps on the same github.io address must not share them), decorations, optional theme colours.
3. `content.py`: new warm-ups and puzzles about this festival, new blessings and wrong-answer lines in the
   cartoon's voice (with a few host jokes), the spoken welcome and the screen texts.
4. `deity.py`: a new cartoon for the festival, drawn with the hooks in `engine/face.py` (eyes, 9 mouths, float).
5. `python3 build.py events/<slug> --all` records the voice, times the lips and builds both versions.
6. Review: `checks/cartoon.py`, `checks/cards.py` (look at every sheet), `checks/asr.py`, `checks/check.py`.
7. Deploy `build/<slug>/site/*` to the root of a GitHub Pages repo, and/or publish `build/<slug>/app/index.html`
   with its `assets/` as a Claude artifact.

## Layout

```
build.py            one command for voice, lip sync, app and web app
setup.sh            downloads everything in vendor/
engine/             festival-agnostic code
  app.py            the quiz app (HTML, CSS, JS in one page) for one event
  webapp.py         GitHub Pages version: manifest, icons, offline service worker
  voice.py          records lines with Piper Hindi voices via sherpa-onnx (only missing clips)
  lips.py           Rhubarb Lip Sync timings for every clip
  face.py           the 9 talking mouths and the hooks a cartoon must have
  kit.py            building blocks for puzzle pictures (emoji, words, 3D letters, rows...)
  event.py          loads an event folder
events/<slug>/      config.json, content.py, deity.py, voice/*.mp3, lips.json
checks/             check.py (play-tests), cards.py (puzzle sheets), cartoon.py (face sheet), asr.py (voice)
```

Voices: Piper Hindi models (CC BY-NC-SA 4.0 data), non-commercial use only. Emoji: Fluent Emoji 3D (MIT).
Fonts: SIL OFL / Apache 2.0. Lip sync: Rhubarb Lip Sync (MIT; its output belongs to you).
