#!/usr/bin/env bash
# One-time setup for the festival puzzle builder: fonts, 3D emoji pictures, natural Hindi voices, Whisper (for
# checking the voice), Rhubarb Lip Sync and the Python packages. Everything goes into builder/vendor (not committed).
# About 1 GB to download; a few minutes. Safe to run again: it skips what is already there.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p vendor/tts vendor/rhubarb
cd vendor

npm_pkg() {  # name version folder
  if [ ! -d "$3/package" ]; then
    echo "fetching $1@$2"
    local tgz
    tgz=$(npm pack "$1@$2" --silent | tail -1)
    mkdir -p "$3" && tar xzf "$tgz" -C "$3" && rm -f "$tgz"
  fi
}
npm_pkg @fontsource/poppins 5.3.0 fontsource-poppins-5.3.0
npm_pkg @fontsource/anton 5.3.0 fontsource-anton-5.3.0
npm_pkg @fontsource/baloo-2 5.3.0 fontsource-baloo-2-5.3.0
npm_pkg @fontsource/luckiest-guy 5.3.0 fontsource-luckiest-guy-5.3.0
npm_pkg @lobehub/fluent-emoji-3d 1.1.0 lobehub-fluent-emoji-3d-1.1.0

REL=https://github.com/k2-fsa/sherpa-onnx/releases/download
for v in rohan pratham priyamvada; do      # Hindi voices: rohan and pratham are male, priyamvada is female
  if [ ! -d "tts/vits-piper-hi_IN-$v-medium" ]; then
    echo "fetching voice $v"
    curl -sSL "$REL/tts-models/vits-piper-hi_IN-$v-medium.tar.bz2" | tar xj -C tts
  fi
done
if [ ! -d tts/sherpa-onnx-whisper-base ]; then
  echo "fetching whisper base"
  curl -sSL "$REL/asr-models/sherpa-onnx-whisper-base.tar.bz2" | tar xj -C tts
fi
if ! ls rhubarb/x/*/rhubarb >/dev/null 2>&1; then
  echo "fetching Rhubarb Lip Sync"
  curl -sSL -o rhubarb.zip https://github.com/DanielSWolf/rhubarb-lip-sync/releases/download/v1.13.0/Rhubarb-Lip-Sync-1.13.0-Linux.zip
  unzip -q -o rhubarb.zip -d rhubarb/x && rm -f rhubarb.zip
  chmod +x rhubarb/x/*/rhubarb
fi

python3 -c "import sherpa_onnx, numpy, PIL, playwright" 2>/dev/null || \
  pip install --quiet --break-system-packages sherpa-onnx numpy pillow playwright || \
  pip install --quiet sherpa-onnx numpy pillow playwright
python3 - <<'EOF' || python3 -m playwright install chromium
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
EOF
command -v ffmpeg >/dev/null || { echo "ffmpeg is missing: install it (apt-get install -y ffmpeg)"; exit 1; }
echo "setup done"
