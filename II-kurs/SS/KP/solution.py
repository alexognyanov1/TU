import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_PATH = os.path.join(OUTPUT_DIR, "solution.docx")

A1, A2 = 3.0, 2.0
a1, a2 = 1.0, 0.5


def generate_plots():
    tau = np.linspace(-6, 6, 1000)

    R11 = (A1**2 / (2 * a1)) * np.exp(-a1 * np.abs(tau))
    R22 = (A2**2 / (2 * a2)) * np.exp(-a2 * np.abs(tau))
    R21 = np.where(
        tau >= 0,
        (A1 * A2 / (a1 + a2)) * np.exp(-a1 * tau),
        (A1 * A2 / (a1 + a2)) * np.exp(a2 * tau),
    )

    fig, axes = plt.subplots(3, 1, figsize=(8, 10))

    axes[0].plot(tau, R11, 'b-', linewidth=2)
    axes[0].set_title(r'$R_{11}(\tau) = \frac{A_1^2}{2a_1} e^{-a_1|\tau|}$', fontsize=14)
    axes[0].set_xlabel(r'$\tau$', fontsize=12)
    axes[0].set_ylabel(r'$R_{11}(\tau)$', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(y=0, color='k', linewidth=0.5)
    axes[0].axvline(x=0, color='k', linewidth=0.5)
    r11_0 = A1**2 / (2 * a1)
    axes[0].annotate(f'R₁₁(0) = {r11_0:.1f}', xy=(0, r11_0),
                     xytext=(1.5, r11_0 * 0.8), fontsize=10,
                     arrowprops=dict(arrowstyle='->', color='red'))

    axes[1].plot(tau, R22, 'r-', linewidth=2)
    axes[1].set_title(r'$R_{22}(\tau) = \frac{A_2^2}{2a_2} e^{-a_2|\tau|}$', fontsize=14)
    axes[1].set_xlabel(r'$\tau$', fontsize=12)
    axes[1].set_ylabel(r'$R_{22}(\tau)$', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='k', linewidth=0.5)
    axes[1].axvline(x=0, color='k', linewidth=0.5)
    r22_0 = A2**2 / (2 * a2)
    axes[1].annotate(f'R₂₂(0) = {r22_0:.1f}', xy=(0, r22_0),
                     xytext=(1.5, r22_0 * 0.8), fontsize=10,
                     arrowprops=dict(arrowstyle='->', color='red'))

    axes[2].plot(tau, R21, 'g-', linewidth=2)
    axes[2].set_title(r'$R_{21}(\tau)$ — Cross-correlation', fontsize=14)
    axes[2].set_xlabel(r'$\tau$', fontsize=12)
    axes[2].set_ylabel(r'$R_{21}(\tau)$', fontsize=12)
    axes[2].grid(True, alpha=0.3)
    axes[2].axhline(y=0, color='k', linewidth=0.5)
    axes[2].axvline(x=0, color='k', linewidth=0.5)
    r21_0 = A1 * A2 / (a1 + a2)
    axes[2].annotate(f'R₂₁(0) = {r21_0:.1f}', xy=(0, r21_0),
                     xytext=(1.5, r21_0 * 0.8), fontsize=10,
                     arrowprops=dict(arrowstyle='->', color='red'))

    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "correlation_plots.png")
    plt.savefig(plot_path, dpi=200, bbox_inches='tight')
    plt.close()

    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 4))
    t = np.linspace(0, 6, 500)
    s1 = A1 * np.exp(-a1 * t)
    s2 = A2 * np.exp(-a2 * t)

    axes2[0].plot(t, s1, 'b-', linewidth=2)
    axes2[0].set_title(r'$S_1(t) = A_1 \cdot e^{-a_1 t}$', fontsize=13)
    axes2[0].set_xlabel('t', fontsize=12)
    axes2[0].set_ylabel(r'$S_1(t)$', fontsize=12)
    axes2[0].grid(True, alpha=0.3)
    axes2[0].set_xlim(-0.5, 6)
    axes2[0].set_ylim(-0.2, A1 + 0.5)
    axes2[0].axhline(y=0, color='k', linewidth=0.5)
    axes2[0].axvline(x=0, color='k', linewidth=0.5)

    axes2[1].plot(t, s2, 'r-', linewidth=2)
    axes2[1].set_title(r'$S_2(t) = A_2 \cdot e^{-a_2 t}$', fontsize=13)
    axes2[1].set_xlabel('t', fontsize=12)
    axes2[1].set_ylabel(r'$S_2(t)$', fontsize=12)
    axes2[1].grid(True, alpha=0.3)
    axes2[1].set_xlim(-0.5, 6)
    axes2[1].set_ylim(-0.2, A2 + 0.5)
    axes2[1].axhline(y=0, color='k', linewidth=0.5)
    axes2[1].axvline(x=0, color='k', linewidth=0.5)

    plt.tight_layout()
    signals_path = os.path.join(OUTPUT_DIR, "signals.png")
    plt.savefig(signals_path, dpi=200, bbox_inches='tight')
    plt.close()

    return plot_path, signals_path


def add_paragraph(doc, text, bold=False, italic=False, size=12, alignment=None, space_after=Pt(6), space_before=Pt(0), font_name='Times New Roman'):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = font_name
    if alignment:
        p.alignment = alignment
    pf = p.paragraph_format
    pf.space_after = space_after
    pf.space_before = space_before
    return p


def add_formula(doc, text, size=12):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.italic = True
    run.font.size = Pt(size)
    run.font.name = 'Cambria Math'
    pf = p.paragraph_format
    pf.space_after = Pt(6)
    pf.space_before = Pt(6)
    return p


def build_document(plot_path, signals_path):
    doc = Document()

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # === TITLE PAGE ===
    for _ in range(4):
        add_paragraph(doc, '', size=12)

    add_paragraph(doc, 'ТЕХНИЧЕСКИ УНИВЕРСИТЕТ', bold=True, size=16,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(4))
    add_paragraph(doc, 'Факултет по електроника и автоматика', size=14,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(24))

    add_paragraph(doc, 'КУРСОВА РАБОТА', bold=True, size=18,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(8))
    add_paragraph(doc, 'по', size=14,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(8))
    add_paragraph(doc, 'Сигнали и Системи', bold=True, size=16,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(30))

    add_paragraph(doc, 'Тема: Корелационни функции на аналогови непериодични сигнали',
                  bold=True, size=13, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(40))

    add_paragraph(doc, 'Изготвил: ......................................', size=12,
                  alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=Pt(8))
    add_paragraph(doc, 'Специалност: ..................................', size=12,
                  alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=Pt(8))
    add_paragraph(doc, 'Фак. №: ..........................................', size=12,
                  alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=Pt(8))
    add_paragraph(doc, 'Група: ............................................', size=12,
                  alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=Pt(8))

    for _ in range(4):
        add_paragraph(doc, '', size=12)

    add_paragraph(doc, 'Оценка: .................    Проверил: .................', size=12,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(12))

    doc.add_page_break()

    # === PAGE 2: ASSIGNMENT ===
    add_paragraph(doc, 'Задание', bold=True, size=14,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(12))

    add_paragraph(doc, 'Дадени са следните аналогови непериодични сигнали:', size=12, space_after=Pt(6))

    add_formula(doc, 'S₁(t) = A₁ · exp(-a₁ · t),    t ≥ 0')
    add_formula(doc, 'S₂(t) = A₂ · exp(-a₂ · t),    t ≥ 0')

    doc.add_picture(signals_path, width=Inches(5.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_paragraph(doc, '', size=6)
    add_paragraph(doc, 'а) Да се определи изразът за автокорелационната функция на първия сигнал.', size=12, space_after=Pt(4))
    add_paragraph(doc, 'б) Да се определи изразът за автокорелационната функция на втория сигнал.', size=12, space_after=Pt(4))
    add_paragraph(doc, 'в) Да се определи изразът за взаимнокорелационната функция на двата сигнала, ако сигналът който се измества във времето е първият сигнал.', size=12, space_after=Pt(4))
    add_paragraph(doc, 'г) Да се начертаят графично получените корелационни функции.', size=12, space_after=Pt(12))

    doc.add_page_break()

    # === PAGE 3+: SOLUTION ===
    add_paragraph(doc, 'Решение', bold=True, size=14,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(12))

    # --- Definitions ---
    add_paragraph(doc, '1. Използвани математически зависимости', bold=True, size=13, space_after=Pt(8), space_before=Pt(12))

    add_paragraph(doc, 'Автокорелационна функция на енергиен сигнал s(t):', size=12, space_after=Pt(4))
    add_formula(doc, 'Rss(τ) = ∫₋∞^∞  s(t) · s(t + τ) dt')

    add_paragraph(doc, 'Взаимнокорелационна функция на два енергийни сигнала:', size=12, space_after=Pt(4))
    add_formula(doc, 'R₂₁(τ) = ∫₋∞^∞  s₂(t) · s₁(t + τ) dt')

    add_paragraph(doc, 'където τ е времевото изместване, а s₁ е сигналът, който се измества.', size=12, space_after=Pt(4))

    add_paragraph(doc, 'Основен интеграл, използван в решението:', size=12, space_after=Pt(4))
    add_formula(doc, '∫₀^∞  e^(-αt) dt = 1/α,    α > 0')
    add_formula(doc, '∫_a^∞  e^(-αt) dt = e^(-αa) / α,    α > 0')

    # --- Task a) ---
    add_paragraph(doc, '2. Задача а) — Автокорелационна функция на S₁(t)', bold=True, size=13, space_after=Pt(8), space_before=Pt(16))

    add_paragraph(doc, 'Даден е сигналът:', size=12, space_after=Pt(4))
    add_formula(doc, 'S₁(t) = A₁ · e^(-a₁t),    t ≥ 0    (иначе S₁(t) = 0)')

    add_paragraph(doc, 'Прилагаме дефиницията за автокорелационна функция:', size=12, space_after=Pt(4))
    add_formula(doc, 'R₁₁(τ) = ∫₋∞^∞  S₁(t) · S₁(t + τ) dt')

    add_paragraph(doc, 'Интегрантът е ненулев само когато и двата аргумента са в областта на определение:', size=12, space_after=Pt(4))
    add_paragraph(doc, '• S₁(t) ≠ 0  ⟹  t ≥ 0', size=12, space_after=Pt(2))
    add_paragraph(doc, '• S₁(t + τ) ≠ 0  ⟹  t + τ ≥ 0  ⟹  t ≥ -τ', size=12, space_after=Pt(8))

    # Case tau >= 0
    add_paragraph(doc, 'Случай 1: τ ≥ 0', bold=True, size=12, space_after=Pt(4), space_before=Pt(8))
    add_paragraph(doc, 'Когато τ ≥ 0, условието t ≥ -τ е автоматично изпълнено за t ≥ 0, така че долната граница е 0:', size=12, space_after=Pt(4))

    add_formula(doc, 'R₁₁(τ) = ∫₀^∞  A₁·e^(-a₁t) · A₁·e^(-a₁(t+τ)) dt')
    add_formula(doc, '= A₁² · e^(-a₁τ) · ∫₀^∞  e^(-2a₁t) dt')
    add_formula(doc, '= A₁² · e^(-a₁τ) · 1/(2a₁)')
    add_formula(doc, '= A₁² / (2a₁) · e^(-a₁τ)')

    # Case tau < 0
    add_paragraph(doc, 'Случай 2: τ < 0', bold=True, size=12, space_after=Pt(4), space_before=Pt(8))
    add_paragraph(doc, 'Когато τ < 0, имаме -τ > 0, така че долната граница е -τ:', size=12, space_after=Pt(4))

    add_formula(doc, 'R₁₁(τ) = ∫₋τ^∞  A₁·e^(-a₁t) · A₁·e^(-a₁(t+τ)) dt')
    add_formula(doc, '= A₁² · e^(-a₁τ) · ∫₋τ^∞  e^(-2a₁t) dt')
    add_formula(doc, '= A₁² · e^(-a₁τ) · e^(-2a₁·(-τ)) / (2a₁)')
    add_formula(doc, '= A₁² · e^(-a₁τ) · e^(2a₁τ) / (2a₁)')
    add_formula(doc, '= A₁² / (2a₁) · e^(a₁τ)')

    add_paragraph(doc, 'Тъй като за τ ≥ 0 имаме e^(-a₁τ), а за τ < 0 имаме e^(a₁τ), и двата случая се обединяват в:', size=12, space_after=Pt(4))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('R₁₁(τ) = A₁² / (2a₁) · e^(-a₁|τ|)')
    run.bold = True
    run.italic = True
    run.font.size = Pt(13)
    run.font.name = 'Cambria Math'
    pf = p.paragraph_format
    pf.space_after = Pt(12)
    pf.space_before = Pt(8)

    # --- Task b) ---
    add_paragraph(doc, '3. Задача б) — Автокорелационна функция на S₂(t)', bold=True, size=13, space_after=Pt(8), space_before=Pt(16))

    add_paragraph(doc, 'Даден е сигналът:', size=12, space_after=Pt(4))
    add_formula(doc, 'S₂(t) = A₂ · e^(-a₂t),    t ≥ 0    (иначе S₂(t) = 0)')

    add_paragraph(doc, 'Процедурата е аналогична на задача а). Прилагаме дефиницията:', size=12, space_after=Pt(4))
    add_formula(doc, 'R₂₂(τ) = ∫₋∞^∞  S₂(t) · S₂(t + τ) dt')

    add_paragraph(doc, 'Случай 1: τ ≥ 0', bold=True, size=12, space_after=Pt(4), space_before=Pt(8))
    add_paragraph(doc, 'Долната граница на интегриране е 0:', size=12, space_after=Pt(4))

    add_formula(doc, 'R₂₂(τ) = ∫₀^∞  A₂·e^(-a₂t) · A₂·e^(-a₂(t+τ)) dt')
    add_formula(doc, '= A₂² · e^(-a₂τ) · ∫₀^∞  e^(-2a₂t) dt')
    add_formula(doc, '= A₂² · e^(-a₂τ) · 1/(2a₂)')
    add_formula(doc, '= A₂² / (2a₂) · e^(-a₂τ)')

    add_paragraph(doc, 'Случай 2: τ < 0', bold=True, size=12, space_after=Pt(4), space_before=Pt(8))
    add_paragraph(doc, 'Долната граница на интегриране е -τ:', size=12, space_after=Pt(4))

    add_formula(doc, 'R₂₂(τ) = ∫₋τ^∞  A₂·e^(-a₂t) · A₂·e^(-a₂(t+τ)) dt')
    add_formula(doc, '= A₂² · e^(-a₂τ) · ∫₋τ^∞  e^(-2a₂t) dt')
    add_formula(doc, '= A₂² · e^(-a₂τ) · e^(2a₂τ) / (2a₂)')
    add_formula(doc, '= A₂² / (2a₂) · e^(a₂τ)')

    add_paragraph(doc, 'Обединявайки двата случая:', size=12, space_after=Pt(4))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('R₂₂(τ) = A₂² / (2a₂) · e^(-a₂|τ|)')
    run.bold = True
    run.italic = True
    run.font.size = Pt(13)
    run.font.name = 'Cambria Math'
    pf = p.paragraph_format
    pf.space_after = Pt(12)
    pf.space_before = Pt(8)

    # --- Task c) ---
    add_paragraph(doc, '4. Задача в) — Взаимнокорелационна функция R₂₁(τ)', bold=True, size=13, space_after=Pt(8), space_before=Pt(16))

    add_paragraph(doc, 'Търсим взаимнокорелационната функция на S₂(t) и S₁(t), където S₁ е сигналът, който се измества във времето:', size=12, space_after=Pt(4))
    add_formula(doc, 'R₂₁(τ) = ∫₋∞^∞  S₂(t) · S₁(t + τ) dt')

    add_paragraph(doc, 'Условия за ненулев интегрант:', size=12, space_after=Pt(4))
    add_paragraph(doc, '• S₂(t) ≠ 0  ⟹  t ≥ 0', size=12, space_after=Pt(2))
    add_paragraph(doc, '• S₁(t + τ) ≠ 0  ⟹  t ≥ -τ', size=12, space_after=Pt(8))

    add_paragraph(doc, 'Случай 1: τ ≥ 0', bold=True, size=12, space_after=Pt(4), space_before=Pt(8))
    add_paragraph(doc, 'Долната граница е max(0, -τ) = 0:', size=12, space_after=Pt(4))

    add_formula(doc, 'R₂₁(τ) = ∫₀^∞  A₂·e^(-a₂t) · A₁·e^(-a₁(t+τ)) dt')
    add_formula(doc, '= A₁·A₂ · e^(-a₁τ) · ∫₀^∞  e^(-(a₁+a₂)t) dt')
    add_formula(doc, '= A₁·A₂ · e^(-a₁τ) · 1/(a₁ + a₂)')
    add_formula(doc, '= A₁·A₂ / (a₁ + a₂) · e^(-a₁τ)')

    add_paragraph(doc, 'Случай 2: τ < 0', bold=True, size=12, space_after=Pt(4), space_before=Pt(8))
    add_paragraph(doc, 'Долната граница е max(0, -τ) = -τ (тъй като -τ > 0):', size=12, space_after=Pt(4))

    add_formula(doc, 'R₂₁(τ) = ∫₋τ^∞  A₂·e^(-a₂t) · A₁·e^(-a₁(t+τ)) dt')
    add_formula(doc, '= A₁·A₂ · e^(-a₁τ) · ∫₋τ^∞  e^(-(a₁+a₂)t) dt')
    add_formula(doc, '= A₁·A₂ · e^(-a₁τ) · e^(-(a₁+a₂)·(-τ)) / (a₁ + a₂)')
    add_formula(doc, '= A₁·A₂ · e^(-a₁τ) · e^((a₁+a₂)τ) / (a₁ + a₂)')
    add_formula(doc, '= A₁·A₂ / (a₁ + a₂) · e^(a₂τ)')

    add_paragraph(doc, 'Крайният резултат:', size=12, space_after=Pt(4))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('R₂₁(τ) = A₁·A₂ / (a₁+a₂) · e^(-a₁τ),    τ ≥ 0')
    run.bold = True
    run.italic = True
    run.font.size = Pt(13)
    run.font.name = 'Cambria Math'
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.space_before = Pt(8)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('R₂₁(τ) = A₁·A₂ / (a₁+a₂) · e^(a₂τ),     τ < 0')
    run.bold = True
    run.italic = True
    run.font.size = Pt(13)
    run.font.name = 'Cambria Math'
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.space_before = Pt(4)

    add_paragraph(doc, 'Забележка: За разлика от автокорелационните функции, взаимнокорелационната функция НЕ е четна. Тя е непрекъсната в τ = 0, където стойността е R₂₁(0) = A₁·A₂/(a₁+a₂), но скоростта на спадане е различна за положителни и отрицателни τ (определя се от a₁ и a₂ съответно).', size=11, italic=True, space_after=Pt(12))

    # --- Task d) Plots ---
    doc.add_page_break()
    add_paragraph(doc, '5. Задача г) — Графики на корелационните функции', bold=True, size=13, space_after=Pt(8), space_before=Pt(4))

    add_paragraph(doc, f'За графичното представяне са използвани следните числени стойности: A₁ = {A1}, A₂ = {A2}, a₁ = {a1}, a₂ = {a2}.', size=12, space_after=Pt(4))

    add_paragraph(doc, 'Стойности в τ = 0 (максимуми на автокорелационните функции):', size=12, space_after=Pt(4))
    add_formula(doc, f'R₁₁(0) = A₁²/(2a₁) = {A1}²/(2·{a1}) = {A1**2/(2*a1):.2f}')
    add_formula(doc, f'R₂₂(0) = A₂²/(2a₂) = {A2}²/(2·{a2}) = {A2**2/(2*a2):.2f}')
    add_formula(doc, f'R₂₁(0) = A₁·A₂/(a₁+a₂) = {A1}·{A2}/({a1}+{a2}) = {A1*A2/(a1+a2):.2f}')

    doc.add_picture(plot_path, width=Inches(5.8))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_paragraph(doc, 'Фиг. 1. Графики на автокорелационните функции R₁₁(τ), R₂₂(τ) и взаимнокорелационната функция R₂₁(τ).', size=10, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(12))

    add_paragraph(doc, 'От графиките се наблюдава:', size=12, space_after=Pt(4))
    add_paragraph(doc, '• Автокорелационните функции R₁₁(τ) и R₂₂(τ) са четни (симетрични спрямо τ = 0) и имат максимум при τ = 0, което е характерно свойство на автокорелационните функции.', size=12, space_after=Pt(2))
    add_paragraph(doc, '• Взаимнокорелационната функция R₂₁(τ) НЕ е четна — скоростта на спадане е различна за τ > 0 (определя се от a₁) и за τ < 0 (определя се от a₂).', size=12, space_after=Pt(2))
    add_paragraph(doc, '• Всички корелационни функции спадат експоненциално към нула за |τ| → ∞.', size=12, space_after=Pt(12))

    # --- Appendix: Source code ---
    doc.add_page_break()
    add_paragraph(doc, 'Приложение — Програмен код (Python)', bold=True, size=13,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(12))

    add_paragraph(doc, 'За генериране на графиките е използван следният Python код:', size=12, space_after=Pt(8))

    code_text = '''import numpy as np
import matplotlib.pyplot as plt

A1, A2 = 3.0, 2.0
a1, a2 = 1.0, 0.5
tau = np.linspace(-6, 6, 1000)

# Autocorrelation R11
R11 = (A1**2 / (2*a1)) * np.exp(-a1 * np.abs(tau))

# Autocorrelation R22
R22 = (A2**2 / (2*a2)) * np.exp(-a2 * np.abs(tau))

# Cross-correlation R21
R21 = np.where(
    tau >= 0,
    (A1*A2 / (a1+a2)) * np.exp(-a1 * tau),
    (A1*A2 / (a1+a2)) * np.exp(a2 * tau),
)

fig, axes = plt.subplots(3, 1, figsize=(8, 10))
axes[0].plot(tau, R11, 'b-', linewidth=2)
axes[0].set_title('R11(tau)')
axes[0].grid(True)

axes[1].plot(tau, R22, 'r-', linewidth=2)
axes[1].set_title('R22(tau)')
axes[1].grid(True)

axes[2].plot(tau, R21, 'g-', linewidth=2)
axes[2].set_title('R21(tau)')
axes[2].grid(True)

plt.tight_layout()
plt.savefig("correlation_plots.png", dpi=200)
plt.show()'''

    p = doc.add_paragraph()
    run = p.add_run(code_text)
    run.font.size = Pt(9)
    run.font.name = 'Consolas'
    pf = p.paragraph_format
    pf.space_after = Pt(6)

    doc.save(DOCX_PATH)
    print(f"Document saved to: {DOCX_PATH}")


if __name__ == "__main__":
    plot_path, signals_path = generate_plots()
    build_document(plot_path, signals_path)
    print("Done!")
