from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

def init_db(db, app):

    # MongoEngine settings
    app.config['MONGODB_SETTINGS'] = {
        'db' : 'adhub',
        'host' : 'mongodb://adhub:3e9XApN7AuDgr0llM47rjAo3NpqIbyLomBeiphIrvn1MIGjNEKk1PppFW1iU8hmIr8VsJWKof20AgXWGA4bxqg==@adhub.documents.azure.com:10255/?ssl=true&replicaSet=globaldb',
        #'port' : 5000,
        'username' : 'adhub_app',
        'password' : '123456789',
    }

    # Initialize connection
    db.init_app(app)

    # Setup interface to visualize operations
    app.session_interface = MongoEngineSessionInterface(db)