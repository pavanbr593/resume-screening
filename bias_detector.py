import re
from typing import List, Dict

# Categorized bias phrase lists
BIAS_PATTERNS: Dict[str, List[str]] = {
    "age_bias": [
        r"\bdigital native\b", r"\byoung\b", r"\brecent graduate\b",
        r"\bfresh graduate\b", r"\bmature\b", r"\bseasoned professional\b",
        r"\boverqualified\b", r"\benergetic\b", r"\bdynamic young\b",
        r"\b(?:1|2|3)\s*-?\s*5\s*years?\s*(?:only|maximum)\b",
    ],
    "gender_bias": [
        r"\bhe\b", r"\bshe\b", r"\bhis\b", r"\bher\b",
        r"\bmanpower\b", r"\bmanmade\b", r"\bchairman\b",
        r"\bstewardess\b", r"\bwaitress\b", r"\bsalesman\b",
        r"\bnurse\b.*\bfemale\b", r"\bgentlemen\b",
        r"\bgirls\b", r"\bboys\b", r"\bmotherhood\b", r"\bfatherhood\b",
    ],
    "discriminatory": [
        r"\bnative speaker\b", r"\bno disability\b",
        r"\bable.bodied\b", r"\bphysically fit\b",
        r"\bcitizens only\b", r"\blocals only\b",
        r"\bno criminal record\b", r"\bclean background\b",
        r"\bmarried\b", r"\bsingle\b", r"\bunmarried\b",
    ],
}


def detect_bias(text: str) -> List[Dict[str, str]]:
    """
    Scan text for potentially biased language.
    Returns list of {category, phrase, context} dicts.
    """
    flags = []
    text_lower = text.lower()

    for category, patterns in BIAS_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text_lower, re.IGNORECASE):
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 40)
                context = text[start:end].replace("\n", " ").strip()
                flags.append({
                    "category": category,
                    "phrase": match.group(),
                    "context": f"...{context}...",
                })

    # Deduplicate by phrase
    seen = set()
    unique_flags = []
    for f in flags:
        key = (f["category"], f["phrase"].lower())
        if key not in seen:
            seen.add(key)
            unique_flags.append(f)

    return unique_flags


def format_category(category: str) -> str:
    return category.replace("_", " ").title()
