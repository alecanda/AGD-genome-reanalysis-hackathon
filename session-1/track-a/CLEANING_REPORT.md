# Cleaning Report: messy_talos_candidates.tsv → clean_talos_candidates.tsv

## Summary
- **Input**: 16 data rows (17 total including header)
- **Output**: 13 data rows (14 total including header)
- **Duplicates removed**: 3

## Issues Fixed

### 1. Boolean Encoding ✓
**Problem**: Mixed `TRUE/False/1/0/yes/no` across columns
**Fix**: Normalized all to lowercase `true`/`false`
- Columns affected: `Talos_category_1`, `Talos_category_2`, `Talos_category_3`, `Talos_category_4`, `PM5`

### 2. Chromosome Naming ✓
**Problem**: Inconsistent `chr` prefix (`chr6`, `chrX` vs bare `6`, `16`, `11`)
**Fix**: Stripped all `chr` prefixes to match canonical Talos format
- Example: `chrX` → `X`, `chr6` → `6`

### 3. sample_id Inconsistency ✓
**Problem**: Case and whitespace variants (`SAMPLE_1`, `sample_1`, `SAMPLE_1 `)
**Fix**: Normalized to uppercase and trimmed whitespace
- All now: `SAMPLE_1` or `SAMPLE_2`

### 4. Talos_category_4 Type Inconsistency ✓
**Problem**: Mixed boolean flags with literal sample_id strings (`SAMPLE_1`)
**Fix**: Converted all to boolean; any non-empty/non-false value → `true`

### 5. Missing Value Representation ✓
**Problem**: Inconsistent null markers (blank, `.`, literal `"missing"`)
**Fix**: Standardized all to `NA`

### 6. ClinVar Significance ✓
**Problem**: Multiple representations of same concept
- `Pathogenic/Likely Pathogenic` vs `P/LP`
- `Uncertain significance` vs `VUS` 
**Fix**: Mapped all to standard full ClinVar terms with underscores
- Examples:
  - `P/LP` → `Pathogenic/Likely_pathogenic`
  - `VUS` → `Uncertain_significance`
  - `Uncertain significance` → `Uncertain_significance`

### 7. Date Format ✓
**Problem**: Mixed ISO (`2026-07-27`) and `DD/MM/YYYY` (`27/07/2026`)
**Fix**: Normalized all to ISO 8601 format `YYYY-MM-DD`

### 8. gnomAD_AF Floating-Point Noise ✓
**Problem**: Same variant shows different values due to round-trip errors
- `2.5e-06` vs `2.499999936844688e-06`
**Fix**: Rounded to 2 significant figures in scientific notation
- All now: `2.50e-06` (consistent)

### 9. Consequence Term Standardization ✓
**Problem**: `missense` vs `missense_variant` (Sequence Ontology inconsistency)
**Fix**: Mapped `missense` → `missense_variant`

### 10. MANE_HGVSp Protein Notation ✓
**Problem**: Mixed formats with transcript prefixes, parentheses, one-letter AA codes
- `p.R222C` vs `p.Arg222Cys`
- `ENSP00000264161.4:p.Ala274Gly` vs `p.Ala274Gly`
- `p.(His916Leu)` vs plain form
**Fix**: Standardized to three-letter HGVS notation without prefixes/parentheses
- One-letter AA codes → three-letter (e.g., `R` → `Arg`, `C` → `Cys`)
- Stripped `ENSP|ENST` transcript ID prefixes
- Removed parentheses

### 11. extra_technical_field SAMD9 Anomaly ✓
**Problem**: SAMD9 row had `3/3` (exon count) instead of MANE status in 4th pipe segment
**Fix**: Blanked malformed segment to `NA`, preserved valid `ENST|ENSP|biotype` parts
- Before: `ENST00000379958|ENSP00000369292|protein_coding|3/3`
- After: `ENST00000379958|ENSP00000369292|protein_coding|NA`

### 12. Duplicate Rows ✓
**Problem**: 3 sets of duplicates/conflicting rows:
- PKHD1 chr6:52043102 C>G (SAMPLE_1): rows 4 & 12 with conflicting MOI
  - Row 4: `AR (Comp-Het)`, no warning
  - Row 12: `AD`, warning "Ambiguous Cat.1 MOI"
- WT1 chr11:32392032 G>A (SAMPLE_1): rows 11 & 15 (identical)
- PKHD1 chr6:52043699 T>A: rows 7 & 17 (case/data quality differences)

**Fix**: Deduplication strategy:
1. Prefer row with no warnings over one with warnings
2. Tie-break: fewer `NA` fields
3. Tie-break: first occurrence

**Result**: Kept rows 4, 11, 7; dropped rows 12, 15, 17

## Verification Checklist

- ✅ Row count: 16 → 13 data rows
- ✅ All `Talos_category_*` and `PM5`: `true`/`false` only
- ✅ All chromosomes: bare (no `chr` prefix)
- ✅ All sample_ids: uppercase, no whitespace
- ✅ All dates: `YYYY-MM-DD` format
- ✅ ClinVar terms: standardized full names with underscores
- ✅ gnomAD_AF: consistent scientific notation (deduplicated DARS1 variant shows `2.50e-06` both places)
- ✅ SAMD9 extra_technical_field: 4th segment is `NA`, not `3/3`
- ✅ Missing values: all represented as `NA` (not blank/`.`/`"missing"`)
- ✅ Consequence: `missense` corrected to `missense_variant`
- ✅ MANE_HGVSp: no transcript prefixes, no parentheses, three-letter AA codes

## Output File
- **Location**: `clean_talos_candidates.tsv`
- **Format**: Tab-separated values
- **Columns**: 33 (same as input)
- **Rows**: 14 total (1 header + 13 data)
