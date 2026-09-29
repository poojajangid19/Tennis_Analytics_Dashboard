"""Audit the raw Sportradar data and report data-quality issues.

Run BEFORE clean_data.py:
    python audit_raw_data.py

Expected folder layout:
    data/   <- raw CSV + JSON files
"""
import json
from pathlib import Path

import pandas as pd

RAW = Path("data")


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def load_csvs() -> dict:
    names = ["categories", "competitions", "complexes",
             "venues", "competitors", "competitor_rankings"]
    return {n: pd.read_csv(RAW / f"{n}.csv") for n in names}


def check_shapes_and_nulls(tables: dict) -> None:
    section("1. Shape, missing values, duplicate rows")
    for name, df in tables.items():
        nulls = df.isnull().sum()
        nulls = nulls[nulls > 0].to_dict()
        print(f"{name:20s} rows={len(df):5d}  full-row duplicates={df.duplicated().sum()}  nulls={nulls}")


def check_primary_keys(tables: dict) -> None:
    section("2. Duplicate primary keys")
    keys = {"categories": "category_id", "competitions": "competition_id",
            "complexes": "complex_id", "venues": "venue_id",
            "competitors": "competitor_id"}
    for table, key in keys.items():
        print(f"{table:15s} duplicate {key}: {tables[table][key].duplicated().sum()}")


def check_foreign_keys(t: dict) -> None:
    section("3. Foreign key / orphan checks")
    comp, ven = t["competitions"], t["venues"]
    print("competitions.category_id not in categories:",
          (~comp.category_id.isin(t["categories"].category_id)).sum())
    parents = comp.parent_id.dropna()
    print("competitions with a parent_id:", len(parents))
    print("  ...whose parent exists in competitions:",
          parents.isin(comp.competition_id).sum(),
          "-> parent_id cannot be a self-referencing foreign key")
    print("venues.complex_id not in complexes:",
          (~ven.complex_id.isin(t["complexes"].complex_id)).sum())
    print("complexes with no venues:",
          (~t["complexes"].complex_id.isin(ven.complex_id)).sum())
    print("rankings.competitor_id not in competitors:",
          (~t["competitor_rankings"].competitor_id.isin(t["competitors"].competitor_id)).sum())


def check_text_quality(t: dict) -> None:
    section("4. Whitespace and formatting problems")
    for name in ["categories", "competitions", "complexes", "venues", "competitors"]:
        df = t[name]
        for col in df.select_dtypes(include=["object", "string"]).columns:
            s = df[col].dropna().astype(str)
            leading_trailing = (s != s.str.strip()).sum()
            double_space = s.str.contains(r"\s{2,}").sum()
            if leading_trailing or double_space:
                print(f"{name}.{col}: leading/trailing={leading_trailing}, double spaces={double_space}")
    print("venues.country_code not 3 upper letters:",
          (~t["venues"].country_code.str.fullmatch(r"[A-Z]{3}")).sum())
    print("competitors.country_code not 3 upper letters:",
          (~t["competitors"].country_code.str.fullmatch(r"[A-Z]{3}")).sum())
    print("competitors with country_code UNK:",
          (t["competitors"].country_code == "UNK").sum())


def check_categorical_values(t: dict) -> None:
    section("5. Allowed values")
    print("competition type:", t["competitions"].type.value_counts().to_dict())
    print("competition gender:", t["competitions"].gender.value_counts().to_dict())


def check_rankings(t: dict) -> None:
    section("6. Rankings (CSV)")
    rk = t["competitor_rankings"]
    print("rank_id range:", rk.rank_id.min(), "-", rk.rank_id.max(),
          "(PostgreSQL SERIAL starts at 1)")
    print("duplicate rank values:", rk["rank"].duplicated().sum(),
          "-> men and women boards are mixed in the CSV")
    print("columns present:", list(rk.columns),
          "-> gender/year/week are missing, rebuild from JSON")


def check_raw_json() -> None:
    section("7. Raw JSON structure")
    comps = json.load(open(RAW / "raw_competitions.json"))["competitions"]
    keys = {k for c in comps for k in c}
    print("competition JSON keys:", sorted(keys))
    print("'level' exists in JSON but not in the CSV:", "level" in keys)

    rankings = json.load(open(RAW / "raw_double_competitors_rankings.json"))["rankings"]
    for board in rankings:
        print(f"board {board['name']}: gender={board['gender']}, "
              f"year={board['year']}, week={board['week']}, "
              f"rows={len(board['competitor_rankings'])}")
    missing_cc = sum(1 for b in rankings for r in b["competitor_rankings"]
                     if "country_code" not in r["competitor"])
    print("competitors with no country_code in JSON:", missing_cc, "(neutral athletes)")


def main() -> None:
    try:
        tables = load_csvs()
    except FileNotFoundError as err:
        raise SystemExit(f"Missing file: {err.filename}. Put raw files in the data/ folder.")
    check_shapes_and_nulls(tables)
    check_primary_keys(tables)
    check_foreign_keys(tables)
    check_text_quality(tables)
    check_categorical_values(tables)
    check_rankings(tables)
    check_raw_json()


if __name__ == "__main__":
    main()
