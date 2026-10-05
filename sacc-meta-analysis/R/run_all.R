# =============================================================================
# SACC meta-analysis: full analysis pipeline
#
# Usage (from the sacc-meta-analysis/ folder):
#   Rscript R/run_all.R                      # reads data/analysis_ready, writes output/
#   Rscript R/run_all.R <data_dir> <out_dir> # custom locations (used by tests/)
#
# Produces: Table 4 (meta-analysis summary), Table 5 (within-SACC), Table S5
# (sensitivity), Figures 3-7 (PDF, SVG, 600-dpi PNG and TIFF), and a log.
# Every figure/table is generated only from rows marked verified == "yes".
# =============================================================================
args <- commandArgs(trailingOnly = TRUE)
data_dir <- if (length(args) >= 1) args[1] else "data/analysis_ready"
out_dir  <- if (length(args) >= 2) args[2] else "output"
script_dir <- local({
  f <- sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))
  if (length(f)) dirname(normalizePath(f)) else "R"
})
source(file.path(script_dir, "sacc_functions.R"))
set.seed(20261005)

fig_dir <- file.path(out_dir, "figures"); tab_dir <- file.path(out_dir, "tables")
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(tab_dir, recursive = TRUE, showWarnings = FALSE)
log_file <- file.path(out_dir, "analysis_log.txt")
cat("SACC meta-analysis run", format(Sys.time()), "\n", R.version.string,
    "\nmetafor", as.character(packageVersion("metafor")), "\n\n", file = log_file)
logm <- function(...) cat(..., "\n", file = log_file, append = TRUE)

summary_rows <- list(); sens_rows <- list()

# ------------------------------------------------------------ binary ---------
bin <- read_verified(file.path(data_dir, "binary_outcomes.csv"))
bin_primary <- bin[bin$species_stratum %in% PRIMARY_SPECIES &
                   tolower(bin$include_primary) == "yes", , drop = FALSE]
check_overlap(bin_primary, "outcome")
logm("Binary rows (verified, primary):", nrow(bin_primary))

bin_fits <- list()
for (oc in unique(bin_primary$outcome)) {
  d <- bin_primary[bin_primary$outcome == oc, , drop = FALSE]
  if (nrow(d) < 2) { logm("  ", oc, ": k = 1, not pooled"); next }
  res <- fit_binary(d)
  bin_fits[[oc]] <- list(res = res, d = d)
  summary_rows[[length(summary_rows) + 1]] <-
    summarise_rma(res, label_of(oc), "OR", sum(d$n_SACC), sum(d$n_NSACC))

  # ---- sensitivity analyses (Table S5) ----
  add_sens <- function(sub, tag) {
    if (nrow(sub) >= 2 && nrow(sub) < nrow(d)) {
      r2 <- fit_binary(sub)
      sens_rows[[length(sens_rows) + 1]] <<-
        summarise_rma(r2, label_of(oc), "OR", sum(sub$n_SACC), sum(sub$n_NSACC), tag)
    }
  }
  add_sens(d[d$n_SACC + d$n_NSACC < max(d$n_SACC + d$n_NSACC), ], "excluding largest cohort")
  add_sens(d[is.na(d$rob_overall) | tolower(d$rob_overall) != "high", ], "excluding high risk of bias")
  add_sens(d[tolower(d$histology_confirmed) %in% "yes", ], "histology-confirmed SACC only")
  add_sens(d[d$species_stratum == "S_japonicum_confirmed", ], "S. japonicum-confirmed only")
  add_sens(d[!grepl("preprint", d$notes, ignore.case = TRUE), ], "excluding preprints")
  l1o <- leave1out(res)
  sens_rows[[length(sens_rows) + 1]] <- data.frame(
    outcome = label_of(oc), analysis = paste("leave-one-out: omit", l1o$slab), k = res$k - 1,
    n_SACC = NA, n_NSACC = NA, measure = "OR", estimate = exp(l1o$estimate),
    lower95 = exp(l1o$ci.lb), upper95 = exp(l1o$ci.ub), p_value = l1o$pval, I2 = l1o$I2,
    tau2 = l1o$tau2, Q = l1o$Q, Q_p = l1o$Qp, fixed_estimate = NA, fixed_lower95 = NA,
    fixed_upper95 = NA, certainty_GRADE = "", stringsAsFactors = FALSE)
  if (res$k >= 10) {
    eg <- regtest(res)
    logm("  ", oc, ": Egger z =", round(eg$zval, 3), "p =", fmt_p(eg$pval))
    save_fig(paste0("FigS_funnel_", oc), 5, 5, function() funnel(res, atransf = exp), fig_dir)
  } else logm("  ", oc, ": k =", res$k, "< 10, small-study tests not performed")

  save_fig(paste0("Fig_forest_", oc), 8, 2.2 + 0.32 * res$k,
           function() forest_study(res, d, "Odds ratio (log scale)", label_of(oc)), fig_dir)
}

# ---- Figure 3: multi-outcome clinicopathological phenotype ----
if (length(bin_fits)) {
  s3 <- do.call(rbind, lapply(names(bin_fits), function(oc) {
    r <- bin_fits[[oc]]$res
    data.frame(outcome = label_of(oc), primary = oc %in% PRIMARY_BINARY,
               yi = r$b[1], lb = r$ci.lb, ub = r$ci.ub, k = r$k, I2 = r$I2)
  }))
  s3 <- s3[order(!s3$primary), ]
  save_fig("Figure3_phenotype_forest", 8, 1.6 + 0.35 * nrow(s3), function() {
    par(mar = c(4, 0, 1, 0), family = "Arial", cex = 0.85)
    fp <- forest(x = s3$yi, ci.lb = s3$lb, ci.ub = s3$ub, slab = s3$outcome, atransf = exp,
           refline = 0, at = log_ticks(min(s3$lb), max(s3$ub)), xlab = "Pooled odds ratio, SACC vs NSACC (log scale)",
           ilab = cbind(s3$k, sprintf("%.0f%%", s3$I2)), header = c("Outcome", "OR [95% CI]"),
           psize = 1, col = ifelse(s3$primary, "#B22222", "#1F4E79"))
    ilab_headers(fp, c("Studies", "I-sq."))
  }, fig_dir)
}

# ------------------------------------------------------------ continuous ----
con <- read_verified(file.path(data_dir, "continuous_outcomes.csv"))
if (nrow(con)) {
  need <- is.na(con$mean_SACC) & !is.na(con$median_SACC)
  for (i in which(need)) {
    a <- wan_mean_sd(con$q1_SACC[i], con$median_SACC[i], con$q3_SACC[i], con$n_SACC[i])
    b <- wan_mean_sd(con$q1_NSACC[i], con$median_NSACC[i], con$q3_NSACC[i], con$n_NSACC[i])
    con[i, c("mean_SACC", "sd_SACC", "mean_NSACC", "sd_NSACC")] <- c(a$mean, a$sd, b$mean, b$sd)
    con$transformation[i] <- "Wan 2014 (median, IQR)"
    logm("  converted median/IQR -> mean/SD:", con$study_id[i], con$outcome[i])
  }
  con <- con[con$species_stratum %in% PRIMARY_SPECIES & tolower(con$include_primary) == "yes", ]
  check_overlap(con, "outcome")
  for (oc in unique(con$outcome)) {
    d <- con[con$outcome == oc, ]
    if (nrow(d) < 2) next
    res <- fit_md(d)
    row <- summarise_rma(res, oc, "MD", sum(d$n_SACC), sum(d$n_NSACC))
    row[, c("estimate", "lower95", "upper95")] <- c(res$b[1], res$ci.lb, res$ci.ub)  # MD is not exponentiated
    fe <- update(res, method = "EE")
    row[, c("fixed_estimate", "fixed_lower95", "fixed_upper95")] <- c(fe$b[1], fe$ci.lb, fe$ci.ub)
    summary_rows[[length(summary_rows) + 1]] <- row
    save_fig(paste0("Fig_forest_", oc), 8, 2.2 + 0.32 * res$k, function() {
      par(mar = c(4, 0, 2, 0), family = "Arial", cex = 0.85)
      fp <- forest(res, refline = 0, xlab = "Mean difference (SACC - NSACC)", mlab = het_label(res),
             ilab = cbind(d$n_SACC, d$n_NSACC), header = c("Study", "MD [95% CI]"))
      ilab_headers(fp, c("SACC n", "NSACC n"))
    }, fig_dir)
  }
}

# ------------------------------------------------------------ survival ------
sv <- read_verified(file.path(data_dir, "survival_outcomes.csv"))
sv <- sv[sv$species_stratum %in% PRIMARY_SPECIES & tolower(sv$include_primary) == "yes", , drop = FALSE]
if (nrow(sv)) {
  sv$adjusted <- ifelse(tolower(sv$adjusted) == "yes", "Adjusted", "Unadjusted")
  check_overlap(transform(sv, key = paste(outcome, adjusted)), "key")
  for (oc in unique(sv$outcome)) {
    d_all <- sv[sv$outcome == oc, ]
    fits <- list()
    for (adj in c("Adjusted", "Unadjusted")) {
      d <- d_all[d_all$adjusted == adj, ]
      if (nrow(d) < 2) next
      res <- fit_hr(d); fits[[adj]] <- res
      summary_rows[[length(summary_rows) + 1]] <-
        summarise_rma(res, paste(oc, "-", adj), "HR", sum(d$n_SACC, na.rm = TRUE),
                      sum(d$n_NSACC, na.rm = TRUE))
      if (nrow(d) >= 3) {
        l1o <- leave1out(res)
        sens_rows[[length(sens_rows) + 1]] <- data.frame(
          outcome = paste(oc, "-", adj), analysis = paste("leave-one-out: omit", l1o$slab),
          k = res$k - 1, n_SACC = NA, n_NSACC = NA, measure = "HR", estimate = exp(l1o$estimate),
          lower95 = exp(l1o$ci.lb), upper95 = exp(l1o$ci.ub), p_value = l1o$pval, I2 = l1o$I2,
          tau2 = l1o$tau2, Q = l1o$Q, Q_p = l1o$Qp, fixed_estimate = NA, fixed_lower95 = NA,
          fixed_upper95 = NA, certainty_GRADE = "", stringsAsFactors = FALSE)
      }
    }
    # Figures 4 (OS) and 5 (DFS/RFS): adjusted and unadjusted shown as separate subgroups
    d_all <- d_all[order(d_all$adjusted, d_all$study_id), ]  # Adjusted block first
    yi <- log(d_all$hr); sei <- (log(d_all$upper95) - log(d_all$lower95)) / (2 * Z975)
    n_adj <- sum(d_all$adjusted == "Adjusted"); n_un <- sum(d_all$adjusted == "Unadjusted")
    rows <- c(if (n_adj) seq(n_un + 3 + n_adj, n_un + 4), if (n_un) seq(n_un, 1))
    fig_name <- if (oc == "OS") "Figure4_OS_forest" else paste0("Figure5_", oc, "_forest")
    save_fig(fig_name, 8.5, 3 + 0.35 * nrow(d_all) + 1.2 * length(fits), function() {
      par(mar = c(4, 0, 1, 0), family = "Arial", cex = 0.85)
      ylim_top <- max(rows) + 4
      fp <- forest(yi, sei = sei, slab = d_all$study_id, atransf = exp, refline = 0,
             at = log_ticks(min(log(d_all$lower95)), max(log(d_all$upper95))),
             rows = rows, ylim = c(-2, ylim_top), xlab = "Hazard ratio, SACC vs NSACC (log scale)",
             ilab = cbind(d_all$n_SACC, d_all$n_NSACC, d_all$hr_priority),
             header = c("Study", "HR [95% CI]"), col = "#1F4E79")
      ilab_headers(fp, c("SACC n", "NSACC n", "Source"))
      if (n_adj) text(par("usr")[1], max(rows) + 1.2, "Multivariable-adjusted", pos = 4, font = 4)
      if (n_un) text(par("usr")[1], n_un + 1.2, "Unadjusted / derived", pos = 4, font = 4)
      if (!is.null(fits$Adjusted)) addpoly(fits$Adjusted, row = n_un + 2.5, mlab = het_label(fits$Adjusted))
      if (!is.null(fits$Unadjusted)) addpoly(fits$Unadjusted, row = -1, mlab = het_label(fits$Unadjusted))
    }, fig_dir)
  }
}

# ------------------------------------------------------------ molecular -----
mol <- read_verified(file.path(data_dir, "molecular_evidence.csv"))
if (nrow(mol)) {
  mol_tab <- aggregate(cbind(total_SACC, total_NSACC) ~ biomarker, data = mol, FUN = sum, na.action = na.pass)
  mol_tab$k <- as.vector(table(mol$biomarker)[mol_tab$biomarker])
  mol_tab$pooled <- "Not pooled (k < 2)"
  mol_fits <- list()
  for (bm in mol_tab$biomarker[mol_tab$k >= 2]) {
    d <- mol[mol$biomarker == bm & mol$comparator_type == "internal", ]
    names(d)[names(d) == "positive_SACC"] <- "event_SACC"; names(d)[names(d) == "total_SACC"] <- "n_SACC"
    names(d)[names(d) == "positive_NSACC"] <- "event_NSACC"; names(d)[names(d) == "total_NSACC"] <- "n_NSACC"
    if (nrow(d) < 2) next
    r <- fit_binary(d)
    mol_fits[[bm]] <- r
    mol_tab$pooled[mol_tab$biomarker == bm] <- sprintf("OR %.2f (%.2f-%.2f); I2 %.0f%%",
                                                       exp(r$b[1]), exp(r$ci.lb), exp(r$ci.ub), r$I2)
  }
  write.csv(mol_tab, file.path(tab_dir, "Table3_molecular_evidence_map.csv"), row.names = FALSE)
  if (length(mol_fits)) {
    m6 <- data.frame(bm = names(mol_fits), yi = sapply(mol_fits, function(r) r$b[1]),
                     lb = sapply(mol_fits, function(r) r$ci.lb), ub = sapply(mol_fits, function(r) r$ci.ub),
                     k = sapply(mol_fits, function(r) r$k), I2 = sapply(mol_fits, function(r) r$I2))
    save_fig("Figure6_molecular", 8, 1.6 + 0.35 * nrow(m6), function() {
      par(mar = c(4, 0, 1, 0), family = "Arial", cex = 0.85)
      fp <- forest(x = m6$yi, ci.lb = m6$lb, ci.ub = m6$ub, slab = m6$bm, atransf = exp, refline = 0,
                   at = log_ticks(min(m6$lb), max(m6$ub)), xlab = "Pooled odds ratio, SACC vs NSACC (log scale)",
                   ilab = cbind(m6$k, sprintf("%.0f%%", m6$I2)), header = c("Biomarker", "OR [95% CI]"), psize = 1)
      ilab_headers(fp, c("Studies", "I-sq."))
    }, fig_dir)
  }
}

# ------------------------------------------------------------ within-SACC ---
ws <- read_verified(file.path(data_dir, "within_sacc_prognostic.csv"))
if (nrow(ws)) {
  check_overlap(transform(ws, key = paste(factor, outcome, adjusted)), "key")
  t5 <- ws[, c("study_id", "factor", "comparison", "outcome", "hr", "lower95", "upper95",
               "adjusted", "covariates", "hr_priority", "n_SACC_total")]
  pooled <- list()
  for (key in unique(paste(ws$factor, ws$outcome))) {
    d <- ws[paste(ws$factor, ws$outcome) == key, ]
    if (nrow(d) < 2) next
    r <- fit_hr(d)
    pooled[[key]] <- summarise_rma(r, key, "HR", sum(d$n_SACC_total), NA, "within-SACC")
  }
  write.csv(t5, file.path(tab_dir, "Table5_within_SACC_studies.csv"), row.names = FALSE)
  if (length(pooled)) write.csv(do.call(rbind, pooled), file.path(tab_dir, "Table5b_within_SACC_pooled.csv"), row.names = FALSE)
}

# ------------------------------------------------------------ heatmap -------
ev <- read_verified(file.path(data_dir, "evidence_direction.csv"))
if (nrow(ev)) {
  p <- plot_evidence_heatmap(ev)
  nf <- length(unique(ev$feature)); ns <- length(unique(ev$study_id))
  save_fig("Figure7_evidence_heatmap", max(6, 2.5 + 0.45 * ns), 1.8 + 0.28 * nf, function() print(p), fig_dir)
}

# ------------------------------------------------------------ tables --------
if (length(summary_rows)) {
  t4 <- do.call(rbind, summary_rows)
  write.csv(t4, file.path(tab_dir, "Table4_meta_analysis_summary.csv"), row.names = FALSE)
  logm("Pooled outcomes:", nrow(t4))
} else logm("No outcome had k >= 2 verified studies; nothing pooled.")
if (length(sens_rows)) write.csv(do.call(rbind, sens_rows), file.path(tab_dir, "TableS5_sensitivity.csv"), row.names = FALSE)

capture.output(sessionInfo(), file = file.path(out_dir, "sessionInfo.txt"))
cat("Done. See", out_dir, "\n")
