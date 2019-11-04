from models import AuthUser

def init_users():
    rob = AuthUser(a_id='1234', email='rob@live.ca', user_id='12344', password='password')
    rob.save()