# 02_orthologues.R — mouse -> human orthologue mapping (Ensembl BioMart).
# Primary analysis: one-to-one orthologues only. One-to-many are flagged and kept
# in a separate column for sensitivity analysis 1 — never silently resolved.
# OUTPUT: 03_processed_data/mouse_signature_human.tsv, 08_supplement/Table_S2_orthologues.tsv

source("04_R_scripts/00_setup.R")
library(biomaRt)

sig <- fread(P("03_processed_data", "mouse_signature.tsv"))
mart <- useEnsembl("genes", dataset = "mmusculus_gene_ensembl", version = 112)
orth <- as.data.table(getBM(
  attributes = c("ensembl_gene_id", "external_gene_name",
                 "hsapiens_homolog_ensembl_gene", "hsapiens_homolog_associated_gene_name",
                 "hsapiens_homolog_orthology_type", "hsapiens_homolog_orthology_confidence"),
  mart = mart))
setnames(orth, c("mm_ensembl", "mm_symbol", "hs_ensembl", "hs_symbol", "orth_type", "orth_conf"))
orth <- orth[hs_ensembl != ""]

# Join on Ensembl ID when present, otherwise on symbol
sig[, key := fifelse(!is.na(ensembl) & ensembl != "", ensembl, NA_character_)]
a <- merge(sig[!is.na(key)], orth, by.x = "key", by.y = "mm_ensembl", allow.cartesian = TRUE)
b <- merge(sig[is.na(key)], orth, by.x = "gene", by.y = "mm_symbol", allow.cartesian = TRUE)
map <- rbind(a, b, fill = TRUE)

map[, n_hs := uniqueN(hs_ensembl), by = gene]
map[, one2one := orth_type == "ortholog_one2one" & n_hs == 1]
fwrite(map, P("08_supplement", "Table_S2_orthologues.tsv"), sep = "\t")

primary <- unique(map[one2one == TRUE], by = "hs_ensembl")
fwrite(primary, P("03_processed_data", "mouse_signature_human.tsv"), sep = "\t")
fwrite(unique(map, by = c("gene", "hs_ensembl")),
       P("03_processed_data", "mouse_signature_human_incl_one2many.tsv"), sep = "\t")

writeLines(c(
  sprintf("Mouse genes in signature: %d", uniqueN(sig$gene)),
  sprintf("With any human orthologue: %d", uniqueN(map$gene)),
  sprintf("One-to-one orthologues: %d", nrow(primary)),
  sprintf("  of which DEGs: %d (UP %d, DOWN %d)", primary[is_deg == TRUE, .N],
          primary[direction == "UP", .N], primary[direction == "DOWN", .N]),
  sprintf("Flagged one-to-many/many-to-many genes: %d", uniqueN(map[one2one == FALSE]$gene))),
  P("05_results", "02_orthologue_summary.txt"))
