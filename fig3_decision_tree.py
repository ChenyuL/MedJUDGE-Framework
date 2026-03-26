"""
Figure 3: Paradigm Selection Decision Tree for Healthcare LaaJ
Updated to align with MedJUDGE framework structure:
  - MedJUDGE Gateway (risk tier) integrated as entry point
  - 3 paradigms only (Table 1): pointwise, pairwise, agent-based
  - CoT treated as adaptation method, not separate paradigm
  - Risk-tier annotations on each outcome
  - MedJUDGE requirements footer
Publication-quality with Times New Roman font.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

C = {
    "bg":       "#FFFFFF",
    "start":    "#2C3E50",
    "diamond":  "#5B7FA5",
    "no_lbl":   "#C0392B",
    "yes_lbl":  "#27864A",
    "arrow":    "#4A4A4A",
    "text":     "#2C2C2C",
    "subtext":  "#5A5A5A",
    "gateway":  "#6C3FA0",
    "gw_bg":    "#F3EEFA",
    "out1_bg":  "#E8F4EC", "out1_bdr": "#5A9E6F",
    "out2_bg":  "#FFF8E7", "out2_bdr": "#C4A946",
    "out3_bg":  "#FDECEB", "out3_bdr": "#C97A75",
    "out4_bg":  "#EDE8F5", "out4_bdr": "#8B7BB8",
    "footer":   "#F7F8FA",
    "tier_a":   "#27864A",
    "tier_b":   "#D4850A",
    "tier_c":   "#C0392B",
}

fig, ax = plt.subplots(figsize=(10, 11.5))
fig.patch.set_facecolor(C["bg"]); ax.set_facecolor(C["bg"])
ax.set_xlim(0.5, 10.5); ax.set_ylim(0.5, 15); ax.axis("off")

def rounded_box(ax, x, y, w, h, text, fc, ec, fontsize=11,
                fontweight="normal", subtext=None, text_color=None, radius=0.15,
                extra_line=None, extra_color=None):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=1.2, zorder=3)
    ax.add_patch(box)
    tc = text_color or C["text"]
    dy = 0.15 if subtext else 0
    if extra_line:
        dy = 0.25
    ax.text(x, y + dy, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, color=tc, zorder=4, linespacing=1.3)
    if subtext:
        sub_y = y - 0.05 if extra_line else y - h/2 + 0.3
        ax.text(x, sub_y, subtext, ha="center", va="center",
                fontsize=8.5, color=C["subtext"], zorder=4, style="italic", linespacing=1.25)
    if extra_line:
        ax.text(x, y - h/2 + 0.22, extra_line, ha="center", va="center",
                fontsize=8, color=extra_color or C["tier_c"], zorder=4,
                fontweight="bold", linespacing=1.2)

def diamond(ax, cx, cy, w, h, text, fc, ec):
    verts = np.array([[cx, cy + h/2], [cx + w/2, cy],
                       [cx, cy - h/2], [cx - w/2, cy], [cx, cy + h/2]])
    poly = plt.Polygon(verts, closed=True, facecolor=fc, edgecolor=ec, linewidth=1.2, zorder=3)
    ax.add_patch(poly)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=9.5, color="#FFFFFF", fontweight="bold", zorder=4, linespacing=1.2)

def arrow_v(ax, x1, y1, x2, y2, label=None, label_color=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=C["arrow"], linewidth=1.3), zorder=2)
    if label:
        ax.text((x1+x2)/2 - 0.3, (y1+y2)/2, label, ha="center", va="center",
                fontsize=10, fontweight="bold", color=label_color or C["text"], zorder=5)

def arrow_h(ax, x1, y1, x2, y2, label=None, label_color=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=C["arrow"], linewidth=1.3), zorder=2)
    if label:
        ax.text((x1+x2)/2, y1 + 0.2, label, ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=label_color or C["text"], zorder=5)

# ── Title ──
ax.text(5.5, 14.7, "Paradigm Selection Decision Tree for Healthcare LaaJ",
        ha="center", va="center", fontsize=16, fontweight="bold", color=C["text"])

cx = 4.0; rx = 8.2; ow, oh = 3.2, 1.35

# ── 1. Start node ──
rounded_box(ax, cx, 14.0, 3.8, 0.6, "CLINICAL EVALUATION TASK",
            C["start"], C["start"], fontsize=12, fontweight="bold",
            text_color="#FFFFFF", radius=0.25)

# ── 2. MedJUDGE Gateway ──
y_gw = 13.0
arrow_v(ax, cx, 13.7, cx, y_gw + 0.35)
gw_box = FancyBboxPatch((cx - 2.2, y_gw - 0.35), 4.4, 0.7,
    boxstyle="round,pad=0,rounding_size=0.12",
    facecolor=C["gw_bg"], edgecolor=C["gateway"], linewidth=1.5,
    linestyle="--", zorder=3)
ax.add_patch(gw_box)
ax.text(cx, y_gw + 0.1, "MedJUDGE Gateway: Determine Risk Tier (Table 3)",
        ha="center", va="center", fontsize=9.5, fontweight="bold",
        color=C["gateway"], zorder=4)
ax.text(cx, y_gw - 0.15, "Tier A (Low)  \u2192  Tier B (Moderate)  \u2192  Tier C (High)",
        ha="center", va="center", fontsize=8, color=C["subtext"], zorder=4)

# ── 3. Decision 1: structured? ──
y_d1 = 11.5
arrow_v(ax, cx, y_gw - 0.35, cx, y_d1 + 0.6)
diamond(ax, cx, y_d1, 3.0, 1.2,
        "Is the task structured?\n(binary rubric, checklist,\nguideline adherence)",
        C["diamond"], "#3E5F80")

# Outcome 1: Pointwise
rounded_box(ax, rx, y_d1, ow, oh,
            "POINTWISE SCORING",
            C["out1_bg"], C["out1_bdr"], fontsize=11, fontweight="bold",
            subtext="85.7% of studies  |  0.82\u20130.93 agreement\nO(n) cost  |  Best for structured tasks",
            extra_line="All tiers  |  Tier 1 bias audit required",
            extra_color=C["tier_a"])
arrow_h(ax, cx + 1.5, y_d1, rx - ow/2, y_d1, label="YES", label_color=C["yes_lbl"])

# ── 4. Decision 2: comparative? ──
sp = 2.0
y_d2 = y_d1 - sp
arrow_v(ax, cx, y_d1 - 0.6, cx, y_d2 + 0.6, label="NO", label_color=C["no_lbl"])
diamond(ax, cx, y_d2, 3.0, 1.2,
        "Is it comparative?\n(which response\nis better?)",
        C["diamond"], "#3E5F80")

# Outcome 2: Pairwise
rounded_box(ax, rx, y_d2, ow, oh,
            "PAIRWISE COMPARISON",
            C["out2_bg"], C["out2_bdr"], fontsize=11, fontweight="bold",
            subtext="14.3% of studies  |  Variable agreement\nO(n\u00b2) cost  |  Subjective quality",
            extra_line="All tiers  |  Positional bias test critical",
            extra_color=C["tier_b"])
arrow_h(ax, cx + 1.5, y_d2, rx - ow/2, y_d2, label="YES", label_color=C["yes_lbl"])

# ── 5. Decision 3: safety-critical AND complex? ──
y_d3 = y_d2 - sp
arrow_v(ax, cx, y_d2 - 0.6, cx, y_d3 + 0.6, label="NO", label_color=C["no_lbl"])
diamond(ax, cx, y_d3, 3.0, 1.2,
        "Is the task safety-\ncritical AND complex?",
        C["diamond"], "#3E5F80")

# Outcome 3: Agent-based
rounded_box(ax, rx, y_d3, ow, oh,
            "AGENT-BASED\nEVALUATION",
            C["out3_bg"], C["out3_bdr"], fontsize=11, fontweight="bold",
            subtext="12.2% of studies  |  ICC 0.47\u20130.82\n3\u201310\u00d7 cost  |  Modular subtask decomposition",
            extra_line="Tier B/C: error propagation analysis REQUIRED",
            extra_color=C["tier_c"])
arrow_h(ax, cx + 1.5, y_d3, rx - ow/2, y_d3, label="YES", label_color=C["yes_lbl"])

# ── 6. Default fallback: enhanced pointwise ──
y_d4 = y_d3 - 1.7
arrow_v(ax, cx, y_d3 - 0.6, cx, y_d4 + 0.5, label="NO", label_color=C["no_lbl"])
rounded_box(ax, cx, y_d4, 3.8, 1.3,
            "POINTWISE SCORING",
            C["out4_bg"], C["out4_bdr"], fontsize=11, fontweight="bold",
            subtext="with enhanced prompting (CoT, few-shot, G-EVAL)\n8.2% CoT  |  24.5% few-shot  |  8.2% G-EVAL",
            extra_line="Consider upgrade to agent-based for Tier C",
            extra_color=C["gateway"])

# ── 7. MedJUDGE Requirements Footer ──
y_foot = 1.8
foot_h = 1.8
foot_box = FancyBboxPatch((1.0, y_foot - foot_h/2), 8.5, foot_h,
    boxstyle="round,pad=0,rounding_size=0.12",
    facecolor=C["footer"], edgecolor=C["gateway"], linewidth=1.2, zorder=3)
ax.add_patch(foot_box)

ax.text(5.25, y_foot + 0.65, "MedJUDGE Requirements Apply to All Paradigms",
        ha="center", va="center", fontsize=11, fontweight="bold",
        color=C["gateway"], zorder=4)

# Three pillar columns
pillars = [
    ("Pillar 1: Validity", C["tier_a"], [
        "\u2022 Task\u2013paradigm alignment verified",
        "\u2022 Model diversity: judge \u2260 evaluated system",
        "\u2022 Tier C: multi-family judge panel",
    ]),
    ("Pillar 2: Safety", C["tier_b"], [
        "\u2022 Tier 1 bias audit: all 3 tests (all tiers)",
        "\u2022 Tier 2 safety validation (Tier B/C)",
        "\u2022 Adversarial robustness (Tier B/C)",
    ]),
    ("Pillar 3: Accountability", C["gateway"], [
        "\u2022 Expert validation panel (scaled by tier)",
        "\u2022 Monitoring & drift detection",
        "\u2022 Regulatory documentation",
    ]),
]

for i, (title, color, items) in enumerate(pillars):
    x_col = 2.2 + i * 3.0
    ax.text(x_col, y_foot + 0.3, title, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=color, zorder=4)
    for j, item in enumerate(items):
        ax.text(x_col, y_foot + 0.02 - j * 0.25, item, ha="center", va="center",
                fontsize=7, color=C["subtext"], zorder=4)

# Key finding callout
ax.text(5.25, y_foot - 0.75, "Key finding: 85.7% of studies default to pointwise regardless of task \u2014\n"
        "paradigm selection should be driven by task characteristics, not convenience",
        ha="center", va="center", fontsize=7.5, color=C["no_lbl"],
        fontweight="bold", style="italic", zorder=4)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/main"
fig.tight_layout(pad=0.3)
fig.savefig(f"{out}/Fig3_Paradigm_Decision_Tree.png", dpi=300, bbox_inches="tight", facecolor=C["bg"])
fig.savefig(f"{out}/Fig3_Paradigm_Decision_Tree.pdf", dpi=300, bbox_inches="tight", facecolor=C["bg"])
print("Fig 3 (Decision Tree) saved — PNG + PDF.")
plt.close()
