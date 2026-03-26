"""
Supplementary Figure 3: Evaluation Paradigm Distribution (N=49)
Publication-quality with Times New Roman font.
Pointwise (incl. hybrid): 42 (85.7%), Pairwise: 7 (14.3%), Agent-based: 6 (12.2%)
Mutually exclusive slices: Pointwise Only 36, Pairwise Only 7, Hybrid Pointwise+Agent 6.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 12

import matplotlib.pyplot as plt

labels = ["Pointwise Only\n(36 studies)", "Pairwise Only\n(7 studies)",
          "Hybrid\n(Pointwise+Agent)\n(6 studies)"]
sizes = [36, 7, 6]
colors = ["#2C5F7C", "#E74C3C", "#1ABC9C"]
explode = (0.02, 0.05, 0.05)

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("#FFFFFF")

wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, autopct="%1.1f%%", startangle=140,
    colors=colors, explode=explode, textprops={"fontsize": 11},
    pctdistance=0.6, labeldistance=1.15,
)
for t in autotexts:
    t.set_fontsize(12)
    t.set_fontweight("bold")
    t.set_color("white")

ax.set_title("Evaluation Paradigm Distribution (N=49)",
             fontsize=14, fontweight="bold", pad=16)

fig.text(0.5, 0.02,
         "Note: 42 studies (85.7%) used pointwise scoring; 7 (14.3%) pairwise; 6 (12.2%) agent-based.\n"
         "Categories overlap \u2014 some studies employ multiple paradigms.",
         ha="center", fontsize=9, color="#5A5A5A", style="italic")

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/supplementary"
fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig(f"{out}/Supplementary_Fig3_Paradigm_Distribution.png", dpi=300, bbox_inches="tight")
print("Supp Fig 3 saved.")
plt.close()
