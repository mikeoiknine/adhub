from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

def init_db(db, app):
    db.init_app(app)

    # MongoEngine settings
    app.config['MONGODB_SETTINGS'] = {
        'db' : 'adhub',
        'host' : 'mongodb://adhub:3e9XApN7AuDgr0llM47rjAo3NpqIbyLomBeiphIrvn1MIGjNEKk1PppFW1iU8hmIr8VsJWKof20AgXWGA4bxqg==@adhub.documents.azure.com:10255/?ssl=true&replicaSet=globaldb',
        'username' : 'adhub_app',
        'password' : '123456789',
        'connect' : True
    }

    # Setup interface to visualize operations
    app.session_interface = MongoEngineSessionInterface(db)