'''
Created on Mar 2, 2013

@author: adam
'''

import json
import urllib
from contextlib import closing

class DataRetriever:
    def __init__(self, processors):
        self.processors = processors
        self.prev_max_post_id = 0
        self.POST_COUNT = 200
        
    def retrieve_latest_data(self):
        url = "https://alpha-api.app.net/stream/0/posts/stream/global"
        url += "?" + str(self.prev_max_post_id) + "&" + str(self.POST_COUNT)
        
        # urllib doesn't actually support the 'with' statement:
        # http://echochamber.me/viewtopic.php?f=11&t=26328&view=next#p819708
        # See 'closing':
        # http://docs.python.org/2/library/contextlib.html
        with closing(urllib.urlopen(url)) as openurl:
            if not openurl.code == 200:
                # TODO Can log errors here - result["meta"]["error_message"]
                # Ignoring all non-200 is pretty basic handling.
                # See http://developers.app.net/docs/basics/responses/#error-conditions
                return
            try:
                result = json.load(openurl)
                if result.has_key("data"):
                    posts = result["data"]
                    self.update_prev_max_post_id(posts)
                    for processor in self.processors:
                        processor.process_posts(posts)
            except ValueError as e:
                # TODO Since we're checking response code, do we need try block?
                print e
                return
            
    def update_prev_max_post_id(self, posts):
        if len(posts) == 0:
                return;
        if posts[0].has_key("id"):
            post_id = posts[0]["id"]
            if post_id > self.prev_max_post_id:
                self.prev_max_post_id = post_id
