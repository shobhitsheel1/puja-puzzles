"""Record every line the cartoon says with the event's natural Hindi voices (Piper, run offline with sherpa-onnx).

Only lines without a clip are recorded, so clips that were already checked stay exactly the same.
Clips are named v-<voice>-<key>.mp3 and live in the event's voice/ folder.
"""
import subprocess
import wave

import numpy as np

from common import TTS


def engine(name):
    import sherpa_onnx
    folder = TTS / f"vits-piper-hi_IN-{name}-medium"
    if not folder.exists():
        raise SystemExit(f"voice {name} is missing: run setup.sh (expected {folder})")
    model = next(folder.glob("*.onnx")).name
    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=str(folder / model), tokens=str(folder / "tokens.txt"), data_dir=str(folder / "espeak-ng-data")),
            num_threads=4),
        max_num_sentences=4)
    return sherpa_onnx.OfflineTts(cfg)


def write_mp3(samples, rate, dest):
    """Normalise, add a short lead-in and tail, and save as a small mono MP3."""
    x = np.asarray(samples, dtype=np.float32)
    peak = float(np.max(np.abs(x))) or 1.0
    x = x / peak * 0.89
    x = np.concatenate([np.zeros(int(rate * 0.08), np.float32), x, np.zeros(int(rate * 0.25), np.float32)])
    wav = dest.with_suffix(".wav")
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "64k", str(dest)], check=True)
    wav.unlink()
    return len(x) / rate, float(np.sqrt(np.mean(x ** 2)))


def say(tts, text):
    # Piper reads "।" and "..." better as "." and ","
    return tts.generate(text.replace("।", ".").replace("...", ","), sid=0, speed=0.9)


def record(ev, redo=False):
    out = ev.voice_dir
    out.mkdir(exist_ok=True)
    lines = ev.lines()
    if redo:
        for old in out.glob("v-*.mp3"):
            old.unlink()
    wanted = {f"v-{v}-{k}.mp3" for v in ev.voices for k in lines}
    for stale in out.glob("v-*.mp3"):
        if stale.name not in wanted:
            stale.unlink()
    made = []
    for vname in ev.voices:
        todo = [k for k in lines if not (out / f"v-{vname}-{k}.mp3").exists()]
        if not todo:
            continue
        tts = engine(vname)
        for key in todo:
            audio = say(tts, lines[key])
            dur, rms = write_mp3(audio.samples, audio.sample_rate, out / f"v-{vname}-{key}.mp3")
            made.append(f"v-{vname}-{key}.mp3")
            print(f"  recorded {vname} {key}: {dur:.1f}s")
    print("voice clips:", len(list(out.glob("v-*.mp3"))), "| new:", len(made))
    return made
