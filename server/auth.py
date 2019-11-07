from __future__ import print_function
import sys
import functools

from flask import (
        Blueprint, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import BasicUser
#from app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if request.method != 'POST':
        print("Err: Recieved non-POST request.", file=sys.stderr)
        return
    content = request.json
    user = BasicUser(username=content['username'], password=content['password'])
    user.save()

    return jsonify(content)

@bp.route('/login', methods=['POST'])
def login():
    if request.method != 'POST':
        return

    content = request.json

    # TODO
    """
    1) Fetch DB Handle
    2) Check if username exists in DB
    3) If it does, check if hashes passord matches the one in db
    4) If all is good, create a new session for this user and redirect to home page
    """
    return jsonify(content)

