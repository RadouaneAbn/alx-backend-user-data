#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home() -> str:
    """ This is a route for '/' """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def create_user():
    """ This route is for creating a new user """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"})
    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def create_sessions():
    """ this route authenticate a user and creates a session """
    email = request.form.get("email")
    password = request.form.get("password")
    if not password or not email:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    new_session = AUTH.create_session(email)
    out = jsonify({"email": email, "message": "logged in"})
    out.set_cookie("session_id", new_session)
    return out


@app.route("/sessions", methods=["DELETE"])
def delete_sessions() -> str:
    """ This route log a user out """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """ This route return email of user using the session_id """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """ This route gets a password reset token for a user """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
