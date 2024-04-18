#!/usr/bin/env python3
""" Create a new Flask view that handles all routes
for the Session authentication """
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_login():
    """ Method POST
    route /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    for usr in user:
        if usr.is_valid_password(password):
            from api.v1.app import auth
            session_user_id = auth.create_session(usr.id)
            response = jsonify(usr.to_json())
            cookie = os.getenv('SESSION_NAME')
            response.set_cookie(cookie, session_user_id)
            return response
    return jsonify({"error": "wrong password"}), 401

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def create_logout():
    """ Method DELETE
    route /api/v1/auth_session/login
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({"status": "success"}), 200
    abort(404)
