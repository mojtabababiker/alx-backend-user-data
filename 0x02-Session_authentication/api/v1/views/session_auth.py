#!/usr/bin/env python3
"""
session based authentication routes
"""
import os
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    login route for the session based auth
    """
    from api.v1.app import auth

    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get("password")
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({"email": email})[0]
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.environ.get("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)
    return response
