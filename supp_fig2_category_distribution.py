"""
Supplementary Figure 2: Distribution of Studies Across Application Categories (N=49)
Publication-quality with Times New Roman font.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt

categories = [
    "Category 1\n(Evaluation &\nBenchmarking)",
    "Category 2\n(Reinforcement\nLearning)",
    "Category 3\n(Multi-Agent\nSystems)",
]
counts = [37, 3, 9]
pcts = [75.5, 6.1, 18.4]
colors = ["#3498DB", "#27AE60", "#E74C3C"]

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

bars = ax.bar(categories, counts, color=colors, edgecolor="white", linewidth=1.2, width=0.5)

for bar, c, p in zip(bars, counts, pcts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
            f"{c} ({p}%)", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color="#2C2C2C")

ax.set_ylabel("Number of Studies", fontsize=12, labelpad=8)
ax.set_title("Distribution of Healthcare LaaJ Studies Across Application Categories (N=49)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_ylim(0, 45)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", labelsize=11)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout()
fig.savefig(f"{out}/Supplementary_Fig2_Category_Distribution.png", dpi=300, bbox_inches="tight")
print("Supp Fig 2 saved.")
plt.close()
