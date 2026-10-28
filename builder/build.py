#!/usr/bin/env python3
"""Build a festival puzzle app from an event folder.

  python build.py events/<slug>             build the app (build/<slug>/app) and the GitHub Pages web app (build/<slug>/site)
  python build.py events/<slug> --voice     first record any voice clips that are missing (natural Hindi voices)
  python build.py events/<slug> --lips      first time the cartoon's mouth for clips that have no timing yet
  python build.py events/<slug> --all       --voice, --lips, then build
  python build.py events/<slug> --redo-voice  record every clip again (rarely needed)

Run setup.sh once per machine first. See README.md.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "engine"))

from event import Event  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("event", help="event folder, e.g. events/diwali-2026")
    ap.add_argument("--voice", action="store_true")
    ap.add_argument("--redo-voice", action="store_true")
    ap.add_argument("--lips", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default=str(HERE / "build"), help="where to put the built app and site")
    a = ap.parse_args()
    ev = Event(a.event)
    if a.voice or a.all or a.redo_voice:
        import voice
        voice.record(ev, redo=a.redo_voice)
    if a.lips or a.all or a.redo_voice:
        import lips
        lips.make(ev)
    import app
    import webapp
    out = Path(a.out) / ev.slug
    app_dir = app.build(ev, out / "app")
    webapp.build_site(ev, app_dir, out / "site", out / "work")
    print("done:", out)


if __name__ == "__main__":
    main()
