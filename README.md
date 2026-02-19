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

---

## Project Structure

```
resume_screener/
├── app.py                  Main Streamlit application
├── auth.py                 Authentication and session management
├── database.py             SQLite database layer
├── resume_parser.py        PDF and DOCX parsing + quality scoring
├── experience_extractor.py Experience extraction from resume text
├── skill_matcher.py        Exact and fuzzy skill matching
├── semantic_matcher.py     Sentence-transformer semantic similarity
├── bias_detector.py        Bias phrase detection
├── scoring_engine.py       Composite scoring logic
├── ai_summary.py           AI and rule-based candidate summaries
├── report_generator.py     Excel and PDF export
├── requirements.txt        Python dependencies
└── .streamlit/
    └── config.toml         Streamlit theme configuration
```

---

## Local Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Set your Anthropic API key for LLM-powered summaries:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

4. Run the app:

```bash
streamlit run app.py
```

---

## Default Credentials

| Role  | Username  | Password  |
|-------|-----------|-----------|
| Admin | admin     | admin123  |
| HR    | hr_user   | hr123     |

Change these immediately in production using the database.

---

## Deploying to Streamlit Cloud

1. Push the project to a GitHub repository.

2. Go to https://share.streamlit.io and connect your repository.

3. Set the main file to `app.py`.

4. Add the following secret in the Streamlit Cloud dashboard under "Secrets":

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

5. Deploy. The SQLite database will be created automatically on first run.

Note: SQLite data on Streamlit Cloud is ephemeral (resets on app restart). For persistent storage in production, replace the SQLite layer with PostgreSQL using the same interface in database.py.

---

## Scoring Formula

```
Final Score = (Skill Score × Skill Weight
             + Experience Score × Experience Weight
             + Semantic Score × Semantic Weight
             + Quality Score × Quality Weight)
             / Total Weight
```

All weights are configurable per job by HR. Weights are normalized automatically.

---

## Recommendation Thresholds

| Score     | Label                 |
|-----------|-----------------------|
| >= 75     | Strongly Recommended  |
| >= 60     | Recommended           |
| >= 45     | Consider              |
| < 45      | Not Recommended       |
# resume-screening
