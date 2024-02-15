#!/usr/bin/env python3
""" view for Session Authentication """
from os import getenv
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """  view that handles all routes for the Session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or email is None:
        return jsonify({'error': 'email missing'}), 400
    if password == '' or password is None:
        return jsonify({'error': 'password missing'}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({'error': 'no user found for thid email'}), 404

    if not user[0].is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401

    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout the user and delete the session cookie
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
