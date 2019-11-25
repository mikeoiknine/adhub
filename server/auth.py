from __future__ import print_function
import sys
import functools

from flask import (
<<<<<<< HEAD
        Blueprint, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import BasicUser
#from app import db
=======
        Blueprint, request, jsonify, g, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import mongo
>>>>>>> 3fd9b72... Crude attempt at returning new ads

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if request.method != 'POST':
<<<<<<< HEAD
        print("Err: Recieved non-POST request.", file=sys.stderr)
        return
    content = request.json
    user = BasicUser(username=content['username'], password=content['password'])
    user.save()

    return jsonify(content)
=======
        print("******Err: Recieved non-POST request.", file=sys.stderr)
        return

    content = request.json

    users = mongo.db.users
    existing_user = users.find_one({"username" : content["username"]})

    if existing_user is None:
        user_id = users.insert({
            'username': content['username'],
            'password': generate_password_hash(content['password'])
        })
        print(user_id, file=sys.stderr)
        return jsonify({'id': str(user_id)})

    return jsonify({'id': None, 'msg': 'User already exists'})
>>>>>>> 3fd9b72... Crude attempt at returning new ads

@bp.route('/login', methods=['POST'])
def login():
    if request.method != 'POST':
        return

    content = request.json

<<<<<<< HEAD
    # TODO
    """
    1) Fetch DB Handle
    2) Check if username exists in DB
    3) If it does, check if hashes passord matches the one in db
    4) If all is good, create a new session for this user and redirect to home page
    """
    return jsonify(content)

=======
    users = mongo.db.users
    existing_user = users.find_one({"username" : content["username"]})

    if existing_user is None:
        return make_response(jsonify({'msg': 'Incorrect Username'}), 500)
    elif not check_password_hash(existing_user['password'], content['password']):
        return make_response(jsonify({'msg': 'Incorrect Password'}), 500)

    session.clear()
    session['user_id'] = str(existing_user['_id'])
    return jsonify({'id': str(existing_user['_id'])})

@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'msg': 'Success'})

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = mongo.db.users.find_one({'_id': user_id})

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'msg': 'Go To Login page pls', 'url': url_for('auth.login')})
        return view(**kwargs)
    return wrapped_view
>>>>>>> 3fd9b72... Crude attempt at returning new ads
