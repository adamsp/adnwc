'''
Created on Mar 16, 2013

@author: Adam Speakman
@contact: http://github.com/adamsp
@contact: http://speakman.net.nz
@license: http://www.apache.org/licenses/LICENSE-2.0.html
'''
import posts_processing
import web
import logging
import time
from data_retrieval import DataRetriever
from datetime import datetime
from data_upload import DataUploader
from google.appengine.api import background_thread
from google.appengine.api import runtime

posts_processor = posts_processing.TopWordsProcessor(50, 'wordcount')
mentions_processor = posts_processing.TopMentionsProcessor(30, 'mentions')
hashtags_processor = posts_processing.TopHashtagsProcessor(30, 'hashtags')
links_processor = posts_processing.TopLinksProcessor(20, 'links')

processors = [posts_processor, mentions_processor, 
              hashtags_processor, links_processor]

data_retriever = DataRetriever(processors)

# Update every 3 seconds for 20 updates a minute. Max is 50.
update_interval = 3.0
current_date = datetime.utcnow()

# We don't handle any requests - will return a 404.
# This is OK, as GAE treats a 404 as succesful startup.
# All our data gets saved to memcache, and the frontend pulls from there.
urls = ()

app = web.application(urls, globals())

def save_processor_data():
    logging.info('Saving data at ' + str(datetime.utcnow()))
    data_uploader = DataUploader()
    for processor in processors:
        processor.save_data(current_date, data_uploader)
        processor.clear_data()

def update_data():
    logging.info('Backend instance has started.')
    while True and not runtime.is_shutting_down():
        new_date = datetime.utcnow()
        global current_date
        if not new_date.day == current_date.day:
            save_processor_data()
            current_date = new_date
        data_retriever.retrieve_latest_data()
        time.sleep(update_interval)
    logging.info('Backend instance is shutting down.')
    save_processor_data();
    
app = app.gaerun()
background_thread.start_new_background_thread(update_data, [])