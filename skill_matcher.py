from typing import Dict, Tuple, List
from rapidfuzz import fuzz


FUZZY_THRESHOLD = 80  # Minimum similarity score to count as a match


def match_skills(
    resume_text: str,
    required_skills: Dict[str, float]
) -> Tuple[List[str], List[str], float]:
    """
    Match required skills against resume text using exact + fuzzy matching.

    Args:
        resume_text: Full resume text
        required_skills: Dict of {skill_name: weight}

    Returns:
        matched_skills, missing_skills, weighted_score (0-100)
    """
    if not required_skills:
        return [], [], 100.0

    text_lower = resume_text.lower()
    words = [w.strip(".,;:()[]") for w in text_lower.split()]

    matched = []
    missing = []
    total_weight = sum(required_skills.values())
    earned_weight = 0.0

    for skill, weight in required_skills.items():
        skill_lower = skill.lower()
        found = False

        # Exact match (substring)
        if skill_lower in text_lower:
            found = True
        else:
            # Fuzzy match against each word / bigram / trigram
            tokens = _get_ngrams(words, max_n=3)
            for token in tokens:
                score = fuzz.ratio(skill_lower, token)
                if score >= FUZZY_THRESHOLD:
                    found = True
                    break

        if found:
            matched.append(skill)
            earned_weight += weight
        else:
            missing.append(skill)

    if total_weight == 0:
        weighted_score = 0.0
    else:
        weighted_score = (earned_weight / total_weight) * 100.0

    return matched, missing, round(weighted_score, 2)


def _get_ngrams(words: List[str], max_n: int = 3) -> List[str]:
    """Generate unigrams, bigrams, trigrams from word list."""
    ngrams = list(words)
    for n in range(2, max_n + 1):
        for i in range(len(words) - n + 1):
            ngrams.append(" ".join(words[i:i + n]))
    return ngrams
