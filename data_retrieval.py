'''
Created on Mar 2, 2013

@author: adam
'''

import json
from google.appengine.api import urlfetch

class DataRetriever:
    def __init__(self, processors):
        self.processors = processors
        self.prev_max_post_id = 0
        self.POST_COUNT = 200
        
    def get_latest_url(self, post_id):
        url = ["https://alpha-api.app.net/stream/0/posts/stream/global?since_id="]
        url.append(`post_id`)
        url.append("&count=")
        url.append(`self.POST_COUNT`)
        return ''.join(url)
        
    def retrieve_latest_data(self):
        url = self.get_latest_url(self.prev_max_post_id)
        response = urlfetch.fetch(url)
        if not response.status_code == 200:
            # TODO Can log errors here - result["meta"]["error_message"]
            # Ignoring all non-200 is pretty basic handling.
            # See http://developers.app.net/docs/basics/responses/#error-conditions
            return
        result = json.loads(response.content)
        if result.has_key("data"):
            posts = result["data"]
            if len(posts) == 0:
                return
            new_max_post_id = int(result["meta"]["max_id"])
            self.update_prev_max_post_id(new_max_post_id)
            for processor in self.processors:
                processor.process_posts(posts)
            
    def update_prev_max_post_id(self, post_id):
        if post_id > self.prev_max_post_id:
            self.prev_max_post_id = post_id
