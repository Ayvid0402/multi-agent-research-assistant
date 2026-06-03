# architecture_diagram.py
# This creates a beautiful architecture diagram for our project
# Run it to generate architecture_diagram.png

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

# ── Helper functions ──────────────────────────────────────────────────────────
def draw_box(ax, x, y, w, h, color, text, subtext="", text_color="white"):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.1",
        facecolor=color,
        edgecolor="white",
        linewidth=1.5
    )
    ax.add_patch(box)
    ax.text(
        x + w/2, y + h/2 + (0.2 if subtext else 0),
        text,
        ha='center', va='center',
        fontsize=11, fontweight='bold',
        color=text_color
    )
    if subtext:
        ax.text(
            x + w/2, y + h/2 - 0.25,
            subtext,
            ha='center', va='center',
            fontsize=8, color='#cccccc'
        )

def draw_arrow(ax, x1, y1, x2, y2, color='white'):
    ax.annotate(
        '',
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle='->', color=color,
            lw=2.0
        )
    )

def draw_label(ax, x, y, text, color='#aaaaaa'):
    ax.text(x, y, text, ha='center', va='center',
            fontsize=8, color=color, style='italic')

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(7, 9.4, '🤖 Multi-Agent Research Assistant',
        ha='center', va='center',
        fontsize=16, fontweight='bold', color='white')
ax.text(7, 9.0, 'Architecture Diagram  |  Powered by Groq + Llama 3.1',
        ha='center', va='center',
        fontsize=10, color='#aaaaaa')

# ── User Box ──────────────────────────────────────────────────────────────────
draw_box(ax, 5.5, 7.8, 3, 0.8,
         '#2ecc71', '👤 User',
         'Types a research query')

# ── Arrow: User → Coordinator ─────────────────────────────────────────────────
draw_arrow(ax, 7, 7.8, 7, 7.1)
draw_label(ax, 7.8, 7.45, 'query')

# ── Coordinator Box ───────────────────────────────────────────────────────────
draw_box(ax, 4.5, 6.2, 5, 0.9,
         '#8e44ad', '📋 Coordinator Agent',
         'Manages pipeline | Delegates tasks | Compiles report')

# ── Arrows: Coordinator → Each Agent ─────────────────────────────────────────
# To Research Agent
draw_arrow(ax, 5.0, 6.2, 2.5, 5.1)
draw_label(ax, 3.2, 5.75, 'delegate')

# To Summarizer Agent
draw_arrow(ax, 7.0, 6.2, 7.0, 5.1)
draw_label(ax, 7.7, 5.65, 'delegate')

# To Reviewer Agent
draw_arrow(ax, 9.0, 6.2, 11.0, 5.1)
draw_label(ax, 10.3, 5.75, 'delegate')

# ── Agent Boxes ───────────────────────────────────────────────────────────────
# Research Agent
draw_box(ax, 1.0, 4.0, 3, 1.1,
         '#2980b9', '🔍 Research Agent',
         'Collects info\nExtracts key points')

# Summarizer Agent
draw_box(ax, 5.5, 4.0, 3, 1.1,
         '#e67e22', '✂️  Summarizer Agent',
         'Removes redundancy\nCreates clean summary')

# Reviewer Agent
draw_box(ax, 10.0, 4.0, 3, 1.1,
         '#c0392b', '✅ Reviewer Agent',
         'Checks completeness\nSuggests improvements')

# ── Arrows: Agents → Coordinator ─────────────────────────────────────────────
draw_arrow(ax, 2.5, 4.0, 5.0, 3.5)
draw_label(ax, 3.2, 3.65, 'research output')

draw_arrow(ax, 7.0, 4.0, 7.0, 3.5)
draw_label(ax, 7.9, 3.75, 'summary')

draw_arrow(ax, 11.0, 4.0, 9.0, 3.5)
draw_label(ax, 10.3, 3.65, 'review output')

# ── Final Report Box ──────────────────────────────────────────────────────────
draw_box(ax, 4.5, 2.6, 5, 0.9,
         '#8e44ad', '📄 Final Report',
         'Compiled by Coordinator | Saved to outputs/ folder')

# ── Arrow: Coordinator → Final Report ────────────────────────────────────────
draw_arrow(ax, 7, 6.2, 7, 3.5)

# ── Output Boxes ─────────────────────────────────────────────────────────────
draw_box(ax, 1.5, 1.3, 2.5, 0.9,
         '#27ae60', '💾 outputs/',
         'Report .txt saved')

draw_box(ax, 5.5, 1.3, 2.5, 0.9,
         '#27ae60', '📊 logs/',
         'Agent logs saved')

draw_box(ax, 9.5, 1.3, 2.5, 0.9,
         '#27ae60', '🌐 Streamlit UI',
         'User sees results')

# ── Arrows to outputs ─────────────────────────────────────────────────────────
draw_arrow(ax, 5.5, 2.6, 2.8, 2.2)
draw_arrow(ax, 7.0, 2.6, 6.75, 2.2)
draw_arrow(ax, 8.5, 2.6, 10.75, 2.2)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color='#2ecc71', label='User'),
    mpatches.Patch(color='#8e44ad', label='Coordinator Agent'),
    mpatches.Patch(color='#2980b9', label='Research Agent'),
    mpatches.Patch(color='#e67e22', label='Summarizer Agent'),
    mpatches.Patch(color='#c0392b', label='Reviewer Agent'),
    mpatches.Patch(color='#27ae60', label='Outputs'),
]
legend = ax.legend(
    handles=legend_items,
    loc='lower left',
    fontsize=8,
    facecolor='#1e1e2e',
    edgecolor='white',
    labelcolor='white',
    ncol=3
)

plt.tight_layout()
plt.savefig('architecture_diagram.png', dpi=150,
            bbox_inches='tight', facecolor='#0f1117')
print("✅ Architecture diagram saved as architecture_diagram.png!")
plt.show()