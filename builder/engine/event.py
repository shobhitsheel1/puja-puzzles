"""Load one event folder: config.json (festival, hosts, cartoon, deployment), content.py (puzzles and lines)
and deity.py (the festival cartoon)."""
import importlib.util
import json
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

# Natural Hindi voices (Piper, run offline with sherpa-onnx): name -> (label, gender)
VOICE_INFO = {"rohan": ("Rohan", "m"), "pratham": ("Pratham", "m"), "priyamvada": ("Priyamvada", "f")}

TEXT_DEFAULTS = {
    "round2_icon": "1f6d5",
    "end_icon": "1f64f",
    "right_banner": "SAHI JAWAB!",
    "wrong_banner": "GALAT JAWAB!",
    "warmup_bottom": "WARM-UP ROUND",
}


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Event:
    def __init__(self, folder):
        self.dir = Path(folder).resolve()
        self.slug = self.dir.name
        self.cfg = json.loads((self.dir / "config.json").read_text(encoding="utf-8"))
        self.content = _load(self.dir / "content.py", f"content_{self.slug.replace('-', '_')}")
        self.deity = _load(self.dir / "deity.py", f"deity_{self.slug.replace('-', '_')}")
        self.texts = {**TEXT_DEFAULTS, **getattr(self.content, "TEXTS", {})}
        self.voice_dir = self.dir / "voice"
        self.lips_file = self.dir / "lips.json"

    # ---- names
    @property
    def hosts(self):
        return self.cfg["hosts"]

    @property
    def hosts_en(self):
        """"Reshma and Shobhit", "Asha, Ravi and Meena"."""
        names = [h["en"] for h in self.hosts]
        return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]

    @property
    def name_words(self):
        """Every spelling of the hosts' names, used to space out lines that mention them."""
        return [h[k] for h in self.hosts for k in ("hi", "en") if h.get(k)]

    @property
    def character(self):
        return self.cfg["character"]

    @property
    def voices(self):
        v = self.character.get("voices") or ["rohan"]
        unknown = [x for x in v if x not in VOICE_INFO]
        if unknown:
            raise SystemExit(f"unknown voices {unknown}; choose from {list(VOICE_INFO)}")
        return v

    def svg(self, cls="bhag", idp="bg"):
        return self.deity.svg(cls=cls, idp=idp)

    def sound_check(self):
        """Short lines for the menu's sound test and voice picker (content.SOUND_CHECK can replace them)."""
        f = self.character.get("gender", "m") == "f"
        default = {
            "test": {"hi": "तथास्तु! आवाज़ ठीक आ रही है।", "en": "Tathastu! The sound is working."},
            "sample": {"hi": "तथास्तु! मैं तुम्हें आशीर्वाद देती हूँ।" if f else "तथास्तु! मैं तुम्हें आशीर्वाद देता हूँ।",
                       "en": "Tathastu! I bless you."},
            "tath": {"hi": "तथास्तु!", "en": "Tathastu!"},
        }
        return {**default, **getattr(self.content, "SOUND_CHECK", {})}

    # ---- every line the voice says: key -> Hindi text
    def lines(self):
        c = self.content
        out = {b.get("key", f"b{i:02d}"): f"{b['open_hi']} {b['hi']} {b['close_hi']}" for i, b in enumerate(c.BLESSINGS, 1)}
        out.update({w.get("key", f"w{i:02d}"): w["hi"] for i, w in enumerate(c.WRONGS, 1)})
        out[c.WELCOME["key"]] = c.WELCOME["hi"]
        out.update({k: v["hi"] for k, v in self.sound_check().items()})
        return out

    def level_ranges(self):
        out = {}
        for i, p in enumerate(self.content.PUZZLES, 1):
            lo, hi = out.get(p["level"], (i, i))
            out[p["level"]] = (min(lo, i), max(hi, i))
        return out
