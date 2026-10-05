# 06_ppi_network.R — STRING network of concordant genes; candidate hub genes by
# consensus of degree, betweenness and Maximal Clique Centrality (MCC, as in cytoHubba).
# Concordant genes are capped at 150 (ranked by |mouse lfc x human lfc|) per Analysis_Plan.
# OUTPUT: 05_results/06_hubs.tsv, 06_figures/Fig5_network.pdf, 08_supplement/Table_S4_network_edges.tsv

source("04_R_scripts/00_setup.R")
suppressPackageStartupMessages({ library(STRINGdb); library(igraph) })

conc <- fread(P("03_processed_data", "concordant_genes.tsv"))[1:min(.N, 150)]
sdb <- STRINGdb$new(version = "12.0", species = 9606, score_threshold = PARAM$string_thr,
                    input_directory = P("01_raw_data"))
mp <- sdb$map(as.data.frame(conc[, .(hs_symbol, class)]), "hs_symbol", removeUnmappedRows = TRUE)
ed <- as.data.table(sdb$get_interactions(mp$STRING_id))
ed <- unique(ed[, .(from, to, combined_score)])
id2sym <- setNames(mp$hs_symbol, mp$STRING_id)
ed[, `:=`(from = id2sym[from], to = id2sym[to])]
fwrite(ed, P("08_supplement", "Table_S4_network_edges.tsv"), sep = "\t")

g <- simplify(graph_from_data_frame(ed, directed = FALSE))
mcc <- function(g) {  # sum over maximal cliques containing v of (|C|-1)!
  cl <- max_cliques(g); s <- setNames(numeric(vcount(g)), V(g)$name)
  for (c in cl) { v <- names(c) %||% V(g)$name[c]; s[v] <- s[v] + factorial(length(c) - 1) }
  s[degree(g) == 0] <- 0; s }
`%||%` <- function(a, b) if (is.null(a)) b else a

cen <- data.table(gene = V(g)$name, degree = degree(g), betweenness = betweenness(g, normalized = TRUE), MCC = mcc(g))
cen[, mean_rank := rowMeans(cbind(frank(-degree), frank(-betweenness), frank(-MCC)))]
cen <- merge(cen, conc[, .(gene = hs_symbol, class, mm_lfc, hs_lfc, replicated_READ)], by = "gene")
setorder(cen, mean_rank)
cen[, hub := seq_len(.N) <= PARAM$n_hubs]
fwrite(cen, P("05_results", "06_hubs.tsv"), sep = "\t")

comm <- cluster_louvain(g, resolution = 1)
fwrite(data.table(gene = V(g)$name, module = membership(comm)), P("05_results", "06_modules.tsv"), sep = "\t")

pdf(P("06_figures", "Fig5_network.pdf"), 7, 7)
set.seed(PARAM$seed)
cls <- cen$class[match(V(g)$name, cen$gene)]
plot(g, layout = layout_with_fr(g),
     vertex.color = ifelse(cls == "Concordant UP", "#B2182B", "#2166AC"),
     vertex.size = 3 + 2 * sqrt(degree(g)),
     vertex.label = ifelse(V(g)$name %in% cen[hub == TRUE]$gene, V(g)$name, NA),
     vertex.label.cex = 0.7, vertex.label.color = "black", vertex.frame.color = NA,
     edge.width = 0.5, edge.color = "grey70")
legend("bottomleft", c("Concordant UP", "Concordant DOWN"), pch = 21, pt.bg = c("#B2182B", "#2166AC"), bty = "n")
dev.off()
