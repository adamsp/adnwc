import web
from posts_processing import TopWordsProcessor
from data_retrieval import DataRetriever

posts_processor = TopWordsProcessor(50)

data_retriever = DataRetriever([posts_processor])

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/wc', 'wordcount'
)

class index:
    def GET(self):
        return render.index()

class wordcount:
    def GET(self):
        # TODO This should be automatic on a timer
        data_retriever.retrieve_latest_data()
        return str(posts_processor.get_top_items_json())

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    
#wc = wordcount()
#wc.GET()
