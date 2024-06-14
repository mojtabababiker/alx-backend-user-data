#!/usr/bin/env python3
"""
End-to-end integration test
"""
import requests
import requests.cookies


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user with email email and password password
    using the /users endpoint test
    """
    data = {
        "email": email,
        "password": password,
    }
    response = requests.post(f"{URL}/users", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Login user with email email and wrong password test"""
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/sessions", data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Login user with the right credentials test"""
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/sessions", data=data)
    session_id = response.cookies.get("session_id")
    assert response.status_code == 200
    assert session_id is not None
    assert response.json() == {"email": email, "message": "logged in"}
    return session_id


def profile_unlogged() -> None:
    """Get the unlogged user profile test"""
    response = requests.get(f"{URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Get logged in user profile test"""

    response = requests.get(f"{URL}/profile",
                            cookies={"session_id": session_id}
                            )
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Logout user test"""
    response = requests.delete(
        f"{URL}/sessions",
        cookies={"session_id": session_id},
        allow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers.get("Location") == "/"


def reset_password_token(email: str) -> str:
    """Get the reset password token test"""
    response = requests.post(f"{URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    reset_password_token = response.json().get("reset_token", None)
    assert reset_password_token is not None
    assert response.json() == {"email": email,
                               "reset_token": reset_password_token
                               }
    return reset_password_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password endpoint test"""
    data = {
        "email": email,
        "new_password": new_password,
        "reset_token": reset_token
        }
    response = requests.put(f"{URL}/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
