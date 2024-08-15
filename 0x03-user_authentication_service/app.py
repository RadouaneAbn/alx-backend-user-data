#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request, abort, sessions
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
