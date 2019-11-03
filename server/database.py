from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

def init_db(db, app):
    db.init_app(app)

    # MongoEngine settings
    app.config['MONGODB_SETTINGS'] = {
        'db' : 'adhub',
        'port' : 27017,
        'host' : 'localhost',
        'username' : 'adhub_app',
        'password' : '123456789',
        'connect' : True
    }

    # Setup interface to visualize operations
    app.session_interface = MongoEngineSessionInterface(db)