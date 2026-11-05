#!/usr/bin/env python3
"""Calculate and validate daily nutrition totals for a weekly meal plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def calculate_day(day: dict, targets: dict) -> dict:
    kcal = sum(float(day[item]["kcal"]) for item in ("breakfast", "lunch", "dinner"))
    protein = sum(float(day[item]["protein"]) for item in ("breakfast", "lunch", "dinner"))
    whey_servings = int(day.get("extra_whey_servings", 0))
    kcal += whey_servings * float(targets["whey_kcal"])
    protein += whey_servings * float(targets["whey_protein"])
    return {
        "day": day["day"],
        "calories": round(kcal),
        "protein": round(protein, 1),
        "kcal_pct": round(kcal / float(targets["calories"]) * 100, 1),
        "protein_min_pct": round(protein / float(targets["protein_min"]) * 100, 1),
        "protein_max_pct": round(protein / float(targets["protein_max"]) * 100, 1),
        "extra_whey_servings": whey_servings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="JSON file containing targets and seven days")
    args = parser.parse_args()
    data = json.loads(args.plan.read_text(encoding="utf-8"))
    days = data.get("days", [])
    if len(days) != 7:
        raise SystemExit(f"Expected 7 days, received {len(days)}")

    results = [calculate_day(day, data["targets"]) for day in days]
    summary = {
        "average_calories": round(sum(day["calories"] for day in results) / 7),
        "average_protein": round(sum(day["protein"] for day in results) / 7, 1),
        "highest_protein_day": max(results, key=lambda day: day["protein"])["day"],
        "lowest_protein_day": min(results, key=lambda day: day["protein"])["day"],
        "all_days_reach_protein_min": all(day["protein"] >= float(data["targets"]["protein_min"]) for day in results),
    }
    print(json.dumps({"days": results, "summary": summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
