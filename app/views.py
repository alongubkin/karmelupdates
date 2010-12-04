# coding=utf-8

import os
import datetime
import time
import utils
import random
import feedparser

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api.channel import channel

from models import *

clients = []

class IndexHandler(webapp.RequestHandler):
    def get(self):         
        self.response.headers['Content-Type'] = 'text/html'
        
        client_id = str(random.random())
        clients.append(client_id)
        
        path = os.path.join(os.path.dirname(__file__) + '/../templates/', 'index.html')
        self.response.out.write(template.render(path, {"token": channel.create_channel(client_id)}))
                    
class UpdateHandler(webapp.RequestHandler):
    def get(self):
        
        count = 20
        updates = Update.all().order("-date").fetch(count, int(self.request.get("page")) * count)
        
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8' 
        self.response.out.write(utils.updates_to_json(updates))
    
class CronHandler(webapp.RequestHandler):
    def get(self): # every 1 minute
        feeds = {"nrg": "http://rss.nrg.co.il/newsflash/",
                 "וואלה!": "http://rss.walla.co.il/?w=/1/22/0/@rss",
                 "ynet": "http://www.ynet.co.il/Integration/StoryRss1854.xml",
                 "mako": "http://rcs.mako.co.il/rss/news-israel.xml"}
        
        updates = []

        for name, url in feeds.iteritems():
            for entry in feedparser.parse(url).entries:
                if Update.get_by_key_name(entry.title) is None:
                    entry = Update(key_name=entry.title, 
                           content=utils.force_unicode(entry.title), 
                           date=datetime.datetime.fromtimestamp(time.mktime(entry.date_parsed)),
                           source=utils.force_unicode(name),
                           description=utils.force_unicode(entry.description));
                           
                    entry.put()
                    updates.append(entry)
        
        updates.sort(key=lambda item:item.date, reverse=True)
        
        for client_id in clients:
            try:
                channel.send_message(client_id, utils.updates_to_json(updates))
            except:
                clients.remove(client_id)