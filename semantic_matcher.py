import streamlit as st


@st.cache_resource(show_spinner=False)
def load_model():
    """Load sentence-transformer model once and cache it."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def compute_semantic_similarity(resume_text: str, job_description: str) -> float:
    """
    Compute cosine similarity between resume and JD using sentence-transformers.
    Returns score scaled to 0-100.
    """
    try:
        model = load_model()
        from sentence_transformers import util

        # Truncate to avoid memory issues with very long texts
        resume_chunk = resume_text[:3000]
        jd_chunk = job_description[:3000]

        embeddings = model.encode([resume_chunk, jd_chunk], convert_to_tensor=True)
        similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

        # Cosine similarity ranges -1 to 1; normalize to 0-100
        score = (similarity + 1) / 2 * 100
        return round(score, 2)

    except Exception:
        # Fallback: simple keyword overlap ratio
        return _fallback_similarity(resume_text, job_description)


def _fallback_similarity(text1: str, text2: str) -> float:
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if not words2:
        return 0.0
    overlap = len(words1 & words2) / len(words2)
    return round(min(overlap * 100, 100), 2)
