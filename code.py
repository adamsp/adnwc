import web
from text_processor import TextProcessor

text_processor = TextProcessor(200)
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
        return str(text_processor.get_top_words())

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
