#!/usr/bin/env python3
"""Single English video of all scheduling algorithms, with synthesized sound effects.

Title grid with all six algorithms -> zoom into each one, play it, zoom back out ->
comparison of the average times -> end card. Every frame is rendered from sim.py
traces (same data as the реферат); the sounds are generated here from sine waves
and filtered noise, no audio files are used.

  python3 video.py                   # renders ../anim/cpu_scheduling_en_4k.mp4 (3840x2160, about 20 min)
  python3 video.py --frame 30 x.png  # one frame at t = 30 s, for checking the layout
  python3 video.py --audio x.wav     # only the sound track
"""
import array
import json
import math
import random
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import anim
import sim

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "anim"
PAGE = OUT / ".video.html"
FINAL = OUT / "cpu_scheduling_en_4k.mp4"
FPS = 60
RATE = 48000

COLORS = ["#0095c8", "#9c3348", "#219e61", "#ad7d00", "#6b46a0"]
INFO = {
    "fcfs": ("FCFS", "First-Come, First-Served", "Runs processes in order of arrival and never takes the CPU away.",
             "non-preemptive", "by arrival"),
    "sjf": ("SJF", "Shortest Job First", "Picks the shortest CPU burst and runs it to completion.",
            "non-preemptive", "by burst length"),
    "srtf": ("SRTF", "Shortest Remaining Time First",
             "Always runs the least remaining work. A shorter arrival preempts.", "preemptive", "by time left"),
    "rr": ("Round Robin", "Round Robin",
           f"Each process gets a {sim.EXAMPLE_QUANTUM}-unit time slice, then goes to the back of the queue.",
           f"preemptive · q = {sim.EXAMPLE_QUANTUM}", "first in, first out"),
    "prio": ("Priority", "Priority", "Highest priority first (lower number wins). Runs to completion.",
             "non-preemptive", "by priority"),
    "prio-p": ("Priority (preemptive)", "Preemptive Priority",
               "Highest priority first. A more important arrival preempts.", "preemptive", "by priority"),
}


def events(alg, steps, res, procs):
    by = {p.name: p for p in procs}
    out = []
    for k in range(len(steps) + 1):
        st = steps[k] if k < len(steps) else None
        prev = steps[k - 1] if k else None
        for p in procs:
            if res.completion[p.name] == k:
                out.append({"t": k, "proc": p.name, "kind": "done", "text": f"{p.name} finishes, waited {res.waiting(p)}"})
        for p in procs:
            if p.arrival == k:
                extra = f", priority {p.priority}" if alg.startswith("prio") else ""
                out.append({"t": k, "proc": p.name, "kind": "arrive", "text": f"{p.name} arrives, burst {p.burst}{extra}"})
        if not st:
            continue
        old, new = prev["run"] if prev else None, st["run"]
        preempted = old and old != new and res.completion[old] != k
        if preempted and alg == "rr":
            out.append({"t": k, "proc": old, "kind": "preempt", "text": f"{old}’s time slice is up, back of the queue"})
        elif preempted and alg == "srtf":
            out.append({"t": k, "proc": new, "kind": "preempt",
                        "text": f"{new} preempts {old}: {st['remaining'][new]} left vs {st['remaining'][old]}"})
            continue
        elif preempted and alg == "prio-p":
            out.append({"t": k, "proc": new, "kind": "preempt",
                        "text": f"{new} preempts {old}: priority {by[new].priority} beats {by[old].priority}"})
            continue
        if new and new != old:
            out.append({"t": k, "proc": new, "kind": "dispatch", "text": f"{new} gets the CPU"})
    return out


def data():
    procs = sim.EXAMPLE
    runs = {}
    for idx, alg in enumerate(anim.ORDER, 1):
        q = sim.EXAMPLE_QUANTUM if alg == "rr" else None
        trace = []
        res = sim.simulate(procs, alg, q, trace=trace)
        sw, last = 0, None
        for st in trace:
            if st["run"] and last is not None and st["run"] != last:
                sw += 1
            if st["run"]:
                last = st["run"]
            st["sw"] = sw
            st["ready"] = anim.display_order(alg, st["ready"], st["remaining"])
        short, label, rule, pill, order = INFO[alg]
        runs[alg] = {
            "index": idx, "short": short, "label": label, "rule": rule, "pill": pill, "order": order,
            "quantum": q, "length": res.length, "steps": trace, "gantt": [list(g) for g in res.gantt],
            "completion": res.completion, "switches": res.switches, "events": events(alg, trace, res, procs),
            "metrics": {p.name: {"wait": res.waiting(p), "tat": res.turnaround(p), "resp": res.response(p)}
                        for p in res.procs},
            "avg": {"wait": res.avg("waiting"), "tat": res.avg("turnaround"), "resp": res.avg("response")},
        }
    return {"order": anim.ORDER, "runs": runs,
            "processes": [{"name": p.name, "arrival": p.arrival, "burst": p.burst, "priority": p.priority, "color": c}
                          for p, c in zip(procs, COLORS)]}


def write_page():
    payload = json.dumps(data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    PAGE.write_text((SRC / "video.html").read_text(encoding="utf-8").replace("/*@DATA*/null", payload), encoding="utf-8")


# ---------------------------------------------------------------- sound

def env(n, attack, decay):
    a = max(1, int(attack * RATE))
    return [min(1.0, i / a) * math.exp(-decay * i / RATE) for i in range(n)]


def tone(freqs, dur, decay, vol, attack=0.003, glide=None):
    n = int(dur * RATE)
    e = env(n, attack, decay)
    out = [0.0] * n
    for f, amp in freqs:
        phase = 0.0
        for i in range(n):
            fi = f * (glide(i / RATE) if glide else 1.0)
            phase += 2 * math.pi * fi / RATE
            out[i] += amp * math.sin(phase)
    return [vol * e[i] * out[i] for i in range(n)]


def air(dur, shape, pan0, pan1, vol, seed):
    """Soft air movement: warm low-passed noise whose brightness follows the camera, panned in stereo."""
    rnd = random.Random(seed)
    n = int(dur * RATE)
    brown = lp1 = lp2 = 0.0
    left, right = [], []
    for i in range(n):
        x = i / n
        if shape == "rise":
            e = math.sin(math.pi / 2 * min(1, x / 0.85)) ** 2 * (1 - max(0, (x - 0.85) / 0.15)) ** 2
        elif shape == "fall":
            e = math.sin(math.pi / 2 * min(1, (1 - x) / 0.85)) ** 2 * (1 - max(0, (0.15 - x) / 0.15)) ** 2
        else:
            e = math.sin(math.pi * x) ** 2
        brown = 0.985 * brown + 0.15 * rnd.uniform(-1, 1)
        fc = 180 + 1400 * e
        k = 1 - math.exp(-2 * math.pi * fc / RATE)
        lp1 += k * (brown - lp1)
        lp2 += k * (lp1 - lp2)
        p = lerp_pan(pan0, pan1, x)
        v = vol * e * lp2
        left.append(v * math.cos((p + 1) * math.pi / 4))
        right.append(v * math.sin((p + 1) * math.pi / 4))
    return left, right


def lerp_pan(a, b, x):
    x = x * x * (3 - 2 * x)
    return a + (b - a) * x


LAND = [130.81, 146.83, 164.81, 196.0, 220.0, 261.63, 98.0]


def land(note):
    f = LAND[min(note, len(LAND) - 1)]
    body = tone([(f, 1.0), (2 * f, 0.32), (3 * f, 0.1)], 0.7, 11, 0.26, attack=0.002,
                glide=lambda t: 1 + 0.12 * math.exp(-t * 55))
    click = tone([(2400, 1.0)], 0.025, 180, 0.025)
    return [body[i] + (click[i] if i < len(click) else 0) for i in range(len(body))]


def pad(dur, notes, vol):
    n = int(dur * RATE)
    out = [0.0] * n
    for f in notes:
        for det in (-0.6, 0.6):
            w = 2 * math.pi * (f + det) / RATE
            for i in range(n):
                out[i] += math.sin(w * i)
    att, rel = 1.2 * RATE, 1.8 * RATE
    return [vol * out[i] * min(1, i / att) * min(1, (n - i) / rel) for i in range(n)]


NOTES = [523.25, 587.33, 659.25, 783.99, 880.0]


def sounds():
    tick = tone([(1760, 1.0), (3520, 0.25)], 0.08, 70, 0.10)
    tock = tone([(520, 1.0), (1040, 0.3)], 0.12, 38, 0.20, glide=lambda t: 1 + 0.5 * math.exp(-t * 90))
    pre = tone([(988, 1.0)], 0.09, 40, 0.11) + [0.0] * int(0.02 * RATE) + tone([(740, 1.0)], 0.14, 30, 0.11)
    chimes = [tone([(f, 1.0), (2 * f, 0.28), (3 * f, 0.08)], 1.4, 3.2, 0.13, attack=0.004) for f in NOTES]
    bar = tone([(1318.5, 1.0)], 0.07, 60, 0.06)
    return {
        "arrive": tick, "dispatch": tock, "preempt": pre, "done": chimes, "bar": bar,
        "tile": tone([(2093, 1.0)], 0.05, 80, 0.035),
        "pad": pad(4.6, [130.81, 196.0, 329.63, 493.88], 0.022),
        "pad_end": pad(4.2, [146.83, 220.0, 349.23, 523.25], 0.020),
    }


def mix(cues, total, path):
    sfx = sounds()
    n = int((total + 2) * RATE)
    left = array.array("f", bytes(4 * n))
    right = array.array("f", bytes(4 * n))

    def add(start, l, r):
        for i in range(min(len(l), n - start)):
            left[start + i] += l[i]
            right[start + i] += r[i]

    for c in cues:
        start = int(c["t"] * RATE)
        if c["type"] in ("zoom_in", "trans", "zoom_out"):
            shape = {"zoom_in": "rise", "trans": "swell", "zoom_out": "fall"}[c["type"]]
            add(start, *air(c["dur"], shape, c["pan0"], c["pan1"], 0.12, c["note"]))
            s = land(c["note"] if c["type"] != "zoom_out" else len(LAND) - 1)
            add(int((c["t"] + c["dur"] * (0.9 if c["type"] != "zoom_out" else 0.95)) * RATE), s, s)
            continue
        s = sfx[c["type"]]
        if c["type"] == "done":
            s = s[c.get("note", 0)]
        add(start, s, s)
    pcm = array.array("h")
    norm = math.tanh(1.2)
    for l, r in zip(left, right):
        pcm.append(int(32767 * math.tanh(1.2 * l) / norm))
        pcm.append(int(32767 * math.tanh(1.2 * r) / norm))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


# ---------------------------------------------------------------- video

def render():
    write_page()
    chrome = anim.Chrome()
    try:
        chrome.open(PAGE.as_uri(), 1920, 1080, scale=2)
        total = chrome.eval("TOTAL")
        cues = chrome.eval("cues()")
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / "sfx.wav"
            mix(cues, total, wav)
            enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS),
                                    "-c:v", "png", "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium",
                                    "-crf", "16", "-profile:v", "high", "-level", "5.2", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                                    "-movflags", "+faststart", str(FINAL)], stdin=subprocess.PIPE)
            frames = round(total * FPS)
            for f in range(frames):
                chrome.eval(f"renderAt({f / FPS})")
                enc.stdin.write(chrome.shot())
                if f % (FPS * 10) == 0:
                    print(f"{f / FPS:.0f}/{total:.0f} s", flush=True)
            enc.stdin.close()
            if enc.wait():
                sys.exit("ffmpeg failed")
    finally:
        chrome.close()
        PAGE.unlink(missing_ok=True)
    print(f"{FINAL.relative_to(SRC.parents[3])}: {total:.1f} s")


def frame(t, out):
    write_page()
    chrome = anim.Chrome()
    try:
        chrome.open(PAGE.as_uri(), 1920, 1080, scale=2)
        chrome.eval(f"renderAt({float(t)})")
        Path(out).write_bytes(chrome.shot())
        print(f"total {chrome.eval('TOTAL'):.1f} s")
    finally:
        chrome.close()
        PAGE.unlink(missing_ok=True)


def audio(out):
    write_page()
    chrome = anim.Chrome()
    try:
        chrome.open(PAGE.as_uri(), 1920, 1080)
        mix(chrome.eval("cues()"), chrome.eval("TOTAL"), Path(out))
    finally:
        chrome.close()
        PAGE.unlink(missing_ok=True)


if __name__ == "__main__":
    if "--audio" in sys.argv:
        audio(sys.argv[sys.argv.index("--audio") + 1])
    elif "--frame" in sys.argv:
        i = sys.argv.index("--frame")
        frame(sys.argv[i + 1], sys.argv[i + 2])
    else:
        render()
