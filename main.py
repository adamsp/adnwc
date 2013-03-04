import web
from posts_processing import TopWordsProcessor
from data_retrieval import DataRetriever
from threading import Timer

posts_processor = TopWordsProcessor(50)

data_retriever = DataRetriever([posts_processor])

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/wc', 'wordcount'
)

update_interval = 3.0

class index:
    def GET(self):
        raise web.seeother('/static/index.html')

class wordcount:
    def GET(self):
        # TODO This should be automatic on a timer
        return str(posts_processor.get_top_items_json())
    
def update_data():
    Timer(update_interval, update_data).start()   
    data_retriever.retrieve_latest_data()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

update_data()
