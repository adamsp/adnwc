import web
from posts_processing import TopWordsProcessor
from data_retrieval import DataRetriever
from threading import Timer
from datetime import datetime
from data_upload import DataUploader

posts_processor = TopWordsProcessor(50)

processors = [posts_processor]

data_retriever = DataRetriever(processors)

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/wc', 'wordcount'
)

update_interval = 3.0
current_date = datetime.utcnow()    

class index:
    def GET(self):
        raise web.seeother('/static/index.html')

class wordcount:
    def GET(self):
        return str(posts_processor.get_top_items_json())

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

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

update_data()
