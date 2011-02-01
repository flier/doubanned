try:
    import simplejson as json
except ImportError:
    import json

from google.appengine.ext import db
from google.appengine.api import memcache, users

class DoubanLocation(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def json(self):
        return json.dumps(self.dict())

class DoubanUser(db.Model):
    user = db.UserProperty(required=True, auto_current_user_add=True)
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
    create_time = db.DateTimeProperty(auto_now_add=True)
    lastupdate_time = db.DateTimeProperty(auto_now=True)

    def dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'location': self.location.dict(),
            'signature': self.signature,
            'content': self.content,
            'page': self.page,
            'homepage': self.homepage,
            'icon': self.icon,
            'uri': self.uri
        }

    def json(self):
        return json.dumps(self.dict())

    @staticmethod
    def find(self, user=users.get_current_user()):
        payload = memcache.get(user.email())

        if payload:
            cached_user = json.loads(payload)
            douban_users = cached_user.get('douban', None)
        else:
            cached_user = {}
            douban_users = None

        if douban_users is None:
            douban_users = DoubanUser.all().filter('user =', user)

            cached_user['douban'] = [user.dict() for user in douban_users]

            memcache.set(user.email(), json.dumps(cached_user))

        return douban_users