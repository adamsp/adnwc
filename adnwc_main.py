'''
Created on Mar 16, 2013

@author: Adam Speakman
@contact: http://github.com/adamsp
@contact: http://speakman.net.nz
@license: http://www.apache.org/licenses/LICENSE-2.0.html
'''        
import web
from google.appengine.api import memcache

class MemcacheError(web.HTTPError):
    def __init__(self):
        status = '500 Internal Server Error'
        headers = {'Content-Type': 'application/json'}
        data = '{ "meta" : { "result" : "fail" } }'
        web.HTTPError.__init__(self, status, headers, data)

urls = (
    '/', 'index',
    '/wc', 'wordcount',
    '/mentions', 'mentions',
    '/hashtags', 'hashtags',
    '/links', 'links'
)

app = web.application(urls, globals())    

class index:
    def GET(self):
        raise web.seeother('/static/index.html')

class wordcount:
    def GET(self):
        result = memcache.get('wordcount')
        if result == None:
            raise MemcacheError()
        else:
            return result
    
class mentions:
    def GET(self):
        result = memcache.get('mentions')
        if result == None:
            raise MemcacheError()
        else:
            return result
    
class hashtags:
    def GET(self):
        result = memcache.get('hashtags')
        if result == None:
            raise MemcacheError()
        else:
            return result
    
class links:
    def GET(self):
        result = memcache.get('links')
        if result == None:
            raise MemcacheError()
        else:
            return result

app = app.gaerun()

