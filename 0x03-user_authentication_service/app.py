#!/usr/bin/env python3
'''
    flask application
'''
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def home() -> str:
    '''
        route definition of home
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', method='POST')
def users() -> str:
    '''
        function that registers a new User
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
