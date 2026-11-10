#!/usr/bin/env python3
"""Renders the two КА lab 3 reports from the simulator screenshots in screens/."""
import base64
import subprocess
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
SCREENS = SRC / "screens"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DATE = "04.11.2026"
STAGES = 5

KEYS = ["clocks", "inst", "cpi", "sf", "busy", "data", "ctrl", "sync"]
LABELS = ["Clocks (тактове)", "Inst. Count (инструкции)", "CPI", "SF (Speed-up Factor)",
          "Busy Stages", "Data Hazards", "Control Hazards", "Inst. Syncs"]


def run(*values):
    return dict(zip(KEYS, values))


NO_PIPE = run(46, 8, 5.75, 0.87, 0, 0, 0, 1)
NO_BUBBLES = run(18, 8, 2.25, 2.22, 0, 0, 0, 1)
NOP = run(19, 9, 2.11, 2.37, 0, 0, 0, 2)
BUBBLES = run(19, 8, 2.38, 2.1, 2, 2, 0, 1)
FORWARD = run(16, 8, 2.0, 2.5, 0, 0, 0, 1)
LOOP = run(224, 44, 5.09, 0.98, 0, 0, 0, 1)
UNROLLED = run(242, 44, 5.5, 0.91, 0, 0, 0, 1)
REARRANGED = run(39, 7, 5.57, 0.9, 0, 0, 0, 1)
PREDICTION = run(480, 219, 2.19, 2.28, 474, 102, 39, 19)
LOOP_BYTES = 33
UNROLLED_BYTES = 234

for r in (NO_PIPE, NO_BUBBLES, NOP, BUBBLES, FORWARD, LOOP, UNROLLED, REARRANGED, PREDICTION):
    assert abs(r["cpi"] - r["clocks"] / r["inst"]) < 0.0051, r
    assert abs(r["sf"] - r["inst"] * STAGES / r["clocks"]) < 0.051, r


def bg(x, d=2):
    return f"{x:.{d}f}".rstrip("0").rstrip(".").replace(".", ",") if d else str(round(x))


def pct(old, new):
    return bg(abs(old - new) / old * 100, 1) + "%"


FW_GAIN = pct(BUBBLES["clocks"], FORWARD["clocks"])
PIPE_GAIN = bg(NO_PIPE["clocks"] / BUBBLES["clocks"])
UNROLL_LOSS = pct(LOOP["clocks"], UNROLLED["clocks"])
SIZE_RATIO = bg(UNROLLED_BYTES / LOOP_BYTES, 1)
LOOP_LONG = (LOOP["clocks"] - STAGES * LOOP["inst"]) // 2
UNROLLED_LONG = (UNROLLED["clocks"] - STAGES * UNROLLED["inst"]) // 2

HANDOUT_T1 = "MOV #1, R01\nMOV #5, R03\nMOV #3, R01\nADD R01, R03\nHLT"
EXECUTED_T1 = "MOV #1, R02\nMOV #1, R01\nMOV #5, R03\nMOV #5, R03\nMOV #3, R04\nMOV #3, R01\nADD R01, R03\nHLT"
SRC_T3 = "program Pipeline_Ex4_1\n  for n = 1 to 8\n    t = t + 1\n  next\nend"
SRC_T4 = "program Pipleine_Ex5_1\n  a = 1\n  b = a\n  c = 2\nend"
SRC_T5 = "program Pipeline_Ex6\n  i = 0\n  for p = 1 to 40\n    i = i + 1\n    if i = 10 then\n      i = 0\n      r = i\n    end if\n  next\nend"
ORDER_NATURAL = "MOV #1, R03\nMOV R03, R01\nMOV R01, R04\nMOV R04, R02\nMOV #2, R05\nMOV R05, R03\nHLT"
ORDER_SHOWN = "MOV #1, R03\nMOV R03, R01\nMOV R01, R04\nMOV #2, R05\nMOV R04, R02\nMOV R05, R03\nHLT"


def code(text, title=None):
    head = f"<div class='codet'>{title}</div>" if title else ""
    return f"<div class='codebox'>{head}<pre class='code'>{text}</pre></div>"


def table(head, rows, cls="sim"):
    th = "".join(f"<th>{c}</th>" for c in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def stats(columns, extra=()):
    """columns: list of (heading, run dict); extra: rows appended below the statistics."""
    def cell(v):
        return bg(v) if isinstance(v, float) else v
    rows = [[lab] + [cell(r[k]) for _, r in columns] for lab, k in zip(LABELS, KEYS)]
    return table(["Показател"] + [h for h, _ in columns], rows + list(extra))


class Figures:
    def __init__(self):
        self.n = 0

    def __call__(self, name, caption):
        self.n += 1
        data = base64.b64encode((SCREENS / name).read_bytes()).decode()
        return (f'<figure><img src="data:image/png;base64,{data}">'
                f'<figcaption>Фиг. {self.n}. {caption}</figcaption></figure>')


def section(p, title, figures, tbl, text):
    parts = [tbl, figures] if p["stats_first"] else [figures, tbl]
    return f"<h3>{title}</h3>" + p.get("lead", {}).get(title, "") + "".join(parts) + text


def build(p):
    fig = Figures()
    t1_stats = stats(
        [("Без конвейер", NO_PIPE), ("Без мехури", NO_BUBBLES), ("Без мехури + NOP", NOP), ("С мехури", BUBBLES)],
        [["R03", "8", "<b>6</b>", "8", "8"]])
    t1_figs = (
        fig("t1_no_pipeline.png", "„No instruction pipeline“: последователно изпълнение")
        + fig("t1_no_bubbles.png", "„Do not insert bubbles“: конвейер без изчакване")
        + fig("t1_nop.png", "„Do not insert bubbles“ и вмъкната инструкция NOP")
        + fig("t1_bubbles.png", "Конвейер с автоматично вмъкване на мехури"))
    t2_stats = stats([("С мехури", BUBBLES), ("С operand forwarding", FORWARD)])
    t2_figs = fig("t2_forwarding.png", "Включен operand forwarding (маркировка FW във времедиаграмата)")
    t3_stats = stats([("Цикъл (test4)", LOOP), ("Loop unrolling (Test42)", UNROLLED)],
                     [["Размер на кода, байтове", LOOP_BYTES, UNROLLED_BYTES],
                      ["Време за изпълнение", "22,573 s", "24,456 s"]])
    t3_figs = (fig("t3_loop.png", "Pipeline_Ex4_1 (в симулатора test4) с цикъл")
               + fig("t3_unrolled.png", "Pipeline_Ex4_2 (в симулатора Test42) с loop unrolling"))
    t4_stats = stats([("Пренаредена последователност (zadabc)", REARRANGED)])
    t4_figs = fig("t4_rearranged.png", "Пренаредена инструкционна последователност, режим „No instruction pipeline“")
    t5_stats = stats([("С jump prediction", PREDICTION)])
    t5_figs = fig("t5_jump_prediction.png", "Pipeline_Ex6 (в симулатора testlast) с jump prediction и таблицата Jump Predict Table")
    jpt = table(["V", "JInstAddr", "JTarget", "PStat", "Count"], [[1, 69, 99, 2, 17]])

    body = f"""
<header class="top">
  <div class="uni">Технически университет – София, ФКСТ</div>
  <table class="meta">
    <tr><td>Дисциплина:</td><td>„Компютърни архитектури“</td><td></td><td></td></tr>
    <tr><td>Специалност:</td><td>„КСИ“, III курс (V семестър), гр. 43</td><td>Дата:</td><td>{DATE}</td></tr>
    <tr><td>Студент:</td><td class="fill">{p["name"]}</td><td>Фак. №</td><td class="fill">{p["fn"]}</td></tr>
  </table>
</header>
<h1>Отчет по проведено лабораторно упражнение № 3<br><span>„Изследване на конвейерни компютърни архитектури (Част 2)“</span></h1>
<p><b>Цел:</b> {p["goal"]}</p>
{section(p, "1. Изследване на 5-фазен линеен конвейер", t1_figs, t1_stats, p["t1"])}
{section(p, "2. Operand forwarding", t2_figs, t2_stats, p["t2"])}
{section(p, "3. Loop unrolling", t3_figs, t3_stats, p["t3"])}
{section(p, "4. Re-arranging instruction sequence", t4_figs, t4_stats, p["t4"])}
{section(p, "5. Jump prediction", t5_figs, t5_stats + jpt, p["t5"])}
<h3>Обобщени изводи</h3>
{p["concl"]}
"""
    html = f"<!doctype html><html lang='bg'><head><meta charset='utf-8'><style>{p['css']}</style></head><body>{body}</body></html>"
    src = OUT / f"{p['file']}.html"
    src.write_text(html, encoding="utf-8")
    pdf = OUT / f"{p['file']}.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    src.unlink()
    print(pdf)


BASE_CSS = """
@page { size: A4; margin: 18mm 18mm 18mm 20mm; }
body { margin: 0; }
table { border-collapse: collapse; margin: 8px auto 10px; page-break-inside: avoid; }
td, th { padding: 3px 9px; text-align: center; }
table.sim td:first-child { text-align: left; }
figure { page-break-inside: avoid; text-align: center; margin: 8px 0; }
figure img { max-width: 100%; max-height: 80mm; }
.codes { display: flex; gap: 22px; justify-content: center; align-items: flex-start; page-break-inside: avoid; }
.codebox { page-break-inside: avoid; }
.codet { text-align: center; font-size: 90%; margin-top: 6px; }
pre.code { margin: 6px auto; padding: 6px 12px; width: fit-content; }
h1, h2, h3, h4 { page-break-after: avoid; }
p, li { text-align: justify; }
"""

CLASSIC = BASE_CSS + """
body { font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 1.35; color: #000; }
.uni { text-align: center; font-weight: bold; font-size: 15pt; color: #555; letter-spacing: .3px; margin-bottom: 8px; }
.meta { width: 100%; margin: 0; border-bottom: 2px solid #000; }
.meta td { text-align: left; padding: 2px 6px; }
.meta td.fill { background: #ccffff; font-weight: bold; }
h1 { font-size: 14pt; font-weight: normal; text-align: center; margin: 18px 0 14px; }
h1 span { font-weight: bold; font-style: italic; }
h3 { background: #cc99ff; padding: 2px 30px; font-size: 12pt; margin: 14px 0 8px; }
table.sim td, table.sim th { border: 1px solid #000; }
table.sim td { background: #ccffff; }
table.sim td:first-child { background: #fff; }
pre.code { font-family: "Courier New", monospace; border: 1px solid #000; }
figcaption { font-style: italic; font-size: 11pt; }
figure img { border: 1px solid #000; }
"""

MODERN = BASE_CSS + """
body { font-family: "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.5; color: #1f2933; }
.top { background: #0f4c5c; color: #fff; padding: 12px 16px; border-radius: 8px; }
.uni { font-size: 13pt; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 6px; }
.meta { width: 100%; margin: 0; color: #e0f2f1; }
.meta td { text-align: left; padding: 1px 4px; }
.meta td.fill { color: #fff; font-weight: 700; border-bottom: 1px solid #f4a259; }
h1 { font-size: 15pt; font-weight: 300; margin: 18px 0 12px; color: #0f4c5c; border-left: 5px solid #f4a259; padding-left: 12px; }
h1 span { font-weight: 700; }
h3 { font-size: 12pt; color: #fff; background: #5f0f40; padding: 4px 10px; border-radius: 4px; margin: 16px 0 8px; }
table.sim th { background: #0f4c5c; color: #fff; font-weight: 600; }
table.sim td { border-bottom: 1px solid #d9e2ec; }
table.sim tbody tr:nth-child(even) td { background: #f0f7f7; }
pre.code { font-family: Menlo, monospace; font-size: 9.5pt; background: #102a43; color: #e0f2f1; border-radius: 6px; }
figcaption { font-size: 9.5pt; color: #627d98; margin-top: 4px; }
figure img { border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,.25); }
"""

CODES_T1 = "<div class='codes'>" + code(HANDOUT_T1, "по заданието") + code(EXECUTED_T1, "изпълнено в симулатора") + "</div>"
CODES_T4 = "<div class='codes'>" + code(SRC_T4, "изходен код") + code(ORDER_NATURAL, "преди пренареждане") + code(ORDER_SHOWN, "след пренареждане") + "</div>"

ALEKS = dict(
    file="KA_LU3_Aleks_Ognyanov_121224052", name="Алекс Огнянов", fn="121224052", css=CLASSIC, stats_first=False,
    goal="Изследване и оптимизация на комуникиращите си процеси в конвейерни компютърни архитектури в условията на конвейерни състезания.",
    lead={
        "1. Изследване на 5-фазен линеен конвейер": CODES_T1 + f"<p>Очакваната стойност на R03 е 8 (5 + 3). Изпълнената в симулатора последователност съдържа три допълнителни инструкции спрямо заданието (MOV #1, R02, повторен MOV #5, R03 и MOV #3, R04), които не променят логиката на изчислението в R03. Програмата е изследвана последователно в четири режима.</p>",
        "3. Loop unrolling": code(SRC_T3),
        "4. Re-arranging instruction sequence": CODES_T4,
        "5. Jump prediction": code(SRC_T5),
    },
    t1=f"""<ul>
<li><b>Без конвейер.</b> Инструкциите се изпълняват строго последователно за {NO_PIPE["clocks"]} такта (CPI = 5,75, SF = 0,87). Резултатът е очакваният, R03 = 8.</li>
<li><b>„Do not insert bubbles“.</b> ADD R01, R03 чете операндите си в същия такт, в който MOV #3, R01 е във фаза Execute, т.е. преди записа в R01. Прочита се старата стойност 1 и R03 = 5 + 1 = 6. Резултатът е грешен, макар изпълнението да е най-кратко за конвейера без оптимизации ({NO_BUBBLES["clocks"]} такта).</li>
<li><b>С NOP.</b> Инструкцията NOP отмества четенето на R01 с един такт, така че то съвпада с фазата Write Result на MOV #3, R01. Резултатът отново е R03 = 8, с цена 19 такта и една допълнителна инструкция.</li>
<li><b>С мехури.</b> Симулаторът сам вмъква мехури: Data Hazards = 2 и Busy Stages = 2. Първият мехур е при втората MOV #5, R03, а вторият задържа ADD R01, R03 до записа на R01. Резултатът е R03 = 8 за 19 такта. Спрямо режима без конвейер времето намалява {PIPE_GAIN} пъти.</li>
</ul>
<p>Следователно NOP и автоматичните мехури дават едно и също време (19 такта), но мехурите не изискват промяна на програмата. По-ниската стойност на CPI при NOP (2,11 срещу 2,38) се дължи единствено на по-големия брой инструкции.</p>""",
    t2=f"""<p>С включен operand forwarding резултатът от изпълнението се подава директно на следващата инструкция, без да се изчаква записът в регистъра. Конфликтите по данни и заетите етапи изчезват (от 2 на 0), R03 остава 8, а времето намалява от 19 на 16 такта, т.е. с {FW_GAIN}. CPI спада от 2,38 на 2, а SF нараства от 2,1 на 2,5. Това е единственият изследван режим, който едновременно запазва коректния резултат и скъсява изпълнението.</p>""",
    t3=f"""<p>Генерираният код е {LOOP_BYTES} байта при цикъла и {UNROLLED_BYTES} байта при loop unrolling, т.е. {SIZE_RATIO} пъти по-голям. И при двете програми се изпълняват по 44 инструкции. Цикълът се превежда до CMP, JGT, две инструкции ADD и JMP на итерация, а развитият вариант повтаря тялото без преходи, но с повече инструкции MOV за t = t + 1.</p>
<p>И двете програми са изпълнени в режим „No instruction pipeline“, затова Control Hazards = 0. В този режим Test42 е с {UNROLL_LOSS} по-бавен (242 срещу 224 такта). Разликата съответства на {UNROLLED_LONG} срещу {LOOP_LONG} удължени фази Fetch, тъй като всички останали инструкции отнемат по 5 такта. В конвейерен режим очакването е премахването на JGT и JMP да намали конфликтите по управление, срещу което се заплаща с по-голям код.</p>""",
    t4=f"""<p>В снетата последователност независимата инструкция MOV #2, R05 е преместена между зависимите MOV R01, R04 и MOV R04, R02. Логиката на програмата не се променя, защото MOV #2, R05 не чете и не записва R01, R04 и R02, а всички променливи получават същите стойности. Целта на пренареждането е да раздели зависимите инструкции, така че между записа и четенето на R04 да има допълнителен такт и да се вмъкват по-малко мехури.</p>""",
    t5=f"""<p>Записите в Jump Predict Table са: V (валиден запис), JInstAddr (адрес на инструкцията за преход), JTarget (адрес на целта), PStat (състояние на предсказването) и Count (брой обръщения към записа). Единственият запис е за JNE 99 на логически адрес 69, който прескача тялото на условието „if i = 10“ и се извършва при 9 от 10 итерации. При включено предсказване симулаторът показва CPI = 2,19 и SF = 2,28, при 102 конфликта по данни и 39 конфликта по управление.</p>""",
    concl=f"""<ul>
<li>Конвейерът ускорява изпълнението {PIPE_GAIN} пъти спрямо последователното, но без защита от зависимостите по данни резултатът е грешен (R03 = 6 вместо 8).</li>
<li>Мехурите и NOP запазват коректността с цена 19 такта, а operand forwarding я запазва и намалява времето на 16 такта (CPI = 2).</li>
<li>Loop unrolling увеличава кода {SIZE_RATIO} пъти, а ползата му се проявява при работещ конвейер чрез отпадане на конфликтите по управление.</li>
<li>Пренареждането на инструкции не променя логиката на програмата и раздалечава зависимите инструкции, а Jump Predict Table съхранява адреса, целта и състоянието на всеки предсказван преход.</li>
</ul>""",
)

YORDAN = dict(
    file="KA_LU3_Yordan_Nachev_121224053", name="Йордан Начев", fn="121224053", css=MODERN, stats_first=True,
    goal="Да се изследват конвейерните състезания и да се оцени доколко operand forwarding, loop unrolling, пренареждането на инструкции и jump prediction намаляват влиянието им.",
    lead={
        "1. Изследване на 5-фазен линеен конвейер": CODES_T1 + "<p>При правилно изпълнение очаквам R03 = 3 + 5 = 8. Освен инструкциите от заданието програмата в симулатора съдържа MOV #1, R02, втора MOV #5, R03 и MOV #3, R04. Те не влияят на крайната стойност на R03.</p>",
        "3. Loop unrolling": code(SRC_T3),
        "4. Re-arranging instruction sequence": CODES_T4,
        "5. Jump prediction": code(SRC_T5),
    },
    t1=f"""<ol>
<li>Последователното изпълнение отнема най-много време: {NO_PIPE["clocks"]} такта при CPI = 5,75. Стойността на R03 е 8.</li>
<li>Когато забраних мехурите, програмата завърши за {NO_BUBBLES["clocks"]} такта, но R03 стана 6. От времедиаграмата се вижда, че ADD чете R01 един такт преди MOV #3, R01 да запише новата стойност, така че събира 5 със старата единица.</li>
<li>След добавянето на NOP между двете инструкции четенето и записът на R01 попадат в един и същ такт и R03 отново е 8. Времето нараства до 19 такта, а инструкциите стават 9.</li>
<li>При включени мехури конвейерът сам изчаква: симулаторът отчита 2 конфликта по данни и 2 заети етапа. R03 = 8 за 19 такта, което е {PIPE_GAIN} пъти по-бързо от изпълнението без конвейер.</li>
</ol>
<p>Сравнението показва, че NOP решава проблема ръчно със същата цена като автоматичните мехури.</p>""",
    t2=f"""<p>Operand forwarding подава резултата към зависимата инструкция веднага след фазата Execute. Така мехурите отпадат напълно: 16 такта срещу 19 ({FW_GAIN} по-малко), Data Hazards и Busy Stages са 0, а CPI = 2 и SF = 2,5. Във времедиаграмата пренасочването е означено с FW. Стойността на R03 остава коректна.</p>""",
    t3=f"""<p>Размерът на кода нараства от {LOOP_BYTES} на {UNROLLED_BYTES} байта ({SIZE_RATIO} пъти). Броят на изпълнените инструкции случайно съвпада и е 44 и в двата случая, но времето е 224 такта за цикъла и 242 за развития вариант ({UNROLL_LOSS} повече). CPI е 5,09 и 5,5, а SF е 0,98 и 0,91.</p>
<p>Важно е, че и двете стартирания са направени с отметка „No instruction pipeline“. Преходите тогава не създават конфликти (Control Hazards = 0), така че това сравнение отчита само цената на по-дългия код: при Test42 има {UNROLLED_LONG} фази Fetch от по 3 такта, а при цикъла {LOOP_LONG}. Очакваната полза от loop unrolling е при работещ конвейер, където отпадат JGT и JMP.</p>""",
    t4=f"""<p>Компилаторът премества MOV #2, R05 между MOV R01, R04 и MOV R04, R02. Тази инструкция не използва регистрите на зависимата двойка, затова смисълът на програмата е същият: a = 1, b = 1, c = 2. Преместването осигурява допълнителен такт между записа и четенето на R04 и така намалява нуждата от мехури.</p>""",
    t5=f"""<p>Таблицата Jump Predict Table пази за всеки предсказван преход дали записът е валиден (V), адреса на самия преход (JInstAddr), адреса на целта (JTarget), състоянието на предсказването (PStat) и броя обръщения (Count). При мен има един запис: 69 → 99, PStat = 2, Count = 17. Той съответства на JNE 99 от условието „if i = 10“. Този преход се извършва 9 пъти от 10, затова е удобен за предсказване.</p>
<p>При включено предсказване симулаторът показва 480 такта, 219 инструкции, CPI = 2,19, SF = 2,28, Data Hazards = 102 и Control Hazards = 39.</p>""",
    concl=f"""<ol>
<li><b>Коректност:</b> без изчакване зависимостта по R01 дава R03 = 6. NOP, мехурите и operand forwarding възстановяват R03 = 8.</li>
<li><b>Бързодействие:</b> 46 такта без конвейер, 19 с мехури и 16 с operand forwarding, което е най-добрият измерен резултат.</li>
<li><b>Loop unrolling:</b> кодът е {SIZE_RATIO} пъти по-голям, а при изключен конвейер времето нараства с {UNROLL_LOSS}.</li>
<li><b>Пренареждане и jump prediction:</b> пренареждането запазва логиката на програмата и раздалечава зависимите инструкции, а Jump Predict Table съхранява адреса, целта и състоянието на всеки предсказван преход.</li>
</ol>""",
)

for person in (ALEKS, YORDAN):
    build(person)
