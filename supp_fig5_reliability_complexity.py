"""
Supplementary Figure 5: Reliability vs. Complexity Tradeoff (N=22)
Publication-quality with Times New Roman font.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt
import numpy as np

# Study data: (name, complexity_x, agreement_y, category_color_idx)
studies = [
    ("Heilmeyer", 0.05, 0.93, 0),
    ("Raju et al.", 0.08, 0.92, 0),
    ("LLMEval-Med", 0.25, 0.92, 0),
    ("Croxford (npj)\nFleiss/ICC", 0.22, 0.82, 0),
    ("DOCLENS", 0.0, 0.81, 0),
    ("Brake & Schaaf", 0.9, 0.79, 1),
    ("Wada et al.", 1.05, 0.82, 1),
    ("Zhu et al.", 0.85, 0.74, 1),
    ("FineRadScore", 1.1, 0.75, 1),
    ("De la Iglesia", 1.15, 0.72, 1),
    ("Madrid-Garcia", 0.9, 0.63, 1),
    ("ChatCLIDS", 1.85, 0.88, 2),
    ("MAGI", 2.15, 0.87, 2),
    ("MedQA-CS", 2.2, 0.80, 2),
    ("SDBench (Nori)", 1.9, 0.70, 2),
    ("Healthcare Agent", 1.85, 0.68, 2),
    ("Szymanski", 2.15, 0.68, 2),
    ("HealthBench", 2.18, 0.67, 2),
    ("Wang (Safety)", 1.88, 0.60, 2),
    ("Wilhelm", 1.88, 0.43, 2),
    ("MedHELM", 2.2, 0.47, 2),
]

colors_map = {0: "#3498DB", 1: "#27AE60", 2: "#E74C3C"}

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#F8F8F8")

for name, x, y, cat in studies:
    ax.scatter(x, y, c=colors_map[cat], s=80, zorder=5, edgecolors="white", linewidth=0.5)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(6, 4),
                fontsize=7, color="#2C2C2C", zorder=6)

ax.axhline(y=0.70, color="#C0392B", linestyle="--", linewidth=1.2, alpha=0.7, zorder=3)
ax.text(0.0, 0.705, "Human Agreement Ceiling", fontsize=9, color="#C0392B", style="italic")

for i, (label, xmin, xmax) in enumerate([
    ("Structured\n(Extraction/Formatting)", -0.2, 0.6),
    ("Semi-Structured\n(Summaries/Reports)", 0.6, 1.4),
    ("Complex Reasoning\n(Diagnosis/Psychiatry)", 1.4, 2.4),
]):
    ax.axvspan(xmin, xmax, alpha=0.05, color=colors_map[i], zorder=1)

ax.set_xlim(-0.3, 2.5)
ax.set_ylim(0.0, 1.05)
ax.set_xticks([0.2, 1.0, 1.9])
ax.set_xticklabels(["Structured\n(Extraction/Formatting)",
                     "Semi-Structured\n(Summaries/Reports)",
                     "Complex Reasoning\n(Diagnosis/Psychiatry)"],
                    fontsize=10)
ax.set_ylabel("Agreement Score (Normalized)", fontsize=12, labelpad=8)
ax.set_xlabel("Task Complexity", fontsize=12, labelpad=8)
ax.set_title("The Reliability vs. Complexity Trade-Off (N=22)",
             fontsize=14, fontweight="bold", pad=12)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.text(0.98, 0.02,
         "Judge reliability limited\nby human consensus\n(MedHELM: clinician ICC = 0.43)",
         ha="right", fontsize=8, color="#5A5A5A", style="italic",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#F0F0F0", edgecolor="#CCCCCC"))

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout()
fig.savefig(f"{out}/Supplementary_Fig5_Reliability_Complexity_Tradeoff.png", dpi=300, bbox_inches="tight")
print("Supp Fig 5 saved.")
plt.close()
