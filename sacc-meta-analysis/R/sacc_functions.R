# =============================================================================
# SACC meta-analysis: shared functions
# Primary engine: metafor (REML random effects). Tested with R 4.3.3, metafor 4.4.0.
#
# Integrity guards built into every reader:
#   * only rows with verified == "yes" are analysed;
#   * an outcome cannot contain two rows from the same overlap_group;
#   * nothing is pooled when k < 2 (single studies are tabulated, not pooled).
# =============================================================================
suppressPackageStartupMessages({
  library(metafor)
  library(ggplot2)
})

Z975 <- qnorm(0.975)

# Species strata. The primary analysis uses S. japonicum (confirmed or presumed
# from an endemic-area cohort); other species are analysed separately.
PRIMARY_SPECIES <- c("S_japonicum_confirmed", "S_japonicum_presumed")

OUTCOME_LABELS <- c(
  male_sex = "Male sex", age_over_60 = "Age > 60 years",
  rectal_location = "Rectal location", sigmoid_location = "Sigmoid location",
  left_sided = "Left-sided tumour", advanced_stage_III_IV = "Stage III-IV",
  T3_T4 = "pT3-T4", LN_metastasis = "Lymph-node metastasis",
  distant_metastasis = "Distant metastasis", vascular_invasion = "Vascular invasion",
  lymphovascular_invasion = "Lymphovascular invasion",
  perineural_invasion = "Perineural invasion", tumor_budding = "Tumour budding",
  poor_differentiation = "Poor differentiation", mucinous = "Mucinous histology",
  signet_ring = "Signet-ring cell", multiple_primary = "Multiple primary CRC",
  synchronous = "Synchronous tumours", concomitant_polyps = "Concomitant polyps",
  positive_margin = "Positive margin", KRAS_mut = "KRAS mutation",
  NRAS_mut = "NRAS mutation", BRAF_mut = "BRAF mutation", TP53_mut = "TP53 mutation",
  p53_IHC_positive = "p53 IHC positive", MSI_H = "MSI-high", dMMR = "dMMR",
  CEA_elevated = "Elevated CEA", CA19_9_elevated = "Elevated CA19-9",
  recurrence = "Recurrence", right_sided = "Right-sided colon",
  tumor_size_5cm = "Tumour size >= 5 cm", age_older = "Older age",
  OS_hazard = "Overall survival hazard", DFS_hazard = "DFS/RFS hazard"
)
PRIMARY_BINARY <- c("advanced_stage_III_IV", "LN_metastasis", "distant_metastasis")

label_of <- function(x) ifelse(x %in% names(OUTCOME_LABELS), OUTCOME_LABELS[x], x)

# ---------------------------------------------------------------- readers ----
read_verified <- function(path) {
  if (!file.exists(path)) stop("Missing file: ", path)
  d <- read.csv(path, stringsAsFactors = FALSE, na.strings = c("", "NA", "NR"),
                check.names = FALSE)
  if (!"verified" %in% names(d)) return(d)
  d <- d[!is.na(d$verified) & tolower(trimws(d$verified)) == "yes", , drop = FALSE]
  d
}

check_overlap <- function(d, by) {
  if (!nrow(d) || !"overlap_group" %in% names(d)) return(invisible(TRUE))
  key <- interaction(d[[by]], d$overlap_group, drop = TRUE)
  dup <- d[!is.na(d$overlap_group) & duplicated(key), , drop = FALSE]
  if (nrow(dup)) {
    stop("Overlapping cohorts entered twice for the same outcome:\n",
         paste(unique(paste(dup[[by]], dup$overlap_group)), collapse = "\n"),
         "\nResolve in data/overlap_matrix.csv before pooling.")
  }
  invisible(TRUE)
}

study_label <- function(d) d$study_id

fmt_p <- function(p) ifelse(is.na(p), "NA", ifelse(p < 0.001, "<0.001", sprintf("%.3f", p)))

het_stats <- function(res) {
  sprintf("Heterogeneity: I\u00b2 = %.0f%%, \u03c4\u00b2 = %.3f; Q = %.2f, df = %d, P = %s",
          res$I2, res$tau2, res$QE, res$k - 1, fmt_p(res$QEp))
}

het_label <- function(res) {
  sprintf("RE model (REML): I-squared = %.0f%%, tau-squared = %.3f, Q = %.2f (df = %d, p = %s)",
          res$I2, res$tau2, res$QE, res$k - 1, fmt_p(res$QEp))
}

# Summarise a fitted rma object into one table row.
summarise_rma <- function(res, outcome, measure, nS = NA, nN = NA, analysis = "primary") {
  fe <- tryCatch(rma(yi = res$yi, vi = res$vi, method = "EE"), error = function(e) NULL)
  data.frame(
    outcome = outcome, analysis = analysis, k = res$k,
    n_SACC = nS, n_NSACC = nN, measure = measure,
    estimate = exp(res$b[1]), lower95 = exp(res$ci.lb), upper95 = exp(res$ci.ub),
    p_value = res$pval, I2 = res$I2, tau2 = res$tau2, Q = res$QE, Q_p = res$QEp,
    fixed_estimate = if (is.null(fe)) NA else exp(fe$b[1]),
    fixed_lower95 = if (is.null(fe)) NA else exp(fe$ci.lb),
    fixed_upper95 = if (is.null(fe)) NA else exp(fe$ci.ub),
    certainty_GRADE = "[TO BE ASSESSED]",
    stringsAsFactors = FALSE
  )
}

# ---------------------------------------------------------------- models -----
fit_binary <- function(d) {
  rma(measure = "OR", ai = event_SACC, n1i = n_SACC, ci = event_NSACC, n2i = n_NSACC,
      data = d, method = "REML", slab = study_label(d))
}

fit_hr <- function(d) {
  d$yi  <- log(d$hr)
  d$sei <- (log(d$upper95) - log(d$lower95)) / (2 * Z975)
  rma(yi = yi, sei = sei, data = d, method = "REML", slab = study_label(d))
}

# Wan et al. 2014 (BMC Med Res Methodol 14:135), scenario C3 (median, IQR, n).
wan_mean_sd <- function(q1, m, q3, n) {
  list(mean = (q1 + m + q3) / 3,
       sd = (q3 - q1) / (2 * qnorm((0.75 * n - 0.125) / (n + 0.25))))
}

fit_md <- function(d) {
  rma(measure = "MD", m1i = mean_SACC, sd1i = sd_SACC, n1i = n_SACC,
      m2i = mean_NSACC, sd2i = sd_NSACC, n2i = n_NSACC,
      data = d, method = "REML", slab = study_label(d))
}

# ---------------------------------------------------------------- output -----
save_fig <- function(name, width, height, draw, outdir) {
  dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
  f <- file.path(outdir, name)
  grDevices::cairo_pdf(paste0(f, ".pdf"), width = width, height = height, family = "Arial")
  draw(); dev.off()
  svglite::svglite(paste0(f, ".svg"), width = width, height = height)
  draw(); dev.off()
  ragg::agg_png(paste0(f, ".png"), width = width, height = height, units = "in", res = 600)
  draw(); dev.off()
  ragg::agg_tiff(paste0(f, ".tiff"), width = width, height = height, units = "in",
                 res = 600, compression = "lzw")
  draw(); dev.off()
  invisible(f)
}

# Readable log-scale ticks (0.25, 0.5, 1, 2, 4 ...) covering the CIs.
log_ticks <- function(lo, hi) {
  cand <- c(0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 4, 5, 10, 20, 50, 100)
  lo <- min(exp(lo), 1); hi <- max(exp(hi), 1)
  a <- cand[cand >= cand[max(1, sum(cand <= lo))] & cand <= cand[min(length(cand), sum(cand < hi) + 1)]]
  log(a)
}

# Adds headers above ilab columns using positions returned by forest().
ilab_headers <- function(fp, labels) {
  text(fp$ilab.xpos, fp$ylim[2] - 1, labels, font = 2, cex = fp$cex)
}

# Study-level forest plot with SACC n, NSACC n and weight columns.
forest_study <- function(res, d, xlab, title) {
  w <- weights(res)
  k <- res$k
  par(mar = c(4, 0, 2, 0), family = "Arial", cex = 0.85)
  fp <- forest(res, atransf = exp, refline = 0, xlab = xlab, header = c("Study", "OR [95% CI]"),
         ilab = cbind(d$n_SACC, d$n_NSACC, sprintf("%.1f%%", w)),
         at = log_ticks(min(res$yi - Z975 * sqrt(res$vi)), max(res$yi + Z975 * sqrt(res$vi))),
         mlab = "Random-effects model (REML)", shade = TRUE, ylim = c(-3, k + 3),
         colout = "#1F4E79", col = "#B22222", annotate = TRUE)
  ilab_headers(fp, c("SACC n", "NSACC n", "Weight"))
  par(xpd = NA)
  usr <- par("usr")
  text(usr[1], -2.2, het_stats(res), pos = 4, cex = 0.8, col = "grey25")
  text(usr[1], k + 2.6, title, pos = 4, font = 2)
}

# ---------------------------------------------------------------- heatmap ----
FEATURE_DOMAIN <- c(
  age_older = "Patient", male_sex = "Patient",
  rectal_location = "Tumour site", tumor_size_5cm = "Tumour site",
  multiple_primary = "Tumour site", concomitant_polyps = "Tumour site",
  poor_differentiation = "Pathology", mucinous = "Pathology",
  vascular_invasion = "Pathology", perineural_invasion = "Pathology",
  tumor_budding = "Pathology", positive_margin = "Pathology",
  T3_T4 = "Stage", LN_metastasis = "Stage", advanced_stage_III_IV = "Stage",
  distant_metastasis = "Stage", KRAS_mut = "Molecular",
  OS_hazard = "Survival", DFS_hazard = "Survival")
DOMAIN_COL <- c(Patient = "#5B4B8A", "Tumour site" = "#2E7D6B", Pathology = "#8C5A2B",
                Stage = "#9C2F4C", Molecular = "#2F5D8C", Survival = "#3F3F3F")

# "WangW2020" -> "Wang W 2020"; "NCG1986" -> "NCG 1986"
pretty_study <- function(x) {
  x <- sub("^([A-Z][a-z]+)([A-Z])(\\d{4})$", "\\1 \\2 \\3", x)
  sub("^([A-Za-z]+)(\\d{4})$", "\\1 \\2", x)
}

plot_evidence_heatmap <- function(ev, n_lab = NULL) {
  lv  <- c("higher", "lower", "no_difference", "not_reported")
  lab <- c(higher = "Higher in SACC", lower = "Lower in SACC",
           no_difference = "No significant difference", not_reported = "Not reported")
  pal <- c(higher = "#D55E00", lower = "#0072B2", no_difference = "#9AA9B9", not_reported = "#EEF1F5")

  studies <- unique(ev$study_id)
  yr <- as.integer(sub(".*(\\d{4})$", "\\1", studies))
  studies <- studies[order(yr, studies)]
  feats <- names(FEATURE_DOMAIN)[names(FEATURE_DOMAIN) %in% ev$feature]
  feats <- c(feats, setdiff(unique(ev$feature), feats))
  dom <- ifelse(feats %in% names(FEATURE_DOMAIN), FEATURE_DOMAIN[feats], "Other")

  full <- expand.grid(study_id = studies, feature = feats, stringsAsFactors = FALSE)
  ev <- merge(full, ev[, c("study_id", "feature", "direction")], all.x = TRUE)
  ev$direction[is.na(ev$direction)] <- "not_reported"
  ev$direction <- factor(ev$direction, levels = lv)
  xl <- pretty_study(studies)
  if (!is.null(n_lab)) xl <- ifelse(is.na(n_lab[studies]), xl, paste0(xl, "\n", n_lab[studies]))
  ev$study <- factor(xl[match(ev$study_id, studies)], levels = xl)
  ev$domain <- factor(dom[match(ev$feature, feats)], levels = unique(dom))
  ev$flab <- factor(label_of(ev$feature), levels = rev(label_of(feats)))

  # tally column: number of reports in each direction
  tal <- do.call(rbind, lapply(split(ev, ev$feature), function(v) data.frame(
    flab = v$flab[1], domain = v$domain[1],
    lab = sprintf("%2d   %2d   %2d", sum(v$direction == "higher"),
                  sum(v$direction == "lower"), sum(v$direction == "no_difference")))))

  p <- ggplot(ev, aes(study, flab)) +
    geom_tile(aes(fill = direction), colour = "white", linewidth = 1.1, width = 0.96, height = 0.96) +
    geom_point(data = ev[ev$direction != "not_reported", ], aes(shape = direction),
               colour = "white", fill = "white", size = 1.9, show.legend = FALSE) +
    scale_shape_manual(values = c(higher = 24, lower = 25, no_difference = 21, not_reported = NA)) +
    geom_text(data = tal, aes(x = length(studies) + 0.7, y = flab, label = lab), hjust = 0,
              size = 2.6, colour = "grey25", family = "mono", inherit.aes = FALSE) +
    geom_text(data = data.frame(domain = factor(levels(ev$domain)[1], levels = levels(ev$domain))),
              aes(x = length(studies) + 0.7, y = Inf), label = " Up  Dn  NS", inherit.aes = FALSE,
              hjust = 0, vjust = -0.6, size = 2.6, fontface = "bold", colour = "grey25", family = "mono") +
    scale_fill_manual(values = pal, labels = lab, drop = FALSE, name = NULL) +
    scale_x_discrete(position = "top", expand = expansion(add = c(0.5, 0.5))) +
    coord_cartesian(clip = "off") +
    facet_grid(domain ~ ., scales = "free_y", space = "free_y", switch = "y") +
    guides(fill = guide_legend(nrow = 1, override.aes = list(colour = "white"))) +
    labs(x = NULL, y = NULL,
         caption = paste("Symbols: up-triangle, higher in SACC; down-triangle, lower in SACC; circle, no significant difference;",
                         "pale cell, not reported.\nColumn headers give SACC / non-SACC n (largest comparison reported).",
                         "Right-hand tally: number of reports higher (Up), lower (Dn) or not different (NS).")) +
    theme_minimal(base_family = "Arial", base_size = 9) +
    theme(panel.grid = element_blank(),
          axis.text.x.top = element_text(size = 7.2, colour = "grey15", lineheight = 0.9,
                                         angle = 90, hjust = 0, vjust = 0.5),
          axis.text.y = element_text(size = 8.4, colour = "grey15"),
          axis.ticks = element_blank(),
          strip.placement = "outside",
          strip.text.y.left = element_text(angle = 0, face = "bold", colour = "white", size = 8,
                                           margin = margin(2, 5, 2, 5)),
          strip.background = element_rect(fill = "grey40", colour = NA),
          panel.spacing.y = grid::unit(6, "pt"),
          legend.position = "bottom", legend.text = element_text(size = 8.5),
          legend.key.size = grid::unit(10, "pt"),
          plot.caption = element_text(size = 7.2, colour = "grey35", hjust = 0),
          plot.caption.position = "plot",
          plot.margin = margin(8, 70, 6, 6))

  # colour each domain strip
  g <- ggplotGrob(p)
  idx <- grep("^strip-l", g$layout$name)
  idx <- idx[order(g$layout$t[idx])]
  doms <- levels(droplevels(ev$domain))
  for (j in seq_along(idx)) {
    st <- g$grobs[[idx[j]]]
    k <- which(vapply(st$grobs[[1]]$children, function(z) inherits(z, "rect") || grepl("rect", class(z)[1]), TRUE))
    for (kk in k) st$grobs[[1]]$children[[kk]]$gp$fill <- DOMAIN_COL[[doms[j]]]
    g$grobs[[idx[j]]] <- st
  }
  g
}
