import re
from datetime import datetime
from typing import Tuple, List


# Month name to number mapping
MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def extract_explicit_years(text: str) -> float:
    """Extract directly stated experience like '5 years', '3+ years'."""
    pattern = r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s*(of\s+)?(experience|exp)?"
    matches = re.findall(pattern, text, re.IGNORECASE)
    values = [float(m[0]) for m in matches if float(m[0]) < 50]
    return max(values) if values else 0.0


def parse_date(month_str: str, year_str: str) -> datetime:
    month = MONTH_MAP.get(month_str.lower(), 1)
    year = int(year_str)
    return datetime(year, month, 1)


def extract_date_ranges(text: str) -> List[Tuple[datetime, datetime]]:
    """Extract date ranges like 'Jan 2019 – Dec 2022' or '2018 - 2021'."""
    now = datetime.now()
    ranges = []

    # Pattern: Month Year – Month Year / Present
    pattern_full = re.compile(
        r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+(\d{4})\s*[-–—to]+\s*"
        r"(?:(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
        r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+(\d{4})|(Present|Current|Now|Till date|Till Date))",
        re.IGNORECASE
    )

    for m in pattern_full.finditer(text):
        try:
            start = parse_date(m.group(1), m.group(2))
            if m.group(5):  # Present
                end = now
            else:
                end = parse_date(m.group(3), m.group(4))
            if start < end:
                ranges.append((start, end))
        except Exception:
            continue

    # Pattern: Year – Year
    pattern_year = re.compile(r"\b(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|19\d{2}|Present|Current)\b",
                              re.IGNORECASE)
    for m in pattern_year.finditer(text):
        try:
            start = datetime(int(m.group(1)), 1, 1)
            end_str = m.group(2)
            if end_str.lower() in ("present", "current"):
                end = now
            else:
                end = datetime(int(end_str), 12, 31)
            if start < end and (start, end) not in ranges:
                ranges.append((start, end))
        except Exception:
            continue

    return ranges


def calculate_total_experience(ranges: List[Tuple[datetime, datetime]]) -> float:
    """Calculate non-overlapping total experience in years."""
    if not ranges:
        return 0.0
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    total_days = sum((e - s).days for s, e in merged)
    return round(total_days / 365.25, 1)


def extract_experience(text: str) -> Tuple[float, List[dict]]:
    """
    Main entry point. Returns (total_years, timeline_segments).
    """
    explicit = extract_explicit_years(text)
    ranges = extract_date_ranges(text)
    timeline_years = calculate_total_experience(ranges)

    total = max(explicit, timeline_years)

    segments = [
        {"start": s.strftime("%b %Y"), "end": e.strftime("%b %Y")}
        for s, e in ranges
    ]

    return total, segments


def score_experience(candidate_years: float, required_years: float) -> float:
    """Score 0-100 based on how candidate experience compares to requirement."""
    if required_years <= 0:
        return 100.0
    ratio = candidate_years / required_years
    if ratio >= 1.0:
        return 100.0
    elif ratio >= 0.75:
        return 75.0
    elif ratio >= 0.5:
        return 50.0
    elif ratio >= 0.25:
        return 25.0
    return 0.0
