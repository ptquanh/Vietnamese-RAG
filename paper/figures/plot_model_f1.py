from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator


OUTPUT_DIR = Path(__file__).resolve().parent
CONFIGURATIONS = [
    "XLM-R\nCRF-HSC",
    "PhoBERT V2\nCRF",
    "PhoBERT V2\nCRF-HSC",
    "ELECTRA\nCRF-HSC",
    "BamiBERT*\nCRF-HSC",
]
F1_SCORES = [97.28, 97.98, 97.92, 98.40, 98.48]
H_SUPCON_INDICES = [0, 2, 3, 4]
CRF_INDEX = 1


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 6.2,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def decimal_comma(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


fig, ax = plt.subplots(figsize=(3.45, 1.82))
x = list(range(len(CONFIGURATIONS)))

ax.plot(
    x,
    F1_SCORES,
    color="#8a98a6",
    linewidth=1.0,
    zorder=2,
)
ax.scatter(
    H_SUPCON_INDICES,
    [F1_SCORES[index] for index in H_SUPCON_INDICES],
    color="#245b85",
    edgecolor="white",
    linewidth=0.45,
    marker="o",
    s=27,
    label="CRF-H-SupCon",
    zorder=4,
)
ax.scatter(
    [CRF_INDEX],
    [F1_SCORES[CRF_INDEX]],
    color="#b45f06",
    edgecolor="white",
    linewidth=0.45,
    marker="D",
    s=27,
    label="CRF (PhoBERT V2)",
    zorder=4,
)

label_offsets = [(0, 7), (0, 8), (0, -11), (0, 7), (0, -11)]
for index, value in enumerate(F1_SCORES):
    ax.annotate(
        decimal_comma(value),
        (index, value),
        xytext=label_offsets[index],
        textcoords="offset points",
        ha="center",
        va="center",
        fontsize=6.8,
        color="#263746" if index != CRF_INDEX else "#874500",
    )

ax.set_xticks(x, CONFIGURATIONS)
ax.set_ylabel("Strict Micro F1 (%)")
ax.set_xlim(-0.32, len(CONFIGURATIONS) - 0.68)
ax.set_ylim(97.15, 98.62)
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
ax.legend(loc="lower right", frameon=False, handlelength=1.5)

fig.tight_layout(pad=0.4)
fig.savefig(OUTPUT_DIR / "model_f1_comparison.pdf", bbox_inches="tight")
fig.savefig(
    OUTPUT_DIR / "model_f1_comparison.png",
    dpi=300,
    bbox_inches="tight",
)
plt.close(fig)
