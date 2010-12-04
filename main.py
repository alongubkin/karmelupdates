import wsgiref.handlers

from google.appengine.ext import webapp
from app.views import *

application = webapp.WSGIApplication([
    ('/', IndexHandler),
    ('/updates', UpdateHandler),
    ('/tasks/updatedb', CronHandler)
], debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(application)
