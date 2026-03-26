"""
Supplementary Figure 7: Validation Rigor Gaps in Healthcare LaaJ (N=49)
Publication-quality with Times New Roman font.
CORRECTED: Panel A: 1-4=22(44.9%), 5-19=9(18.4%). Panel B: GPT=36, Claude=6, Gemini=4.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.patch.set_facecolor("#FFFFFF")
fig.suptitle("Validation Rigor Gaps in Healthcare LaaJ (N=49)",
             fontsize=15, fontweight="bold", y=0.98)

# ── Panel A: Expert Validator Distribution ──
ax = axes[0, 0]
cats_a = ["0 experts", "1\u20134 experts", "5\u201319 experts", "\u226520 experts"]
vals_a = [13, 22, 9, 5]
pcts_a = [26.5, 44.9, 18.4, 10.2]
colors_a = ["#E74C3C", "#F39C12", "#3498DB", "#27AE60"]
bars_a = ax.barh(cats_a, vals_a, color=colors_a, edgecolor="white", height=0.5)
for bar, v, p in zip(bars_a, vals_a, pcts_a):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"{v} ({p}%)", va="center", fontsize=10)
ax.set_xlabel("Number of Studies", fontsize=11)
ax.set_title("A. Expert Validator Distribution", fontsize=12, fontweight="bold", loc="left")
ax.set_xlim(0, 30)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.axvline(x=3, color="#F39C12", linestyle="--", linewidth=1, alpha=0.7)
ax.text(3.5, 3.5, "Median = 3\nexperts", fontsize=9, color="#F39C12", style="italic")

# ── Panel B: Judge Model Family Concentration ──
ax = axes[0, 1]
models = ["GPT/OpenAI", "Claude", "Llama", "Gemini", "Mistral", "DeepSeek", "Med-Specialized"]
vals_b = [36, 6, 8, 4, 3, 3, 6]
pcts_b = [73.5, 12.2, 16.3, 8.2, 6.1, 6.1, 12.2]
colors_b = ["#E74C3C", "#3498DB", "#3498DB", "#3498DB", "#3498DB", "#3498DB", "#3498DB"]
bars_b = ax.barh(models, pcts_b, color=colors_b, edgecolor="white", height=0.5)
for bar, v, p in zip(bars_b, vals_b, pcts_b):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f"{p}% (n={v})", va="center", fontsize=9)
ax.set_xlabel("Studies Using Model Family (%)", fontsize=11)
ax.set_title("B. Judge Model Family Concentration", fontsize=12, fontweight="bold", loc="left")
ax.set_xlim(0, 90)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(70, 0.5, "MONOCULTURE\nRISK", fontsize=10, fontweight="bold",
        color="#E74C3C", ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF5F5", edgecolor="#E74C3C"))

# ── Panel C: Deployment Readiness Gap ──
ax = axes[1, 0]
deploy_cats = ["Research Only", "Demo / Prototype", "Deployed"]
deploy_vals = [44, 4, 1]
deploy_pcts = [89.8, 8.2, 2.0]
deploy_colors = ["#F39C12", "#3498DB", "#27AE60"]
bars_c = ax.barh(deploy_cats, deploy_pcts, color=deploy_colors, edgecolor="white", height=0.4)
for bar, v, p in zip(bars_c, deploy_vals, deploy_pcts):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f"{p}% (n={v})", va="center", fontsize=10)
ax.set_xlabel("Percentage of Studies (%)", fontsize=11)
ax.set_title("C. Deployment Readiness Gap", fontsize=12, fontweight="bold", loc="left")
ax.set_xlim(0, 100)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(50, -0.6, "Despite ICC up to 0.818\nin validation studies",
        fontsize=9, color="#C0392B", style="italic")

# ── Panel D: Reproducibility Indicators ──
ax = axes[1, 1]
repro_cats = ["Code\nAvailable", "Data\nAvailable", "Prompt\nTemplates", "Model Version\nReported"]
repro_pcts = [49, 71, 40, 20]
repro_colors = ["#3498DB", "#27AE60", "#F39C12", "#E74C3C"]
bars_d = ax.bar(repro_cats, repro_pcts, color=repro_colors, edgecolor="white", width=0.5)
for bar, p in zip(bars_d, repro_pcts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"{p}%", ha="center", fontsize=11, fontweight="bold", color="#2C2C2C")
ax.axhline(y=100, color="#E74C3C", linestyle="--", linewidth=1, alpha=0.5)
ax.text(3.5, 101, "Ideal", fontsize=9, color="#E74C3C", style="italic")
ax.set_ylabel("Percentage of Studies (%)", fontsize=11)
ax.set_title("D. Reproducibility Indicators", fontsize=12, fontweight="bold", loc="left")
ax.set_ylim(0, 110)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(f"{out}/Supplementary_Fig7_Validation_Rigor_Gaps.png", dpi=300, bbox_inches="tight")
print("Supp Fig 7 saved.")
plt.close()
