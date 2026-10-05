# 00_setup.R — install packages and define shared paths/parameters.
# Run once. Every other script sources this file.

if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")

cran <- c("data.table", "dplyr", "tidyr", "readxl", "ggplot2", "ggrepel",
          "igraph", "survival", "survminer", "pROC", "msigdbr", "here",
          "VennDiagram", "patchwork", "remotes")
bioc <- c("TCGAbiolinks", "SummarizedExperiment", "DESeq2", "apeglm",
          "biomaRt", "clusterProfiler", "org.Hs.eg.db", "org.Mm.eg.db",
          "enrichplot", "fgsea", "STRINGdb", "ComplexHeatmap")

need <- function(p) p[!vapply(p, requireNamespace, logical(1), quietly = TRUE)]
if (length(need(cran))) install.packages(need(cran))
if (length(need(bioc))) BiocManager::install(need(bioc), update = FALSE)
if (!requireNamespace("MCPcounter", quietly = TRUE))
  remotes::install_github("ebecht/MCPcounter", subdir = "Source")

suppressPackageStartupMessages({
  library(data.table); library(dplyr); library(ggplot2)
})

# ---- Paths (project root = Schisto_CRC_Tenure/) -----------------------------
# Run all scripts from the project root, e.g. Rscript 04_R_scripts/01_mouse_signature.R
ROOT <- Sys.getenv("SCHISTO_ROOT", getwd())
stopifnot(dir.exists(file.path(ROOT, "00_protocol")))
P <- function(...) file.path(ROOT, ...)

# ---- Pre-specified parameters (Analysis_Plan_v1 §4) — DO NOT EDIT -----------
PARAM <- list(
  fdr        = 0.05,
  lfc        = 1,
  lfc_sens   = log2(1.5),
  gsea_fdr   = 0.05,
  gsea_sugg  = 0.25,
  gsea_min   = 15,
  gsea_max   = 500,
  string_thr = 700,
  n_hubs     = 10,
  seed       = 20261005
)
set.seed(PARAM$seed)

writeLines(capture.output(sessionInfo()), P("05_results", "sessionInfo.txt"))
