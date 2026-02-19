"""
Database layer — SQLite with field-level encryption on sensitive columns.
- candidates.raw_text: Fernet-encrypted at rest
- All queries go through helpers that auto-encrypt/decrypt
"""

import sqlite3
import json
from datetime import datetime
from encryption import encrypt_text, decrypt_text, sanitize_filename

DB_PATH = "resume_screening.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'hr',
            created_at TEXT NOT NULL,
            last_login TEXT
        );

        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            required_experience REAL NOT NULL DEFAULT 0,
            skill_weight REAL NOT NULL DEFAULT 0.4,
            experience_weight REAL NOT NULL DEFAULT 0.2,
            semantic_weight REAL NOT NULL DEFAULT 0.3,
            quality_weight REAL NOT NULL DEFAULT 0.1,
            created_by INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS skill_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            weight REAL NOT NULL DEFAULT 1.0,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            raw_text TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER UNIQUE NOT NULL,
            skill_score REAL,
            experience_score REAL,
            semantic_score REAL,
            quality_score REAL,
            final_score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            experience_years REAL,
            ai_summary TEXT,
            bias_flags TEXT,
            scored_at TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            detail TEXT,
            ts TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


# ── Audit ──────────────────────────────────────────────────────────
def audit(user_id, action, detail=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO audit_log (user_id, action, detail, ts) VALUES (?, ?, ?, ?)",
        (user_id, action, detail, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


# ── Users ──────────────────────────────────────────────────────────
def create_user(username, password_hash, role="hr"):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
            (username, password_hash, role, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_last_login(user_id):
    conn = get_connection()
    conn.execute("UPDATE users SET last_login=? WHERE id=?", (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()


# ── Jobs ───────────────────────────────────────────────────────────
def save_job(title, description, required_experience, skill_weight, experience_weight,
             semantic_weight, quality_weight, skills, created_by):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO jobs (title, description, required_experience, skill_weight,
           experience_weight, semantic_weight, quality_weight, created_by, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (title, description, required_experience, skill_weight, experience_weight,
         semantic_weight, quality_weight, created_by, datetime.now().isoformat())
    )
    job_id = c.lastrowid
    for skill_name, weight in skills.items():
        c.execute("INSERT INTO skill_weights (job_id, skill_name, weight) VALUES (?, ?, ?)",
                  (job_id, skill_name, weight))
    conn.commit()
    conn.close()
    return job_id


def update_job(job_id, title, description, required_experience, skill_weight,
               experience_weight, semantic_weight, quality_weight, skills):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """UPDATE jobs SET title=?, description=?, required_experience=?, skill_weight=?,
           experience_weight=?, semantic_weight=?, quality_weight=? WHERE id=?""",
        (title, description, required_experience, skill_weight, experience_weight,
         semantic_weight, quality_weight, job_id)
    )
    c.execute("DELETE FROM skill_weights WHERE job_id=?", (job_id,))
    for skill_name, weight in skills.items():
        c.execute("INSERT INTO skill_weights (job_id, skill_name, weight) VALUES (?, ?, ?)",
                  (job_id, skill_name, weight))
    conn.commit()
    conn.close()


def get_all_jobs():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_job(job_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_job_skills(job_id):
    conn = get_connection()
    rows = conn.execute("SELECT skill_name, weight FROM skill_weights WHERE job_id=?", (job_id,)).fetchall()
    conn.close()
    return {r["skill_name"]: r["weight"] for r in rows}


def delete_job(job_id):
    conn = get_connection()
    conn.execute("DELETE FROM jobs WHERE id=?", (job_id,))
    conn.commit()
    conn.close()


# ── Candidates (with encrypted raw_text) ──────────────────────────
def save_candidate(job_id, filename, raw_text):
    filename = sanitize_filename(filename)
    encrypted_text = encrypt_text(raw_text)
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO candidates (job_id, filename, raw_text, uploaded_at) VALUES (?, ?, ?, ?)",
        (job_id, filename, encrypted_text, datetime.now().isoformat())
    )
    cid = c.lastrowid
    conn.commit()
    conn.close()
    return cid


def get_candidates_for_job(job_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT c.id, c.job_id, c.filename, c.uploaded_at,
           s.final_score, s.skill_score, s.experience_score, s.semantic_score,
           s.quality_score, s.matched_skills, s.missing_skills, s.experience_years,
           s.ai_summary, s.bias_flags
           FROM candidates c LEFT JOIN scores s ON c.id = s.candidate_id
           WHERE c.job_id = ? ORDER BY s.final_score DESC NULLS LAST""",
        (job_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_candidate(candidate_id):
    conn = get_connection()
    row = conn.execute(
        """SELECT c.id, c.job_id, c.filename, c.uploaded_at,
           c.raw_text,
           s.final_score, s.skill_score, s.experience_score, s.semantic_score,
           s.quality_score, s.matched_skills, s.missing_skills, s.experience_years,
           s.ai_summary, s.bias_flags, s.scored_at
           FROM candidates c LEFT JOIN scores s ON c.id = s.candidate_id
           WHERE c.id = ?""",
        (candidate_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    # Decrypt resume text transparently
    d["raw_text"] = decrypt_text(d.get("raw_text") or "")
    return d


def save_score(candidate_id, skill_score, experience_score, semantic_score, quality_score,
               final_score, matched_skills, missing_skills, experience_years, ai_summary, bias_flags):
    conn = get_connection()
    conn.execute(
        """INSERT OR REPLACE INTO scores
           (candidate_id, skill_score, experience_score, semantic_score, quality_score,
            final_score, matched_skills, missing_skills, experience_years, ai_summary, bias_flags, scored_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (candidate_id, skill_score, experience_score, semantic_score, quality_score, final_score,
         json.dumps(matched_skills), json.dumps(missing_skills),
         experience_years, ai_summary, json.dumps(bias_flags),
         datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def delete_candidates_for_job(job_id):
    conn = get_connection()
    conn.execute("DELETE FROM candidates WHERE job_id=?", (job_id,))
    conn.commit()
    conn.close()
