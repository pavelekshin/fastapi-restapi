import base64

import bcrypt


def hash_password(password: str) -> str:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt).decode()


def check_password(password: str, password_in_db: str) -> bool:
    pw_bytes = bytes(password, "utf-8")
    pw_in_db_bytes = bytes(password_in_db, "utf-8")
    return bcrypt.checkpw(pw_bytes, pw_in_db_bytes)


def b64e(s: str) -> str:
    """encode string to base64"""
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")


def b64d(s: str) -> str:
    """decode base64 string to string"""
    return base64.b64decode(s).decode("utf-8")
