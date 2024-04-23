#!/usr/bin/env python3
""" Start my application - Main file """
import requests

HOST_URL = "http://127.0.0.1:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test register users """
    data = {"email": email, "password": password}
    response = requests.post(f"{HOST_URL}/users", data=data)

    msg = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test validation password """
    data = {"email": email, "password": password}
    response = requests.post(f"{HOST_URL}/sessions", data=data)
    assert(response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """ Test Login users """
    data = {"email": email, "password": password}
    response = requests.post(f"{HOST_URL}/sessions", data=data)
    assert(response.status_code == 200)
    assert(response.json() == {"email": email, "message": "logged in"})
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """ for profile without being logged in with session_id """
    response = requests.get(f"{HOST_URL}/profile")
    return (response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """ Test for log in with the given correct email and password """
    cookies = {'session_id': session_id}
    response = requests.get(f'{HOST_URL}/profile',
                            cookies=cookies)
    assert(response.status_code == 200)


def log_out(session_id: str) -> None:
    """ Test logout using session_id """
    cookies = {'session_id': session_id}
    response = requests.delete(f'{HOST_URL}/sessions',
                               cookies=cookies)
    if response.status_code == 302:
        assert(response.url == f'{HOST_URL}')
    else:
        assert(response.status_code == 200)


def reset_password_token(email: str) -> str:
    """ Test reset password using token """
    data = {'email': email}
    response = requests.post(f'{HOST_URL}/reset_password', data=data)

    if response.status_code == 200:
        return response.json()['reset_token']
    assert(response.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test update the password """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(f'{HOST_URL}/reset_password',
                            data=data)
    if response.status_code == 200:
        assert(response.json() == {"email": email,
                                   "message": "Password updated"})
    else:
        assert(response.status_code == 403)


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
