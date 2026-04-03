"""
Figure 1: PRISMA 2020 Flow Diagram (Main Figure 1)
Matches the original PowerPoint layout.
Publication-quality with Times New Roman font.
"""
import matplotlib
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["font.size"] = 18

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

C = {
    "bg": "#FFFFFF", "text": "#2C2C2C", "subtext": "#5A5A5A",
    "arrow": "#4A4A4A", "phase": "#3B6E9E", "phase_bg": "#E3EEF7",
    "phase_bdr": "#3B6E9E", "box_bg": "#FFFFFF", "box_bdr": "#4A4A4A",
    "grey_bg": "#F7F3E8", "grey_bdr": "#B8A04A",
    "inc_bg": "#EAF4EA", "inc_bdr": "#3A6B3A",
    "search_bg": "#FDF6E3", "search_bdr": "#B8A04A",
    "excl": "#8B0000", "excl_bg": "#FFF5F5",
}

fig, ax = plt.subplots(figsize=(16, 14))
fig.patch.set_facecolor(C["bg"]); ax.set_facecolor(C["bg"])
ax.set_xlim(0, 14); ax.set_ylim(0, 14); ax.axis("off")

def rbox(x, y, w, h, fc, ec, lw=1.6, radius=0.12, zorder=3, linestyle="-"):
    box = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=linestyle, zorder=zorder)
    ax.add_patch(box); return box

def phase_label(x, y, h, text):
    rbox(x, y, 1.1, h, C["phase_bg"], C["phase_bdr"], lw=1.6, zorder=2)
    ax.text(x + 0.55, y + h/2, text, ha="center", va="center",
            fontsize=20, fontweight="bold", color=C["phase"], rotation=90, zorder=3)

def flow_box(x, y, w, h, text, fc=None, ec=None, fontsize=16, fontweight="normal",
             linestyle="-"):
    rbox(x, y, w, h, fc or C["box_bg"], ec or C["box_bdr"], zorder=3, linestyle=linestyle)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color=C["text"], linespacing=1.15, fontweight=fontweight, zorder=4)

def arr_down(x1, y1, x2, y2, label=None, label_side="left"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=C["arrow"], linewidth=1.6,
                                shrinkA=2, shrinkB=2), zorder=2)
    if label:
        off = -0.15 if label_side == "left" else 0.15
        ha = "right" if label_side == "left" else "left"
        ax.text((x1+x2)/2 + off, (y1+y2)/2, label, ha=ha, va="center",
                fontsize=15, color=C["excl"], style="italic", fontweight="bold", zorder=4)

def arr_horiz(x1, y, x2):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=C["arrow"], linewidth=1.6,
                                shrinkA=2, shrinkB=2), zorder=2)

# ── Layout constants ──
lcx = 2.2            # left column x
bw = 4.6             # main box width
bh = 0.65            # standard box height
bh2 = 0.85           # 2-line box height
rcx = 8.5            # right column x
rw = 4.0             # right box width
vgap = 0.30          # vertical gap between rows

# Title
ax.text(7.0, 13.5, "PRISMA 2020 Flow Diagram", ha="center", va="center",
        fontsize=24, fontweight="bold", color=C["text"])

# ═══════════════════════════════════════════
# ROW 0: Records identified (GREEN) + Search Strategy
# ═══════════════════════════════════════════
r0_h = 1.3
r0_y = 11.8
flow_box(lcx, r0_y, bw, r0_h,
         "Records identified from databases\nSources: Ovid MEDLINE, Ovid EMBASE,\n"
         "Scopus, Web of Science, ACM, IEEE Xplore\n(n = 12,379)",
         fc=C["inc_bg"], ec=C["inc_bdr"], fontsize=15)

# Search strategy (top right)
ss_x, ss_w, ss_h = rcx, rw, 1.3
rbox(ss_x, r0_y, ss_w, ss_h, C["search_bg"], C["search_bdr"], lw=1.6, zorder=3)
ax.text(ss_x + ss_w/2, r0_y + ss_h - 0.25, "Search Strategy:",
        ha="center", va="center", fontsize=17, fontweight="bold", color=C["text"], zorder=4)
ax.text(ss_x + ss_w/2, r0_y + ss_h/2 - 0.15,
        '"(LLM OR large language model OR\nlanguage model OR NLP) AND\n'
        '(Evaluator OR evaluation OR judge\nOR reviewer OR LLM-as-a-judge)"',
        ha="center", va="center", fontsize=13, color=C["subtext"],
        style="italic", linespacing=1.15, zorder=4)

# ═══════════════════════════════════════════
# ROW 1: Records without duplicates + Excluded by keyword
# ═══════════════════════════════════════════
r1_y = r0_y - vgap - bh
arr_down(lcx + bw/2, r0_y, lcx + bw/2, r1_y + bh,
         label="Remove duplicates (n = 652)", label_side="left")

flow_box(lcx, r1_y, bw, bh, "Records without duplicates (n = 11,727)", fontsize=17)

# Exclusion: keyword filtering (right, same row)
r1_mid = r1_y + bh/2
excl_kw_h = bh2
flow_box(rcx, r1_mid - excl_kw_h/2, rw, excl_kw_h,
         "Records excluded by keyword\nfiltering (n = 11,006)",
         fc=C["excl_bg"], ec=C["excl"], fontsize=16)
arr_horiz(lcx + bw + 0.15, r1_mid, rcx - 0.15)

# ═══════════════════════════════════════════
# ROW 2: Title/abstract screening + Grey literature search
# ═══════════════════════════════════════════
r2_y = r1_y - vgap - bh
arr_down(lcx + bw/2, r1_y, lcx + bw/2, r2_y + bh)

flow_box(lcx, r2_y, bw, bh, "Title and abstract screening (n = 721)", fontsize=17)

# Grey literature search (right)
r2_mid = r2_y + bh/2
gl_h = 1.0
flow_box(rcx, r2_mid - gl_h/2, rw, gl_h,
         "Grey literature search\nSources: Citation tracking,\npreprints, proceedings (n = 82)",
         fc=C["grey_bg"], ec=C["grey_bdr"], fontsize=15)

# ═══════════════════════════════════════════
# ROW 3: Exclusion boxes (dashed borders) — LEFT and RIGHT
# ═══════════════════════════════════════════
excl_h = 0.85
r3_y = r2_y - vgap - excl_h

# LEFT exclusion box (database side) — dashed red border
excl_l_w = 4.2
excl_l_x = 1.2
flow_box(excl_l_x, r3_y, excl_l_w, excl_h,
         "Full-text articles excluded based\non inclusion/exclusion criteria (n = 688)",
         fc=C["excl_bg"], ec=C["excl"], fontsize=14, linestyle="-.")

# Arrow from T&A screening down, then branch LEFT to exclusion box
excl_l_mid_y = r3_y + excl_h / 2
# Vertical line from T&A screening down to exclusion row
ax.plot([lcx + bw/2, lcx + bw/2], [r2_y, excl_l_mid_y],
        color=C["arrow"], linewidth=1.6, zorder=2)
# Horizontal arrow to left exclusion box
ax.annotate("", xy=(excl_l_x + excl_l_w, excl_l_mid_y),
            xytext=(lcx + bw/2, excl_l_mid_y),
            arrowprops=dict(arrowstyle="-|>", color=C["arrow"], linewidth=1.6,
                            shrinkA=0, shrinkB=2), zorder=2)

# RIGHT exclusion box (grey lit side) — dashed red border
flow_box(rcx, r3_y, rw, excl_h,
         "Full-text articles excluded based\non inclusion/exclusion criteria (n = 66)",
         fc=C["excl_bg"], ec=C["excl"], fontsize=14, linestyle="-.")

# Arrow from grey lit search down to right exclusion
gl_bot = r2_mid - gl_h/2
excl_r_mid_y = r3_y + excl_h / 2
arr_down(rcx + rw/2, gl_bot, rcx + rw/2, r3_y + excl_h)

# ═══════════════════════════════════════════
# ROW 4: Eligible from database + Grey lit included
# ═══════════════════════════════════════════
r4_y = r3_y - vgap - bh2

# Eligible studies (left)
flow_box(lcx, r4_y, bw, bh2,
         "Eligible studies from\ndatabase search (n = 33)", fontsize=17)

# Arrow continues down from main flow to eligible
arr_down(lcx + bw/2, excl_l_mid_y, lcx + bw/2, r4_y + bh2)

# Grey literature included (right)
flow_box(rcx, r4_y, rw, bh,
         "Grey literature included (n = 16)",
         fc=C["inc_bg"], ec=C["inc_bdr"], fontsize=17)

# Arrow from right exclusion down to grey lit included
arr_down(rcx + rw/2, r3_y, rcx + rw/2, r4_y + bh)

# ═══════════════════════════════════════════
# ROW 5: INCLUDED — merge into synthesis
# ═══════════════════════════════════════════
merge_y = r4_y - vgap - 0.05
arr_down(lcx + bw/2, r4_y, lcx + bw/2, merge_y)
arr_down(rcx + rw/2, r4_y, rcx + rw/2, merge_y)

# Horizontal merge line
ax.plot([lcx + bw/2, rcx + rw/2], [merge_y, merge_y],
        color=C["arrow"], linewidth=1.6, zorder=2)

# Arrow down to synthesis box
merge_cx = (lcx + bw/2 + rcx + rw/2) / 2
syn_h = 1.0
syn_w = 5.6
syn_y = merge_y - 0.15 - syn_h
arr_down(merge_cx, merge_y, merge_cx, syn_y + syn_h)

flow_box(merge_cx - syn_w/2, syn_y, syn_w, syn_h,
         "Studies included in synthesis (n = 49)\n"
         "  \u2022  Database search: n = 33\n"
         "  \u2022  Grey literature: n = 16",
         fc=C["inc_bg"], ec=C["inc_bdr"], fontsize=18, fontweight="bold")

# ═══════════════════════════════════════════
# Phase labels
# ═══════════════════════════════════════════
phase_label(0.2, r1_y - 0.1, r0_y + r0_h - r1_y + 0.1, "Identification")
phase_label(0.2, r4_y - 0.1, r2_y + bh - r4_y + 0.2, "Screening")
phase_label(0.2, syn_y - 0.05, merge_y - syn_y + 0.15, "Included")

# Tighten ylim to content
ax.set_ylim(syn_y - 0.3, 14)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/main"
fig.tight_layout(pad=0.2)
fig.savefig(f"{out}/Fig1_PRISMA_FlowDiagram.png", dpi=300, bbox_inches="tight", facecolor=C["bg"])
fig.savefig(f"{out}/Fig1_PRISMA_FlowDiagram.pdf", dpi=300, bbox_inches="tight", facecolor=C["bg"])
print("Fig 1 (PRISMA) saved — PNG + PDF.")
plt.close()
