import os

from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    #app.config["MONGO_URI"] = {
    #        "db": "testdb",
    #        "host": "localhost",
    #        "port": 27017,
    #        "alias": "default"
    #}
    #global mongo
    from .db import mongo
    mongo.init_app(app)

    CORS(app)
    # Initialize MongoDB Engine with app
    #app.config['MONGODB_SETTINGS'] = {
    #        "db": "testdb",
    #        "host": "localhost",
    #        "port": 27017,
    #        "alias": "default"
    #}
    ##database.init_db(db, app)
    #db.init_app(app, config={
    #    'db': 'testdb',
    #    'host': 'localhost',
    #    'port': 27017,
    #    'alias': 'default'
    #})
    #toolbar = DebugToolbarExtension(app)

    # Add User
    #data.init_users()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return "Hello World!"

    from . import auth
    app.register_blueprint(auth.bp)

    from . import data
    app.register_blueprint(data.bp)

    return app