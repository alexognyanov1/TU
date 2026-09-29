# OIP: Subject Rules

> Follows the repo-wide [RULES.md](../../RULES.md). Rules here override it for this subject only.

| | |
| --- | --- |
| **Full name (BG)** | Основи на инженерното проектиране |
| **Full name (EN)** | Fundamentals of Engineering Design |
| **Course / semester** | I-kurs, winter semester (2024) |

## Required language(s) / tools

- **CAD** is the main part of the course (drawings and models). TODO: note which program is used.
- **Python 3** for the programming labs.

## Required techniques / libraries / tools

- CAD: TODO
- Python: `numpy`, `matplotlib`, `scipy` (`scipy.io.wavfile`), `random`.
- Genetic algorithms (population, fitness, selection, crossover, mutation), heatmaps, signal synthesis, FFT, WAV export.

## Not allowed

- TODO (confirm with the lecturer)

## Folder layout

- `I-kurs/OIP/Lab/YYYY.MM.DD/`: scripts plus the files they generate (plots, `.wav`). CAD files go in dated folders too.

## How to run

```sh
pip install numpy matplotlib scipy
python3 I-kurs/OIP/Lab/2024.12.03/audio_signal_synthesis.py
```
