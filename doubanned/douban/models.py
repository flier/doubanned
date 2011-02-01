from google.appengine.ext import db

class DoubanLocation(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)

class DoubanUser(db.Model):
    id = db.IntegerProperty(required=True)
    uid = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    location = db.ReferenceProperty(DoubanLocation)
    signature = db.StringProperty()
    content = db.StringProperty()
    page = db.StringProperty()
    homepage = db.StringProperty()
    icon = db.StringProperty()
    uri = db.StringProperty()
