'''
Created on Mar 16, 2013

@author: Adam Speakman
@contact: http://github.com/adamsp
@contact: http://speakman.net.nz
@license: http://www.apache.org/licenses/LICENSE-2.0.html
'''        
import web
import posts_processing
from data_upload import DataUploader
from datetime import datetime
from data_retrieval import DataRetriever

posts_processor = posts_processing.TopWordsProcessor(50, 'wordcount')
mentions_processor = posts_processing.TopMentionsProcessor(30, 'mentions')
hashtags_processor = posts_processing.TopHashtagsProcessor(30, 'hashtags')
links_processor = posts_processing.TopLinksProcessor(20, 'links')

processors = [posts_processor, mentions_processor, 
              hashtags_processor, links_processor]

data_retriever = DataRetriever(processors)

urls = (
    '/', 'index',
    '/wc', 'wordcount',
    '/mentions', 'mentions',
    '/hashtags', 'hashtags',
    '/links', 'links',
    '/update', 'update'
)

app = web.application(urls, globals())    
current_date = datetime.utcnow() 

class index:
    def GET(self):
        raise web.seeother('/static/index.html')

class wordcount:
    def GET(self):
        return posts_processor.get_json()
    
class mentions:
    def GET(self):
        return mentions_processor.get_json()
    
class hashtags:
    def GET(self):
        return hashtags_processor.get_json()
    
class links:
    def GET(self):
        return links_processor.get_json()
        
class update:
    def GET(self):
        new_date = datetime.utcnow()
        global current_date
        if not new_date.day == current_date.day:
            data_uploader = DataUploader()
            for processor in processors:
                processor.save_data(current_date, data_uploader)
                processor.clear_data()
            current_date = new_date
        data_retriever.retrieve_latest_data()
        return ''

app = app.gaerun()
update().GET()

