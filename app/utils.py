# coding=utf-8

import re

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

# I should use serialization here...
def updates_to_json(updates):
    json = '['
    
    for counter, update in enumerate(updates):
        json += '{"content": "%s", "date": "%s", "source": "%s", "source_url": "%s", "description": "%s"}' % (update.content.replace('"', '\\"'), update.date.isoformat(), update.source, find_source_url(update.source), remove_html_tags(update.description).replace('"', '\\"').strip())
        
        if counter < len(updates) - 1:
            json += ','
            
    json += ']'
    
    return json

def find_source_url(source):
    if source == "וואלה!":
        return "http://www.walla.co.il"
    elif source == "ynet":
        return "http://www.ynet.co.il"
    elif source == "nrg":
        return "http://www.nrg.co.il"
    elif source == "mako":
        return "http://www.mako.co.il"
    
def force_unicode(string):
    if type(string) == unicode:
        return string
    return string.decode('utf-8')