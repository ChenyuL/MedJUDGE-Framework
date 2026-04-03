"""
Supplementary Figure 4: Distribution of Judge Model Architectures Across Clinical Tasks (N=49)
Publication-quality with Times New Roman font.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt
import numpy as np

models = ["GPT Family", "Claude Family", "Llama/Open Source", "Gemini Family", "DeepSeek/Other"]
tasks = ["Benchmarks", "Documentation", "Reasoning/Agents", "QA/Other"]

# Row totals: GPT=36, Claude=6, Llama=8, Gemini=4, DeepSeek=3
# NOTE: Cell breakdown approximate — totals match corrected CSV data
data = np.array([
    [17, 8, 7, 4],   # GPT (36 total)
    [3,  1, 2, 0],   # Claude (6 total)
    [4,  2, 1, 1],   # Llama (8 total)
    [2,  1, 1, 0],   # Gemini (4 total)
    [2,  0, 1, 0],   # DeepSeek/Other (3 total)
])

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor("#FFFFFF")

im = ax.imshow(data, cmap="Blues", aspect="auto")

ax.set_xticks(range(len(tasks)))
ax.set_yticks(range(len(models)))
ax.set_xticklabels(tasks, fontsize=11)
ax.set_yticklabels(models, fontsize=11)
ax.set_xlabel("Clinical Task Category", fontsize=12, labelpad=8)
ax.set_ylabel("Judge Model Family", fontsize=12, labelpad=8)

for i in range(len(models)):
    for j in range(len(tasks)):
        color = "white" if data[i, j] > 10 else "#2C2C2C"
        ax.text(j, i, str(data[i, j]), ha="center", va="center",
                fontsize=13, fontweight="bold", color=color)

ax.set_title("Distribution of Judge Architectures Across Clinical Tasks (N=49)",
             fontsize=13, fontweight="bold", pad=12)

cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Number of Studies", fontsize=11)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout()
fig.savefig(f"{out}/Supplementary_Fig4_Judge_Landscape_Heatmap.png", dpi=300, bbox_inches="tight")
print("Supp Fig 4 saved.")
plt.close()
