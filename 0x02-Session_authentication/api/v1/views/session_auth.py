#!/usr/bin/env python3
""" Module of Session Authentication views
"""

from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort
import os


# Route for user login with session authentication
@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth():
    '''
        method for handling session authentification
    '''
    # Extract email and password from the request form
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    # Search for users with the given email
    users = User.search({"email": email})

    # If no users found, return an error
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    # Check each user's password to find a match
    for user in users:
        if user.is_valid_password(password):
            # If the password is valid, create a session, set the
            # session cookie, and return the user data
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp

    # If no user has a matching password, return an error
    return jsonify({"error": "wrong password"}), 401


# Route for user logout with session authentication
@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    '''
        Logout user
    '''
    # Retrieve the authentication instance
    from api.v1.app import auth

    # Destroy the session and return success or 404 if not found
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
