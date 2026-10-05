#!/usr/bin/env bash
# Run the full pipeline from the project root: bash 04_R_scripts/run_all.sh
set -euo pipefail
cd "$(dirname "$0")/.."
Rscript 04_R_scripts/00_setup.R
Rscript 04_R_scripts/01_mouse_signature.R
[ -d 03_processed_data/salmon ] && Rscript 04_R_scripts/01c_reprocess_deseq2.R || echo "Skipping 01c (run 01b_reprocess_raw.sh first if desired)"
Rscript 04_R_scripts/02_orthologues.R
Rscript 04_R_scripts/03_tcga_deseq2.R COAD
Rscript 04_R_scripts/03_tcga_deseq2.R READ
# ---- FREEZE CHECK: Analysis_Plan_v1 must be dated and committed before this line ----
Rscript 04_R_scripts/04_cross_species_overlap.R
Rscript 04_R_scripts/05_gsea.R
Rscript 04_R_scripts/06_ppi_network.R
Rscript 04_R_scripts/07_tcga_validation.R
Rscript 04_R_scripts/08_immune_infiltration.R
echo "Done. Fill ⟦R⟧ slots in 09_manuscript/Manuscript.md from 05_results/ and 07_tables/."
