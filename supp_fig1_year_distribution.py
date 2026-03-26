"""
Supplementary Figure 1: Temporal Distribution of Included Studies (N=49)
Publication-quality with Times New Roman font.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt

years = ["2023", "2024", "2025\u20132026"]
counts = [1, 12, 36]
pcts = [2.0, 24.5, 73.5]
colors = ["#2C3E50", "#1ABC9C", "#D4AC0D"]

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

bars = ax.bar(years, counts, color=colors, edgecolor="white", linewidth=1.2, width=0.55)

for bar, c, p in zip(bars, counts, pcts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
            f"{c}\n({p}%)", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color="#2C2C2C")

ax.set_xlabel("Publication Year", fontsize=12, labelpad=8)
ax.set_ylabel("Number of Studies", fontsize=12, labelpad=8)
ax.set_title("Temporal Distribution: Rapid Emergence of Healthcare LaaJ (N=49)",
             fontsize=14, fontweight="bold", pad=12)
ax.set_ylim(0, max(counts) + 6)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=11)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout()
fig.savefig(f"{out}/Supplementary_Fig1_Year_Distribution.png", dpi=300, bbox_inches="tight")
print("Supp Fig 1 saved.")
plt.close()
