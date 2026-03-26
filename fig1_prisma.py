"""
Figure 1: PRISMA 2020 Flow Diagram (Main Figure 1)
Publication-quality with Times New Roman font. Packed layout, large fonts, no overlap.
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

fig, ax = plt.subplots(figsize=(16, 13))
fig.patch.set_facecolor(C["bg"]); ax.set_facecolor(C["bg"])
ax.set_xlim(0, 14); ax.set_ylim(0, 13); ax.axis("off")

def rbox(x, y, w, h, fc, ec, lw=1.6, radius=0.12, zorder=3):
    box = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder)
    ax.add_patch(box); return box

def phase_label(x, y, h, text):
    rbox(x, y, 1.1, h, C["phase_bg"], C["phase_bdr"], lw=1.6, zorder=2)
    ax.text(x + 0.55, y + h/2, text, ha="center", va="center",
            fontsize=20, fontweight="bold", color=C["phase"], rotation=90, zorder=3)

def flow_box(x, y, w, h, text, fc=None, ec=None, fontsize=16, fontweight="normal"):
    rbox(x, y, w, h, fc or C["box_bg"], ec or C["box_bdr"], zorder=3)
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
bh = 0.55            # standard box height (tight single-line)
bh2 = 0.75           # 2-line box height (tight)
rcx = 8.2            # right column x
rw = 4.0             # right box width
vgap = 0.22          # vertical gap between rows
hgap = 0.15          # horizontal gap for arrows

# Title
ax.text(7.0, 12.7, "PRISMA 2020 Flow Diagram", ha="center", va="center",
        fontsize=24, fontweight="bold", color=C["text"])

# ═══════════════════════════════════════════
# ROW 0: Records identified (tall box) + Search Strategy
# ═══════════════════════════════════════════
r0_h = 1.1
r0_y = 11.3
flow_box(lcx, r0_y, bw, r0_h,
         "Records identified from databases\nSources: Ovid MEDLINE, Ovid EMBASE,\n"
         "Scopus, Web of Science, ACM, IEEE Xplore\n(n = 12,379)", fontsize=15)

# Search strategy (top right, aligned with row 0)
ss_x, ss_w, ss_h = rcx, rw, 1.1
rbox(ss_x, r0_y, ss_w, ss_h, C["search_bg"], C["search_bdr"], lw=1.6, zorder=3)
ax.text(ss_x + ss_w/2, r0_y + ss_h - 0.2, "Search Strategy:",
        ha="center", va="center", fontsize=17, fontweight="bold", color=C["text"], zorder=4)
ax.text(ss_x + ss_w/2, r0_y + ss_h/2 - 0.12,
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

# Exclusion box: SAME vertical center as row 1
r1_mid = r1_y + bh/2
flow_box(rcx, r1_mid - bh2/2, rw, bh2,
         "Records excluded by\nkeyword filtering (n = 11,006)",
         fc=C["excl_bg"], ec=C["excl"], fontsize=16)
arr_horiz(lcx + bw + hgap, r1_mid, rcx - hgap)

# ═══════════════════════════════════════════
# ROW 2: Title/abstract screening + Grey literature
# ═══════════════════════════════════════════
r2_y = r1_y - vgap - bh
arr_down(lcx + bw/2, r1_y, lcx + bw/2, r2_y + bh)

flow_box(lcx, r2_y, bw, bh, "Title and abstract screening (n = 721)", fontsize=17)

# Grey literature (right, same vertical center)
r2_mid = r2_y + bh/2
gl_h = 0.9
flow_box(rcx, r2_mid - gl_h/2, rw, gl_h,
         "Grey literature search\nSources: Citation tracking,\npreprints, proceedings (n = 82)",
         fc=C["grey_bg"], ec=C["grey_bdr"], fontsize=15)

# ═══════════════════════════════════════════
# ROW 3: Full-text assessed + Excluded at title/abstract
# ═══════════════════════════════════════════
r3_y = r2_y - vgap - bh2
arr_down(lcx + bw/2, r2_y, lcx + bw/2, r3_y + bh2)

flow_box(lcx, r3_y, bw, bh2,
         "Full-text articles assessed\nfor eligibility (n = 66)", fontsize=17)

# Exclusion box: SAME vertical center as row 3
r3_mid = r3_y + bh2/2
flow_box(rcx, r3_mid - bh2/2, rw, bh2,
         "Records excluded at title and\nabstract screening (n = 655)",
         fc=C["excl_bg"], ec=C["excl"], fontsize=16)
arr_horiz(lcx + bw + hgap, r3_mid, rcx - hgap)

# Grey literature arrow: route through gap between columns
# Step 1: horizontal line from grey lit LEFT edge to gap midpoint
# Step 2: vertical line down in the gap
# Step 3: horizontal arrow from gap into left box RIGHT edge
gap_x = (lcx + bw + rcx) / 2  # midpoint of gap between columns

gl_left = rcx                  # left edge of grey lit box
gl_bot_y = r2_mid - gl_h/2     # bottom of grey lit box
target_y = (r2_y + r3_y + bh2) / 2  # merge point between row 2 and row 3

# Horizontal line from grey lit left edge to gap
ax.plot([gl_left, gap_x], [r2_mid, r2_mid],
        color=C["arrow"], linewidth=1.6, zorder=2)
# Vertical line down in the gap
ax.plot([gap_x, gap_x], [r2_mid, target_y],
        color=C["arrow"], linewidth=1.6, zorder=2)
# Horizontal arrow from gap to left box right edge
ax.annotate("", xy=(lcx + bw, target_y),
            xytext=(gap_x, target_y),
            arrowprops=dict(arrowstyle="-|>", color=C["arrow"], linewidth=1.6,
                            shrinkA=0, shrinkB=2), zorder=2)

# ═══════════════════════════════════════════
# ROW 4: Eligible from database + Full-text excluded
# ═══════════════════════════════════════════
r4_y = r3_y - vgap - bh2
arr_down(lcx + bw/2, r3_y, lcx + bw/2, r4_y + bh2)

flow_box(lcx, r4_y, bw, bh2,
         "Eligible studies from\ndatabase search (n = 33)", fontsize=17)

# Exclusion box: SAME vertical center as row 4
r4_mid = r4_y + bh2/2
flow_box(rcx, r4_mid - bh2/2, rw, bh2,
         "Full-text articles excluded based\non inclusion/exclusion criteria (n = 33)",
         fc=C["excl_bg"], ec=C["excl"], fontsize=16)
arr_horiz(lcx + bw + hgap, r4_mid, rcx - hgap)

# ═══════════════════════════════════════════
# ROW 5: Grey literature included (right column only)
# ═══════════════════════════════════════════
r5_y = r4_y - vgap - bh
flow_box(rcx, r5_y, rw, bh, "Grey literature included (n = 16)",
         fc=C["grey_bg"], ec=C["grey_bdr"], fontsize=17)

# ═══════════════════════════════════════════
# ROW 6: INCLUDED — merge into synthesis
# ═══════════════════════════════════════════
merge_y = r5_y - vgap - 0.05
arr_down(lcx + bw/2, r4_y, lcx + bw/2, merge_y)
arr_down(rcx + rw/2, r5_y, rcx + rw/2, merge_y)

# Horizontal merge line
ax.plot([lcx + bw/2, rcx + rw/2], [merge_y, merge_y],
        color=C["arrow"], linewidth=1.6, zorder=2)

# Arrow down to synthesis box
merge_cx = (lcx + bw/2 + rcx + rw/2) / 2
syn_h = 0.9
syn_w = 5.2
syn_y = merge_y - 0.15 - syn_h
arr_down(merge_cx, merge_y, merge_cx, syn_y + syn_h)

flow_box(merge_cx - syn_w/2, syn_y, syn_w, syn_h,
         "Studies included in synthesis (n = 49)\n"
         "  \u2022  Database search: n = 33\n"
         "  \u2022  Grey literature: n = 16",
         fc=C["inc_bg"], ec=C["inc_bdr"], fontsize=18, fontweight="bold")

# ═══════════════════════════════════════════
# Phase labels (aligned to actual content rows)
# ═══════════════════════════════════════════
phase_label(0.5, r1_y - 0.1, r0_y + r0_h - r1_y + 0.1, "Identification")
phase_label(0.5, r4_y - 0.1, r2_y + bh - r4_y + 0.2, "Screening")
phase_label(0.5, syn_y - 0.05, merge_y - syn_y + 0.15, "Included")

# Tighten ylim to content
ax.set_ylim(syn_y - 0.25, 13)

out = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/supplements/figures/main"
fig.tight_layout(pad=0.2)
fig.savefig(f"{out}/Fig1_PRISMA_FlowDiagram.png", dpi=300, bbox_inches="tight", facecolor=C["bg"])
print("Fig 1 (PRISMA) saved.")
plt.close()
