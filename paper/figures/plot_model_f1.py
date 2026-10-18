from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator


OUTPUT_DIR = Path(__file__).resolve().parent
CONFIGURATIONS = [
    "PhoBERT V2\nCRF",
    "PhoBERT V2\nCRF-HSC",
    "XLM-R\nCRF-HSC",
    "ELECTRA\nCRF-HSC",
    "BamiBERT*\nCRF-HSC",
]
F1_SCORES = [97.98, 97.92, 97.28, 98.40, 98.48]


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 6.2,
        "ytick.labelsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def decimal_comma(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


fig, ax = plt.subplots(figsize=(3.45, 2.15))
x = list(range(len(CONFIGURATIONS)))

ax.bar(
    x,
    F1_SCORES,
    color="#245b85",
    width=0.58,
    zorder=3,
)

for index, value in enumerate(F1_SCORES):
    ax.annotate(
        decimal_comma(value),
        (index, value),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color="#263746",
    )

ax.set_xticks(x, CONFIGURATIONS)
ax.set_ylabel("Strict Micro F1 (%)")
ax.set_xlim(-0.55, len(CONFIGURATIONS) - 0.45)
ax.set_ylim(97.0, 98.8)
ax.yaxis.set_major_locator(MultipleLocator(0.2))
ax.yaxis.set_major_formatter(
    FuncFormatter(lambda value, _: decimal_comma(value, digits=1))
)
ax.grid(axis="y", color="#c5cbd1", linestyle=":", linewidth=0.55, zorder=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.7)
ax.spines["bottom"].set_linewidth(0.7)
ax.tick_params(axis="both", width=0.6, length=3)

fig.tight_layout(pad=0.4)
fig.savefig(OUTPUT_DIR / "model_f1_comparison.pdf", bbox_inches="tight")
fig.savefig(
    OUTPUT_DIR / "model_f1_comparison.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
