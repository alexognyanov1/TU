#!/usr/bin/env python3
"""4K "Liquid Glass" video of all scheduling algorithms, made with the Motion Graphics starter kit.

Style, motion and sound follow the kit (Damiano Caudullo): frosted glass cards on a soft gradient with
drifting colour blobs, Inter, green only for ticks, calm power3 motion with no bounce. Moves used:
blur-in, typewriter, reframe (full-screen panel shrinks into the header card), rise, count-up, bar
fill, checklist tick and punch-in. The fonts and sound effects are the kit's files in kit/.
Every frame comes from sim.py traces, the same data as the реферат.

  python3 glass.py                   # renders ../anim/cpu_scheduling_glass_4k.mp4 (3840x2160, 60 fps)
  python3 glass.py --frame 30 x.png  # one frame at t = 30 s, for checking the layout
  python3 glass.py --audio x.wav     # only the sound track
"""
import array
import base64
import json
import math
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import anim
import video

SRC = Path(__file__).resolve().parent
KIT = SRC / "kit"
OUT = SRC.parent / "anim"
PAGE = OUT / ".glass.html"
FINAL = OUT / "cpu_scheduling_glass_4k.mp4"
FPS = 60
RATE = 48000

COLORS = ["#0a84ff", "#ff375f", "#bf5af2", "#ff9f0a", "#ac8e68"]
GAIN = {"tick": 0.9, "pop": 0.3, "switch": 0.4, "snap": 0.5, "success": 0.5, "fill": 0.9, "counter": 0.55, "chime": 0.8}
MASTER = 2.0


def data():
    d = video.data()
    for p, c in zip(d["processes"], COLORS):
        p["color"] = c
    return d


def fonts():
    css = ""
    for weight in (400, 700):
        b64 = base64.b64encode((KIT / "fonts" / f"Inter-{weight}.woff2").read_bytes()).decode()
        css += f'@font-face {{ font-family: "Inter"; font-weight: {weight}; src: url(data:font/woff2;base64,{b64}) format("woff2"); }}\n'
    return css


def write_page():
    payload = json.dumps(data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (SRC / "glass.html").read_text(encoding="utf-8")
    PAGE.write_text(page.replace("/*@FONTS*/", fonts()).replace("/*@DATA*/null", payload), encoding="utf-8")


def load(name):
    with wave.open(str(KIT / "sfx" / f"{name}.wav")) as w:
        if (w.getsampwidth(), w.getframerate(), w.getnchannels()) != (2, RATE, 1):
            sys.exit(f"{name}.wav: expected 16-bit mono {RATE} Hz")
        pcm = array.array("h", w.readframes(w.getnframes()))
    return [x / 32768 for x in pcm]


def mix(cues, total, path):
    sfx = {name: load(name) for name in GAIN}
    n = int((total + 1) * RATE)
    buf = array.array("f", bytes(4 * n))
    for c in cues:
        s, g, start = sfx[c["type"]], MASTER * GAIN[c["type"]], int(c["t"] * RATE)
        for i in range(min(len(s), n - start)):
            buf[start + i] += g * s[i]
    norm = math.tanh(1.1)
    pcm = array.array("h")
    for v in buf[:int(total * RATE)]:
        x = int(32767 * math.tanh(1.1 * v) / norm)
        pcm.append(x)
        pcm.append(x)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def session(fn, scale=2):
    write_page()
    chrome = anim.Chrome()
    try:
        chrome.open(PAGE.as_uri(), 1920, 1080, scale=scale)
        return fn(chrome)
    finally:
        chrome.close()
        PAGE.unlink(missing_ok=True)


def render():
    def run(chrome):
        total = chrome.eval("TOTAL")
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "sfx.wav"
            mix(chrome.eval("cues()"), total, wav)
            enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS),
                                    "-c:v", "png", "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium",
                                    "-crf", "16", "-profile:v", "high", "-level", "5.2", "-pix_fmt", "yuv420p",
                                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(FINAL)],
                                   stdin=subprocess.PIPE)
            frames = round(total * FPS)
            for f in range(frames):
                chrome.eval(f"renderAt({f / FPS})")
                enc.stdin.write(chrome.shot())
                if f % (FPS * 10) == 0:
                    print(f"{f / FPS:.0f}/{total:.0f} s", flush=True)
            enc.stdin.close()
            if enc.wait():
                sys.exit("ffmpeg failed")
        print(f"{FINAL.relative_to(SRC.parents[3])}: {total:.1f} s")
    session(run)


def frame(t, out):
    def run(chrome):
        chrome.eval(f"renderAt({float(t)})")
        Path(out).write_bytes(chrome.shot())
        print(f"total {chrome.eval('TOTAL'):.1f} s")
    session(run)


def audio(out):
    session(lambda chrome: mix(chrome.eval("cues()"), chrome.eval("TOTAL"), Path(out)), scale=1)


if __name__ == "__main__":
    if "--audio" in sys.argv:
        audio(sys.argv[sys.argv.index("--audio") + 1])
    elif "--frame" in sys.argv:
        i = sys.argv.index("--frame")
        frame(sys.argv[i + 1], sys.argv[i + 2])
    else:
        render()
