#!/usr/bin/env python3
""" Start my application - Main file """
import requests


def register_user(email: str, password: str) -> None:
    """ Test register users """
    r = requests.post("http://127.0.0.1:5000/users",
                      data_fields={"email": email, "password": password})
    if r.status_code == 200:
        assert(r.json() == {"email": email, "message": "user created"})
    else:
        assert(r.status_code == 400)
        assert(r.json() == {"message": "email already registred"})


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test validation password """
    r = requests.post("http://127.0.0.1:5000/sessions",
                      data_fields={"email": email, "password": password})
    assert(r.status_code == 401)


def log_in(email: str, password: str) -> str:
    """ Test Login users """
    r = requests.post("http://127.0.0.1:5000/sessions",
                      data_fields={"email": email, "password": password})
    assert(r.status_code == 200)
    assert(r.json() == {"email": email, "message": "logged in"})
    return r.cookies["session_id"]


def profile_unlogged() -> None:
    """ for profile without being logged in with session_id """
    response = requests.get("http://127.0.0.1:5000/profile")
    return (response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """ Test for log in with the given correct email and password """
    cookies = {'session_id': session_id}
    response = requests.get('http://127.0.0.1:5000/profile',
                            cookies=cookies)
    assert(response.status_code == 200)


def log_out(session_id: str) -> None:
    """ Test logout using session_id """
    cookies = {'session_id': session_id}
    response = requests.delete('http://127.0.0.1:5000/sessions',
                               cookies=cookies)
    if response.status_code == 302:
        assert(response.url == 'http://127.0.0.1:5000/')
    else:
        assert(response.status_code == 200)


def reset_password_token(email: str) -> str:
    """ Test reset password using token """
    response = requests.post('http://127.0.0.1:5000/reset_password',
                             data_fields={'email': email})
    if response.status_code == 200:
        return response.json()['reset_token']
    assert(response.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test update the password """
    data_fields = {'email': email, 'reset_token': reset_token,
                   'new_password': new_password}
    response = requests.put('http://127.0.0.1:5000/reset_password',
                            data_fields=data_fields)
    if response.status_code == 200:
        assert(response.json() == {"email": email,
                                   "message": "Password updated"})
    else:
        assert(response.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
