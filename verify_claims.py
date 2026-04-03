"""
Verification script for the 11 discrepancies identified in the manuscript
vs. CSV data (full-text-reading - evidence generation-49.csv).

Checks each claim systematically against the raw CSV.
"""

import pandas as pd
import numpy as np
import re

CSV_PATH = "/Users/chenyuli/Desktop/LLM_as_a_Judge/manuscript/npj_submission/full-text-reading - evidence generation-49.csv"

# Load CSV - skip rows marked for exclusion
df = pd.read_csv(CSV_PATH)
print(f"Total rows in CSV: {len(df)}")
print(f"Columns: {list(df.columns)}\n")

# Use ALL 49 rows — the paper analyzes n=49
# The "exclude" column contains notes, not actual exclusions for this dataset
included = df.copy()
print(f"Using all {len(included)} studies (paper reports n=49)\n")

n = len(included)

print("=" * 80)
print(f"WORKING WITH {n} INCLUDED STUDIES")
print("=" * 80)

# Add study index (1-based) for reference
included = included.reset_index(drop=True)
included['study_num'] = range(1, n + 1)

# ============================================================================
# CLAIM 1: Demographic bias — Paper says "Zero studies assessed demographic bias"
# ============================================================================
print("\n" + "=" * 80)
print("CLAIM 1: Demographic Bias Testing")
print("Paper claims: Zero studies assessed demographic bias")
print("=" * 80)

bias_col = 'Bias Testing'
if bias_col in included.columns:
    print(f"\nAll Bias Testing values:")
    for idx, row in included.iterrows():
        val = str(row[bias_col]).strip()
        if val and val.lower() not in ['not specified', 'nan', 'no', 'not mentioned']:
            print(f"  Study [{row['study_num']}]: {val}")

    # Check for demographic/race/gender/ethnicity keywords
    demographic_keywords = ['demographic', 'race', 'racial', 'gender', 'ethnic', 'sex', 'age bias']
    demo_studies = []
    for idx, row in included.iterrows():
        val = str(row[bias_col]).lower()
        for kw in demographic_keywords:
            if kw in val:
                demo_studies.append((row['study_num'], row[bias_col]))
                break

    print(f"\nStudies with demographic bias keywords in Bias Testing: {len(demo_studies)}")
    for snum, val in demo_studies:
        print(f"  Study [{snum}]: {val}")

    # Also check Fairness Assessment column
    fairness_col = 'Fairness Assessment'
    if fairness_col in included.columns:
        print(f"\nFairness Assessment values (non-empty/non-NaN):")
        for idx, row in included.iterrows():
            val = str(row[fairness_col]).strip()
            if val and val.lower() not in ['not specified', 'nan', 'no', 'not mentioned', 'not assessed']:
                print(f"  Study [{row['study_num']}]: {val}")

# ============================================================================
# CLAIM 2: Positional bias count — Paper says 4 (8.2%), comment says CSV yields 3
# ============================================================================
print("\n" + "=" * 80)
print("CLAIM 2: Positional Bias Count")
print("Paper claims: 4 (8.2%)")
print("Comment claims CSV shows: 3")
print("=" * 80)

positional_keywords = ['position', 'positional', 'order bias', 'order/position']
positional_studies = []
for idx, row in included.iterrows():
    val = str(row[bias_col]).lower()
    for kw in positional_keywords:
        if kw in val:
            positional_studies.append((row['study_num'], row[bias_col]))
            break

print(f"\nStudies with positional/order bias in Bias Testing: {len(positional_studies)}")
for snum, val in positional_studies:
    print(f"  Study [{snum}]: {val}")

# ============================================================================
# CLAIM 3: Prompt engineering adaptation — Paper says 15 (30.6%), comment says 10
# ============================================================================
print("\n" + "=" * 80)
print("CLAIM 3: Prompt Engineering as Adaptation Method")
print("Paper claims: 15 (30.6%)")
print("Comment claims CSV shows: 10")
print("=" * 80)

adapt_col = 'Adaptation Method'
pe_col = 'Prompt Engineering'

if adapt_col in included.columns:
    pe_in_adapt = 0
    pe_adapt_studies = []
    for idx, row in included.iterrows():
        val = str(row[adapt_col]).lower()
        if 'prompt engineering' in val or 'prompt-engineering' in val:
            pe_in_adapt += 1
            pe_adapt_studies.append((row['study_num'], row[adapt_col]))
    print(f"\n'Prompt Engineering' in Adaptation Method column: {pe_in_adapt}")
    for snum, val in pe_adapt_studies:
        print(f"  Study [{snum}]: {val}")

if pe_col in included.columns:
    pe_yes = 0
    pe_yes_studies = []
    for idx, row in included.iterrows():
        val = str(row[pe_col]).strip().lower()
        if val and val not in ['nan', 'not specified', 'no', 'n/a', 'not mentioned', 'none']:
            pe_yes += 1
            pe_yes_studies.append((row['study_num'], row[pe_col]))
    print(f"\n'Prompt Engineering' column (Yes/non-empty): {pe_yes}")
    # Just show first 5
    for snum, val in pe_yes_studies[:10]:
        print(f"  Study [{snum}]: {val}")
    if len(pe_yes_studies) > 10:
        print(f"  ... and {len(pe_yes_studies) - 10} more")

# ============================================================================
# CLAIM 4: IQR for median validators — Paper says IQR 2–7.75, comment says 2–7.0
# ============================================================================
print("\n" + "=" * 80)
print("CLAIM 4: IQR for Number of Human Experts (among studies with involvement)")
print("Paper claims: IQR 2–7.75")
print("Comment claims CSV shows: IQR 2–7.0")
print("=" * 80)

experts_col = 'Number of Human Experts'
if experts_col in included.columns:
    expert_vals = []
    expert_details = []
    for idx, row in included.iterrows():
        val = str(row[experts_col]).strip()
        if val.lower() in ['nan', 'not specified', 'n/a', '']:
            continue
        # Parse carefully — extract numbers but ignore dataset sizes
        # Split by semicolons to handle multiple roles
        parts = val.split(';')
        candidate_nums = []
        for part in parts:
            part_lower = part.lower().strip()
            # Skip parts that describe dataset/case sizes, not expert counts
            if any(skip in part_lower for skip in ['case study', 'dataset', 'qa pairs', 'summaries']):
                continue
            nums = re.findall(r'(\d+)', part)
            for n_str in nums:
                num = int(n_str)
                # Ignore very large numbers (likely dataset sizes, not expert counts)
                if num <= 500:
                    candidate_nums.append(num)
        if candidate_nums:
            parsed = max(candidate_nums)
            expert_details.append((row['study_num'], val, parsed))
            if parsed > 0:
                expert_vals.append(parsed)
        else:
            # No valid number found
            expert_details.append((row['study_num'], val, 0))

    print(f"\nAll expert count values (parsed):")
    for snum, raw, parsed in expert_details:
        marker = " *" if parsed > 0 else ""
        print(f"  Study [{snum}]: raw='{raw}' -> parsed={parsed}{marker}")

    if expert_vals:
        arr = np.array(expert_vals)
        print(f"\nStudies with >0 experts: {len(expert_vals)}")
        print(f"Median: {np.median(arr)}")
        print(f"Q1 (25th): {np.percentile(arr, 25)}")
        print(f"Q3 (75th): {np.percentile(arr, 75)}")
        print(f"IQR: {np.percentile(arr, 25)}-{np.percentile(arr, 75)}")

    # Also compute for ALL studies (including 0)
    all_expert_vals = [parsed for _, _, parsed in expert_details]
    if all_expert_vals:
        arr_all = np.array(all_expert_vals)
        print(f"\nAll studies (including 0): n={len(all_expert_vals)}")
        print(f"Median: {np.median(arr_all)}")
        print(f"Q1 (25th): {np.percentile(arr_all, 25)}")
        print(f"Q3 (75th): {np.percentile(arr_all, 75)}")

# ============================================================================
# CLAIM 5-8: Judge Model Family Counts
# ============================================================================
print("\n" + "=" * 80)
print("CLAIMS 5-8: Judge Model Family Counts")
print("Paper: GPT=37(75.5%), Claude=7(14.3%), Llama=8(16.3%), Gemini=5(10.2%)")
print("Comment: GPT=36, Claude=6, Llama=7, Gemini=4")
print("=" * 80)

judge_family_col = 'Judge Model Family'
if judge_family_col in included.columns:
    families = {'gpt': [], 'claude': [], 'llama': [], 'gemini': []}

    for idx, row in included.iterrows():
        val = str(row[judge_family_col]).lower()
        if 'gpt' in val or 'openai' in val:
            families['gpt'].append(row['study_num'])
        if 'claude' in val or 'anthropic' in val:
            families['claude'].append(row['study_num'])
        if 'llama' in val or 'meta' in val:
            families['llama'].append(row['study_num'])
        if 'gemini' in val or 'google' in val:
            families['gemini'].append(row['study_num'])

    for fam, studies in families.items():
        pct = len(studies) / n * 100
        print(f"\n{fam.upper()} family: {len(studies)} ({pct:.1f}%)")
        print(f"  Studies: {studies}")

    # Show studies that DON'T match GPT to find the ambiguous ones
    print(f"\nStudies NOT matching GPT family:")
    for idx, row in included.iterrows():
        val = str(row[judge_family_col]).lower()
        if 'gpt' not in val and 'openai' not in val:
            print(f"  Study [{row['study_num']}]: {row[judge_family_col]}")

# Also check the working model family (not judge)
model_family_col = 'Model Family'
if model_family_col in included.columns:
    print(f"\n--- Also checking 'Model Family' column for Llama ---")
    llama_model = []
    for idx, row in included.iterrows():
        val = str(row[model_family_col]).lower()
        if 'llama' in val:
            llama_model.append((row['study_num'], row[model_family_col]))
    print(f"Llama in Model Family: {len(llama_model)}")
    for snum, val in llama_model:
        print(f"  Study [{snum}]: {val}")

# ============================================================================
# CLAIMS 9-10: General-purpose vs Domain-adapted judges
# ============================================================================
print("\n" + "=" * 80)
print("CLAIMS 9-10: General-purpose vs Domain-adapted Judges")
print("Paper: General=43(87.8%), Domain-adapted=6(12.2%)")
print("Comment: General≈40, Domain-adapted≈9")
print("=" * 80)

judge_spec_col = 'Judge Specialization'
if judge_spec_col in included.columns:
    general_studies = []
    specialized_studies = []
    ambiguous_studies = []

    for idx, row in included.iterrows():
        val = str(row[judge_spec_col]).strip()
        val_lower = val.lower()
        if 'general' in val_lower or val_lower in ['nan', 'not specified']:
            general_studies.append((row['study_num'], val))
        elif 'speciali' in val_lower or 'domain' in val_lower or 'adapted' in val_lower or 'fine-tun' in val_lower:
            specialized_studies.append((row['study_num'], val))
        else:
            ambiguous_studies.append((row['study_num'], val))

    print(f"\nGeneral-purpose: {len(general_studies)}")
    for snum, val in general_studies:
        print(f"  Study [{snum}]: {val}")

    print(f"\nSpecialized/Domain-adapted: {len(specialized_studies)}")
    for snum, val in specialized_studies:
        print(f"  Study [{snum}]: {val}")

    print(f"\nAmbiguous (not clearly categorized): {len(ambiguous_studies)}")
    for snum, val in ambiguous_studies:
        print(f"  Study [{snum}]: {val}")

    print(f"\nTotal: {len(general_studies) + len(specialized_studies) + len(ambiguous_studies)} (should be {n})")

# ============================================================================
# CLAIM 11: Production deployment — Paper says 5 (10.2%), comment says 2 clearly
# ============================================================================
print("\n" + "=" * 80)
print("CLAIM 11: Production Deployment")
print("Paper claims: 5 (10.2%)")
print("Comment claims: 2 clearly deployed")
print("=" * 80)

deploy_col = 'Deployment Readiness'
impl_col = 'Implementation Stage'
if deploy_col in included.columns:
    print(f"\nDeployment Readiness values:")
    for idx, row in included.iterrows():
        val = str(row[deploy_col]).strip()
        if val and val.lower() not in ['nan']:
            print(f"  Study [{row['study_num']}]: {val}")

if impl_col in included.columns:
    print(f"\nImplementation Stage values:")
    for idx, row in included.iterrows():
        val = str(row[impl_col]).strip()
        if val and val.lower() not in ['nan']:
            print(f"  Study [{row['study_num']}]: {val}")

    # Count deployment-related
    deploy_keywords = ['deploy', 'production', 'operational', 'pilot', 'implementation']
    deployed_studies = []
    for idx, row in included.iterrows():
        deploy_val = str(row.get(deploy_col, '')).lower()
        impl_val = str(row.get(impl_col, '')).lower()
        combined = deploy_val + ' ' + impl_val
        for kw in deploy_keywords:
            if kw in combined:
                deployed_studies.append((row['study_num'], row.get(deploy_col, ''), row.get(impl_col, '')))
                break
    print(f"\nStudies with deployment-related keywords: {len(deployed_studies)}")
    for snum, dep, impl in deployed_studies:
        print(f"  Study [{snum}]: Deploy='{dep}', Impl='{impl}'")

# ============================================================================
# ADDITIONAL CHECKS (confirmed correct claims for completeness)
# ============================================================================
print("\n" + "=" * 80)
print("ADDITIONAL CHECKS: Year Distribution, Paradigm, Application Categories")
print("=" * 80)

# Year distribution
year_col = 'Year'
if year_col in included.columns:
    year_counts = included[year_col].value_counts().sort_index()
    print(f"\nYear distribution:")
    for year, count in year_counts.items():
        print(f"  {year}: {count}")

# Paradigm
paradigm_col = 'LaaJ_Paradigm'
if paradigm_col in included.columns:
    paradigm_counts = included[paradigm_col].value_counts()
    print(f"\nParadigm distribution:")
    for p, count in paradigm_counts.items():
        print(f"  {p}: {count}")

# Application categories (Type column)
type_col = 'Type'
if type_col in included.columns:
    type_counts = included[type_col].value_counts()
    print(f"\nApplication categories (Type):")
    for t, count in type_counts.items():
        print(f"  {t}: {count}")

# GPT-only judge count (studies where ONLY GPT is judge)
print(f"\n--- GPT-only as judge ---")
if judge_family_col in included.columns:
    gpt_only = 0
    gpt_only_studies = []
    for idx, row in included.iterrows():
        val = str(row[judge_family_col]).lower()
        has_gpt = 'gpt' in val or 'openai' in val
        has_other = any(x in val for x in ['claude', 'llama', 'gemini', 'mixtral', 'palm', 'bard', 'mistral'])
        if has_gpt and not has_other:
            gpt_only += 1
            gpt_only_studies.append(row['study_num'])
    print(f"GPT-only judge studies: {gpt_only}")

# Adaptation method counts
print(f"\n--- Adaptation Method Counts ---")
if adapt_col in included.columns:
    adapt_keywords = {
        'few-shot': ['few-shot', 'few shot', 'in-context learning'],
        'SFT': ['supervised fine-tuning', 'sft', 'fine-tuning (supervised)'],
        'RAG': ['rag', 'retrieval augmented', 'retrieval-augmented'],
        'CoT': ['chain-of-thought', 'chain of thought', 'cot'],
        'LoRA': ['lora', 'qlora'],
        'DPO': ['dpo', 'direct preference optimization'],
        'Prompt Engineering': ['prompt engineering', 'prompt-engineering'],
    }

    for method, keywords in adapt_keywords.items():
        count = 0
        method_studies = []
        for idx, row in included.iterrows():
            val = str(row[adapt_col]).lower()
            if any(kw in val for kw in keywords):
                count += 1
                method_studies.append(row['study_num'])
        print(f"  {method}: {count} studies {method_studies}")

# Bias testing overall
print(f"\n--- Bias Testing Overall ---")
if bias_col in included.columns:
    yes_bias = 0
    no_bias = 0
    for idx, row in included.iterrows():
        val = str(row[bias_col]).strip().lower()
        if val in ['not specified', 'nan', 'no', 'not mentioned', 'none', 'not assessed', '']:
            no_bias += 1
        else:
            yes_bias += 1
    print(f"  Yes (some bias testing): {yes_bias}")
    print(f"  No/Not specified: {no_bias}")
    print(f"  Ratio: {yes_bias}/{n} = {yes_bias/n*100:.1f}%")

# Verbosity bias
print(f"\n--- Verbosity Bias ---")
verb_studies = []
for idx, row in included.iterrows():
    val = str(row[bias_col]).lower()
    if 'verbos' in val:
        verb_studies.append((row['study_num'], row[bias_col]))
print(f"  Verbosity bias studies: {len(verb_studies)}")
for snum, val in verb_studies:
    print(f"    Study [{snum}]: {val}")

# Self-enhancement bias
print(f"\n--- Self-Enhancement Bias ---")
self_enh_studies = []
for idx, row in included.iterrows():
    val = str(row[bias_col]).lower()
    if 'self-enhancement' in val or 'self enhancement' in val or 'self-prefer' in val:
        self_enh_studies.append((row['study_num'], row[bias_col]))
print(f"  Self-enhancement bias studies: {len(self_enh_studies)}")
for snum, val in self_enh_studies:
    print(f"    Study [{snum}]: {val}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
