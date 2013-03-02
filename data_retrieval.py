'''
Created on Mar 2, 2013

@author: adam
'''

import json
import urllib

class DataRetriever:
    def __init__(self, processors):
        self.processors = processors
        self.prev_max_post_id = 0
        self.POST_COUNT = 200
        
    def retrieve_latest_data(self):
        # TODO Need to take into account API failure, rate limiting, etc.
        url = "https://alpha-api.app.net/stream/0/posts/stream/global"
        url += "?" + str(self.prev_max_post_id) + "&" + str(self.POST_COUNT)
        result = json.load(urllib.urlopen(url))
        if result.has_key("data"):
            posts = result["data"]
            self.update_prev_max_post_id(posts)
            for processor in self.processors:
                processor.process_posts(posts)
                
    def update_prev_max_post_id(self, posts):
        if len(posts) == 0:
                return;
        if posts[0].has_key("id"):
            post_id = posts[0]["id"]
            if post_id > self.prev_max_post_id:
                self.prev_max_post_id = post_id
