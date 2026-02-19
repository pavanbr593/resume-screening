from typing import Dict, Any
from skill_matcher import match_skills
from experience_extractor import extract_experience, score_experience
from semantic_matcher import compute_semantic_similarity
from resume_parser import compute_resume_quality_score


def score_candidate(
    resume_text: str,
    job: Dict[str, Any],
    skills: Dict[str, float],
) -> Dict[str, Any]:
    """
    Score a single candidate against a job configuration.

    Args:
        resume_text: Parsed resume text
        job: Job row dict from DB
        skills: {skill_name: weight} dict

    Returns:
        Full scoring breakdown dict
    """
    # 1. Skill matching
    matched_skills, missing_skills, skill_score = match_skills(resume_text, skills)

    # 2. Experience
    exp_years, timeline = extract_experience(resume_text)
    experience_score = score_experience(exp_years, job["required_experience"])

    # 3. Semantic similarity
    semantic_score = compute_semantic_similarity(resume_text, job["description"])

    # 4. Resume quality
    quality_score = compute_resume_quality_score(resume_text)

    # 5. Weights
    w_skill = job["skill_weight"]
    w_exp = job["experience_weight"]
    w_sem = job["semantic_weight"]
    w_qual = job["quality_weight"]
    total_weight = w_skill + w_exp + w_sem + w_qual

    if total_weight == 0:
        final_score = 0.0
    else:
        final_score = (
            skill_score * w_skill
            + experience_score * w_exp
            + semantic_score * w_sem
            + quality_score * w_qual
        ) / total_weight

    return {
        "skill_score": round(skill_score, 2),
        "experience_score": round(experience_score, 2),
        "semantic_score": round(semantic_score, 2),
        "quality_score": round(quality_score, 2),
        "final_score": round(final_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "experience_years": exp_years,
        "timeline": timeline,
    }


def recommendation_label(score: float) -> str:
    if score >= 75:
        return "Strongly Recommended"
    elif score >= 60:
        return "Recommended"
    elif score >= 45:
        return "Consider"
    return "Not Recommended"
