"""Figures 1, 2 and 8 (no pooled data needed).

Figure 1: PRISMA 2020 flow diagram. Counts are read from
          data/analysis_ready/prisma_counts.csv; any box without a verified count
          shows "[TO BE CALCULATED]". No count is ever invented.
Figure 2: chronological landscape of identified studies (study descriptors only,
          from data/study_inventory.csv).
Figure 8: conceptual model. Solid arrows = established histopathology; dashed
          arrows = hypothesised/unconfirmed in human SACC. Pathway boxes appear only
          where a cited study supports them; numbers refer to the manuscript list.
Exports PDF + SVG (vector) and 600-dpi PNG + TIFF.
"""
import csv
import json
import os
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
                     "font.size": 9, "pdf.fonttype": 42, "svg.fonttype": "none"})
NAVY, GREY, ORANGE, BLUE = "#1F4E79", "#6E6E6E", "#D55E00", "#0072B2"


def save(fig, name):
    for ext in ("pdf", "svg"):
        fig.savefig(os.path.join(HERE, f"{name}.{ext}"), bbox_inches="tight")
    for ext in ("png", "tiff"):
        kw = {"pil_kwargs": {"compression": "tiff_lzw"}} if ext == "tiff" else {}
        fig.savefig(os.path.join(HERE, f"{name}.{ext}"), dpi=600, bbox_inches="tight", **kw)
    plt.close(fig)


def box(ax, x, y, w, h, text, fc="white", ec=NAVY, fs=8, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.01",
                                fc=fc, ec=ec, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, x1, y1, x2, y2, dashed=False, color="black"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=10,
                                 lw=1.1, color=color, linestyle="--" if dashed else "-"))


# ----------------------------------------------------------------- Figure 1 --
def figure1():
    counts = {}
    with open(os.path.join(ROOT, "data/analysis_ready/prisma_counts.csv")) as f:
        for r in csv.DictReader(f):
            counts[r["box"]] = r["n"] if r["verified"].strip().lower() == "yes" and r["n"].strip() else None
    n = lambda k: f"n = {counts[k]}" if counts.get(k) else "n = [TO BE CALCULATED]"

    fig, ax = plt.subplots(figsize=(7.2, 9.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    L, R, W = 0.08, 0.56, 0.42
    rows = {"id": (0.78, 0.20), "scr": (0.64, 0.09), "sought": (0.52, 0.09), "assess": (0.33, 0.16),
            "qual": (0.17, 0.11), "quant": (0.03, 0.10)}
    for lab, top, bot in [("Identification", "id", "id"), ("Screening", "scr", "assess"), ("Included", "qual", "quant")]:
        y0 = rows[bot][0]; y1 = rows[top][0] + rows[top][1]
        ax.add_patch(FancyBboxPatch((0.0, y0), 0.05, y1 - y0, boxstyle="round,pad=0,rounding_size=0.01", fc="#DCE6F1", ec="none"))
        ax.text(0.025, (y0 + y1) / 2, lab, rotation=90, ha="center", va="center", fontweight="bold", fontsize=8.5)
    y, h = rows["id"]
    box(ax, L, y, W, h, "Records identified from databases\n(searched 5 October 2026):\n\n"
        f"MEDLINE via PubMed: {n('db_pubmed')}\nEurope PMC: {n('db_europepmc')}\nCrossref: {n('db_crossref')}\n\n"
        f"Total: n = {int(counts['db_pubmed']) + int(counts['db_europepmc']) + int(counts['db_crossref'])}", fs=7.4)
    box(ax, R, y + 0.05, W, 0.10, "Records removed before screening:\nduplicate records, " + n("duplicates_removed"), fs=7.2)
    y, h = rows["scr"];    box(ax, L, y, W, h, "Records screened (title/abstract)\n" + n("screened"), fs=7.2)
    box(ax, R, y, W, h, "Records excluded\n" + n("excluded_title_abstract"), fs=7.2)
    y, h = rows["sought"]; box(ax, L, y, W, h, "Reports sought for retrieval\n" + n("reports_sought"), fs=7.2)
    box(ax, R, y, W, h, "Reports not retrieved\n" + n("reports_not_retrieved") + "\n(full text unavailable; excluded)", fs=7.2)
    y, h = rows["assess"]; box(ax, L, y, W, h, "Full-text reports assessed\nfor eligibility\n" + n("full_text_assessed"), fs=7.2)
    box(ax, R, y, W, h, "Full-text reports excluded, " + n("full_text_excluded") + "\n"
        "No non-schistosomal comparator (n = 2)\nNo CRC-specific comparison (n = 1)", fs=6.5)
    y, h = rows["qual"];   box(ax, L, y, W, h, "Reports included in the review\n" + n("included_qualitative") +
                               "\n(12 S. japonicum comparative cohorts, 2 SACC-only\ncohorts, 1 genomic study; 2 S. mansoni reports)", fs=7.2)
    y, h = rows["quant"];  box(ax, L, y, W, h, "Reports included in\nmeta-analysis\n" + n("included_quantitative"), fs=7.2)
    cx = L + W / 2
    order = ["id", "scr", "sought", "assess", "qual", "quant"]
    for t, b_ in zip(order[:-1], order[1:]):
        arrow(ax, cx, rows[t][0], cx, rows[b_][0] + rows[b_][1])
    arrow(ax, L + W, rows["id"][0] + 0.10, R, rows["id"][0] + 0.10)
    for k in ("scr", "sought", "assess"):
        arrow(ax, L + W, rows[k][0] + rows[k][1] / 2, R, rows[k][0] + rows[k][1] / 2)
    save(fig, "Figure1_PRISMA_flow")


# ----------------------------------------------------------------- Figure 2 --
def figure2():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/study_inventory.csv"))))
    keep = [r for r in rows if r["eligibility_status"].startswith("Included")]
    num = lambda v: (re.match(r"\d[\d,]*", v).group(0) if re.match(r"\d", v) else v.split(" ")[0])
    keep.sort(key=lambda r: (r["recruitment_period"] == "NR", int(r["year"])))
    fig, ax = plt.subplots(figsize=(7.4, 0.42 * len(keep) + 1.2))
    for i, r in enumerate(reversed(keep)):
        per = r["recruitment_period"]
        col = {"Primary": NAVY, "Within": ORANGE, "Molecular": "#009E73", "Separate": GREY}[
            next(k for k in ("Primary", "Within", "Molecular", "Separate") if r["analysis_set"].startswith(k))]
        if per != "NR":
            yrs = [int(y) for y in re.findall(r"(?:19|20)\d\d", per)]
            a, b = yrs[0], yrs[-1]
            ax.plot([a, b + 1], [i, i], lw=6, color=col, solid_capstyle="butt")
        ax.plot(int(r["year"]) + 0.5, i, marker="D", ms=5, color="black", zorder=3)
        ns = num(r["n_SACC"]) if r["n_SACC"] != "NR" else "NR"
        nn = num(r["n_NSACC"]) if r["n_NSACC"] not in ("NR", "", "0") else ("-" if "Within" in r["analysis_set"] or r["n_NSACC"] == "0" else "NR")
        loc = r["city_province"] if r["city_province"] != "NR" else "location NR"
        ax.text(1983.5, i, f"{r['study_id']}  ({loc})", va="center", ha="right", fontsize=7.4)
        ax.text(2027.3, i, f"{ns} / {nn}", va="center", ha="left", fontsize=7.4)
    ax.set_xlim(1984, 2027); ax.set_ylim(-0.8, len(keep) - 0.2)
    ax.set_yticks([]); ax.set_xlabel("Calendar year")
    ax.text(2027.3, len(keep) - 0.1, "SACC / NSACC n", fontsize=7.4, fontweight="bold")
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="#E5E5E5", lw=0.6)
    h = [plt.Line2D([], [], color=c, lw=6) for c in (NAVY, ORANGE, "#009E73", GREY)] + \
        [plt.Line2D([], [], marker="D", color="black", lw=0)]
    ax.legend(h, ["Recruitment period: comparative (S. japonicum)", "within-SACC", "molecular map",
                  "S. mansoni (separate)", "Publication year"],
              loc="upper center", bbox_to_anchor=(0.45, -0.12), ncol=3, frameon=False, fontsize=7)
    save(fig, "Figure2_landscape_timeline")


# ----------------------------------------------------------------- Figure 8 --
def figure8():
    refs = json.load(open(os.path.join(ROOT, "manuscript/ref_numbers.json")))

    def c(*keys):
        return "[" + ",".join(str(refs[k]) for k in keys) + "]"

    fig, ax = plt.subplots(figsize=(8.4, 6.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    main = [
        (0.86, "Schistosoma japonicum infection\n(IARC Group 2B: possibly carcinogenic) " + c("iarc61"), "#DCE6F1"),
        (0.73, "Egg deposition in the colorectal wall\nand regional lymph nodes " + c("hamid2019", "pan2023"), "#DCE6F1"),
        (0.60, "Chronic granulomatous inflammation\nand fibrosis " + c("iarc61", "hamid2019"), "#DCE6F1"),
        (0.47, "Epithelial injury and regeneration;\nimmune remodelling", "#F2F2F2"),
        (0.34, "Potential genomic / epigenetic\nalterations", "#F2F2F2"),
        (0.21, "Colorectal carcinogenesis", "#F2F2F2"),
        (0.07, "Possible distinctive clinicopathological\nphenotype (tested by this meta-analysis)", "#FFF2CC"),
    ]
    W, H, X = 0.38, 0.085, 0.31
    for y, t, fc in main:
        box(ax, X, y, W, H, t, fc=fc, fs=7.4)
    for (y1, _, _), (y2, _, _) in zip(main[:-1], main[1:]):
        arrow(ax, X + W / 2, y1, X + W / 2, y2 + H, dashed=(y2 < 0.5))
    side = [
        (0.47, "R", "Tumour-associated macrophage\npolarisation in schistosomal\nCRC " + c("tam2021")),
        (0.47, "L", "CD8+/CD4+ TIL, PD-L1 and CRP:\nprognostic value differs by\nschistosomiasis status\n(observational) " + c("wangw2021", "wangw2023", "bmcgastro2023")),
        (0.34, "R", "S. japonicum soluble egg\nantigen: MAPK and PI3K-AKT\nactivation (experimental) " + c("sea2025")),
        (0.34, "L", "S. mansoni eggs: Wnt/\u03b2-catenin\nand c-Jun activation\n(different species) " + c("wnt2020")),
        (0.21, "R", "SACC exomes: lower TMB,\nMSS/MSI-L (30 tumours;\nexternal comparator) " + c("genomic2023")),
        (0.21, "L", "KRAS G12S/D more frequent\n(single cohort) " + c("li2024") + "; c-MYC\namplification prognostic\nwithin SACC " + c("pan2020")),
    ]
    SW = 0.27
    for y, side_, t in side:
        x = 0.01 if side_ == "L" else 0.72
        box(ax, x, y - 0.02, SW, 0.125, t, fc="white", ec=GREY, fs=6.2)
        if side_ == "R":
            arrow(ax, x, y + 0.042, X + W, y + 0.042, dashed=True, color=GREY)
        else:
            arrow(ax, x + SW, y + 0.042, X, y + 0.042, dashed=True, color=GREY)
    h = [plt.Line2D([], [], color="black", lw=1.1), plt.Line2D([], [], color="black", lw=1.1, ls="--"),
         plt.Line2D([], [], color=GREY, lw=1.1, ls="--")]
    ax.legend(h, ["Established histopathology", "Hypothesised / not confirmed in human SACC",
                  "Supporting observation (evidence type stated)"],
              loc="upper center", bbox_to_anchor=(0.5, 0.03), ncol=2, frameon=False, fontsize=7)
    save(fig, "Figure8_conceptual_model")


if __name__ == "__main__":
    figure1(); figure2()
    if os.path.exists(os.path.join(ROOT, "manuscript/ref_numbers.json")):
        figure8()
    print("Figures 1, 2, 8 written to", HERE)
