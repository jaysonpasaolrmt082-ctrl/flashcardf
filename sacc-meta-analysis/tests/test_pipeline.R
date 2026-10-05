# =============================================================================
# Software validation for R/run_all.R. This is NOT SACC data.
#
# 1. Benchmark: metafor's BCG vaccine dataset (dat.bcg) gives a REML log-RR of
#    -0.7145, tau^2 = 0.3132, I^2 = 92.22% (metafor documentation).
# 2. The BCG 2x2 tables are written into the binary_outcomes.csv template under
#    a dummy outcome code. The pipeline is run into a temporary directory and
#    its pooled OR is checked against a direct rma() call.
# 3. Synthetic HRs check the survival and heatmap paths and the overlap guard.
# All outputs go to tempdir() and are deleted; nothing is written to output/.
# =============================================================================
suppressPackageStartupMessages(library(metafor))
here <- normalizePath(".")
tmp <- file.path(tempdir(), "sacc_test"); unlink(tmp, recursive = TRUE)
dd <- file.path(tmp, "data"); od <- file.path(tmp, "out"); dir.create(dd, recursive = TRUE)
for (f in list.files("data/analysis_ready", full.names = TRUE)) file.copy(f, dd)

ok <- function(cond, msg) { if (!cond) stop("FAIL: ", msg); cat("PASS:", msg, "\n") }

# --- 1. benchmark ------------------------------------------------------------
b <- rma(measure = "RR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = dat.bcg, method = "REML")
ok(abs(b$b[1] - (-0.7145)) < 1e-3 && abs(b$tau2 - 0.3132) < 1e-3, "metafor REML reproduces BCG benchmark")

# --- 2. binary path ----------------------------------------------------------
tmpl <- read.csv(file.path(dd, "binary_outcomes.csv"), check.names = FALSE)
bcg <- data.frame(study_id = paste0("TEST_", dat.bcg$author, dat.bcg$year), outcome = "LN_metastasis",
                  event_SACC = dat.bcg$tpos, n_SACC = dat.bcg$tpos + dat.bcg$tneg,
                  event_NSACC = dat.bcg$cpos, n_NSACC = dat.bcg$cpos + dat.bcg$cneg,
                  species_stratum = "S_japonicum_confirmed", histology_confirmed = "yes",
                  overlap_group = paste0("T", seq_len(nrow(dat.bcg))), include_primary = "yes",
                  rob_overall = c(rep("low", 10), rep("high", 3)), data_origin = "test",
                  source_location = "metafor::dat.bcg", extractor_1 = "test", extractor_2 = "test",
                  verified = "yes", notes = "SOFTWARE TEST ONLY")
bcg$verified[1] <- "no"   # an unverified row must be ignored
write.csv(rbind(tmpl, bcg[names(tmpl)]), file.path(dd, "binary_outcomes.csv"), row.names = FALSE)

# --- 3. survival + heatmap path ---------------------------------------------
sv <- read.csv(file.path(dd, "survival_outcomes.csv"), check.names = FALSE)
syn <- data.frame(study_id = paste0("SYN", 1:5), outcome = "OS", hr = c(1.2, 0.9, 1.5, 1.1, 0.8),
                  lower95 = c(0.9, 0.6, 1.0, 0.8, 0.5), upper95 = c(1.6, 1.35, 2.25, 1.5, 1.28),
                  adjusted = c("yes", "yes", "yes", "no", "no"), covariates = "", hr_priority = "P1",
                  reference_group = "NSACC", n_SACC = 50, n_NSACC = 100, median_follow_up_months = 60,
                  species_stratum = "S_japonicum_presumed", histology_confirmed = "yes",
                  overlap_group = paste0("S", 1:5), include_primary = "yes", rob_overall = "low",
                  data_origin = "test", source_location = "synthetic", extractor_1 = "t", extractor_2 = "t",
                  verified = "yes", notes = "SOFTWARE TEST ONLY")
write.csv(rbind(sv, syn[names(sv)]), file.path(dd, "survival_outcomes.csv"), row.names = FALSE)
ev <- data.frame(study_id = rep(c("SYN1", "SYN2"), each = 3), feature = rep(c("male_sex", "LN_metastasis", "KRAS_mut"), 2),
                 direction = c("higher", "no_difference", "higher", "lower", "no_difference", "not_reported"),
                 basis = "test", source_location = "synthetic", verified = "yes")
write.csv(ev, file.path(dd, "evidence_direction.csv"), row.names = FALSE)

st <- system2("Rscript", c(file.path(here, "R/run_all.R"), dd, od), stdout = TRUE, stderr = TRUE)
ok(is.null(attr(st, "status")), paste("pipeline runs end-to-end", paste(tail(st, 3), collapse = " | ")))

t4 <- read.csv(file.path(od, "tables/Table4_meta_analysis_summary.csv"))
direct <- rma(measure = "OR", ai = event_SACC, n1i = n_SACC, ci = event_NSACC, n2i = n_NSACC,
              data = bcg[bcg$verified == "yes", ], method = "REML")
ln <- t4[t4$outcome == "Lymph-node metastasis", ]
ok(nrow(ln) == 1 && ln$k == 12, "unverified row excluded (k = 12 of 13)")
ok(abs(ln$estimate - exp(direct$b[1])) < 1e-8 && abs(ln$tau2 - direct$tau2) < 1e-8,
   "pipeline OR and tau^2 equal direct rma()")
ok(any(grepl("OS - Adjusted", t4$outcome)), "survival adjusted subgroup pooled")
s5 <- read.csv(file.path(od, "tables/TableS5_sensitivity.csv"))
ok(any(s5$analysis == "excluding high risk of bias" & s5$k == 9), "risk-of-bias sensitivity analysis")
ok(sum(grepl("leave-one-out", s5$analysis) & s5$outcome == "Lymph-node metastasis") == 12, "leave-one-out")
for (f in c("Figure3_phenotype_forest", "Figure4_OS_forest", "Figure7_evidence_heatmap", "Fig_forest_LN_metastasis"))
  for (ext in c("pdf", "svg", "png", "tiff")) ok(file.exists(file.path(od, "figures", paste0(f, ".", ext))), paste(f, ext))
logtxt <- readLines(file.path(od, "analysis_log.txt"))
ok(any(grepl("Egger", logtxt)), "Egger test run when k >= 10")

# --- 4. overlap guard --------------------------------------------------------
bcg$overlap_group[3] <- bcg$overlap_group[2]
write.csv(rbind(tmpl, bcg[names(tmpl)]), file.path(dd, "binary_outcomes.csv"), row.names = FALSE)
st2 <- suppressWarnings(system2("Rscript", c(file.path(here, "R/run_all.R"), dd, file.path(tmp, "o2")), stdout = TRUE, stderr = TRUE))
ok(!is.null(attr(st2, "status")) && any(grepl("Overlapping cohorts", st2)), "overlap guard blocks double-counting")

# --- 5. empty templates: pipeline must run and pool nothing -----------------
st3 <- system2("Rscript", c(file.path(here, "R/run_all.R"), "data/analysis_ready", file.path(tmp, "o3")), stdout = TRUE, stderr = TRUE)
ok(is.null(attr(st3, "status")) && !file.exists(file.path(tmp, "o3/tables/Table4_meta_analysis_summary.csv")),
   "empty verified dataset produces no pooled estimates")
unlink(tmp, recursive = TRUE)
cat("\nAll tests passed.\n")
