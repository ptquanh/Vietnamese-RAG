from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


OUTPUT_DIR = Path(__file__).resolve().parent
BACKBONES = ["XLM-R", "PhoBERT V2", "ELECTRA", "BamiBERT*"]
H_SUPCON_F1 = [97.28, 97.92, 98.40, 98.48]


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def decimal_comma(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


fig, ax = plt.subplots(figsize=(3.45, 1.75))
x = list(range(len(BACKBONES)))

ax.plot(
    x,
    H_SUPCON_F1,
    color="#245b85",
    linewidth=1.35,
    marker="o",
    markersize=4.2,
    label="CRF-H-SupCon",
    zorder=3,
)
ax.scatter(
    [1],
    [97.98],
    color="#b45f06",
    marker="D",
    s=24,
    label="CRF (PhoBERT V2)",
    zorder=4,
)

for index, value in enumerate(H_SUPCON_F1):
    if index == 1:
        offset = (-11, 8)
    elif index == 3:
        offset = (0, -12)
    else:
        offset = (0, 7)
    ax.annotate(
        decimal_comma(value),
        (index, value),
        xytext=offset,
        textcoords="offset points",
        ha="center",
        va="center",
        fontsize=6.8,
    )

ax.annotate(
    decimal_comma(97.98),
    (1, 97.98),
    xytext=(13, -4),
    textcoords="offset points",
    ha="left",
    va="center",
    fontsize=6.8,
    color="#874500",
)

ax.set_xticks(x, BACKBONES)
ax.set_ylabel("Strict Micro F1 (%)")
ax.set_ylim(97.15, 98.62)
ax.yaxis.set_major_formatter(
    FuncFormatter(lambda value, _: decimal_comma(value, digits=1))
)
ax.grid(axis="y", linestyle=":", linewidth=0.55, alpha=0.75, zorder=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="lower right", frameon=False, handlelength=1.8)

fig.tight_layout(pad=0.45)
fig.savefig(OUTPUT_DIR / "model_f1_comparison.pdf", bbox_inches="tight")
fig.savefig(
    OUTPUT_DIR / "model_f1_comparison.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
