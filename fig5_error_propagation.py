"""
Main Figure 4: Error Propagation in Multi-Judge Healthcare LaaJ Systems
Two panels based on Equations 1-4 from the manuscript.
Panel A: Cascaded systems — error accumulation with k judges.
Panel B: Majority voting — effect of error correlation on 3-judge ensemble.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 13

import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5),
                                gridspec_kw={"wspace": 0.32})
fig.patch.set_facecolor("#F7F7F7")
ax1.set_facecolor("#EFEFEF")
ax2.set_facecolor("#EFEFEF")
fig.suptitle("Error Propagation in Multi-Judge Healthcare LaaJ Systems",
             fontsize=16, fontweight="bold", y=1.01)

# ── Panel A: Error Accumulation in Cascaded Systems ──
ks = np.arange(1, 6)

p85 = 0.15  # 85% accuracy
p90 = 0.10  # 90% accuracy

cascade_85_indep = 1 - (1 - p85) ** ks
cascade_90_indep = 1 - (1 - p90) ** ks

r_corr = 0.5
cascade_85_corr = (1 - r_corr) * cascade_85_indep + r_corr * p85

ax1.plot(ks, cascade_85_indep, "o-", color="#8B0000", linewidth=2.5, markersize=9,
         label="85% acc., independent (r=0)")
ax1.plot(ks, cascade_85_corr, "s--", color="#8B0000", linewidth=2.5, markersize=9,
         label="85% acc., correlated (r=0.5)")
ax1.plot(ks, cascade_90_indep, "^-", color="#2C5F7C", linewidth=2.5, markersize=9,
         label="90% acc., independent (r=0)")

# Data labels on key points
for k_i in [1, 3, 5]:
    idx = k_i - 1
    ax1.annotate(f"{cascade_85_indep[idx]:.2f}", (k_i, cascade_85_indep[idx]),
                 textcoords="offset points", xytext=(8, 4), fontsize=9,
                 color="#8B0000", fontweight="bold")
    ax1.annotate(f"{cascade_90_indep[idx]:.2f}", (k_i, cascade_90_indep[idx]),
                 textcoords="offset points", xytext=(8, -12), fontsize=9,
                 color="#2C5F7C", fontweight="bold")

# Healthcare safety threshold
ax1.axhline(y=0.30, color="#C0392B", linestyle=":", linewidth=1.5, alpha=0.8)
ax1.text(1.5, 0.31, "Healthcare Safety Threshold (0.30)",
         fontsize=10, color="#C0392B", style="italic", fontweight="bold",
         bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFF5F5",
                   edgecolor="#C0392B", alpha=0.8))

# Equation callout
ax1.text(0.97, 0.03, "Eq. 1: P = 1 − (1−p)$^k$",
         transform=ax1.transAxes, fontsize=10, ha="right", va="bottom",
         color="#444444", style="italic",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                   edgecolor="#AAAAAA", alpha=0.9))

ax1.set_xlabel("Number of Judges in Cascade (k)", fontsize=13, labelpad=6)
ax1.set_ylabel("P(≥1 error reaches output)", fontsize=13, labelpad=6)
ax1.set_title("A. Error Accumulation in Cascaded Systems",
              fontsize=14, fontweight="bold", loc="left")
ax1.set_xticks(ks)
ax1.set_xlim(0.8, 5.4)
ax1.set_ylim(0, 0.65)
ax1.legend(fontsize=9.5, loc="upper left", framealpha=0.95,
           edgecolor="#CCCCCC")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", alpha=0.3)

# ── Panel B: Majority Voting — Effect of Error Correlation ──
p = 0.15
r_vals = np.linspace(0, 1, 100)

p_indep = 3 * p**2 * (1 - p) + p**3  # ≈ 0.061
p_corr_curve = p_indep + r_vals * (p - p_indep)

ax2.plot(r_vals, p_corr_curve, "-", color="#2C3E50", linewidth=3)
ax2.fill_between(r_vals, p_indep, p_corr_curve, alpha=0.2, color="#2C5F7C")

# Danger zone shading above single-judge error
ax2.fill_between(r_vals, p, 0.18, alpha=0.06, color="#8B0000")
ax2.text(0.5, 0.165, "Worse than single judge", fontsize=9, ha="center",
         color="#8B0000", style="italic", alpha=0.7)

# Reference lines
ax2.axhline(y=p, color="#8B0000", linestyle="--", linewidth=1.5, alpha=0.8)
ax2.text(0.02, p + 0.004, f"Single judge error (p={p})", fontsize=10,
         color="#8B0000", style="italic", fontweight="bold")

ax2.axhline(y=p_indep, color="#27AE60", linestyle="--", linewidth=1.5, alpha=0.8)
ax2.text(0.02, p_indep + 0.004, f"Ideal independent voting ({p_indep:.3f})",
         fontsize=10, color="#27AE60", style="italic", fontweight="bold")

# "Only 20% reduction" annotation at r=0.7
ax2.annotate("Only 20% error\nreduction at 3× cost",
             xy=(0.35, 0.10), fontsize=9, ha="center", color="#555555",
             style="italic",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                       edgecolor="#AAAAAA", alpha=0.9))

# Estimated LLM correlation
r_est = 0.6
p_at_r07 = p_indep + r_est * (p - p_indep)
ax2.axvline(x=r_est, color="#888888", linestyle="--", linewidth=1.2, alpha=0.6)
ax2.plot(r_est, p_at_r07, "D", color="#8B0000", markersize=12, zorder=5,
         markeredgecolor="white", markeredgewidth=1.5)
ax2.annotate(f"r={r_est}: {p_at_r07:.3f}",
             xy=(r_est, p_at_r07), xytext=(r_est - 0.2, p_at_r07 + 0.018),
             fontsize=12, fontweight="bold", color="#8B0000",
             arrowprops=dict(arrowstyle="->", color="#8B0000", lw=1.5))
ax2.text(0.87, 0.04, "Estimated LLM\ncorrelation\n(same training)",
         fontsize=9, color="#5A5A5A", ha="center", style="italic",
         bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                   edgecolor="#CCCCCC", alpha=0.8))

# Equation callout
ax2.text(0.97, 0.03, "Eq. 3–4: P$_{corr}$ ≈ P$_{ind}$ + r(p − P$_{ind}$)",
         transform=ax2.transAxes, fontsize=10, ha="right", va="bottom",
         color="#444444", style="italic",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                   edgecolor="#AAAAAA", alpha=0.9))

ax2.set_xlabel("Error Correlation Between Judges (r)", fontsize=13, labelpad=6)
ax2.set_ylabel("System Error Rate (3-judge majority vote)", fontsize=13, labelpad=6)
ax2.set_title("B. Majority Voting: Effect of Error Correlation",
              fontsize=14, fontweight="bold", loc="left")
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 0.18)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="both", alpha=0.3)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/main"
fig.tight_layout()
fig.savefig(f"{out}/Fig4_Error_Propagation.png", dpi=300, bbox_inches="tight")
print("Fig 4 saved.")
plt.close()
