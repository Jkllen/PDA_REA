import json
import hashlib
from pathlib import Path

DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"


def _ensure_users_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        default_users = {
            "2026-001": {
                "password_hash": hashlib.sha256("password123".encode("utf-8")).hexdigest()
            }
        }
        USERS_FILE.write_text(json.dumps(default_users, indent=2), encoding="utf-8")


def _load_users() -> dict:
    _ensure_users_file()
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_users(users: dict):
    _ensure_users_file()
    USERS_FILE.write_text(json.dumps(users, indent=2), encoding="utf-8")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def login(client: str, password: str) -> bool:
    if not client or not password:
        return False

    users = _load_users()
    client = client.strip()

    if client not in users:
        return False

    return users[client].get("password_hash") == hash_password(password)


def signup(client: str, password: str) -> tuple[bool, str]:
    client = client.strip()

    if not client:
        return False, "Client number is required."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    users = _load_users()

    if client in users:
        return False, "Client number already exists."

    users[client] = {"password_hash": hash_password(password)}
    _save_users(users)

    return True, "Account created successfully."