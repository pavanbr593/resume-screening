# Resume Screening System

A production-ready internal AI resume screening and ranking system built with Python and Streamlit.

---

## Features

- Secure login with bcrypt password hashing and role-based access (HR / Admin)
- Job configuration with dynamic skills and configurable score weights
- Bulk PDF/DOCX resume upload and parsing
- Skill matching using exact + fuzzy matching (RapidFuzz)
- Experience extraction via regex and date range parsing
- Semantic similarity scoring using sentence-transformers (all-MiniLM-L6-v2)
- Resume quality scoring based on structure heuristics
- AI-generated candidate summaries (uses Claude API if key is provided, otherwise rule-based)
- Bias detection in job descriptions and resumes
- Ranking dashboard with filtering and metrics
- Candidate detail view with score breakdown charts
- Export to Excel and PDF
