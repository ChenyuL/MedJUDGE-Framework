"""
Supplementary Figure 9: Transparency Gap Radar Chart (N=49)
Publication-quality with Times New Roman font.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt
import numpy as np

categories = [
    "Expert Validator\nCount",
    "Bias\nTesting",
    "Model\nTransparency",
    "Robustness\nTesting",
    "Clinical\nIntegration",
]
N = len(categories)

current = [30, 26.5, 20, 10, 10.2]
required = [100, 100, 100, 100, 100]

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
current += current[:1]
required += required[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
fig.patch.set_facecolor("#FFFFFF")

ax.plot(angles, required, "o--", color="#2C5F7C", linewidth=2, label="Required Standard (Target)")
ax.fill(angles, required, alpha=0.08, color="#2C5F7C")

ax.plot(angles, current, "o-", color="#2C3E50", linewidth=2, label="Current State (N=49 Studies)")
ax.fill(angles, current, alpha=0.25, color="#2C3E50")

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11, fontweight="bold")
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=9, color="#5A5A5A")
ax.set_rlabel_position(30)

ax.set_title("The Transparency Gap in Healthcare LaaJ:\nCurrent State vs. Required Standard (N=49)",
             fontsize=14, fontweight="bold", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=10, framealpha=0.9)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout()
fig.savefig(f"{out}/Supplementary_Fig9_Transparency_Gap_Radar.png", dpi=300, bbox_inches="tight")
print("Supp Fig 9 saved.")
plt.close()
