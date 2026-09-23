#!/usr/bin/env python3
"""
Clean messy_talos_candidates.tsv: normalize booleans, dates, chromosome format,
ClinVar terms, HGVS notation, and deduplicate rows.
"""

import pandas as pd
import re
from collections import Counter

# Amino acid one-letter to three-letter mapping
AA_MAP = {
    'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys',
    'Q': 'Gln', 'E': 'Glu', 'G': 'Gly', 'H': 'His', 'I': 'Ile',
    'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro',
    'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val',
    '*': 'Ter'
}

def normalize_bool(s):
    """Normalize boolean values: true/false lowercase strings."""
    s = s.astype(str).str.strip().str.lower()
    return s.map(lambda x: 'true' if x in ('true', '1', 'yes') else 'false' if x in ('false', '0', 'no', '') else x)

def normalize_category_4(s):
    """Category_4: any non-empty, non-false/no/0 value becomes true."""
    s = s.astype(str).str.strip()
    return s.map(lambda x: 'false' if x.lower() in ('false', '0', 'no', '') else 'true' if x else 'false')

def normalize_chrom(s):
    """Strip chr prefix from chromosome names."""
    return s.astype(str).str.strip().str.replace(r'^[Cc]hr', '', regex=True)

def normalize_sample_id(s):
    """Trim and uppercase sample IDs."""
    return s.astype(str).str.strip().str.upper()

def normalize_date(s):
    """Parse dates (ISO YYYY-MM-DD or DD/MM/YYYY) and return ISO format."""
    def parse_date(x):
        x = str(x).strip()
        if not x or x == 'NA':
            return 'NA'
        # Try ISO format first
        try:
            return pd.to_datetime(x, format='%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            pass
        # Try DD/MM/YYYY
        try:
            return pd.to_datetime(x, format='%d/%m/%Y').strftime('%Y-%m-%d')
        except:
            return 'NA'
    return s.astype(str).apply(parse_date)

def normalize_clinvar(s):
    """Map ClinVar significance to standard full terms, underscores joined."""
    clinvar_map = {
        'pathogenic/likely pathogenic': 'Pathogenic/Likely_pathogenic',
        'pathogenic/likely_pathogenic': 'Pathogenic/Likely_pathogenic',
        'p/lp': 'Pathogenic/Likely_pathogenic',
        'uncertain significance': 'Uncertain_significance',
        'uncertain_significance': 'Uncertain_significance',
        'vus': 'Uncertain_significance',
        'pathogenic': 'Pathogenic',
        'likely pathogenic': 'Likely_pathogenic',
        'likely_pathogenic': 'Likely_pathogenic',
        'benign': 'Benign',
        'likely benign': 'Likely_benign',
        'likely_benign': 'Likely_benign',
    }

    def map_term(x):
        x = str(x).strip()
        if x.lower() in ('', 'missing', 'na'):
            return 'NA'
        key = x.lower()
        return clinvar_map.get(key, x)  # Return as-is if not in map

    return s.astype(str).apply(map_term)

def normalize_af(s):
    """Parse gnomAD_AF as float, round to remove noise, return scientific notation."""
    def round_af(x):
        x = str(x).strip()
        if x in ('', 'NA', 'missing', '0', '.'):
            return x if x == '0' else 'NA'
        try:
            val = float(x)
            if val == 0:
                return '0'
            # Round to 2 significant figures in the exponent
            return f'{val:.2e}'
        except:
            return 'NA'

    return s.astype(str).apply(round_af)

def normalize_consequence(s):
    """Map consequence terms to standard Sequence Ontology terms."""
    consequence_map = {
        'missense': 'missense_variant',
    }

    def map_consequence(x):
        x = str(x).strip()
        return consequence_map.get(x, x)

    return s.astype(str).apply(map_consequence)

def normalize_hgvsp(s):
    """Normalize HGVS protein notation: strip transcript prefix, parentheses, one-letter AA."""
    def normalize_one(x):
        x = str(x).strip()
        if x in ('', 'NA', 'missing', '.'):
            return 'NA'

        # Strip transcript/protein ID prefix (e.g., ENSP00000...:)
        x = re.sub(r'^[A-Z]+\d+\.\d+:', '', x)

        # Remove parentheses but keep content
        x = x.replace('(', '').replace(')', '')

        # Convert one-letter AA codes to three-letter (e.g., p.R222C -> p.Arg222Cys)
        def replace_aa(match):
            prefix = match.group(1)  # 'p.' or 'p'
            aa1 = match.group(2)  # One-letter code
            num = match.group(3)  # Position number
            aa2 = match.group(4)  # Second one-letter code (if present)

            aa1_full = AA_MAP.get(aa1, aa1)
            if aa2:
                aa2_full = AA_MAP.get(aa2, aa2)
                return f'{prefix}.{aa1_full}{num}{aa2_full}'
            else:
                return f'{prefix}.{aa1_full}{num}'

        # Pattern: p.R222C or p.Arg222Cys
        x = re.sub(r'(p\.?)([A-Z\*])(\d+)([A-Z\*]?)', replace_aa, x)

        return x if x else 'NA'

    return s.astype(str).apply(normalize_one)

def fix_extra_technical_field(row):
    """Fix extra_technical_field: blank 4th pipe segment if it's not a MANE status."""
    x = str(row).strip()
    if not x or x == 'NA':
        return 'NA'

    parts = x.split('|')
    if len(parts) >= 4:
        fourth = parts[3]
        # If 4th segment looks like an exon count (e.g., '3/3') or is otherwise invalid, blank it
        if fourth and fourth not in ('NA', '-', 'MANE') and not fourth.startswith('NM_'):
            parts[3] = 'NA'

    return '|'.join(parts)

def normalize_missing(s):
    """Convert blank, '.', 'missing' to 'NA' for any field."""
    def convert(x):
        x = str(x).strip()
        if x in ('', '.', 'missing'):
            return 'NA'
        return x

    return s.astype(str).apply(convert)

def main():
    input_file = 'messy_talos_candidates.tsv'
    output_file = 'clean_talos_candidates.tsv'

    # Read with everything as string to preserve original types
    df = pd.read_csv(input_file, sep='\t', dtype=str, keep_default_na=False)

    print(f"Loaded {len(df)} rows from {input_file}")

    # Apply column-specific normalizers
    df['Talos_category_1'] = normalize_bool(df['Talos_category_1'])
    df['Talos_category_2'] = normalize_bool(df['Talos_category_2'])
    df['Talos_category_3'] = normalize_bool(df['Talos_category_3'])
    df['Talos_category_4'] = normalize_category_4(df['Talos_category_4'])
    df['PM5'] = normalize_bool(df['PM5'])

    df['chromosome'] = normalize_chrom(df['chromosome'])
    df['sample_id'] = normalize_sample_id(df['sample_id'])
    df['first_tagged'] = normalize_date(df['first_tagged'])
    df['ClinVar'] = normalize_clinvar(df['ClinVar'])
    df['gnomAD_AF'] = normalize_af(df['gnomAD_AF'])
    df['consequence'] = normalize_consequence(df['consequence'])
    df['MANE_HGVSp'] = normalize_hgvsp(df['MANE_HGVSp'])
    df['extra_technical_field'] = df['extra_technical_field'].apply(fix_extra_technical_field)

    # Generic missing-value normalization for remaining columns
    for col in df.columns:
        if col not in ['Talos_category_1', 'Talos_category_2', 'Talos_category_3', 'Talos_category_4', 'PM5',
                       'chromosome', 'sample_id', 'first_tagged', 'ClinVar', 'gnomAD_AF', 'consequence',
                       'MANE_HGVSp', 'extra_technical_field']:
            df[col] = normalize_missing(df[col])

    # Deduplication: key is (sample_id, chromosome, position, REF, ALT)
    df['dedup_key'] = df.apply(lambda row: (row['sample_id'], row['chromosome'], row['position'], row['REF'], row['ALT']), axis=1)

    dropped_rows = []
    deduplicated = []

    for key, group in df.groupby('dedup_key'):
        if len(group) == 1:
            deduplicated.append(group.iloc[0])
        else:
            # Multiple rows for same variant
            # Prefer: no warnings > fewer NA > first occurrence
            group_list = group.reset_index(drop=True).to_dict('records')

            # Sort by: (has_warning, na_count, original_index)
            def sort_key(idx):
                row = group_list[idx]
                has_warning = 0 if row['warnings'] == 'NA' else 1
                na_count = sum(1 for v in row.values() if v == 'NA')
                return (has_warning, na_count, idx)

            best_idx = min(range(len(group_list)), key=sort_key)
            best_row = group.iloc[best_idx]
            deduplicated.append(best_row)

            # Log dropped rows
            for i, row in enumerate(group_list):
                if i != best_idx:
                    reason = f"Duplicate of row (sample={key[0]}, chrom={key[1]}, pos={key[2]}, {key[3]}>{key[4]})"
                    dropped_rows.append(reason)

    df_clean = pd.DataFrame(deduplicated).drop(columns=['dedup_key'])

    # Write output
    df_clean.to_csv(output_file, sep='\t', index=False)

    print(f"\nCleaning summary:")
    print(f"  Input:  {len(df)} rows")
    print(f"  Output: {len(df_clean)} rows")
    print(f"  Dropped: {len(dropped_rows)} duplicate/conflicting rows")
    if dropped_rows:
        print(f"\nDropped rows:")
        for reason in dropped_rows:
            print(f"  - {reason}")

    print(f"\nWrote cleaned data to {output_file}")

if __name__ == '__main__':
    main()
