#!/usr/bin/env python3
"""CPU scheduling simulator: FCFS, SJF, SRTF, Round Robin, priority (non-preemptive,
preemptive and non-preemptive with aging).

Time is discrete (one unit per step). For every algorithm the simulator returns the
Gantt chart and, per process, completion, turnaround, waiting and response time.

  python3 sim.py                      # examples and experiments used in the реферат
  python3 sim.py procs.csv [-q 4]     # own workload: lines "name,arrival,burst,priority"

Conventions:
  * smaller priority number = higher priority;
  * ties are broken by arrival time, then by input order;
  * in Round Robin a process that arrives at the same moment its predecessor's
    quantum expires joins the queue before the preempted process;
  * SRTF and preemptive priority preempt only on a strictly better candidate;
  * aging raises a waiting process by one priority level per AGING_STEP units in the ready queue.
"""
import random
import sys
from collections import deque
from dataclasses import dataclass, field

ALGORITHMS = {
    "fcfs": "FCFS",
    "sjf": "SJF",
    "srtf": "SRTF",
    "rr": "Round Robin",
    "prio": "Приоритетно (без изместване)",
    "prio-p": "Приоритетно (с изместване)",
    "prio-a": "Приоритетно със стареене",
}
AGING_STEP = 50


@dataclass
class Proc:
    name: str
    arrival: int
    burst: int
    priority: int = 0
    index: int = 0


@dataclass
class Result:
    gantt: list = field(default_factory=list)
    completion: dict = field(default_factory=dict)
    first_run: dict = field(default_factory=dict)
    switches: int = 0
    procs: list = field(default_factory=list)

    def turnaround(self, p):
        return self.completion[p.name] - p.arrival

    def waiting(self, p):
        return self.turnaround(p) - p.burst

    def response(self, p):
        return self.first_run[p.name] - p.arrival

    def avg(self, metric):
        return sum(getattr(self, metric)(p) for p in self.procs) / len(self.procs)

    def worst(self, metric):
        return max(getattr(self, metric)(p) for p in self.procs)

    @property
    def length(self):
        return self.gantt[-1][2] if self.gantt else 0

    @property
    def cs_time(self):
        return sum(e - s for n, s, e in self.gantt if n == "CS")


def simulate(procs, alg, quantum=None, cs_cost=0):
    if alg not in ALGORITHMS:
        raise ValueError(f"unknown algorithm: {alg}")
    if alg == "rr" and not quantum:
        raise ValueError("Round Robin needs a quantum")
    procs = [Proc(p.name, p.arrival, p.burst, p.priority, i) for i, p in enumerate(procs)]
    pending = deque(sorted(procs, key=lambda p: (p.arrival, p.index)))
    remaining = {p.name: p.burst for p in procs}
    ready = deque()
    since = {}
    res = Result(procs=procs)
    current, last, used, cs_left, t = None, None, 0, 0, 0

    def key(p):
        if alg in ("sjf", "srtf"):
            return (remaining[p.name], p.arrival, p.index)
        if alg in ("prio", "prio-p"):
            return (p.priority, p.arrival, p.index)
        if alg == "prio-a":
            return (p.priority - (t - since[p.name]) // AGING_STEP, p.arrival, p.index)
        return (p.arrival, p.index)

    def record(name):
        if res.gantt and res.gantt[-1][0] == name and res.gantt[-1][2] == t:
            res.gantt[-1][2] = t + 1
        else:
            res.gantt.append([name, t, t + 1])

    while pending or ready or current:
        while pending and pending[0].arrival <= t:
            since[pending[0].name] = t
            ready.append(pending.popleft())

        if current and cs_left == 0:
            preempt = False
            if alg == "rr":
                preempt = used >= quantum
            elif alg == "srtf" and ready:
                preempt = key(min(ready, key=key)) < key(current)
            elif alg == "prio-p" and ready:
                preempt = min(p.priority for p in ready) < current.priority
            if preempt:
                since[current.name] = t
                ready.append(current)
                current = None

        if current is None and ready:
            if alg == "rr":
                current = ready.popleft()
            else:
                current = min(ready, key=key)
                ready.remove(current)
            used = 0
            if last is not None and current is not last:
                res.switches += 1
                cs_left = cs_cost

        if current is None:
            record(None)
        elif cs_left:
            record("CS")
            cs_left -= 1
        else:
            record(current.name)
            res.first_run.setdefault(current.name, t)
            remaining[current.name] -= 1
            used += 1
            last = current
            if remaining[current.name] == 0:
                res.completion[current.name] = t + 1
                current = None
        t += 1

    res.gantt = [tuple(g) for g in res.gantt]
    return res


EXAMPLE = [
    Proc("P1", 0, 8, 3),
    Proc("P2", 1, 4, 1),
    Proc("P3", 2, 9, 4),
    Proc("P4", 3, 5, 2),
    Proc("P5", 4, 2, 5),
]

CONVOY_LONG_FIRST = [Proc("P1", 0, 24), Proc("P2", 0, 3), Proc("P3", 0, 3)]
CONVOY_SHORT_FIRST = [Proc("P2", 0, 3), Proc("P3", 0, 3), Proc("P1", 0, 24)]

EXAMPLE_QUANTUM = 3
QUANTA = [1, 2, 4, 8, 16, 32, 64, 128, 256]
CS_COST = 1


def workload(n=200, seed=2026):
    """Mixed load: 80 % short interactive bursts (2-20), 20 % long CPU-bound bursts (50-200)."""
    rnd = random.Random(seed)
    procs, t = [], 0
    for i in range(n):
        t += int(rnd.expovariate(1 / 38))
        burst = rnd.randint(2, 20) if rnd.random() < 0.8 else rnd.randint(50, 200)
        procs.append(Proc(f"P{i + 1}", t, burst, rnd.randint(1, 8)))
    return procs


def runs(procs, quantum):
    order = [("fcfs", None), ("sjf", None), ("srtf", None), ("rr", quantum), ("prio", None), ("prio-p", None),
             ("prio-a", None)]
    return [(alg, q, simulate(procs, alg, q)) for alg, q in order]


def label(alg, q):
    return f"{ALGORITHMS[alg]} (q = {q})" if q else ALGORITHMS[alg]


def gantt_text(res):
    return " ".join(f"[{s}–{e} {n or 'idle'}]" for n, s, e in res.gantt)


def print_table(procs, res):
    print(f"  {'Процес':<7}{'Пристигане':>11}{'Burst':>7}{'Приор.':>7}{'Край':>6}{'Обраб.':>8}{'Чакане':>8}{'Отговор':>9}")
    for p in res.procs:
        print(f"  {p.name:<7}{p.arrival:>11}{p.burst:>7}{p.priority:>7}{res.completion[p.name]:>6}"
              f"{res.turnaround(p):>8}{res.waiting(p):>8}{res.response(p):>9}")
    print(f"  средно: обработка {res.avg('turnaround'):.2f}, чакане {res.avg('waiting'):.2f}, "
          f"отговор {res.avg('response'):.2f}, превключвания {res.switches}")


def print_summary(procs, quantum):
    print(f"  {'Алгоритъм':<34}{'ср. обраб.':>11}{'ср. чакане':>11}{'ср. отговор':>12}{'макс. чакане':>13}{'превкл.':>9}")
    for alg, q, res in runs(procs, quantum):
        print(f"  {label(alg, q):<34}{res.avg('turnaround'):>11.2f}{res.avg('waiting'):>11.2f}"
              f"{res.avg('response'):>12.2f}{res.worst('waiting'):>13}{res.switches:>9}")


def quantum_sweep(procs):
    rows = []
    for q in QUANTA:
        res = simulate(procs, "rr", q, CS_COST)
        rows.append((q, res.avg("turnaround"), res.avg("response"), res.switches, 100 * res.cs_time / res.length))
    return rows


def main(argv):
    if len(argv) > 1 and argv[1] not in ("-q",):
        quantum = int(argv[argv.index("-q") + 1]) if "-q" in argv else EXAMPLE_QUANTUM
        procs = []
        with open(argv[1], encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    name, arrival, burst, *prio = [x.strip() for x in line.split(",")]
                    procs.append(Proc(name, int(arrival), int(burst), int(prio[0]) if prio else 0))
        for alg, q, res in runs(procs, quantum):
            print(f"\n{label(alg, q)}\n  {gantt_text(res)}")
            print_table(procs, res)
        return

    print("Ефект на конвоя (FCFS):")
    for procs in (CONVOY_LONG_FIRST, CONVOY_SHORT_FIRST):
        res = simulate(procs, "fcfs")
        print(f"  {gantt_text(res)}  средно чакане {res.avg('waiting'):.2f}")

    print(f"\nОбщ пример, q = {EXAMPLE_QUANTUM}:")
    for alg, q, res in runs(EXAMPLE, EXAMPLE_QUANTUM):
        print(f"\n{label(alg, q)}\n  {gantt_text(res)}")
        print_table(EXAMPLE, res)

    load = workload()
    total = sum(p.burst for p in load)
    print(f"\nСмесено натоварване: {len(load)} процеса, общо {total} единици CPU време, "
          f"последно пристигане {load[-1].arrival}")
    for q in (4, 20):
        print(f"\nq = {q}:")
        print_summary(load, q)

    print(f"\nRound Robin при различен квант, цена на превключването {CS_COST}:")
    print(f"  {'q':>5}{'ср. обраб.':>12}{'ср. отговор':>13}{'превкл.':>9}{'загуба %':>10}")
    for q, tat, resp, sw, loss in quantum_sweep(load):
        print(f"  {q:>5}{tat:>12.2f}{resp:>13.2f}{sw:>9}{loss:>10.2f}")


if __name__ == "__main__":
    main(sys.argv)
