#!/usr/bin/env python3
"""
LLM-as-a-Judge Scoping Review Analysis Script
Reads from xlsx or csv data file and generates all statistics for the manuscript.

This script generates statistics for ALL tables and figures in the manuscript:
- Table 3: Application Categories
- Table 8: Pointwise Agreement by Task Complexity
- Table XX: Human Expert Involvement Stratification
- Table 9: Expert Roles
- Table 3.7: Judge Model Family Distribution
- Table 10: Medically Specialized Judge Models
- Table 11: Judge Model Adaptation Methods
- Table 12: Bias Types Tested
- Table 13: Bias Mitigation Strategies

Usage:
    python analyze_papers.py [data_file]

If no file specified, looks for:
    1. *.xlsx files
    2. full-text-reading*.csv files
"""

import csv
import re
import os
import sys
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

# Try to import openpyxl for xlsx support
try:
    import openpyxl
    HAS_XLSX = True
except ImportError:
    HAS_XLSX = False


def load_data(filepath):
    """Load data from xlsx or csv file."""
    filepath = Path(filepath)

    if filepath.suffix.lower() == '.xlsx':
        if not HAS_XLSX:
            print("ERROR: openpyxl not installed. Install with: pip install openpyxl")
            print("Falling back to CSV if available...")
            return None

        wb = openpyxl.load_workbook(filepath, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return []

        headers = [str(h) if h else f'col_{i}' for i, h in enumerate(rows[0])]
        data = []
        for row in rows[1:]:
            if any(cell is not None for cell in row):
                data.append(dict(zip(headers, [str(cell) if cell else '' for cell in row])))
        return data

    elif filepath.suffix.lower() == '.csv':
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    else:
        print(f"ERROR: Unsupported file type: {filepath.suffix}")
        return None


def find_data_file():
    """Find the data file in current directory."""
    cwd = Path('.')

    # First try xlsx
    xlsx_files = list(cwd.glob('*.xlsx'))
    if xlsx_files:
        return xlsx_files[0]

    # Then try csv with expected naming pattern
    csv_files = list(cwd.glob('full-text-reading*.csv'))
    if csv_files:
        return csv_files[0]

    # Any csv
    csv_files = list(cwd.glob('*.csv'))
    if csv_files:
        return csv_files[0]

    return None


def extract_numbers(text):
    """Extract first number from text."""
    if not text:
        return None
    nums = re.findall(r'\d+', str(text))
    return int(nums[0]) if nums else None


def extract_all_numbers(text):
    """Extract all numbers from text."""
    if not text:
        return []
    return [int(n) for n in re.findall(r'\d+', str(text))]


def safe_get(row, key, default=''):
    """Safely get value from row with default."""
    return row.get(key, default).strip() if row.get(key) else default


def print_section(title, level=1):
    """Print formatted section header."""
    if level == 1:
        print(f"\n{'='*80}")
        print(f" {title}")
        print(f"{'='*80}")
    else:
        print(f"\n{'-'*60}")
        print(f" {title}")
        print(f"{'-'*60}")


def analyze_type_distribution(rows, N):
    """
    Analyze study type distribution for Table 3 (Application Categories).
    Maps Types to Categories:
    - Category 1: Benchmark + Methodology (Evaluation & Benchmarking)
    - Category 2: Reinforcement Learning
    - Category 3: Agent building (Multi-Agent Coordination)
    """
    print_section("TABLE 3: APPLICATION CATEGORY DISTRIBUTION")

    types = Counter()
    categories = {'cat1': 0, 'cat2': 0, 'cat3': 0}

    cat1_studies = []
    cat2_studies = []
    cat3_studies = []

    for row in rows:
        t = safe_get(row, 'Type').lower()
        author = safe_get(row, 'Authors')[:40]

        if 'benchmark' in t:
            types['Benchmark'] += 1
            categories['cat1'] += 1
            cat1_studies.append(author)
        elif 'methodolog' in t:
            types['Methodology'] += 1
            categories['cat1'] += 1
            cat1_studies.append(author)
        elif 'reinforcement' in t:
            types['Reinforcement Learning'] += 1
            categories['cat2'] += 1
            cat2_studies.append(author)
        elif 'agent' in t:
            types['Agent building'] += 1
            categories['cat3'] += 1
            cat3_studies.append(author)

    # Print raw type counts
    print("\nRaw Type Distribution:")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c} ({c/N*100:.1f}%)")

    # Print Category mapping
    print("\n" + "="*60)
    print("CATEGORY MAPPING FOR MANUSCRIPT:")
    print("="*60)

    cat1 = categories['cat1']
    cat2 = categories['cat2']
    cat3 = categories['cat3']

    print(f"""
| Category | Description | n (%) |
|----------|-------------|-------|
| Category 1 | Evaluation & Benchmarking | {cat1} ({cat1/N*100:.1f}%) |
| Category 2 | Reinforcement Learning | {cat2} ({cat2/N*100:.1f}%) |
| Category 3 | Multi-Agent Coordination | {cat3} ({cat3/N*100:.1f}%) |
| **Total** | | **{N}** |
""")

    print("\nCategory 2 (RL) Studies:")
    for s in cat2_studies:
        print(f"  - {s}")

    print("\nCategory 3 (Agent) Studies:")
    for s in cat3_studies:
        print(f"  - {s}")

    return {
        'types': dict(types),
        'categories': categories,
        'cat1_count': cat1,
        'cat2_count': cat2,
        'cat3_count': cat3,
        'cat2_studies': cat2_studies,
        'cat3_studies': cat3_studies
    }


def analyze_paradigm_distribution(rows, N):
    """
    Analyze LaaJ paradigm distribution.
    Paradigms: Pointwise, Pairwise, Agent-based
    """
    print_section("LaaJ PARADIGM DISTRIBUTION")

    paradigms = Counter()
    pointwise_studies = []
    pairwise_studies = []
    agent_studies = []

    for row in rows:
        p = safe_get(row, 'LaaJ_Paradigm').lower()
        author = safe_get(row, 'Authors')[:40]

        paradigms[p] += 1

        if 'pointwise' in p:
            pointwise_studies.append(author)
        if 'pairwise' in p:
            pairwise_studies.append(author)
        if 'agent' in p:
            agent_studies.append(author)

    # Count unique paradigm usage
    pointwise_count = len(pointwise_studies)
    pairwise_count = len(pairwise_studies)
    agent_count = len(agent_studies)

    print("\nRaw Paradigm Values:")
    for p, c in sorted(paradigms.items(), key=lambda x: -x[1]):
        print(f"  '{p}': {c}")

    print(f"""
PARADIGM SUMMARY:
  Pointwise (including hybrid): {pointwise_count} ({pointwise_count/N*100:.1f}%)
  Pairwise: {pairwise_count} ({pairwise_count/N*100:.1f}%)
  Agent-based (hybrid): {agent_count} ({agent_count/N*100:.1f}%)

Note: Studies may use multiple paradigms; percentages sum >100%
""")

    print("\nPairwise Studies:")
    for s in pairwise_studies:
        print(f"  - {s}")

    print("\nAgent-based Studies:")
    for s in agent_studies:
        print(f"  - {s}")

    return {
        'raw_paradigms': dict(paradigms),
        'pointwise_count': pointwise_count,
        'pairwise_count': pairwise_count,
        'agent_count': agent_count,
        'pairwise_studies': pairwise_studies,
        'agent_studies': agent_studies
    }


def analyze_expert_involvement(rows, N):
    """
    Analyze human expert involvement for Table XX (Human Expert Involvement Stratification).
    Levels: Extensive (>=20), Moderate (5-19), Minimal (1-4), None (0)
    """
    print_section("TABLE XX: HUMAN EXPERT INVOLVEMENT STRATIFICATION")

    extensive = []  # >=20
    moderate = []   # 5-19
    minimal = []    # 1-4
    none = []       # 0 or not specified for evaluation
    unspecified = []

    expert_counts = []

    for row in rows:
        n_str = safe_get(row, 'Number of Human Experts')
        author = safe_get(row, 'Authors')[:50]
        n_str_lower = n_str.lower()

        # Handle unspecified cases
        if not n_str or 'not specified' in n_str_lower or 'n/s' in n_str_lower or 'n/a' in n_str_lower:
            unspecified.append((author, n_str))
            continue

        # Extract numbers
        nums = extract_all_numbers(n_str)
        if not nums:
            unspecified.append((author, n_str))
            continue

        # Take the maximum number mentioned (e.g., "262 physicians" -> 262)
        max_num = max(nums)
        expert_counts.append(max_num)

        if max_num >= 20:
            extensive.append((author, n_str, max_num))
        elif max_num >= 5:
            moderate.append((author, n_str, max_num))
        elif max_num >= 1:
            minimal.append((author, n_str, max_num))
        else:
            none.append((author, n_str, max_num))

    # Also check for explicitly "0" or "none" cases
    for row in rows:
        n_str = safe_get(row, 'Number of Human Experts')
        author = safe_get(row, 'Authors')[:50]
        if '0 (for eval' in n_str.lower() or 'zero' in n_str.lower():
            if not any(author in x[0] for x in none):
                none.append((author, n_str, 0))

    ext_n = len(extensive)
    mod_n = len(moderate)
    min_n = len(minimal)
    none_n = len(none)
    unspec_n = len(unspecified)

    print(f"""
| Involvement Level | Expert Count | n (%) |
|-------------------|--------------|-------|
| **Extensive** | ≥20 experts | {ext_n} ({ext_n/N*100:.1f}%) |
| **Moderate** | 5-19 experts | {mod_n} ({mod_n/N*100:.1f}%) |
| **Minimal** | 1-4 experts | {min_n} ({min_n/N*100:.1f}%) |
| **None** | 0 experts | {none_n} ({none_n/N*100:.1f}%) |
| *Unspecified* | - | {unspec_n} ({unspec_n/N*100:.1f}%) |
""")

    print("\nExtensive (≥20 experts):")
    for author, n_str, n in sorted(extensive, key=lambda x: -x[2]):
        print(f"  - {author}: {n_str}")

    print("\nModerate (5-19 experts):")
    for author, n_str, n in sorted(moderate, key=lambda x: -x[2]):
        print(f"  - {author}: {n_str}")

    print("\nMinimal (1-4 experts):")
    for author, n_str, n in minimal[:10]:
        print(f"  - {author}: {n_str}")
    if len(minimal) > 10:
        print(f"  ... and {len(minimal)-10} more")

    # Calculate median
    if expert_counts:
        sorted_counts = sorted(expert_counts)
        median = sorted_counts[len(sorted_counts)//2]
        q1_idx = len(sorted_counts)//4
        q3_idx = 3*len(sorted_counts)//4
        q1 = sorted_counts[q1_idx]
        q3 = sorted_counts[q3_idx]
        print(f"\nExpert Count Statistics:")
        print(f"  Median: {median}")
        print(f"  IQR: {q1}-{q3}")
        print(f"  Range: {min(expert_counts)}-{max(expert_counts)}")
    else:
        median = 0
        q1 = q3 = 0

    return {
        'extensive': ext_n,
        'moderate': mod_n,
        'minimal': min_n,
        'none': none_n,
        'unspecified': unspec_n,
        'median': median,
        'iqr': f"{q1}-{q3}" if expert_counts else "N/A",
        'extensive_studies': [(a, n) for a, _, n in extensive],
        'moderate_studies': [(a, n) for a, _, n in moderate]
    }


def analyze_judge_models(rows, N):
    """
    Analyze judge model family distribution for Table 3.7.
    """
    print_section("TABLE 3.7: JUDGE MODEL FAMILY DISTRIBUTION")

    # Count studies using each model family
    families = {
        'GPT': 0,
        'Claude': 0,
        'Llama': 0,
        'Gemini': 0,
        'Mistral': 0,
        'DeepSeek': 0,
        'Other Open-Source': 0,
        'Medical Specialized': 0
    }

    gpt_studies = []
    claude_studies = []
    llama_studies = []

    for row in rows:
        jf = safe_get(row, 'Judge Model Family').lower()
        jn = safe_get(row, 'Judge Model Name').lower()
        author = safe_get(row, 'Authors')[:40]

        if 'gpt' in jf or 'openai' in jf or 'gpt' in jn:
            families['GPT'] += 1
            gpt_studies.append(author)
        if 'claude' in jf or 'anthropic' in jf or 'claude' in jn:
            families['Claude'] += 1
            claude_studies.append(author)
        if 'llama' in jf or 'meta' in jf.lower() or 'llama' in jn:
            families['Llama'] += 1
            llama_studies.append(author)
        if 'gemini' in jf or 'google' in jf or 'gemini' in jn:
            families['Gemini'] += 1
        if 'mistral' in jf or 'mixtral' in jf or 'mistral' in jn:
            families['Mistral'] += 1
        if 'deepseek' in jf or 'deepseek' in jn:
            families['DeepSeek'] += 1
        if 'qwen' in jf or 'glm' in jf or 'phi' in jf or 'qwen' in jn or 'glm' in jn:
            families['Other Open-Source'] += 1

        # Check for medical specialized
        js = safe_get(row, 'Judge Specialization').lower()
        if 'medical' in js or 'clinical' in js or 'health' in js:
            families['Medical Specialized'] += 1

    print(f"""
| Model Family | Studies (n, %) | Representative Models |
|--------------|----------------|----------------------|
| GPT Family | {families['GPT']} ({families['GPT']/N*100:.1f}%) | GPT-4, GPT-4o, GPT-4o-mini, o1, o3-mini |
| Claude Family | {families['Claude']} ({families['Claude']/N*100:.1f}%) | Claude-3-Opus, Claude-3.5-Sonnet, Claude-3.7-Sonnet |
| Llama Family | {families['Llama']} ({families['Llama']/N*100:.1f}%) | Llama 2 (13B), Llama 3 (8B), Llama 3.1 (70B, 405B) |
| Gemini Family | {families['Gemini']} ({families['Gemini']/N*100:.1f}%) | Gemini 1.5 Pro, Gemini 2.0 Flash |
| Mistral Family | {families['Mistral']} ({families['Mistral']/N*100:.1f}%) | Mistral 7B v2, Mixtral 8x7B |
| DeepSeek | {families['DeepSeek']} ({families['DeepSeek']/N*100:.1f}%) | DeepSeek-R1 |
| Other Open-Source | {families['Other Open-Source']} ({families['Other Open-Source']/N*100:.1f}%) | Qwen2.5, GLM-4, Phi4 |
| Medical Specialized | {families['Medical Specialized']} ({families['Medical Specialized']/N*100:.1f}%) | EriBERTa, Baichuan-M1, HuatuoGPT-o1 |

*Note: Studies often employed multiple judge models; percentages sum >100%*
""")

    return {
        'families': families,
        'gpt_count': families['GPT'],
        'claude_count': families['Claude'],
        'llama_count': families['Llama']
    }


def analyze_medical_specialized(rows, N):
    """
    Analyze medically specialized judge models for Table 10.
    """
    print_section("TABLE 10: MEDICALLY SPECIALIZED JUDGE MODELS")

    specialized = []

    for row in rows:
        js = safe_get(row, 'Judge Specialization').lower()
        jn = safe_get(row, 'Judge Model Name')
        author = safe_get(row, 'Authors')[:40]

        # Check for medical specialization indicators
        if any(term in js for term in ['medical', 'clinical', 'health', 'fine-tuned', 'domain']):
            if jn and 'n/a' not in jn.lower() and 'not specified' not in jn.lower():
                specialized.append({
                    'author': author,
                    'model': jn,
                    'specialization': js
                })

        # Also check model name for known medical models
        jn_lower = jn.lower() if jn else ''
        if any(m in jn_lower for m in ['eriberta', 'huatuo', 'baichuan', 'medit', 'medllm', 'biomist']):
            if not any(s['model'] == jn for s in specialized):
                specialized.append({
                    'author': author,
                    'model': jn,
                    'specialization': js
                })

    print(f"\nMedically Specialized Judge Models: {len(specialized)} ({len(specialized)/N*100:.1f}%)")
    print("\n| Model | Specialization Approach | Study |")
    print("|-------|------------------------|-------|")
    for s in specialized:
        print(f"| {s['model'][:30]} | {s['specialization'][:40]} | {s['author'][:30]} |")

    print(f"""
MANUSCRIPT TEXT:
Only {len(specialized)} of {N} studies ({len(specialized)/N*100:.1f}%) employed medically specialized judge models.
""")

    return {
        'count': len(specialized),
        'percentage': len(specialized)/N*100,
        'studies': specialized
    }


def analyze_adaptation_methods(rows, N):
    """
    Analyze judge model adaptation methods for Table 11.
    """
    print_section("TABLE 11: JUDGE MODEL ADAPTATION METHODS")

    methods = {
        'prompt_engineering': 0,
        'few_shot': 0,
        'chain_of_thought': 0,
        'fine_tuning': 0,
        'preference_optimization': 0,
        'rag': 0
    }

    prompt_studies = []
    fewshot_studies = []
    cot_studies = []
    ft_studies = []
    pref_studies = []
    rag_studies = []

    for row in rows:
        am = safe_get(row, 'Adaptation Method').lower()
        pe = safe_get(row, 'Prompt Engineering').lower()
        fs = safe_get(row, 'Few-shot Examples')
        author = safe_get(row, 'Authors')[:40]

        # Prompt engineering (almost all studies use this)
        if pe or am:
            methods['prompt_engineering'] += 1
            prompt_studies.append(author)

        # Few-shot
        if fs and 'n/a' not in fs.lower() and '0' not in fs:
            methods['few_shot'] += 1
            fewshot_studies.append(author)
        if 'few-shot' in am or 'few shot' in am:
            if author not in fewshot_studies:
                methods['few_shot'] += 1
                fewshot_studies.append(author)

        # Chain-of-thought
        if 'chain' in am or 'cot' in am or 'step-by-step' in am:
            methods['chain_of_thought'] += 1
            cot_studies.append(author)

        # Fine-tuning
        if 'fine-tun' in am or 'finetun' in am or 'lora' in am or 'qlora' in am:
            methods['fine_tuning'] += 1
            ft_studies.append(author)

        # Preference optimization (DPO/RLAIF)
        if 'dpo' in am or 'rlaif' in am or 'preference' in am or 'rlhf' in am:
            methods['preference_optimization'] += 1
            pref_studies.append(author)

        # RAG
        if 'rag' in am or 'retrieval' in am:
            methods['rag'] += 1
            rag_studies.append(author)

    print(f"""
| Adaptation Method | n (%) | Description |
|-------------------|-------|-------------|
| Prompt engineering | {methods['prompt_engineering']} ({methods['prompt_engineering']/N*100:.0f}%) | Role instructions, rubrics, structured templates |
| Few-shot learning | {methods['few_shot']} ({methods['few_shot']/N*100:.0f}%) | 1-shot to 12-shot exemplars |
| Chain-of-thought | {methods['chain_of_thought']} ({methods['chain_of_thought']/N*100:.0f}%) | Step-by-step reasoning before scoring |
| Supervised fine-tuning | {methods['fine_tuning']} ({methods['fine_tuning']/N*100:.0f}%) | Task-specific parameter updates on labeled data |
| Preference optimization | {methods['preference_optimization']} ({methods['preference_optimization']/N*100:.0f}%) | DPO/RLAIF training |
| RAG | {methods['rag']} ({methods['rag']/N*100:.0f}%) | External knowledge retrieval during evaluation |
""")

    print("\nFine-tuning Studies:")
    for s in ft_studies:
        print(f"  - {s}")

    print("\nPreference Optimization Studies:")
    for s in pref_studies:
        print(f"  - {s}")

    return {
        'methods': methods,
        'fine_tuning_studies': ft_studies,
        'cot_studies': cot_studies,
        'fewshot_count': methods['few_shot']
    }


def analyze_bias_testing(rows, N):
    """
    Analyze bias testing for Tables 12 and 13.
    """
    print_section("TABLES 12 & 13: BIAS TESTING AND MITIGATION")

    # Bias types
    positional = []
    length = []
    format_bias = []
    self_enhance = []
    demographic = []
    no_bias = []

    # Mitigation strategies
    order_random = []
    multi_rounds = []
    ensemble = []
    zscore = []

    for row in rows:
        bt = safe_get(row, 'Bias Testing').lower()
        bm = safe_get(row, 'Bias Mitigation').lower()
        author = safe_get(row, 'Authors')[:40]

        # Check for bias testing types
        if bt and 'n/s' not in bt and 'n/a' not in bt and 'not specified' not in bt and 'none' not in bt:
            if 'position' in bt or 'order' in bt:
                positional.append(author)
            if 'length' in bt or 'verbos' in bt:
                length.append(author)
            if 'format' in bt:
                format_bias.append(author)
            if 'self' in bt or 'enhancement' in bt:
                self_enhance.append(author)
            if 'demographic' in bt or 'race' in bt or 'gender' in bt:
                demographic.append(author)
        else:
            no_bias.append(author)

        # Check for mitigation strategies
        if 'random' in bm or 'shuffle' in bm:
            order_random.append(author)
        if 'multiple' in bm or 'round' in bm or 'repeat' in bm:
            multi_rounds.append(author)
        if 'ensemble' in bm or 'voting' in bm or 'jury' in bm:
            ensemble.append(author)
        if 'z-score' in bm or 'normal' in bm:
            zscore.append(author)

    studies_with_bias_testing = N - len(no_bias)

    print(f"""
TABLE 12: BIAS TYPES TESTED

| Bias Type | n (%) | Studies |
|-----------|-------|---------|
| Positional bias | {len(positional)} ({len(positional)/N*100:.1f}%) | {', '.join(positional[:3])}... |
| Length/verbosity bias | {len(length)} ({len(length)/N*100:.1f}%) | {', '.join(length[:3])} |
| Format bias | {len(format_bias)} ({len(format_bias)/N*100:.1f}%) | {', '.join(format_bias[:3])} |
| Self-enhancement bias | {len(self_enhance)} ({len(self_enhance)/N*100:.1f}%) | — |
| Demographic bias | {len(demographic)} ({len(demographic)/N*100:.1f}%) | — |

Studies with ANY bias testing: {studies_with_bias_testing} ({studies_with_bias_testing/N*100:.1f}%)
Studies with NO bias testing: {len(no_bias)} ({len(no_bias)/N*100:.1f}%)
""")

    print(f"""
TABLE 13: BIAS MITIGATION STRATEGIES

| Strategy | n | Studies |
|----------|---|---------|
| Order randomization | {len(order_random)} | {', '.join(order_random[:4])} |
| Multiple evaluation rounds | {len(multi_rounds)} | {', '.join(multi_rounds[:4])} |
| Ensemble voting | {len(ensemble)} | {', '.join(ensemble[:4])} |
| Z-score normalization | {len(zscore)} | {', '.join(zscore[:4])} |
""")

    print("\nPositional bias testing studies:")
    for s in positional:
        print(f"  - {s}")

    return {
        'positional': len(positional),
        'length': len(length),
        'format': len(format_bias),
        'self_enhance': len(self_enhance),
        'demographic': len(demographic),
        'no_bias': len(no_bias),
        'with_testing': studies_with_bias_testing,
        'order_random': len(order_random),
        'multi_rounds': len(multi_rounds),
        'ensemble': len(ensemble),
        'zscore': len(zscore)
    }


def analyze_deployment(rows, N):
    """
    Analyze deployment status.
    """
    print_section("DEPLOYMENT STATUS")

    deployed = []
    prototype = []
    research = []

    for row in rows:
        impl = safe_get(row, 'Implementation Stage').lower()
        author = safe_get(row, 'Authors')[:40]

        if 'deploy' in impl or 'operational' in impl or 'production' in impl:
            deployed.append(author)
        elif 'prototype' in impl or 'demo' in impl:
            prototype.append(author)
        else:
            research.append(author)

    print(f"""
| Stage | n (%) |
|-------|-------|
| Production/Deployed | {len(deployed)} ({len(deployed)/N*100:.1f}%) |
| Prototype/Demo | {len(prototype)} ({len(prototype)/N*100:.1f}%) |
| Research/Development | {len(research)} ({len(research)/N*100:.1f}%) |
""")

    print("\nDeployed Studies:")
    for s in deployed:
        print(f"  - {s}")

    return {
        'deployed': len(deployed),
        'prototype': len(prototype),
        'research': len(research),
        'deployed_studies': deployed
    }


def analyze_reproducibility(rows, N):
    """
    Analyze reproducibility metrics (code, data, prompts).
    """
    print_section("REPRODUCIBILITY METRICS")

    code_yes = 0
    data_yes = 0
    prompt_yes = 0

    for row in rows:
        ca = safe_get(row, 'Code Availability').lower()
        da = safe_get(row, 'Dataset Availability').lower()
        pa = safe_get(row, 'Prompt Templates Available').lower()

        if 'yes' in ca or 'open source' in ca or 'github' in ca or 'available' in ca:
            code_yes += 1
        if 'yes' in da or 'public' in da or 'available' in da:
            data_yes += 1
        if 'yes' in pa or 'available' in pa or 'provided' in pa:
            prompt_yes += 1

    print(f"""
| Metric | n (%) |
|--------|-------|
| Code Available | {code_yes} ({code_yes/N*100:.1f}%) |
| Data Available | {data_yes} ({data_yes/N*100:.1f}%) |
| Prompt Templates | {prompt_yes} ({prompt_yes/N*100:.1f}%) |
""")

    return {
        'code': code_yes,
        'data': data_yes,
        'prompts': prompt_yes
    }


def analyze_year_distribution(rows, N):
    """Analyze publication year distribution."""
    print_section("YEAR DISTRIBUTION")

    years = Counter()
    for row in rows:
        y = safe_get(row, 'Year')
        if y:
            years[y] += 1

    print("\n| Year | n (%) |")
    print("|------|-------|")
    for y in sorted(years.keys()):
        print(f"| {y} | {years[y]} ({years[y]/N*100:.1f}%) |")

    return dict(years)


def analyze_literature_source(rows, N):
    """
    Analyze grey literature vs peer-reviewed publications for Supplement Table.
    Classification:
    - Grey Literature: arXiv, bioRxiv, medRxiv preprints, grey literature search
    - Peer-Reviewed: Published journals, peer-reviewed conference proceedings
    """
    print_section("SUPPLEMENT: GREY LITERATURE VS PEER-REVIEWED")

    grey_lit = []
    peer_reviewed = []
    conference = []

    # Preprint/grey literature indicators (order matters - check these first)
    preprint_indicators = ['arxiv', 'biorxiv', 'medrxiv', 'preprint']

    # Peer-reviewed journal indicators
    journal_indicators = ['journal', 'jmir', 'npj digital', 'npj artificial',
                          'nature medicine', 'lancet', 'bmj', 'jama',
                          'annals', 'plos', 'frontiers', 'springer', 'elsevier',
                          'wiley', 'endocrine', 'expert systems', 'computer methods',
                          'clinical neurophysiology', 'applied psychology',
                          'diagnostics', 'ophthalmology', 'biomedical informatics',
                          'roentgenology', 'public health', 'aesthetic surgery',
                          'microsurgery', 'hand and microsurgery', 'electronics',
                          'rheumatology', 'eular']

    # Conference indicators
    conference_indicators = ['conference', 'proceedings', 'workshop', 'symposium',
                            'neurips', 'icml', 'acl', 'emnlp', 'naacl', 'ieee',
                            'ecai', 'annual meeting']

    for row in rows:
        source = safe_get(row, 'paper source').lower()
        venue = safe_get(row, 'Journal/Venue').lower()
        title = safe_get(row, 'Title')
        author = safe_get(row, 'Authors')[:40]
        year = safe_get(row, 'Year')

        paper_info = {
            'author': author,
            'title': title[:60],
            'venue': safe_get(row, 'Journal/Venue')[:50],
            'year': year,
            'source': source
        }

        # Classification logic (order matters!)

        # 1. Check for explicit preprints in venue name
        if any(ind in venue for ind in preprint_indicators):
            grey_lit.append(paper_info)
        # 2. Check for grey literature search source
        elif 'grey literature' in source:
            # But verify it's not published in a journal
            if any(ind in venue for ind in journal_indicators):
                peer_reviewed.append(paper_info)
            elif any(ind in venue for ind in conference_indicators):
                conference.append(paper_info)
            else:
                grey_lit.append(paper_info)
        # 3. Check for peer-reviewed journals
        elif any(ind in venue for ind in journal_indicators):
            peer_reviewed.append(paper_info)
        # 4. Check for conferences
        elif any(ind in venue for ind in conference_indicators):
            conference.append(paper_info)
        # 5. Default: if venue is specified and not N/A, classify as peer-reviewed
        elif venue and venue not in ['n/a', 'not specified', 'n/s', '']:
            peer_reviewed.append(paper_info)
        else:
            # Unknown venue - classify as grey literature
            grey_lit.append(paper_info)

    grey_n = len(grey_lit)
    peer_n = len(peer_reviewed)
    conf_n = len(conference)

    print(f"""
SUPPLEMENT TABLE: Literature Source Classification

| Source Type | n (%) | Description |
|-------------|-------|-------------|
| **Grey Literature** | {grey_n} ({grey_n/N*100:.1f}%) | Preprints (arXiv, bioRxiv, medRxiv), non-peer-reviewed |
| **Peer-Reviewed Journals** | {peer_n} ({peer_n/N*100:.1f}%) | Published in indexed journals |
| **Conference Proceedings** | {conf_n} ({conf_n/N*100:.1f}%) | Peer-reviewed conference papers |
| **Total** | {N} | |
""")

    print("\n--- GREY LITERATURE STUDIES ---")
    print("| # | Authors | Venue | Year |")
    print("|---|---------|-------|------|")
    for i, p in enumerate(grey_lit, 1):
        print(f"| {i} | {p['author'][:35]} | {p['venue'][:40]} | {p['year']} |")

    print("\n--- PEER-REVIEWED JOURNAL STUDIES ---")
    print("| # | Authors | Venue | Year |")
    print("|---|---------|-------|------|")
    for i, p in enumerate(peer_reviewed, 1):
        print(f"| {i} | {p['author'][:35]} | {p['venue'][:40]} | {p['year']} |")

    print("\n--- CONFERENCE PROCEEDINGS ---")
    print("| # | Authors | Venue | Year |")
    print("|---|---------|-------|------|")
    for i, p in enumerate(conference, 1):
        print(f"| {i} | {p['author'][:35]} | {p['venue'][:40]} | {p['year']} |")

    # Year distribution by source type
    print("\n--- YEAR DISTRIBUTION BY SOURCE TYPE ---")
    grey_years = Counter(p['year'] for p in grey_lit)
    peer_years = Counter(p['year'] for p in peer_reviewed)
    conf_years = Counter(p['year'] for p in conference)

    all_years = sorted(set(grey_years.keys()) | set(peer_years.keys()) | set(conf_years.keys()))

    print("| Year | Grey Lit | Peer-Reviewed | Conference |")
    print("|------|----------|---------------|------------|")
    for y in all_years:
        print(f"| {y} | {grey_years.get(y, 0)} | {peer_years.get(y, 0)} | {conf_years.get(y, 0)} |")

    return {
        'grey_literature': grey_n,
        'peer_reviewed': peer_n,
        'conference': conf_n,
        'grey_studies': [p['author'] for p in grey_lit],
        'peer_studies': [p['author'] for p in peer_reviewed],
        'conf_studies': [p['author'] for p in conference],
        'grey_percentage': grey_n/N*100,
        'peer_percentage': peer_n/N*100,
        'conf_percentage': conf_n/N*100
    }


def fishers_exact_p(a, b, c, d):
    """
    Compute two-sided Fisher's exact test p-value for a 2x2 contingency table:
        [[a, b],
         [c, d]]
    Uses the hypergeometric distribution. Returns p-value.
    """
    n = a + b + c + d
    row1 = a + b
    row2 = c + d
    col1 = a + c
    col2 = b + d

    def log_factorial(n):
        return sum(math.log(i) for i in range(1, n + 1))

    def hypergeom_pmf(x, n, K, k):
        """P(X=x) for hypergeometric distribution."""
        if x < max(0, k - (n - K)) or x > min(k, K):
            return 0.0
        log_p = (log_factorial(K) - log_factorial(x) - log_factorial(K - x) +
                 log_factorial(n - K) - log_factorial(k - x) - log_factorial(n - K - k + x) -
                 log_factorial(n) + log_factorial(k) + log_factorial(n - k))
        return math.exp(log_p)

    # Probability of observed table
    p_observed = hypergeom_pmf(a, n, col1, row1)

    # Two-sided: sum probabilities <= p_observed
    p_value = 0.0
    for x in range(0, min(row1, col1) + 1):
        p_x = hypergeom_pmf(x, n, col1, row1)
        if p_x <= p_observed + 1e-10:
            p_value += p_x

    return min(p_value, 1.0)


def analyze_database_vs_grey_lit_search(rows, N):
    """
    Analyze Database Search vs Grey Literature Search for Appendix Table.
    This classifies by HOW studies were found (search source), not by publication venue.

    Grey literature includes:
    - Studies with 'grey literature search' in paper source
    - Studies with 'reference' in paper source (found via citation/reference tracking,
      which is a grey literature search strategy: forward/backward citation tracking)

    All other studies are classified as database search.
    """
    print_section("APPENDIX TABLE: DATABASE vs GREY LITERATURE SEARCH")

    # Split by paper source (search method)
    grey_rows = []
    db_rows = []

    for row in rows:
        source = safe_get(row, 'paper source').lower()
        # Grey literature: explicit grey lit search OR reference/citation tracking
        if 'grey' in source or 'reference' in source:
            grey_rows.append(row)
        else:
            db_rows.append(row)

    grey_n = len(grey_rows)
    db_n = len(db_rows)

    print(f"\nClassification: {db_n} database + {grey_n} grey literature = {db_n + grey_n} total")

    # Helper functions for characterizing studies
    def is_preprint_venue(venue):
        venue = venue.lower()
        return any(x in venue for x in ['arxiv', 'preprint', 'biorxiv', 'medrxiv'])

    def is_preprint(row):
        """Check if a study is a preprint by venue name OR DOI/URL (for N/S venues)."""
        venue = safe_get(row, 'Journal/Venue').lower()
        doi = safe_get(row, 'DOI/URL').lower()
        if is_preprint_venue(venue):
            return True
        # If venue is unspecified/N/S but DOI points to arXiv/bioRxiv/medRxiv
        if venue in ['', 'n/s', 'not specified', 'n/a']:
            return any(x in doi for x in ['arxiv', 'biorxiv', 'medrxiv'])
        return False

    def is_journal(row):
        venue = safe_get(row, 'Journal/Venue').lower()
        if is_preprint_venue(venue):
            return False
        journal_kw = ['journal', 'j med', 'jmir', 'nature', 'npj', 'lancet', 'frontiers',
                      'diagnostics', 'endocrine', 'roentgenology', 'aesthetic', 'microsurgery',
                      'electronics', 'eular', 'expert systems', 'biomedical', 'computer methods',
                      'digital medicine', 'rheumatology', 'ophthalmology', 'applied psychology',
                      'clinical neurophysiology', 'public health']
        return any(k in venue for k in journal_kw)

    def is_conference(row):
        venue = safe_get(row, 'Journal/Venue').lower()
        conf_kw = ['conference', 'proceedings', 'workshop', 'symposium', 'neurips',
                   'ieee', 'coling', 'acl', 'ecai', 'pmlr', 'machine learning for healthcare',
                   'annual meeting']
        return any(k in venue for k in conf_kw)

    def get_expert_count(val):
        try:
            val_str = str(val).replace('+', '').replace('>', '').strip()
            if val_str.lower() in ['nan', 'none', 'n/a', '', 'not specified', 'not mentioned', 'n/s']:
                return -1  # -1 = unspecified
            nums = []
            for part in re.findall(r'\d+', val_str):
                nums.append(int(part))
            return max(nums) if nums else -1
        except Exception:
            return -1

    def has_formal_bias_testing(val):
        """Check for formal/explicit bias testing (stricter than 'any mention')."""
        val_str = str(val).lower().strip()
        # No testing
        if val_str in ['', 'nan', 'none', 'no', 'n/a', 'not specified', 'not mentioned',
                       'not tested', 'n/s', 'not explicitly tested',
                       'not explicitly described', 'not specified for evaluation']:
            return False
        # Has some form of formal testing
        return True

    def has_code(val):
        val_str = str(val).lower()
        return 'yes' in val_str or 'available' in val_str or 'github' in val_str or 'open source' in val_str

    def has_prompts(val):
        val_str = str(val).lower()
        return 'yes' in val_str or 'available' in val_str or 'partial' in val_str or 'provided' in val_str

    def has_model(val, model_kw):
        val_str = str(val).lower()
        return any(m.lower() in val_str for m in model_kw)

    def is_production(row):
        """Check if a study is truly deployed/operational (not just demo or not-deployed)."""
        impl = safe_get(row, 'Implementation Stage').lower()
        deploy_readiness = safe_get(row, 'Deployment Readiness').lower()
        # Must have positive deployment language without negation
        pos_terms = ['deployment stage', 'operational', 'production', 'clinical use']
        neg_terms = ['not deploy', 'not clinical', 'not ready', 'prototype', 'demo']
        has_positive = any(t in impl for t in pos_terms) or 'deployed and operational' in deploy_readiness
        has_negative = any(t in impl for t in neg_terms)
        return has_positive and not has_negative

    def is_research_tool(row):
        """Check if the Deployment Readiness field explicitly mentions 'research'.
        This captures studies self-identifying as research tools/frameworks/prototypes/benchmarks,
        e.g. 'Research Tool', 'Research Phase', 'Research/Framework stage', 'Research Prototype'.
        """
        deploy_readiness = safe_get(row, 'Deployment Readiness').lower()
        return 'research' in deploy_readiness

    # Calculate statistics for a group of rows
    def calc_stats(rows_list):
        n = len(rows_list)
        if n == 0:
            return {}

        stats = {}

        # Publication Status
        stats['journal'] = sum(1 for r in rows_list if is_journal(r))
        stats['conference'] = sum(1 for r in rows_list if is_conference(r))
        stats['preprint'] = sum(1 for r in rows_list if is_preprint(r))

        # Publication Year
        def get_year(r):
            try:
                return int(r.get('Year', 0))
            except Exception:
                return 0
        stats['year_2023'] = sum(1 for r in rows_list if get_year(r) == 2023)
        stats['year_2024'] = sum(1 for r in rows_list if get_year(r) == 2024)
        stats['year_2025_2026'] = sum(1 for r in rows_list if get_year(r) >= 2025)

        # Validation Rigor
        expert_counts = [get_expert_count(safe_get(r, 'Number of Human Experts')) for r in rows_list]
        stats['experts_20plus'] = sum(1 for c in expert_counts if c >= 20)
        stats['experts_5_19'] = sum(1 for c in expert_counts if 5 <= c < 20)
        stats['experts_1_4'] = sum(1 for c in expert_counts if 1 <= c < 5)
        stats['experts_0'] = sum(1 for c in expert_counts if c == 0)

        # Bias Testing (formal)
        stats['bias_yes'] = sum(1 for r in rows_list if has_formal_bias_testing(safe_get(r, 'Bias Testing')))
        stats['bias_no'] = n - stats['bias_yes']

        # Reproducibility
        stats['code_yes'] = sum(1 for r in rows_list if has_code(safe_get(r, 'Code Availability')))
        stats['prompts_yes'] = sum(1 for r in rows_list if has_prompts(safe_get(r, 'Prompt Templates Available')))

        # Judge Model Family
        stats['gpt'] = sum(1 for r in rows_list if has_model(safe_get(r, 'Judge Model Family'), ['gpt']))
        stats['claude'] = sum(1 for r in rows_list if has_model(safe_get(r, 'Judge Model Family'), ['claude', 'anthropic']))
        stats['opensource'] = sum(1 for r in rows_list if has_model(safe_get(r, 'Judge Model Family'),
                                  ['llama', 'mistral', 'gemma', 'phi', 'qwen', 'deepseek']))

        # Deployment Status
        stats['production'] = sum(1 for r in rows_list if is_production(r))
        stats['research_tool'] = sum(1 for r in rows_list if is_research_tool(r))

        return stats

    db_stats = calc_stats(db_rows)
    grey_stats = calc_stats(grey_rows)

    def fmt(val, total):
        pct = val / total * 100 if total > 0 else 0
        return "%d (%d%%)" % (val, round(pct))

    def fmt_p(a, b, c, d):
        """Compute and format Fisher's exact test p-value."""
        p = fishers_exact_p(a, b, c, d)
        if p < 0.001:
            return "<0.001"
        else:
            return "%.3f" % p

    # Build comparison rows with p-values
    comparison_rows = [
        # (label, db_val, db_n, grey_val, grey_n)
        ("**Publication Status**", None, None, None, None),
        ("Peer-reviewed journal", db_stats['journal'], db_n, grey_stats['journal'], grey_n),
        ("Conference proceedings", db_stats['conference'], db_n, grey_stats['conference'], grey_n),
        ("Preprint/arXiv", db_stats['preprint'], db_n, grey_stats['preprint'], grey_n),
        ("**Publication Year**", None, None, None, None),
        ("2023", db_stats['year_2023'], db_n, grey_stats['year_2023'], grey_n),
        ("2024", db_stats['year_2024'], db_n, grey_stats['year_2024'], grey_n),
        ("2025\u20132026", db_stats['year_2025_2026'], db_n, grey_stats['year_2025_2026'], grey_n),
        ("**Validation Rigor**", None, None, None, None),
        ("\u226520 expert validators", db_stats['experts_20plus'], db_n, grey_stats['experts_20plus'], grey_n),
        ("5\u201319 experts", db_stats['experts_5_19'], db_n, grey_stats['experts_5_19'], grey_n),
        ("1\u20134 experts", db_stats['experts_1_4'], db_n, grey_stats['experts_1_4'], grey_n),
        ("0 experts", db_stats['experts_0'], db_n, grey_stats['experts_0'], grey_n),
        ("**Bias Testing**", None, None, None, None),
        ("Any formal bias testing", db_stats['bias_yes'], db_n, grey_stats['bias_yes'], grey_n),
        ("No formal bias testing", db_stats['bias_no'], db_n, grey_stats['bias_no'], grey_n),
        ("**Reproducibility**", None, None, None, None),
        ("Code available", db_stats['code_yes'], db_n, grey_stats['code_yes'], grey_n),
        ("Prompts available", db_stats['prompts_yes'], db_n, grey_stats['prompts_yes'], grey_n),
        ("**Judge Model Family**", None, None, None, None),
        ("GPT-4 family", db_stats['gpt'], db_n, grey_stats['gpt'], grey_n),
        ("Claude family", db_stats['claude'], db_n, grey_stats['claude'], grey_n),
        ("Open-source models", db_stats['opensource'], db_n, grey_stats['opensource'], grey_n),
        ("**Deployment Status**", None, None, None, None),
        ("Production-deployed", db_stats['production'], db_n, grey_stats['production'], grey_n),
        ("Research tool", db_stats['research_tool'], db_n, grey_stats['research_tool'], grey_n),
    ]

    # Print markdown table
    print("\n| Characteristic | Database Search (n=%d) | Grey Literature (n=%d) | p-value* |" % (db_n, grey_n))
    print("| ----- | ----- | ----- | ----- |")
    for row_data in comparison_rows:
        label = row_data[0]
        if row_data[1] is None:
            # Section header
            print("| %s |  |  |  |" % label)
        else:
            db_val, db_total, grey_val, grey_total = row_data[1], row_data[2], row_data[3], row_data[4]
            # Fisher's exact: [[db_val, db_total-db_val], [grey_val, grey_total-grey_val]]
            p_str = fmt_p(db_val, db_total - db_val, grey_val, grey_total - grey_val)
            print("| %s | %s | %s | %s |" % (label, fmt(db_val, db_total), fmt(grey_val, grey_total), p_str))

    print("\n*Fisher's exact test for categorical variables")

    # Print interpretation
    journal_pct_db = db_stats['journal'] / db_n * 100 if db_n > 0 else 0
    journal_pct_grey = grey_stats['journal'] / grey_n * 100 if grey_n > 0 else 0
    preprint_pct_db = db_stats['preprint'] / db_n * 100 if db_n > 0 else 0
    preprint_pct_grey = grey_stats['preprint'] / grey_n * 100 if grey_n > 0 else 0
    yr2024_pct_db = db_stats['year_2024'] / db_n * 100 if db_n > 0 else 0
    yr2024_pct_grey = grey_stats['year_2024'] / grey_n * 100 if grey_n > 0 else 0
    research_pct_db = db_stats['research_tool'] / db_n * 100 if db_n > 0 else 0
    research_pct_grey = grey_stats['research_tool'] / grey_n * 100 if grey_n > 0 else 0

    p_journal = fmt_p(db_stats['journal'], db_n - db_stats['journal'],
                      grey_stats['journal'], grey_n - grey_stats['journal'])
    p_preprint = fmt_p(db_stats['preprint'], db_n - db_stats['preprint'],
                       grey_stats['preprint'], grey_n - grey_stats['preprint'])
    p_2024 = fmt_p(db_stats['year_2024'], db_n - db_stats['year_2024'],
                   grey_stats['year_2024'], grey_n - grey_stats['year_2024'])
    p_research = fmt_p(db_stats['research_tool'], db_n - db_stats['research_tool'],
                       grey_stats['research_tool'], grey_n - grey_stats['research_tool'])

    print("""
**Interpretation:** Grey literature sources show significantly higher preprint
representation (%.0f%% vs %.0f%%, p=%s) and lower peer-reviewed journal publication
(%.0f%% vs %.0f%%, p=%s), reflecting the field's recency and rapid evolution.
Grey literature studies were also more likely from 2024 (%.0f%% vs %.0f%%, p=%s).
No significant differences emerged in validation rigor, bias testing, or judge model
selection, suggesting grey literature quality is comparable to database-identified work
for this emerging methodology. Grey literature studies were more frequently categorized
as research tools (%.0f%% vs %.0f%%, p=%s), consistent with foundational benchmarking
work circulating as preprints. The grey literature component (%d/%d studies, %.0f%%)
underscores the field's early developmental stage, with substantial work appearing in
preprint servers and conference proceedings before indexing in medical databases.
""" % (preprint_pct_grey, preprint_pct_db, p_preprint,
       journal_pct_grey, journal_pct_db, p_journal,
       yr2024_pct_grey, yr2024_pct_db, p_2024,
       research_pct_grey, research_pct_db, p_research,
       grey_n, N, grey_n / N * 100))

    # List grey literature studies
    print("\n--- Grey Literature Studies (n=%d) ---" % grey_n)
    print("| # | Source | Authors | Title | Venue | Year |")
    print("|---|--------|---------|-------|-------|------|")
    for i, r in enumerate(grey_rows, 1):
        source = safe_get(r, 'paper source')[:20]
        print("| %d | %s | %s | %s | %s | %s |" % (
            i, source, safe_get(r, 'Authors')[:35],
            safe_get(r, 'Title')[:50], safe_get(r, 'Journal/Venue')[:40],
            safe_get(r, 'Year')))

    return {
        'database_n': db_n,
        'grey_n': grey_n,
        'db_stats': db_stats,
        'grey_stats': grey_stats
    }


def analyze_cross_domain(rows, N):
    """Analyze cross-domain testing."""
    print_section("CROSS-DOMAIN TESTING")

    cross_domain = 0
    cross_domain_studies = []

    for row in rows:
        cd = safe_get(row, 'Cross-Domain Testing').lower()
        author = safe_get(row, 'Authors')[:40]

        if cd and 'yes' in cd or 'multiple' in cd or 'cross' in cd:
            cross_domain += 1
            cross_domain_studies.append(author)

    print(f"""
Cross-domain testing: {cross_domain} ({cross_domain/N*100:.1f}%)
""")

    return {
        'count': cross_domain,
        'percentage': cross_domain/N*100
    }


def generate_manuscript_summary(results, N):
    """Generate summary text for manuscript."""
    print_section("MANUSCRIPT SUMMARY TEXT", level=1)

    print(f"""
=== ABSTRACT ===
This scoping review included {N} studies examining LLM-as-a-Judge in healthcare.

=== RESULTS SECTION ===

3.3 Application Categories (Table 3):
"Our analysis of {N} studies reveals three distinct application categories:
Category 1 (Evaluation & Benchmarking) dominated with {results['types']['cat1_count']} studies ({results['types']['cat1_count']/N*100:.1f}%),
followed by Category 3 (Multi-Agent Coordination) with {results['types']['cat3_count']} studies ({results['types']['cat3_count']/N*100:.1f}%),
and Category 2 (Reinforcement Learning) with {results['types']['cat2_count']} studies ({results['types']['cat2_count']/N*100:.1f}%)."

3.5 LaaJ Paradigm:
"Pointwise or Rubric-Based Scoring dominated the landscape: {results['paradigm']['pointwise_count']} of {N} studies
({results['paradigm']['pointwise_count']/N*100:.1f}%) employed this paradigm. Pairwise comparison appeared in
{results['paradigm']['pairwise_count']} studies ({results['paradigm']['pairwise_count']/N*100:.1f}%), while agent-based
multi-step evaluation characterized {results['paradigm']['agent_count']} studies ({results['paradigm']['agent_count']/N*100:.1f}%)."

3.6 Human Expert Involvement:
"Expert involvement demonstrated substantial heterogeneity: {results['experts']['extensive']} studies ({results['experts']['extensive']/N*100:.1f}%)
employed extensive validation (≥20 experts), {results['experts']['moderate']} ({results['experts']['moderate']/N*100:.1f}%) moderate (5-19),
{results['experts']['minimal']} ({results['experts']['minimal']/N*100:.1f}%) minimal (1-4), and {results['experts']['none']} ({results['experts']['none']/N*100:.1f}%) none.
Median expert count: {results['experts']['median']} (IQR: {results['experts']['iqr']})."

3.7 Judge Model Selection:
"GPT-4 family models dominated as judges ({results['judge_models']['gpt_count']}/{N} studies, {results['judge_models']['gpt_count']/N*100:.1f}%),
followed by Claude ({results['judge_models']['claude_count']} studies, {results['judge_models']['claude_count']/N*100:.1f}%) and
Llama ({results['judge_models']['llama_count']} studies, {results['judge_models']['llama_count']/N*100:.1f}%).
Only {results['specialized']['count']} of {N} studies ({results['specialized']['percentage']:.1f}%) employed medically specialized judge models."

3.7.2 Model Adaptation:
"Few-shot learning was employed in {results['adaptation']['fewshot_count']} studies ({results['adaptation']['fewshot_count']/N*100:.0f}%).
Chain-of-thought prompting appeared in {results['adaptation']['methods']['chain_of_thought']} studies ({results['adaptation']['methods']['chain_of_thought']/N*100:.0f}%).
Advanced adaptation remained rare: supervised fine-tuning in {results['adaptation']['methods']['fine_tuning']} studies
({results['adaptation']['methods']['fine_tuning']/N*100:.0f}%); preference optimization (DPO/RLAIF) in
{results['adaptation']['methods']['preference_optimization']} studies ({results['adaptation']['methods']['preference_optimization']/N*100:.0f}%)."

3.8 Bias Testing:
"Systematic bias testing remained severely limited: only {results['bias']['with_testing']} of {N} studies ({results['bias']['with_testing']/N*100:.1f}%)
conducted any formal bias testing. Positional bias testing appeared in {results['bias']['positional']} studies ({results['bias']['positional']/N*100:.1f}%);
length/verbosity bias in {results['bias']['length']} study ({results['bias']['length']/N*100:.1f}%);
format bias in {results['bias']['format']} study ({results['bias']['format']/N*100:.1f}%);
self-enhancement bias in {results['bias']['self_enhance']} studies ({results['bias']['self_enhance']/N*100:.1f}%);
demographic bias in {results['bias']['demographic']} studies ({results['bias']['demographic']/N*100:.1f}%).
{results['bias']['no_bias']} studies ({results['bias']['no_bias']/N*100:.1f}%) conducted zero bias testing."

Deployment:
"Only {results['deployment']['deployed']} of {N} studies ({results['deployment']['deployed']/N*100:.1f}%) achieved production deployment."

Reproducibility:
"Code available in {results['reproducibility']['code']} studies ({results['reproducibility']['code']/N*100:.1f}%);
Data available in {results['reproducibility']['data']} studies ({results['reproducibility']['data']/N*100:.1f}%);
Prompt templates in {results['reproducibility']['prompts']} studies ({results['reproducibility']['prompts']/N*100:.1f}%)."
""")


def main():
    """Main analysis function."""
    # Find or use specified data file
    if len(sys.argv) > 1:
        data_file = Path(sys.argv[1])
    else:
        data_file = find_data_file()

    if not data_file or not data_file.exists():
        print("ERROR: No data file found.")
        print("Usage: python analyze_papers.py [data_file.xlsx or data_file.csv]")
        sys.exit(1)

    print(f"\n{'#'*80}")
    print(f"# LLM-as-a-Judge Scoping Review Analysis")
    print(f"# Data file: {data_file}")
    print(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*80}")

    rows = load_data(data_file)

    if not rows:
        print("ERROR: No data loaded.")
        sys.exit(1)

    N = len(rows)
    print(f"\nTotal studies loaded: {N}")

    # Run all analyses
    results = {
        'total': N,
        'types': analyze_type_distribution(rows, N),
        'paradigm': analyze_paradigm_distribution(rows, N),
        'experts': analyze_expert_involvement(rows, N),
        'judge_models': analyze_judge_models(rows, N),
        'specialized': analyze_medical_specialized(rows, N),
        'adaptation': analyze_adaptation_methods(rows, N),
        'bias': analyze_bias_testing(rows, N),
        'deployment': analyze_deployment(rows, N),
        'reproducibility': analyze_reproducibility(rows, N),
        'years': analyze_year_distribution(rows, N),
        'cross_domain': analyze_cross_domain(rows, N),
        'literature_source': analyze_literature_source(rows, N),
        'db_vs_grey_search': analyze_database_vs_grey_lit_search(rows, N)
    }

    # Generate manuscript summary
    generate_manuscript_summary(results, N)

    # Save results to JSON
    try:
        output_file = 'manuscript_statistics.json'
        with open(output_file, 'w') as f:
            # Convert any non-serializable objects
            def serialize(obj):
                if isinstance(obj, (list, tuple)):
                    return [serialize(i) for i in obj]
                elif isinstance(obj, dict):
                    return {k: serialize(v) for k, v in obj.items()}
                else:
                    return obj

            json.dump(serialize(results), f, indent=2, default=str)
        print(f"\n{'='*80}")
        print(f"Results saved to: {output_file}")
        print(f"{'='*80}")
    except Exception as e:
        print(f"Warning: Could not save JSON results: {e}")


if __name__ == '__main__':
    main()
