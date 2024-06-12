#!/usr/bin/env python3
"""Basic flask app module
"""
from flask import Flask, Response, abort, request, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home() -> Response:
    """Home endpoint
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users() -> Response:
    """Users registration endpoint
    """
    try:
        user = AUTH.register_user(
            request.form.get("email"), request.form.get("password")
            )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> Response:
    """Login endpoint based on the form creadentials
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(401)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
    else:
        abort(401)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
