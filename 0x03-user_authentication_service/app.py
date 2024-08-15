#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
