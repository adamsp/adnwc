import web
import posts_processing
from data_retrieval import DataRetriever
from threading import Timer
from datetime import datetime
from data_upload import DataUploader

posts_processor = posts_processing.TopWordsProcessor(50)
mentions_processor = posts_processing.TopMentionsProcessor(30)
hashtags_processor = posts_processing.TopHashtagsProcessor(30)
links_processor = posts_processing.TopLinksProcessor(20)

processors = [posts_processor, mentions_processor, 
              hashtags_processor, links_processor]

data_retriever = DataRetriever(processors)

urls = (
    '/', 'index',
    '/wc', 'wordcount',
    '/mentions', 'mentions',
    '/hashtags', 'hashtags',
    '/links', 'links'
)

app = web.application(urls, globals())

update_interval = 3.0
current_date = datetime.utcnow()    

class index:
    def GET(self):
        raise web.seeother('/static/index.html')

class wordcount:
    def GET(self):
        return str(posts_processor.get_top_items_json())
    
class mentions:
    def GET(self):
        return str(mentions_processor.get_top_items_json())
    
class hashtags:
    def GET(self):
        return str(hashtags_processor.get_top_items_json())
    
class links:
    def GET(self):
        return str(links_processor.get_top_items_json())

def update_data():
    new_date = datetime.utcnow()
    global current_date
    if not new_date.day == current_date.day:
        data_uploader = DataUploader()
        for processor in processors:
            processor.save_data(current_date, data_uploader)
            processor.clear_data()
        current_date = new_date
    data_retriever.retrieve_latest_data()
    Timer(update_interval, update_data).start()

app = app.gaerun()
update_data()
