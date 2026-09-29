import json
import re
from pathlib import Path
import pandas as pd

RAW = Path("data")
OUT = Path("clean")
OUT.mkdir(exist_ok=True)


def squash_spaces(s: pd.Series) -> pd.Series:
    """Trim and collapse repeated spaces."""
    return s.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)


def clean_categories():
    df = pd.read_csv(RAW / "categories.csv")
    df["category_name"] = squash_spaces(df["category_name"])
    df.drop_duplicates("category_id").to_csv(OUT / "categories.csv", index=False)


def clean_competitions():
    """Rebuild from raw JSON so the 'level' field (grand_slam, atp_500...) is kept."""
    raw = json.load(open(RAW / "raw_competitions.json"))["competitions"]
    df = pd.DataFrame(
        {
            "competition_id": c["id"],
            "competition_name": c["name"],
            "parent_id": c.get("parent_id"),
            "type": c["type"],
            "gender": c["gender"],
            "level": c.get("level"),
            "category_id": c["category"]["id"],
        }
        for c in raw
    )
    df["competition_name"] = squash_spaces(df["competition_name"])
    for col in ("type", "gender", "level"):
        df[col] = df[col].astype("string").str.strip().str.lower()
    df = df.drop_duplicates("competition_id")
    df.to_csv(OUT / "competitions.csv", index=False)  # None -> empty -> NULL


def clean_complexes_and_venues():
    cx = pd.read_csv(RAW / "complexes.csv")
    cx["complex_name"] = squash_spaces(cx["complex_name"])
    cx.drop_duplicates("complex_id").to_csv(OUT / "complexes.csv", index=False)

    ven = pd.read_csv(RAW / "venues.csv")
    for col in ("venue_name", "city_name", "country_name", "timezone"):
        ven[col] = squash_spaces(ven[col])
    ven["country_code"] = ven["country_code"].str.strip().str.upper()
    ven = ven.drop_duplicates("venue_id")
    ven.to_csv(OUT / "venues.csv", index=False)


def clean_rankings():
    """Rebuild rankings from raw JSON so gender/year/week are kept."""
    data = json.load(open(RAW / "raw_double_competitors_rankings.json"))
    competitors, rankings = {}, []
    for board in data["rankings"]:
        for row in board["competitor_rankings"]:
            c = row["competitor"]
            competitors[c["id"]] = {
                "competitor_id": c["id"],
                "name": re.sub(r"\s+", " ", c["name"]).strip(),
                "country": c["country"].strip(),
                "country_code": (c.get("country_code") or "UNK").strip().upper(),
                "abbreviation": c["abbreviation"].strip().upper(),
            }
            rankings.append({
                "ranking_type": board["name"],   # ATP / WTA
                "gender": board["gender"],
                "year": board["year"],
                "week": board["week"],
                "rank": row["rank"],
                "movement": row["movement"],
                "points": row["points"],
                "competitions_played": row["competitions_played"],
                "competitor_id": c["id"],
            })
    pd.DataFrame(competitors.values()).to_csv(OUT / "competitors.csv", index=False)
    pd.DataFrame(rankings).to_csv(OUT / "competitor_rankings.csv", index=False)


if __name__ == "__main__":
    clean_categories()
    clean_competitions()
    clean_complexes_and_venues()
    clean_rankings()
    print("done")
