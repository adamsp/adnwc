'''
Created on Mar 2, 2013

@author: Adam Speakman
@contact: http://github.com/adamsp
@contact: http://speakman.net.nz
@license: http://www.apache.org/licenses/LICENSE-2.0.html
'''

import json
import logging
from google.appengine.api import urlfetch

class DataRetriever:
    def __init__(self, processors):
        self.processors = processors
        self.prev_max_post_id = 0
        self.POST_COUNT = 200
        
    def get_latest_url(self, post_id):
        url = ["https://alpha-api.app.net/stream/0/posts/stream/global"]
        
        # Note we do negative count - returns up to 200 from previous max towards newest.
        # If we do positive count, it counts down from latest post towards the requested
        # 'since' post. Easier to count from the 'since' post towards newest.
        # If first time run though, we just do latest 200.
        if post_id > 0:
            url.append("?since_id=")
            url.append(`post_id`)
            url.append("&count=-")
        else:
            url.append("?count=")
        url.append(`self.POST_COUNT`)
        return ''.join(url)
        
    def retrieve_latest_data(self):
        more_posts = True
        while more_posts:
            url = self.get_latest_url(self.prev_max_post_id)
            response = urlfetch.fetch(url)
            if not response.status_code == 200:
                logging.error('Request failed with status code ' + str(response.status_code)
                              + ' and content: ' + str(response.content))
                return
            result = json.loads(response.content)
            if result.has_key("data"):
                posts = result["data"]
                if len(posts) == 0:
                    return
                for processor in self.processors:
                    processor.process_posts(posts)
            # We want to short-circuit this if this is the first time
            # we've run - otherwise we'll end up scanning *all* ADN posts.
            if self.prev_max_post_id > 0:
                more_posts = result["meta"]["more"]
            else:
                more_posts = False
            self.prev_max_post_id = int(result["meta"]["max_id"])
