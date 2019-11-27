from __future__ import print_function
import sys
import functools

from flask import (
        Blueprint, request, jsonify, g, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import mongo

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if request.method != 'POST':
        return jsonify({"msg": "Invalid Request type"})

    content = request.json
    if 'username' not in content or content['username'] == "":
        return jsonify({"msg": "Invalid Request - Missing username field"})
    if 'password' not in content or content['password'] == "":
        return jsonify({"msg": "Invalid Request - Missing password field"})
    if 'name' not in content or content['name'] == "":
        return jsonify({"msg": "Invalid Request - Missing name field"})
    if 'businessName' not in content or content['businessName'] == "":
        return jsonify({"msg": "Invalid Request - Missing businessName field"})
    if 'location' not in content or content['location'] == "":
        return jsonify({"msg": "Invalid Request - Missing location field"})


    users = mongo.db.users
    existing_user = users.find_one({"username" : content["username"]})

    if existing_user is None:
        user_id = users.insert({
            'username': content['username'],
            'password': generate_password_hash(content['password']),
            'name': content['name'],
            'businessName': content['businessName'],
            'location': content['location'],
            'stats': {
                'total_ads_displayed': 0
                }
        })
        print(user_id, file=sys.stderr)
        return jsonify({'id': str(user_id)})

    return jsonify({'id': None, 'msg': 'User already exists'})

@bp.route('/login', methods=['POST'])
def login():
    if request.method != 'POST':
        return

    content = request.json
    if 'username' not in content or content['username'] == "":
        return jsonify({"msg": "Invalid Request - Missing username field"})
    if 'password' not in content or content['password'] == "":
        return jsonify({"msg": "Invalid Request - Missing password field"})

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
