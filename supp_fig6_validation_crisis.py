"""
Supplementary Figure 6: The Validation Crisis — Expert Validators Per Study (N=49)
Publication-quality with Times New Roman font.
CORRECTED: 0=13 (26.5%), 1-4=22 (44.9%), 5-19=9 (18.4%), 20+=5 (10.2%) — sums to 49.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt

bins = ["0\n(AI Only)", "1\u20134\n(Minimal)", "5\u201319\n(Moderate)", "20+\n(Extensive)"]
counts = [13, 22, 9, 5]
pcts = [26.5, 44.9, 18.4, 10.2]
colors = ["#E74C3C", "#F39C12", "#3498DB", "#27AE60"]

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

bars = ax.bar(bins, counts, color=colors, edgecolor="white", linewidth=1.2, width=0.55)

for bar, c, p in zip(bars, counts, pcts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{c}\n({p}%)", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color="#2C2C2C")

ax.annotate("Median Expert Count = 3\n(44.9% of studies use 1\u20134 validators)",
            xy=(1, 21), xytext=(1.8, 17),
            fontsize=10, color="#5A5A5A",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF8E1", edgecolor="#F39C12"),
            arrowprops=dict(arrowstyle="->", color="#888888"))

ax.set_xlabel("Number of Expert Validators Per Study", fontsize=12, labelpad=8)
ax.set_ylabel("Number of Studies", fontsize=12, labelpad=8)
ax.set_title("The Validation Crisis: Scarcity of Human Expert Oversight (N=49)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_ylim(0, 27)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=11)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout()
fig.savefig(f"{out}/Supplementary_Fig6_Validation_Crisis.png", dpi=300, bbox_inches="tight")
print("Supp Fig 6 saved.")
plt.close()
