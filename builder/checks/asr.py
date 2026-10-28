#!/usr/bin/env python3
"""Listen to voice clips with Whisper (offline) to check that every word, especially the hosts' names, comes through.

  python checks/asr.py events/<slug>                     all clips of the first voice
  python checks/asr.py events/<slug> --keys b23,w15 --voice pratham --lang hi,en

Whisper "base" writes Hindi speech loosely (often in Urdu script, and --lang en gives a rough translation), so judge
whether the words are there, not the spelling. Re-word a line if a name or a key word is missing in both.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "engine"))
from common import TTS  # noqa: E402
from event import Event  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("event")
    ap.add_argument("--voice")
    ap.add_argument("--keys", help="comma-separated line keys (default: all)")
    ap.add_argument("--lang", default="hi")
    a = ap.parse_args()
    ev = Event(a.event)
    voice = a.voice or ev.voices[0]
    lines = ev.lines()
    keys = a.keys.split(",") if a.keys else list(lines)
    import sherpa_onnx
    w = TTS / "sherpa-onnx-whisper-base"
    recs = {l: sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(w / "base-encoder.onnx"), decoder=str(w / "base-decoder.onnx"), tokens=str(w / "base-tokens.txt"),
        language=l, task="transcribe", num_threads=4) for l in a.lang.split(",")}
    for k in keys:
        mp3 = ev.voice_dir / f"v-{voice}-{k}.mp3"
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, dtype=np.float32)
        print(f"{k}: {lines[k]}")
        for l, r in recs.items():
            s = r.create_stream(); s.accept_waveform(16000, x); r.decode_stream(s)
            print(f"   heard ({l}): {s.result.text.strip()}")


if __name__ == "__main__":
    main()
