#!/usr/bin/env python3
""" main Module to test routes """
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ This function test the register user route """
    msg = requests.post("http://0.0.0.0:5000/users", data={
        "email": EMAIL, "password": PASSWD
    })
    assert msg.json() == {'email': EMAIL,
                          'message': 'user created'}
    msg = requests.post("http://0.0.0.0:5000/users", data={
        "email": email, "password": password
    })
    assert msg.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ This function test login route"""
    msg = requests.post("http://0.0.0.0:5000/sessions", data={
        "email": email, "password": password
    })
    assert msg.status_code == 401


def profile_unlogged() -> None:
    """ This function tests the profile route """
    msg = requests.get("http://0.0.0.0:5000/profile", cookies={
        "session_id": "fake_id"
    })

    assert msg.status_code == 403


def log_in(email: str, password: str) -> str:
    """ This function test login route"""
    msg = requests.post("http://0.0.0.0:5000/sessions", data={
        "email": email, "password": password
    })

    assert msg.json() == {"email": EMAIL, "message": "logged in"}
    session_id = msg.cookies.get("session_id")
    assert type(session_id) is str
    return session_id


def profile_logged(session_id: str) -> None:
    """ This function tests the profile route """
    msg = requests.get("http://0.0.0.0:5000/profile", cookies={
        "session_id": session_id
    })
    assert msg.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ This function test logout route"""
    msg = requests.delete("http://0.0.0.0:5000/sessions", cookies={
        "session_id": session_id
    })
    assert msg.url == "http://0.0.0.0:5000/"


def reset_password_token(email: str) -> str:
    """ This function test reset password route"""
    msg = requests.post("http://0.0.0.0:5000/reset_password", data={
        "email": email
    })
    data = msg.json()
    assert data["email"] == EMAIL
    assert type(data["reset_token"]) is str
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ This function test update password route"""
    msg = requests.put("http://0.0.0.0:5000/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    data = msg.json()
    assert data == {"email": EMAIL, "message": "Password updated"}


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
