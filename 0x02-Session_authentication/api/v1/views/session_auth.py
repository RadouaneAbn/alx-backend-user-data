#!/usr/bin/env python3
""" Auth related routes
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def login() -> str:
    """ This route to athenticate a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    out = jsonify(user.to_json())
    out.set_cookie(getenv("SESSION_NAME"), session_id)
    return out


@app_views.route("/auth_session/logout",
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ This route is for logout """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
