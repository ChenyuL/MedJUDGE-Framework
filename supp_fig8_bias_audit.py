"""
Supplementary Figure 8: Bias Testing Audit Card (N=49)
Publication-quality with Times New Roman font.
CORRECTED: Positional=6.1%, Demographic(Race)=2.0%, Format=0%, per Table 2.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

dimensions = [
    "Positional Bias",
    "Cross-Specialty",
    "Self-Enhancement",
    "Length / Verbosity",
    "Format Bias",
    "Demographic (Race)",
    "Demographic (Gender)",
    "Demographic (SES)",
    "Severity Calibration",
    "Temporal Stability",
]
pcts = [6.1, 6.1, 4.1, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0]
risk_levels = ["HIGH", "HIGH", "CRITICAL", "MEDIUM", "MEDIUM",
               "CRITICAL", "CRITICAL", "CRITICAL", "HIGH", "HIGH"]
risk_colors = {"CRITICAL": "#8B0000", "HIGH": "#E74C3C", "MEDIUM": "#F39C12"}
bar_colors = ["#F39C12", "#F39C12", "#E74C3C", "#F7DC6F", "#F7DC6F",
              "#E74C3C", "#E74C3C", "#E74C3C", "#F39C12", "#F39C12"]

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

y_pos = np.arange(len(dimensions))
bars = ax.barh(y_pos, pcts, color=bar_colors, edgecolor="white", height=0.55)

ax.set_yticks(y_pos)
ax.set_yticklabels(dimensions, fontsize=11)
ax.invert_yaxis()
ax.set_xlabel("Studies Conducting Testing (%)", fontsize=12, labelpad=8)
ax.set_title("Bias Testing Audit Card: Critical Gaps in Healthcare LaaJ Validation (N=49)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlim(0, 28)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for i, (p, risk) in enumerate(zip(pcts, risk_levels)):
    if p > 0:
        ax.text(p + 0.3, i, f"{p}%", va="center", fontsize=10, color="#2C2C2C")
    ax.text(24, i, risk, va="center", ha="center", fontsize=9, fontweight="bold",
            color="white",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=risk_colors[risk], edgecolor="none"))

ax.text(24, -0.8, "RISK LEVEL", ha="center", fontsize=10, fontweight="bold", color="#8B0000")

legend_elements = [
    Patch(facecolor="#8B0000", label="Critical Risk"),
    Patch(facecolor="#E74C3C", label="High Risk"),
    Patch(facecolor="#F39C12", label="Medium Risk"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=9,
          title="Clinical Risk if Untested", title_fontsize=10, framealpha=0.9)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout()
fig.savefig(f"{out}/Supplementary_Fig8_Bias_Testing_Audit.png", dpi=300, bbox_inches="tight")
print("Supp Fig 8 saved.")
plt.close()
