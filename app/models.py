from google.appengine.ext import db

class Update(db.Model):
    content = db.StringProperty()
    date = db.DateTimeProperty()
    source = db.StringProperty()
    description = db.TextProperty()