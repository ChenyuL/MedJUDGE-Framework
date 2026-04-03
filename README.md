# MedJUDGE Framework

Code and data repository for the manuscript:

**"MedJUDGE: A Framework for Evaluating LLM-as-a-Judge in Healthcare — A Scoping Review"**

## Overview

This repository contains the analysis scripts, figure generation code, and extracted data for a scoping review of LLM-as-a-Judge (LaaJ) applications in healthcare. The review follows PRISMA-ScR guidelines and covers 49 included studies identified from 12,379 records across PubMed, Web of Science, Scopus, IEEE Xplore, ACL Anthology, and grey literature sources.



## Data

**`full-text-reading - evidence generation-49.csv`** contains structured metadata for all 49 included studies with 56 columns covering:

- Study identifiers (title, authors, journal/venue, year, DOI)
- Methodology (study design, healthcare setting, medical specialty)
- LaaJ configuration (paradigm, judge model name/family, prompt strategy)
- Validation metrics (agreement scores, expert validator counts)
- Bias testing (positional, demographic, format biases)
- Reproducibility indicators (code/data/prompt availability, model versions)
- Deployment readiness assessment

## Scripts

### Core Analysis

| Script | Description |
|---|---|
| `analyze_papers.py` | Generates all summary statistics, tables (Tables 3, 8--13), and quantitative findings reported in the manuscript from the extracted CSV data |
| `verify_claims.py` | Systematically verifies 11 key manuscript claims against the raw data (e.g., bias testing rates, model family distributions, expert validator counts) |

### Main Figures

| Script | Output |
|---|---|
| `fig1_prisma.py` | **Figure 1** -- PRISMA 2020 flow diagram (12,379 records to 49 included studies) |
| `fig4_decision_tree.py` | **Figure 3** -- Paradigm selection decision tree with MedJUDGE Gateway risk tiering (Tier A/B/C) |
| `fig5_error_propagation.py` | **Figure 4** -- Error propagation in multi-judge systems: (A) cascaded error accumulation; (B) majority voting with correlated errors |

### Supplementary Figures

| Script | Output |
|---|---|
| `supp_fig1_year_distribution.py` | Temporal distribution (73.5% of studies from 2025--2026) |
| `supp_fig2_category_distribution.py` | Application categories (Evaluation/Benchmarking 75.5%, Multi-Agent 18.4%, RL 6.1%) |
| `supp_fig3_paradigm_distribution.py` | Evaluation paradigm distribution (Pointwise 85.7%, Pairwise 14.3%, Agent-based 12.2%) |
| `supp_fig4_judge_heatmap.py` | Judge model family vs. clinical task heatmap |
| `supp_fig5_reliability_complexity.py` | Reliability--complexity tradeoff scatter plot (N=22 studies with agreement scores) |
| `supp_fig6_validation_crisis.py` | Expert validator distribution (median=3; 26.5% AI-only) |
| `supp_fig7_validation_rigor_gaps.py` | Four-panel validation rigor gap analysis |
| `supp_fig8_bias_audit.py` | Bias testing audit card across 10 bias dimensions |
| `supp_fig9_transparency_radar.py` | Transparency gap radar chart (current vs. required standard) |

## Requirements

- Python 3.9+
- matplotlib
- numpy
- pandas (for `analyze_papers.py` and `verify_claims.py`)

Install dependencies:

```bash
pip install matplotlib numpy pandas
```

## Usage

### Reproduce all figures

```bash
# Main figures
python fig1_prisma.py
python fig4_decision_tree.py
python fig5_error_propagation.py

# Supplementary figures
python supp_fig1_year_distribution.py
python supp_fig2_category_distribution.py
python supp_fig3_paradigm_distribution.py
python supp_fig4_judge_heatmap.py
python supp_fig5_reliability_complexity.py
python supp_fig6_validation_crisis.py
python supp_fig7_validation_rigor_gaps.py
python supp_fig8_bias_audit.py
python supp_fig9_transparency_radar.py
```

### Run analysis

```bash
# Generate all tables and statistics
python analyze_papers.py

# Verify manuscript claims against data
python verify_claims.py
```

## License

This repository is provided for academic and research purposes accompanying the manuscript submission.

## Citation

If you use this code or data, please cite:

```
[Citation will be added upon publication]
```
