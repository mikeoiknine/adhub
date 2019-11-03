from flask_mongoengine.wtf import model_form
from flask_mongoengine.MongoEngine import .
from datetime import date

class AdItemStats(EmbeddedDocument):
    month_display_count = StringField(max_length=50)
    week_display_count = StringField(max_length=50)
    day_display_count = StringField(max_length=50)

    def __init__(self, month_display_count, week_display_count, day_display_count):
        self.month_display_count = month_display_count
        self.week_display_count = week_display_count
        self.day_display_count = day_display_count

    @property
    def serialize(self):
        return {
            '# Times Displayed Month' : self.month_display_count,
            '# Times Displayed Week' : self.week_display_count,
            '# Times Displayed Day' : self.day_display_count
        }

    def __repre__(self):
        print("# Times Displayed Month", self.month_display_count)
        print("# Times Displayed Week", self.week_display_count)
        print("# Times Displayed Day", self.day_display_count)

class AdItem(EmbeddedDocument):
    id = StringField(max_length=50, required=True)
    name = StringField(max_length=50, required=True)
    user_id = StringField(max_length=50, required=True)
    image_path = StringField(max_length=50, required=True)
    image_64 = StringField(max_length=50, required=True)
    region = StringField(max_length=50)
    stats = EmbeddedDocumentField(AdItemStats)
    upload_date = EmbeddedDocumentField(date)

    def __init__(self, id, name, user_id, image_path, image_64, region, stats, upload_date):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.image_path = image_path
        self.image_64 = image_64
        self.region = region
        self.stats = stats
        self.upload_date = upload_date

    @property
    def serialize(self):
        return {
            'ID: ' : self.id,
            'Name: ' : self.name,
            'User ID: ' : self.user_id,
            'Image Path: ' : self.image_path,
            'Image 64: ' : self.image_64,
            'Region: ' : self.region,
            'Stats: ' : self.stats.serialize()
        }            

    def __repr__(self):
        print("ID", self.id)
        print("Name", self.name)
        print("User ID", self.user_id)
        print("Image Path", self.image_path)
        print("Region", self.region)
        print("Stats", self.stats.__repr__())

class AuthUser(Document):
    id = StringField(max_length=50, required=True)
    email = StringField(max_length=50, required=True)
    uer_id = StringField(max_length=50, required=True)
    password = StringField(max_length=50, required=True)

    def __init__(self, id, email, user_id, password):
        self.id = id
        self.email = email
        self.user_id = user_id
        self.password = password

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'email' : self.email,
            'user id' : self.user_id,
            'password' : self.password
        }

    def __repr__(self):
        print("ID: ", self.id)
        print("Email: ", self.email)
        print("User ID: ", self.user_id)
        print("Password: ", self.password)

class User(Document, AuthUser):
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    company = StringField(max_length=50, required=True)
    address = StringField(max_length=50, required=True)
    ad_items = ListField(EmbeddedDocumentField(AdItem))

    def __init__(self, id, email, user_id, password, first_name=None, last_name=None, company, address, ad_items=None):
        super(AuthUser, self).__init__(id, email, user_id, password)
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.address = address
        self.ad_items = ad_items
        
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'email' : self.email,
            'user id' : self.user_id,
            'password' : self.password,
            'first_name' : self.firrst_name,
            'last_name' : self.last_name,
            'company' : self.company,
            'address' : self.address
        }

    def __repr__(self):
        super(AuthUser, self).__repr__()
        print("First Name: ", self.first_name)
        print("Last Name: ", self.last_name)
        print("Company: ", self.company)
        print("Address: ", self.address)

