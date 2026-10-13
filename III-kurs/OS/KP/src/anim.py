#!/usr/bin/env python3
"""Animations of the scheduling algorithms on the example from the реферат.

The data for every frame comes from sim.py (Gantt chart, ready queue and remaining
time at each step), so the animations always match the PDF.

  python3 anim.py                    # writes ../anim/scheduling.html (interactive, works offline)
  python3 anim.py --video            # also records ../anim/*.mp4 with headless Chrome + ffmpeg
  python3 anim.py --frame rr 12.5 out.png   # one frame, for checking the layout
"""
import base64
import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import sim

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "anim"
HTML = OUT / "scheduling.html"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FPS = 30

ORDER = ["fcfs", "sjf", "srtf", "rr", "prio", "prio-p"]
COLORS = ["#00a2da", "#b8445a", "#23ac6a", "#bd8800", "#8059bb"]
INFO = {
    "fcfs": ("FCFS", "First-Come, First-Served", "Процесорът се дава по реда на пристигане и не се отнема.",
             "без изместване", "подредба: по пристигане"),
    "sjf": ("SJF", "SJF – Shortest Job First", "Избира се процесът с най-кратък CPU burst и се изпълнява докрай.",
            "без изместване", "подредба: по дължина на burst"),
    "srtf": ("SRTF", "SRTF – Shortest Remaining Time First",
             "Избира се най-малкото оставащо време; по-кратък нов процес измества текущия.",
             "с изместване", "подредба: по оставащо време"),
    "rr": ("Round Robin", "Round Robin",
           f"Всеки процес получава квант от {sim.EXAMPLE_QUANTUM} единици, после отива в края на опашката.",
           "с изместване по таймер", "подредба: FIFO"),
    "prio": ("Приоритетно", "Приоритетно планиране",
             "Избира се най-високият приоритет (по-малко число) и се изпълнява докрай.",
             "без изместване", "подредба: по приоритет"),
    "prio-p": ("Приоритетно с изм.", "Приоритетно с изместване",
               "Избира се най-високият приоритет; по-важен нов процес измества текущия.",
               "с изместване", "подредба: по приоритет"),
}


def lighten(hex_color, amount=0.2):
    rgb = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(c + (255 - c) * amount):02x}" for c in rgb)


def display_order(alg, names, remaining):
    if alg == "rr":
        return names
    procs = {p.name: (p, i) for i, p in enumerate(sim.EXAMPLE)}

    def key(n):
        p, i = procs[n]
        if alg in ("sjf", "srtf"):
            return (remaining[n], p.arrival, i)
        if alg in ("prio", "prio-p"):
            return (p.priority, p.arrival, i)
        return (p.arrival, i)
    return sorted(names, key=key)


def events(alg, steps, res, procs):
    by = {p.name: p for p in procs}
    out = []
    for k in range(len(steps) + 1):
        st = steps[k] if k < len(steps) else None
        prev = steps[k - 1] if k else None
        for p in procs:
            if res.completion[p.name] == k:
                out.append({"t": k, "proc": p.name, "text": f"{p.name} завършва · чакане {res.waiting(p)}"})
        for p in procs:
            if p.arrival == k:
                extra = f" · приоритет {p.priority}" if alg.startswith("prio") else ""
                out.append({"t": k, "proc": p.name, "text": f"{p.name} пристига · burst {p.burst}{extra}"})
        if not st:
            continue
        old, new = prev["run"] if prev else None, st["run"]
        preempted = old and old != new and res.completion[old] != k
        if preempted and alg == "rr":
            out.append({"t": k, "proc": old, "text": f"Квантът на {old} изтече → в края на опашката"})
        elif preempted and alg == "srtf":
            out.append({"t": k, "proc": new, "text": f"{new} измества {old}: остават {st['remaining'][new]} < "
                                                      f"{st['remaining'][old]}"})
            continue
        elif preempted and alg == "prio-p":
            out.append({"t": k, "proc": new, "text": f"{new} измества {old}: приоритет {by[new].priority} "
                                                      f"пред {by[old].priority}"})
            continue
        if new and new != old:
            out.append({"t": k, "proc": new, "text": f"{new} получава процесора"})
    return out


def data():
    procs = sim.EXAMPLE
    runs = {}
    for alg in ORDER:
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
            st["ready"] = display_order(alg, st["ready"], st["remaining"])
        short, label, rule, pill, order = INFO[alg]
        runs[alg] = {
            "short": short, "label": label + (f" (q = {q})" if q else ""), "rule": rule,
            "pill": pill, "order": order, "quantum": q, "length": res.length,
            "steps": trace, "gantt": [list(g) for g in res.gantt], "completion": res.completion,
            "switches": res.switches, "events": events(alg, trace, res, procs),
            "metrics": {p.name: {"wait": res.waiting(p), "tat": res.turnaround(p), "resp": res.response(p)}
                        for p in res.procs},
        }
    return {
        "order": ORDER,
        "processes": [{"name": p.name, "arrival": p.arrival, "burst": p.burst, "priority": p.priority,
                       "color": c, "light": lighten(c)} for p, c in zip(procs, COLORS)],
        "runs": runs,
    }


def write_html():
    OUT.mkdir(exist_ok=True)
    payload = json.dumps(data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (SRC / "anim.html").read_text(encoding="utf-8").replace("/*@DATA*/null", payload)
    HTML.write_text(page, encoding="utf-8")
    print(f"{HTML.relative_to(SRC.parents[3])}")


class Chrome:
    """Minimal Chrome DevTools Protocol client over --remote-debugging-pipe (fd 3 in, fd 4 out)."""

    def __init__(self):
        self.profile = tempfile.mkdtemp()
        to_r, to_w = os.pipe()
        from_r, from_w = os.pipe()
        child_in = fcntl.fcntl(to_r, fcntl.F_DUPFD, 10)
        child_out = fcntl.fcntl(from_w, fcntl.F_DUPFD, 10)
        os.close(to_r)
        os.close(from_w)
        actions = [(os.POSIX_SPAWN_DUP2, child_in, 3), (os.POSIX_SPAWN_DUP2, child_out, 4),
                   (os.POSIX_SPAWN_OPEN, 1, "/dev/null", os.O_WRONLY, 0),
                   (os.POSIX_SPAWN_OPEN, 2, "/dev/null", os.O_WRONLY, 0)]
        args = [CHROME, "--headless=new", "--remote-debugging-pipe", "--no-first-run", "--no-default-browser-check",
                "--hide-scrollbars", "--force-color-profile=srgb", f"--user-data-dir={self.profile}", "about:blank"]
        self.pid = os.posix_spawn(CHROME, args, os.environ, file_actions=actions)
        os.close(child_in)
        os.close(child_out)
        self.w = os.fdopen(to_w, "wb", buffering=0)
        self.r = os.fdopen(from_r, "rb", buffering=0)
        self.buf = b""
        self.id = 0
        self.session = None

    def _read(self):
        while b"\0" not in self.buf:
            chunk = self.r.read(1 << 20)
            if not chunk:
                raise RuntimeError("Chrome closed the pipe")
            self.buf += chunk
        msg, self.buf = self.buf.split(b"\0", 1)
        return json.loads(msg)

    def call(self, method, wait_event=None, **params):
        self.id += 1
        msg = {"id": self.id, "method": method, "params": params}
        if self.session and not method.startswith("Target."):
            msg["sessionId"] = self.session
        self.w.write(json.dumps(msg).encode() + b"\0")
        result, seen = None, wait_event is None
        while result is None or not seen:
            m = self._read()
            if m.get("id") == self.id:
                if "error" in m:
                    raise RuntimeError(f"{method}: {m['error']}")
                result = m["result"]
            elif wait_event and m.get("method") == wait_event:
                seen = True
        return result

    def open(self, url, width, height):
        target = self.call("Target.createTarget", url="about:blank")["targetId"]
        self.session = self.call("Target.attachToTarget", targetId=target, flatten=True)["sessionId"]
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=1, mobile=False)
        self.call("Page.enable")
        self.call("Page.navigate", wait_event="Page.loadEventFired", url=url)
        self.eval("document.fonts.ready.then(() => true)")

    def eval(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"])
        return r["result"].get("value")

    def shot(self):
        return base64.b64decode(self.call("Page.captureScreenshot", format="png", optimizeForSpeed=True)["data"])

    def close(self):
        try:
            self.call("Browser.close")
        except RuntimeError:
            pass
        os.waitpid(self.pid, 0)
        shutil.rmtree(self.profile, ignore_errors=True)


def ffmpeg(path):
    return subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS),
                             "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)], stdin=subprocess.PIPE)


def record():
    chrome = Chrome()
    try:
        chrome.open(HTML.as_uri() + "?record", 1920, 1080)
        clips = []
        for i, alg in enumerate(ORDER, 1):
            path = OUT / f"{i}_{alg.replace('-', '_')}.mp4"
            frames = round(chrome.eval(f"durationOf({json.dumps(alg)})") * FPS)
            enc = ffmpeg(path)
            for f in range(frames):
                chrome.eval(f"renderFrame({json.dumps(alg)}, {f / FPS})")
                enc.stdin.write(chrome.shot())
            enc.stdin.close()
            if enc.wait():
                sys.exit(f"ffmpeg failed for {path.name}")
            clips.append(path)
            print(f"{path.relative_to(SRC.parents[3])}: {frames / FPS:.1f} s")
    finally:
        chrome.close()
    listing = OUT / ".concat.txt"
    listing.write_text("".join(f"file '{c.name}'\n" for c in clips))
    allp = OUT / "scheduling_all.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-c", "copy", "-movflags", "+faststart", str(allp)], check=True)
    listing.unlink()
    print(f"{allp.relative_to(SRC.parents[3])}")


def frame(alg, tau, out):
    chrome = Chrome()
    try:
        chrome.open(HTML.as_uri() + "?record", 1920, 1080)
        chrome.eval(f"renderFrame({json.dumps(alg)}, {float(tau)})")
        Path(out).write_bytes(chrome.shot())
    finally:
        chrome.close()


if __name__ == "__main__":
    write_html()
    if "--video" in sys.argv:
        record()
    elif "--frame" in sys.argv:
        i = sys.argv.index("--frame")
        frame(sys.argv[i + 1], sys.argv[i + 2], sys.argv[i + 3])
