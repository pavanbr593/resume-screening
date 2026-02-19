import os
from typing import Dict, Any, List


def generate_ai_summary(
    resume_text: str,
    job_description: str,
    matched_skills: List[str],
    missing_skills: List[str],
    experience_years: float,
    required_experience: float,
    final_score: float,
) -> str:
    """
    Generate a candidate summary. Uses Claude API if key is set,
    otherwise falls back to a rule-based summary.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if api_key:
        return _llm_summary(
            api_key, resume_text, job_description, matched_skills,
            missing_skills, experience_years, required_experience, final_score
        )
    return _rule_based_summary(
        matched_skills, missing_skills, experience_years,
        required_experience, final_score
    )


def _llm_summary(
    api_key: str,
    resume_text: str,
    job_description: str,
    matched_skills: List[str],
    missing_skills: List[str],
    experience_years: float,
    required_experience: float,
    final_score: float,
) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""You are an expert HR analyst. Analyze this candidate's fit for the role.

Job Description (excerpt):
{job_description[:800]}

Resume (excerpt):
{resume_text[:1500]}

Analysis data:
- Matched skills: {', '.join(matched_skills) or 'None'}
- Missing skills: {', '.join(missing_skills) or 'None'}
- Candidate experience: {experience_years} years (required: {required_experience} years)
- Overall score: {final_score}/100

Provide a concise structured summary with these four sections:
1. Strengths
2. Weakness Areas
3. Job Fit Assessment
4. Interview Focus Suggestions

Keep each section to 2-3 bullet points. Be specific and actionable."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return _rule_based_summary(
            matched_skills, missing_skills, experience_years,
            required_experience, final_score
        ) + f"\n\n[LLM unavailable: {e}]"


def _rule_based_summary(
    matched_skills: List[str],
    missing_skills: List[str],
    experience_years: float,
    required_experience: float,
    final_score: float,
) -> str:
    lines = []

    # Strengths
    lines.append("Strengths:")
    if matched_skills:
        lines.append(f"  - Matches {len(matched_skills)} required skill(s): {', '.join(matched_skills[:5])}")
    if experience_years >= required_experience and required_experience > 0:
        lines.append(f"  - Meets experience requirement ({experience_years} vs {required_experience} years required)")
    elif experience_years > 0:
        lines.append(f"  - Has {experience_years} years of experience")
    if final_score >= 75:
        lines.append("  - Strong overall profile alignment with the role")

    # Weakness Areas
    lines.append("\nWeakness Areas:")
    if missing_skills:
        lines.append(f"  - Missing skills: {', '.join(missing_skills[:5])}")
    if required_experience > 0 and experience_years < required_experience:
        gap = round(required_experience - experience_years, 1)
        lines.append(f"  - Experience gap of {gap} year(s) below requirement")
    if final_score < 50:
        lines.append("  - Overall profile is a weak match for the role")

    # Job Fit Assessment
    lines.append("\nJob Fit Assessment:")
    if final_score >= 75:
        lines.append("  - Strong candidate — highly recommended for interview")
    elif final_score >= 60:
        lines.append("  - Good candidate — recommended for interview with some gaps to explore")
    elif final_score >= 45:
        lines.append("  - Borderline candidate — review carefully before proceeding")
    else:
        lines.append("  - Weak match — significant gaps relative to requirements")

    # Interview Focus
    lines.append("\nInterview Focus Suggestions:")
    if missing_skills:
        lines.append(f"  - Probe depth of knowledge in: {', '.join(missing_skills[:3])}")
    if experience_years < required_experience:
        lines.append("  - Ask about project scale and complexity to assess maturity")
    lines.append("  - Verify claimed skills with technical or scenario-based questions")

    return "\n".join(lines)
