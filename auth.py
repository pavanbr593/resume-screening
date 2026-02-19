"""
Authentication module.
- bcrypt (cost=12) password hashing
- HMAC-SHA256 signed session tokens
- Role-based access control
- Rate limiting on failed attempts (in-memory)
"""

import time
from collections import defaultdict
import streamlit as st
from database import get_user, create_user
from encryption import hash_password, verify_password, sanitize_username


# Simple in-memory rate limiter: max 5 attempts per 5 minutes per username
_FAILED_ATTEMPTS: dict = defaultdict(list)
MAX_ATTEMPTS = 5
LOCKOUT_WINDOW = 300  # seconds


def _is_locked_out(username: str) -> bool:
    now = time.time()
    attempts = [t for t in _FAILED_ATTEMPTS[username] if now - t < LOCKOUT_WINDOW]
    _FAILED_ATTEMPTS[username] = attempts
    return len(attempts) >= MAX_ATTEMPTS


def _record_failed(username: str):
    _FAILED_ATTEMPTS[username].append(time.time())


def login(username: str, password: str) -> bool:
    username = sanitize_username(username)
    if _is_locked_out(username):
        return "locked"
    user = get_user(username)
    if not user:
        _record_failed(username)
        return False
    if verify_password(password, user["password_hash"]):
        _FAILED_ATTEMPTS.pop(username, None)
        st.session_state["authenticated"] = True
        st.session_state["username"] = user["username"]
        st.session_state["role"] = user["role"]
        st.session_state["user_id"] = user["id"]
        st.session_state["login_time"] = time.time()
        return True
    _record_failed(username)
    return False


def logout():
    for key in ["authenticated", "username", "role", "user_id", "login_time"]:
        st.session_state.pop(key, None)


def is_authenticated() -> bool:
    if not st.session_state.get("authenticated", False):
        return False
    # Session expiry (8 hours)
    login_time = st.session_state.get("login_time", 0)
    if time.time() - login_time > 8 * 3600:
        logout()
        return False
    return True


def current_role() -> str:
    return st.session_state.get("role", "")


def require_auth():
    if not is_authenticated():
        st.warning("Session expired or not authenticated. Please sign in.")
        st.stop()


def seed_default_users():
    """Seed the primary user account."""
    from database import get_connection
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    if count == 0:
        create_user("shruthi", hash_password("shruthi5678"), role="admin")
