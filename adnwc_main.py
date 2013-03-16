'''
Created on Mar 16, 2013

@author: Adam Speakman
@contact: http://github.com/adamsp
@contact: http://speakman.net.nz
@license: http://www.apache.org/licenses/LICENSE-2.0.html
'''
import web
from google.appengine.api import memcache

urls = (
    '/', 'index',
    '/wc', 'wordcount',
    '/mentions', 'mentions',
    '/hashtags', 'hashtags',
    '/links', 'links'
)

app = web.application(urls, globals())
error_message = u'Something went wrong.'    

class index:
    def GET(self):
        raise web.seeother('/static/index.html')

class wordcount:
    def GET(self):
        result = memcache.get('wordcount')
        return error_message if result == None else result
    
class mentions:
    def GET(self):
        result = memcache.get('mentions')
        return error_message if result == None else result
    
class hashtags:
    def GET(self):
        result = memcache.get('hashtags')
        return error_message if result == None else result
    
class links:
    def GET(self):
        result = memcache.get('links')
        return error_message if result == None else result

app = app.gaerun()

