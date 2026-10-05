#!/usr/bin/env bash
# 01b_reprocess_raw.sh — independent reprocessing of SRR15682843–SRR15682848 (sensitivity analysis 4).
# Requires: sra-tools (prefetch, fasterq-dump), fastp, salmon >= 1.10.
# FIRST fill 02_metadata/sra_runs.tsv with run -> tissue/group from the SRA RunInfo table
# (https://www.ncbi.nlm.nih.gov/Traces/study/ , search each SRR). Do not guess assignments.
set -euo pipefail
cd "$(dirname "$0")/.."

THREADS=${THREADS:-8}
IDX=03_processed_data/salmon_index_GRCm39
RAW=01_raw_data/fastq
OUT=03_processed_data/salmon
mkdir -p "$RAW" "$OUT"

if [ ! -d "$IDX" ]; then
  wget -q -P 01_raw_data https://ftp.ensembl.org/pub/release-112/fasta/mus_musculus/cdna/Mus_musculus.GRCm39.cdna.all.fa.gz
  wget -q -P 01_raw_data https://ftp.ensembl.org/pub/release-112/fasta/mus_musculus/dna/Mus_musculus.GRCm39.dna.primary_assembly.fa.gz
  zcat 01_raw_data/Mus_musculus.GRCm39.dna.primary_assembly.fa.gz | grep '^>' | cut -d' ' -f1 | sed 's/>//' > 01_raw_data/decoys.txt
  cat 01_raw_data/Mus_musculus.GRCm39.cdna.all.fa.gz 01_raw_data/Mus_musculus.GRCm39.dna.primary_assembly.fa.gz > 01_raw_data/gentrome.fa.gz
  salmon index -t 01_raw_data/gentrome.fa.gz -d 01_raw_data/decoys.txt -i "$IDX" -p "$THREADS"
fi

for i in $(seq 43 48); do
  R="SRR156828$i"
  [ -f "$OUT/$R/quant.sf" ] && continue
  prefetch "$R" -O "$RAW"
  fasterq-dump "$RAW/$R" -O "$RAW" -e "$THREADS" --split-files
  if [ -f "$RAW/${R}_2.fastq" ]; then
    fastp -i "$RAW/${R}_1.fastq" -I "$RAW/${R}_2.fastq" -o "$RAW/${R}_1.trim.fq.gz" -O "$RAW/${R}_2.trim.fq.gz" \
          -w "$THREADS" -j "$OUT/${R}_fastp.json" -h "$OUT/${R}_fastp.html"
    salmon quant -i "$IDX" -l A -1 "$RAW/${R}_1.trim.fq.gz" -2 "$RAW/${R}_2.trim.fq.gz" \
          --validateMappings --gcBias -p "$THREADS" -o "$OUT/$R"
  else
    fastp -i "$RAW/${R}.fastq" -o "$RAW/${R}.trim.fq.gz" -w "$THREADS" -j "$OUT/${R}_fastp.json" -h "$OUT/${R}_fastp.html"
    salmon quant -i "$IDX" -l A -r "$RAW/${R}.trim.fq.gz" --validateMappings --gcBias -p "$THREADS" -o "$OUT/$R"
  fi
  rm -f "$RAW/${R}"*.fastq
done
echo "Done. Next: Rscript 04_R_scripts/01c_reprocess_deseq2.R"
