# ASLS Lab 1: logic functions, Boolean algebra, Multisim basics

Handout: [Lab1_2026.pdf](Lab1_2026.pdf). Every answer below is checked by brute force over all input combinations in [verify.py](verify.py) (`python3 III-kurs/ASLS/2026.10.07/verify.py`).

Notation: `·` or juxtaposition = AND, `∨` = OR, `X̄` = NOT X, `⊕` = XOR. Set numbers (номер на набора) read the inputs as a binary number, first variable = most significant bit.

## B1. Simplifying with Boolean algebra

### 1. f1 = AB̄ ∨ AB ∨ ABC ∨ ĀBC (theorem 4)

```
f1 = A(B̄ ∨ B) ∨ ABC ∨ ĀBC          distributive law
   = A·1 ∨ ABC ∨ ĀBC                theorem 4: B ∨ B̄ = 1
   = A ∨ ABC ∨ ĀBC                  theorem 1: A·1 = A
   = A ∨ ĀBC                        absorption: A ∨ A·BC = A
   = A ∨ BC                         reduction law (10): A ∨ ĀX = A ∨ X
```

**f1 = A ∨ BC** (1 on sets 3, 4, 5, 6, 7)

### 2. f2 = A(‾(B ∨ C)‾ ∨ AC)BD ∨ AD (associative + absorption)

The overline covers the whole `B ∨ C`.

```
f2 = A(B̄C̄ ∨ AC)BD ∨ AD             De Morgan: ‾(B ∨ C)‾ = B̄C̄
   = AB̄C̄BD ∨ AACBD ∨ AD             distributive law
   = 0 ∨ ABCD ∨ AD                  B̄B = 0, AA = A (theorems 4, 3), associative/commutative laws
   = AD ∨ AD·BC
   = AD                             absorption: X ∨ X·Y = X
```

**f2 = AD** (1 on sets 9, 11, 13, 15)

### 3. f3 = AB ∨ ĀC ∨ BCD (removing redundant implicants)

```
BCD = BCD(A ∨ Ā) = ABCD ∨ ĀBCD
ABCD is absorbed by AB, ĀBCD is absorbed by ĀC
f3 = AB ∨ ĀC ∨ ABCD ∨ ĀBCD = AB ∨ ĀC
```

(BC is the consensus of AB and ĀC, so every term containing BC is redundant.)

**f3 = AB ∨ ĀC** (1 on sets 2, 3, 6, 7, 12, 13, 14, 15)

### 4. f4 = A(B̄ ∨ C̄) ∨ BC (removing a variable or its inverse)

```
f4 = A·‾(BC)‾ ∨ BC                  De Morgan: B̄ ∨ C̄ = ‾(BC)‾
   = A ∨ BC                         reduction law: X̄·A ∨ X = A ∨ X, with X = BC
```

**f4 = A ∨ BC** (1 on sets 3, 4, 5, 6, 7; same function as f1)

### 5. f5 = AB̄ ∨ BC̄ ∨ B̄C ∨ ĀB (adding a missing variable and its inverse)

```
AB̄ = AB̄(C ∨ C̄) = AB̄C ∨ AB̄C̄
BC̄ = BC̄(A ∨ Ā) = ABC̄ ∨ ĀBC̄
B̄C = B̄C(A ∨ Ā) = AB̄C ∨ ĀB̄C
ĀB = ĀB(C ∨ C̄) = ĀBC ∨ ĀBC̄

f5 = AB̄C ∨ AB̄C̄ ∨ ABC̄ ∨ ĀBC̄ ∨ ĀB̄C ∨ ĀBC        duplicates removed (X ∨ X = X)
   = AB̄(C ∨ C̄) ∨ BC̄(A ∨ Ā) ∨ ĀC(B̄ ∨ B)        regroup in pairs
   = AB̄ ∨ BC̄ ∨ ĀC
```

**f5 = AB̄ ∨ BC̄ ∨ ĀC** (1 on every set except 000 and 111). Grouping the pairs the other way gives the equally minimal **ĀB ∨ B̄C ∨ AC̄**.

### 6. f6 = (A ∨ ĀB)·‾((BC ∨ AC̄)·Ā)‾

The overline covers `(BC ∨ AC̄)·Ā`, which matches the circuit in Fig. 1.13 (U13 = AND, U6A = inverter).

```
A ∨ ĀB = A ∨ B                                   reduction law
(BC ∨ AC̄)·Ā = ĀBC ∨ AĀC̄ = ĀBC                  distributive law, AĀ = 0
‾(ĀBC)‾ = A ∨ B̄ ∨ C̄                              De Morgan
f6 = (A ∨ B)(A ∨ B̄ ∨ C̄)
   = A ∨ B(B̄ ∨ C̄)                                distributive law (OR form): (A ∨ X)(A ∨ Y) = A ∨ XY
   = A ∨ BB̄ ∨ BC̄ = A ∨ BC̄
```

**f6 = A ∨ BC̄** (1 on sets 2, 4, 5, 6, 7)

### 7. Functions set by the lecturer

These are handed out in class. Simplify them the same way, then add them to `verify.py` to check them.

## B2. Multisim

### Shortcuts

- **Inputs:** Place → Sources → DIGITAL_SOURCES → **INTERACTIVE_DIGITAL_CONSTANT** (as in Fig. 1.13). Give each one its own key (double-click → Value → Key: A, B, C, D). By default every input uses Space, so they would all toggle together.
  If the switches from Fig. 1.10 are required: Basic → SWITCH → **SPDT**, common pin to the gate, one throw to VCC through 1 kΩ, the other to GND. Again, one key per switch.
- **Outputs:** Indicators → **PROBE**. It lights above 2.5 V and has a single pin.
- **Power:** real TTL chips (7408N, 7400N, …) have hidden VCC/GND pins. Put one **VCC** (5 V) and one **GND** anywhere on the sheet; no wiring needed. When placing a chip, choose section A.
- **74LS266N (XNOR) is open-collector.** If its probe never lights, add a 1 kΩ pull-up resistor from its output to VCC.
- Reuse sheets: copy them, or right-click a gate → **Replace components**.

### 1. Six two-input gates (Fig. 1.10)

Inputs A and B go to 7408N (AND), 7400N (NAND), 7432N (OR), 7402N (NOR), 74S86D (XOR) and 74LS266N (XNOR), with one probe per output. Run the simulation and step through 00, 01, 10, 11.

| A | B | AND | NAND | OR | NOR | XOR | XNOR |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 0 | 1 | 0 | 0 | 1 |

### 2. Circuits from Fig. 1.11

**(a)** OUT = (X1 ⊕ X2) ⊕ X3, two 74S86D. This is a **3-bit odd-parity generator** (схема за проверка по нечетност): the output is 1 when an odd number of inputs are 1.

| X1 X2 X3 | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| OUT | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 1 |

**(b)** OUT = ‾(X1 ⊕ X2) ⊕ (X3 ⊕ X4)‾, two 74S86D + one 74LS266N. This is a **4-bit even-parity checker** (схема за проверка по четност): the output is 1 when an even number of inputs are 1 (0, 2 or 4).

| X1X2 \ X3X4 | 00 | 01 | 10 | 11 |
|---|---|---|---|---|
| **00** | 1 | 0 | 0 | 1 |
| **01** | 0 | 1 | 1 | 0 |
| **10** | 0 | 1 | 1 | 0 |
| **11** | 1 | 0 | 0 | 1 |

OUT = 1 on sets 0, 3, 5, 6, 9, 10, 12, 15.

### 3. AND, NAND, OR, NOR with Word Generator and Logic Analyzer (Fig. 1.12)

1. From the Instruments toolbar (right side), place the **Word Generator (XWG1)** and the **Logic Analyzer (XLA1)**.
2. Word-generator bit 0 → input B of every gate, bit 1 → input A of every gate (gates: 7408N, 7400N, 7432N, 7402N).
3. Logic Analyzer: channels 1–2 → the two generator bits; channels 3–6 → the four gate outputs. Give the wires different colours; the traces take the wire colour.
4. Double-click the Word Generator → **Set…** → **Up counter**, buffer size **4** → Accept. This generates 00, 01, 10, 11. Set the frequency to about 1 kHz.
5. Logic Analyzer → Clock **Set…** → internal clock rate about 10 kHz (around 10× the generator rate).
6. Start the simulation, click **Cycle** on the Word Generator and take a screenshot of the analyzer. The waveforms match the truth table in B2.1 (AND high only for 11, NAND its inverse, OR low only for 00, NOR its inverse).

### 4. XOR and XNOR with Word Generator and Logic Analyzer

Same setup as task 3 with 74S86D and 74LS266N (remember the pull-up on the 74LS266N). The fastest way is to put all six gates on the task-3 sheet and use analyzer channels 7–8. XOR is high for 01 and 10; XNOR is high for 00 and 11.

### 5. f6 in Multisim (Fig. 1.13)

1. Three interactive digital constants A, B, C (keys A, B, C).
2. The original circuit, as in the figure: U4A = Ā, U9 = Ā·B, U8 = A ∨ ĀB, U10 = B·C, U5A = C̄, U11 = A·C̄, U12 = BC ∨ AC̄, U13 = (BC ∨ AC̄)·Ā, U6A = inverter, U14 = U8 · U6A → probe 1.
3. The minimized form **f6 = A ∨ BC̄** on the same inputs: one 7404N (C̄), one AND2 (B·C̄), one OR2 (A ∨ BC̄) → probe 2.
4. Step through all 8 combinations; both probes match on every row.

| A B C | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| f6 (circuit) | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
| A ∨ BC̄ (minimized) | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |

The minimized circuit uses 3 gates instead of 11.
