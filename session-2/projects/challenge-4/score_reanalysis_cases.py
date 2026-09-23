#!/usr/bin/env python3
"""Score and rank reanalysis-triage cases per challenge-4-scoring-spec.md.

Usage:
    python3 score_reanalysis_cases.py --input cases.tsv \
        [--config config.json] [--top-n 30] \
        [--output-tsv top_cases.tsv] [--output-html top_cases_report.html]

Only the Python standard library is used, so no extra packages need
installing.
"""

from __future__ import annotations

import argparse
import copy
import csv
import datetime
import html
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = SCRIPT_DIR / "config.default.json"

DATE_FORMAT = "%Y-%m-%d"

# Columns whose scoring only makes sense when the value is a known number.
# When NA, they're treated as 0 for scoring and the case is flagged.
COUNT_COLUMNS_SCORED = [
    "new_candidates",
    "new_high_priority_candidates",
    "new_gene_evidence",
    "new_clinvar_evidence",
    "clinvar_upgrades_to_plp",
    "phenotype_changes",
]

# Recorded for visibility only; not used in any scoring formula.
COUNT_COLUMNS_UNUSED = ["hpo_term_count"]


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge `override` onto a copy of `base`."""
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_path: str | None) -> dict:
    with open(DEFAULT_CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)
    if config_path:
        with open(config_path, encoding="utf-8") as f:
            override = json.load(f)
        config = deep_merge(config, override)
    return config


def parse_optional_int(value: str) -> int | None:
    value = (value or "").strip()
    if value == "" or value.upper() == "NA":
        return None
    return int(value)


def parse_date(value: str) -> datetime.date:
    return datetime.datetime.strptime(value.strip(), DATE_FORMAT).date()


def score_tier_a(row: dict, cfg: dict, flags: list[str]) -> float:
    a = cfg["tier_a"]

    def counted(field: str) -> int:
        value = parse_optional_int(row[field])
        if value is None:
            flags.append(field)
            return 0
        return value

    clinvar_upgrades = counted("clinvar_upgrades_to_plp")
    clinvar_total = counted("new_clinvar_evidence")
    clinvar_other = max(clinvar_total - clinvar_upgrades, 0)
    gene_evidence = counted("new_gene_evidence")
    high_priority = counted("new_high_priority_candidates")
    new_candidates = counted("new_candidates")

    score = 0.0
    score += a["clinvar_upgrade_points"] * min(clinvar_upgrades, a["clinvar_upgrade_cap_count"])
    score += a["clinvar_other_points"] * min(clinvar_other, a["clinvar_other_cap_count"])
    score += a["gene_evidence_points"] * min(gene_evidence, a["gene_evidence_cap_count"])
    score += a["high_priority_points"] * min(high_priority, a["high_priority_cap_count"])
    score += a["new_candidates_points"] * min(new_candidates, a["new_candidates_cap_count"])
    return score


def score_tier_b(row: dict, cfg: dict, flags: list[str]) -> float:
    b = cfg["tier_b"]
    score = 0.0

    prior_flag = (row.get("prior_analysis_flag") or "").strip()
    prior_complete = parse_optional_int(row.get("prior_analysis_complete", ""))
    if prior_flag:
        score += b["prior_flag_points"].get(prior_flag, 0)
    elif prior_complete is None:
        flags.append("prior_analysis_complete")

    phenotype_changes = parse_optional_int(row.get("phenotype_changes", ""))
    if phenotype_changes is None:
        flags.append("phenotype_changes")
        phenotype_changes = 0
    score += b["phenotype_change_points"] * min(phenotype_changes, b["phenotype_change_cap_count"])

    return score


def score_tier_c(note: str, cfg: dict) -> tuple[float, str | None, str]:
    """Returns (score, matched_phrase_or_None, category)."""
    c = cfg["tier_c"]
    note_clean = (note or "").strip()
    if not note_clean:
        return 0.0, None, "blank"

    note_lower = note_clean.lower()

    best_phrase = None
    best_points = -1.0
    for phrase, points in c["signal_phrases"].items():
        if phrase in note_lower and points > best_points:
            best_phrase = phrase
            best_points = points
    if best_phrase is not None:
        return best_points, best_phrase, "signal"

    for phrase in c["administrative_phrases"]:
        if phrase in note_lower:
            return 0.0, None, "administrative"

    return 0.0, None, "unclassified"


def score_age_tiebreaker(last_analysis: datetime.date, current_analysis: datetime.date, cfg: dict) -> float:
    t = cfg["tiebreaker"]
    years = (current_analysis - last_analysis).days / 365.25
    return min(max(years, 0) * t["points_per_year"], t["cap"])


def score_case(row: dict, cfg: dict) -> dict:
    flags: list[str] = []

    for field in COUNT_COLUMNS_UNUSED:
        if parse_optional_int(row.get(field, "")) is None:
            flags.append(f"{field}(unused)")

    case_status = row["case_status"].strip()
    excluded = case_status == "solved"

    tier_a = 0.0 if excluded else score_tier_a(row, cfg, flags)
    tier_b = 0.0 if excluded else score_tier_b(row, cfg, flags)
    note = row.get("note", "")
    tier_c, matched_phrase, note_category = (0.0, None, "excluded") if excluded else score_tier_c(note, cfg)
    if note_category == "unclassified":
        flags.append("unclassified_note")

    last_analysis = parse_date(row["last_analysis"])
    current_analysis = parse_date(row["current_analysis"])
    age_bonus = 0.0 if excluded else score_age_tiebreaker(last_analysis, current_analysis, cfg)

    multiplier = 0.0 if excluded else cfg["case_status_multiplier"].get(case_status, 1.0)
    raw_score = tier_a + tier_b + tier_c + age_bonus
    final_score = raw_score * multiplier

    return {
        "case_id": row["case_id"],
        "case_status": case_status,
        "excluded": excluded,
        "tier_a_score": round(tier_a, 2),
        "tier_b_score": round(tier_b, 2),
        "tier_c_score": round(tier_c, 2),
        "age_tiebreaker_score": round(age_bonus, 2),
        "case_status_multiplier": multiplier,
        "final_score": round(final_score, 2),
        "matched_note_phrase": matched_phrase or "",
        "note_category": note_category,
        "data_completeness_flags": ";".join(flags),
        "last_analysis": row["last_analysis"],
        "prior_analysis_flag": row.get("prior_analysis_flag", ""),
        "sequencing_type": row.get("sequencing_type", ""),
        "family_structure": row.get("family_structure", ""),
        "note": note,
    }


def load_cases(input_path: str) -> list[dict]:
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [row for row in reader if row.get("case_id")]


def rank_cases(scored: list[dict]) -> list[dict]:
    eligible = [c for c in scored if not c["excluded"]]
    eligible.sort(key=lambda c: (-c["final_score"], c["last_analysis"]))
    return eligible


TSV_OUTPUT_COLUMNS = [
    "rank",
    "case_id",
    "final_score",
    "tier_a_score",
    "tier_b_score",
    "tier_c_score",
    "age_tiebreaker_score",
    "case_status",
    "case_status_multiplier",
    "matched_note_phrase",
    "data_completeness_flags",
    "last_analysis",
    "prior_analysis_flag",
    "sequencing_type",
    "family_structure",
    "note",
]


def write_tsv(ranked_top: list[dict], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TSV_OUTPUT_COLUMNS, delimiter="\t")
        writer.writeheader()
        for i, case in enumerate(ranked_top, start=1):
            row = {col: case.get(col, "") for col in TSV_OUTPUT_COLUMNS}
            row["rank"] = i
            writer.writerow(row)


def render_explanation_html(cfg: dict) -> str:
    a = cfg["tier_a"]
    b = cfg["tier_b"]
    c = cfg["tier_c"]
    t = cfg["tiebreaker"]
    m = cfg["case_status_multiplier"]

    prior_flag_rows = "".join(
        f"<tr><td><code>{html.escape(flag)}</code></td><td>{points}</td></tr>"
        for flag, points in b["prior_flag_points"].items()
    )
    signal_rows = "".join(
        f"<tr><td>{html.escape(phrase)}</td><td>{points}</td></tr>"
        for phrase, points in c["signal_phrases"].items()
    )
    admin_list = ", ".join(f"<code>{html.escape(p)}</code>" for p in c["administrative_phrases"])

    return f"""
    <section>
      <h2>How this score is built</h2>
      <p>Every non-<code>solved</code> case gets a <strong>final_score</strong> computed as:</p>
      <pre>final_score = (Tier A + Tier B + Tier C + age tiebreaker) &times; case_status_multiplier</pre>
      <p><code>solved</code> cases are excluded from ranking entirely, not scored low.</p>

      <h3>Tier A &mdash; direct evidence of new molecular findings</h3>
      <table>
        <tr><th>Signal</th><th>Points per unit</th><th>Capped at</th></tr>
        <tr><td>ClinVar upgrades to Pathogenic/Likely Pathogenic</td><td>{a['clinvar_upgrade_points']}</td><td>{a['clinvar_upgrade_cap_count']}</td></tr>
        <tr><td>Other ClinVar reclassifications</td><td>{a['clinvar_other_points']}</td><td>{a['clinvar_other_cap_count']}</td></tr>
        <tr><td>New gene&ndash;disease evidence</td><td>{a['gene_evidence_points']}</td><td>{a['gene_evidence_cap_count']}</td></tr>
        <tr><td>New high-priority candidates</td><td>{a['high_priority_points']}</td><td>{a['high_priority_cap_count']}</td></tr>
        <tr><td>New candidates (weak signal)</td><td>{a['new_candidates_points']}</td><td>{a['new_candidates_cap_count']}</td></tr>
      </table>

      <h3>Tier B &mdash; analytic headroom</h3>
      <p><strong>B1. Prior analysis completeness</strong> &mdash; points awarded once, based on <code>prior_analysis_flag</code>:</p>
      <table>
        <tr><th>Flag</th><th>Points</th></tr>
        {prior_flag_rows}
      </table>
      <p><strong>B2. Phenotype expansion</strong> &mdash; {b['phenotype_change_points']} points per new HPO term, capped at {b['phenotype_change_cap_count']} terms.</p>

      <h3>Tier C &mdash; free-text note classification</h3>
      <p>The <code>note</code> field is matched (case-insensitive substring) against fixed phrase lists. If several signal phrases match, the highest-scoring one wins &mdash; points are not summed.</p>
      <table>
        <tr><th>Signal phrase</th><th>Points</th></tr>
        {signal_rows}
      </table>
      <p><strong>Administrative / no-signal phrases (0 points):</strong> {admin_list}.</p>
      <p>Notes matching neither list are flagged <code>unclassified_note</code> for manual review rather than silently scored 0.</p>

      <h3>Tiebreaker &mdash; time since last analysis</h3>
      <p>{t['points_per_year']} points per year since <code>last_analysis</code>, capped at {t['cap']} points. Small on purpose &mdash; it only matters among otherwise-similar scores.</p>

      <h3>Case-status multiplier</h3>
      <table>
        <tr><th>case_status</th><th>Multiplier</th></tr>
        <tr><td><code>unsolved</code></td><td>{m['unsolved']}</td></tr>
        <tr><td><code>partially_solved</code></td><td>{m['partially_solved']}</td></tr>
        <tr><td><code>solved</code></td><td>excluded from ranking</td></tr>
      </table>

      <h3>Missing data</h3>
      <p>No case is dropped for having <code>NA</code> values. Any scoring-relevant field that was <code>NA</code> is treated as 0 for that component and listed in <strong>data_completeness_flags</strong> so a reviewer can see which scores rest on incomplete data.</p>

      <p><em>Full rationale: <code>challenge-4-scoring-spec.md</code>. All weights above come from the loaded config file, not hardcoded text &mdash; if you change the config, this explanation reflects the run that produced the table below.</em></p>
    </section>
    """


def render_table_html(ranked_top: list[dict]) -> str:
    header_cells = "".join(
        f"<th>{h}</th>"
        for h in [
            "Rank", "Case ID", "Final score", "Tier A", "Tier B", "Tier C",
            "Age bonus", "Status", "Matched note signal", "Data flags",
            "Last analysis", "Note",
        ]
    )
    rows = []
    for i, case in enumerate(ranked_top, start=1):
        flags = case["data_completeness_flags"]
        flags_html = f'<span class="flag">{html.escape(flags)}</span>' if flags else ""
        matched = case["matched_note_phrase"] or "&mdash;"
        rows.append(
            "<tr>"
            f"<td>{i}</td>"
            f"<td><code>{html.escape(case['case_id'])}</code></td>"
            f"<td><strong>{case['final_score']}</strong></td>"
            f"<td>{case['tier_a_score']}</td>"
            f"<td>{case['tier_b_score']}</td>"
            f"<td>{case['tier_c_score']}</td>"
            f"<td>{case['age_tiebreaker_score']}</td>"
            f"<td>{html.escape(case['case_status'])}</td>"
            f"<td>{html.escape(matched) if matched != '&mdash;' else matched}</td>"
            f"<td>{flags_html}</td>"
            f"<td>{html.escape(case['last_analysis'])}</td>"
            f"<td>{html.escape(case['note'])}</td>"
            "</tr>"
        )
    return f"""
    <section>
      <h2>Top {len(ranked_top)} cases by final score</h2>
      <table class="results">
        <thead><tr>{header_cells}</tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
    """


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Reanalysis triage &mdash; scoring report</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Helvetica, Arial, sans-serif; margin: 2rem auto; max-width: 960px; line-height: 1.5; color: #1a1a1a; }}
  h1 {{ font-size: 1.6rem; }}
  h2 {{ font-size: 1.25rem; margin-top: 2rem; border-bottom: 1px solid #ddd; padding-bottom: 0.25rem; }}
  h3 {{ font-size: 1.05rem; margin-top: 1.5rem; }}
  table {{ border-collapse: collapse; width: 100%; margin: 0.75rem 0 1.25rem; font-size: 0.9rem; }}
  th, td {{ border: 1px solid #ddd; padding: 0.4rem 0.6rem; text-align: left; vertical-align: top; }}
  th {{ background: #f4f4f4; }}
  table.results tbody tr:nth-child(-n+3) {{ background: #fff8e1; }}
  code {{ background: #f0f0f0; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.85em; }}
  pre {{ background: #f4f4f4; padding: 0.6rem 1rem; border-radius: 4px; overflow-x: auto; }}
  .flag {{ color: #b45309; font-size: 0.85em; }}
  .caveat {{ background: #fff3cd; border: 1px solid #f0d58c; padding: 0.75rem 1rem; border-radius: 4px; margin: 1rem 0; }}
</style>
</head>
<body>
  <h1>Reanalysis triage &mdash; scoring report</h1>
  <p class="caveat">Synthetic data, generated for a hackathon exercise. Not clinical evidence. Weights below are judgment calls, not derived from outcomes data.</p>
  {explanation}
  {table}
</body>
</html>
"""


def write_html(ranked_top: list[dict], cfg: dict, output_path: str) -> None:
    content = HTML_TEMPLATE.format(
        explanation=render_explanation_html(cfg),
        table=render_table_html(ranked_top),
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to a cases TSV (same shape as synthetic_reanalysis_cases.tsv)")
    parser.add_argument("--config", default=None, help="Optional JSON file overriding config.default.json")
    parser.add_argument("--top-n", type=int, default=None, help="Number of top cases to output (default: from config, 30)")
    parser.add_argument("--output-tsv", default="top_reanalysis_cases.tsv")
    parser.add_argument("--output-html", default="top_reanalysis_cases_report.html")
    args = parser.parse_args()

    cfg = load_config(args.config)
    top_n = args.top_n if args.top_n is not None else cfg["top_n"]

    rows = load_cases(args.input)
    scored = [score_case(row, cfg) for row in rows]
    ranked = rank_cases(scored)
    ranked_top = ranked[:top_n]

    write_tsv(ranked_top, args.output_tsv)
    write_html(ranked_top, cfg, args.output_html)

    n_excluded = sum(1 for c in scored if c["excluded"])
    n_unclassified = sum(1 for c in scored if c["note_category"] == "unclassified")
    print(f"Scored {len(scored)} cases ({n_excluded} excluded as already solved).")
    print(f"{n_unclassified} note(s) did not match any known phrase and were flagged unclassified_note.")
    print(f"Wrote top {len(ranked_top)} cases to {args.output_tsv} and {args.output_html}")


if __name__ == "__main__":
    main()
