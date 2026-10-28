"""Work out the cartoon's mouth shapes for every voice clip with Rhubarb Lip Sync (phonetic mode works for Hindi).

Writes the event's lips.json: {voice: {line key: "@<onset ms>|X0B10C23..."}}. Each letter is a mouth shape
(A-H, X as in Rhubarb) followed by its start time in hundredths of a second. The onset is when the voice first gets
loud in the same decode, so the app can line the cues up however a phone decodes the MP3.
"""
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from common import VENDOR

THRESH = 0.02


def rhubarb():
    found = list((VENDOR / "rhubarb" / "x").glob("*/rhubarb"))
    if not found:
        raise SystemExit("Rhubarb Lip Sync is missing: run setup.sh")
    return found[0]


def onset_ms(mp3):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    rate = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate",
                               "-of", "csv=p=0", str(mp3)], capture_output=True, text=True, check=True).stdout.strip())
    loud = np.nonzero(np.abs(x) >= THRESH)[0]
    return round(1000 * loud[0] / rate) if len(loud) else 0


def cues(mp3, tool):
    with tempfile.TemporaryDirectory() as tmp:
        wav, js = Path(tmp) / "a.wav", Path(tmp) / "a.json"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(mp3), "-ac", "1", "-ar", "16000", str(wav)], check=True)
        subprocess.run([str(tool), "-q", "-r", "phonetic", "-f", "json", "--extendedShapes", "GHX", str(wav), "-o", str(js)],
                       check=True)
        data = json.loads(js.read_text())
    out, last = [], None
    for c in data["mouthCues"]:
        if c["value"] == last:
            continue
        out.append(f'{c["value"]}{round(c["start"] * 100)}')
        last = c["value"]
    return f"@{onset_ms(mp3)}|" + "".join(out)


def make(ev):
    """Time the mouth for every clip that has no timing yet (or whose clip is newer than lips.json)."""
    tool = rhubarb()
    old = json.loads(ev.lips_file.read_text(encoding="utf-8")) if ev.lips_file.exists() else {}
    stamp = ev.lips_file.stat().st_mtime if ev.lips_file.exists() else 0
    clips = sorted(ev.voice_dir.glob("v-*.mp3"))
    todo = [m for m in clips if m.stem.split("-", 2)[2] not in old.get(m.stem.split("-", 2)[1], {}) or m.stat().st_mtime > stamp]
    with ThreadPoolExecutor(6) as pool:
        done = dict(zip(todo, pool.map(lambda m: cues(m, tool), todo)))
    lips = {}
    for mp3 in clips:
        _, voice, key = mp3.stem.split("-", 2)
        lips.setdefault(voice, {})[key] = done[mp3] if mp3 in done else old[voice][key]
    ev.lips_file.write_text(json.dumps(lips, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    print("lip sync:", len(clips), "clips | newly timed:", len(todo))
