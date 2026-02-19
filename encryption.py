"""
Industry-level encryption and security utilities.
- Passwords: bcrypt with cost factor 12
- Sensitive data at rest: Fernet (AES-128-CBC + HMAC-SHA256)
- Session tokens: HMAC-SHA256 signed, time-limited
- Key derivation: PBKDF2-HMAC-SHA256
"""

import os
import hmac
import hashlib
import base64
import time
import secrets
from typing import Optional

import bcrypt

# ── Fernet for field-level encryption ──────────────────────────────
def _get_fernet():
    """Return a Fernet instance keyed from environment or a stable derived key."""
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        return None

    raw_key = os.environ.get("APP_ENCRYPTION_KEY", "")
    if raw_key:
        # Expect a URL-safe base64 32-byte key
        try:
            key = base64.urlsafe_b64decode(raw_key.encode())
            if len(key) == 32:
                return Fernet(base64.urlsafe_b64encode(key))
        except Exception:
            pass

    # Derive a stable key from a salt stored in the DB directory
    salt_path = os.path.join(os.path.dirname(__file__), ".app_salt")
    if not os.path.exists(salt_path):
        salt = secrets.token_bytes(16)
        with open(salt_path, "wb") as fh:
            fh.write(salt)
    else:
        with open(salt_path, "rb") as fh:
            salt = fh.read()

    # Derive 32 bytes via PBKDF2
    master = os.environ.get("APP_MASTER_PASSPHRASE", "resume_screening_default_dev_key")
    derived = hashlib.pbkdf2_hmac("sha256", master.encode(), salt, iterations=200_000, dklen=32)
    return Fernet(base64.urlsafe_b64encode(derived))


_FERNET = None

def get_fernet():
    global _FERNET
    if _FERNET is None:
        _FERNET = _get_fernet()
    return _FERNET


# ── Password hashing ───────────────────────────────────────────────
BCRYPT_ROUNDS = 12

def hash_password(password: str) -> str:
    """Hash a password with bcrypt (cost=12)."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=BCRYPT_ROUNDS)).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Constant-time bcrypt comparison."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# ── Field-level encryption ─────────────────────────────────────────
def encrypt_text(plaintext: str) -> str:
    """Encrypt a string. Returns base64-encoded ciphertext, or plaintext if crypto unavailable."""
    fernet = get_fernet()
    if fernet is None or not plaintext:
        return plaintext
    try:
        return fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")
    except Exception:
        return plaintext


def decrypt_text(ciphertext: str) -> str:
    """Decrypt a Fernet-encrypted string. Returns original on failure."""
    fernet = get_fernet()
    if fernet is None or not ciphertext:
        return ciphertext
    try:
        return fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except Exception:
        # Already plaintext (e.g. legacy unencrypted row)
        return ciphertext


# ── Session token ──────────────────────────────────────────────────
_SESSION_SECRET = os.environ.get("APP_SESSION_SECRET", secrets.token_hex(32))
SESSION_TTL = 8 * 3600  # 8 hours


def generate_session_token(user_id: int, username: str) -> str:
    """Generate a signed session token: base64(payload):hmac"""
    payload = f"{user_id}:{username}:{int(time.time())}"
    encoded = base64.urlsafe_b64encode(payload.encode()).decode()
    sig = hmac.new(_SESSION_SECRET.encode(), encoded.encode(), hashlib.sha256).hexdigest()
    return f"{encoded}.{sig}"


def validate_session_token(token: str) -> Optional[dict]:
    """Validate a session token. Returns {user_id, username} or None."""
    try:
        encoded, sig = token.rsplit(".", 1)
        expected = hmac.new(_SESSION_SECRET.encode(), encoded.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        payload = base64.urlsafe_b64decode(encoded.encode()).decode()
        user_id_str, username, ts_str = payload.split(":")
        if time.time() - int(ts_str) > SESSION_TTL:
            return None
        return {"user_id": int(user_id_str), "username": username}
    except Exception:
        return None


# ── Input sanitization ─────────────────────────────────────────────
import re

def sanitize_username(username: str) -> str:
    """Allow only alphanumeric, underscore, hyphen (max 64 chars)."""
    return re.sub(r"[^a-zA-Z0-9_\-]", "", username)[:64]


def sanitize_filename(filename: str) -> str:
    """Strip path components and dangerous chars from filename."""
    filename = os.path.basename(filename)
    filename = re.sub(r"[^\w\s.\-]", "", filename)
    return filename[:255]
