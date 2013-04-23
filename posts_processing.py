'''
Created on 2/03/2013

@author: Adam Speakman
@contact: http://github.com/adamsp
@contact: http://speakman.net.nz
@license: http://www.apache.org/licenses/LICENSE-2.0.html
'''
import operator
import json
import codecs
import unicodedata
from datetime import datetime

class TopItems:
    def __init__(self, max_words):
        self.max_words = max_words
        self.lowest_count = -1
        self.lowest_word = ''
        self.words = {}
        self.sorted_vals = []
        
    def add_word(self, word, count):
        if count > self.lowest_count or not self.is_full():
            if self.is_full() and not self.words.has_key(word):
                del self.words[self.lowest_word]
            self.words[word] = count
            self.update_lowest_count();
            
    def is_full(self):
        return len(self.sorted_vals) == self.max_words;

    def update_lowest_count(self):
        self.sorted_vals = sorted(self.words.items(), key=operator.itemgetter(1), reverse=True)
        sorted_length = len(self.sorted_vals)
        self.lowest_word = self.sorted_vals[sorted_length - 1][0]
        self.lowest_count = self.sorted_vals[sorted_length - 1][1]
        
    def clear_data(self):
        self.lowest_count = -1
        self.lowest_word = ''
        self.words.clear()
        self.sorted_vals = []

class PostsProcessor:
    def __init__(self, max_items, name):
        self.name = name 
        self.MAX_ITEMS = max_items
        self.itemcount = {}
        self.top_items = TopItems(self.MAX_ITEMS)
        self.latest_time = datetime.utcnow()
        
    def save_data(self, data_date, data_uploader):
        data_uploader.save_data(data_date, self.top_items)
        
    def clear_data(self):
        self.top_items.clear_data()
        for item in self.itemcount:
            self.itemcount[item] = 0
        
    def process_posts(self, posts):
        # Do nothing in base class
        return
    
    def add_item(self, item):
        if self.itemcount.has_key(item):
            self.itemcount[item] += 1
        else:
            self.itemcount[item] = 1
        self.top_items.add_word(item, self.itemcount[item])
        
    def get_top_items(self):
        return self.top_items.sorted_vals
    
    def get_json(self):
        return json.dumps(dict(meta=dict(time=str(self.latest_time),
                                                        result='success',
                                                        content=self.name), 
                                                data=self.get_top_items()))
    
    def is_mention(self, item):
        if len(item) > 0 and item[0] == "@":
            return True
        return False
    
    def is_hashtag(self, item):
        if len(item) > 0 and item[0] == "#":
            return True
        return False
    
    def is_link(self, item):
        if len(item) > 0 and item.startswith(("http", "https")):
            return True
        return False
    
    def clean_text(self, to_clean):
        # Trim non-chars (Punctuation - P, Symbols - S) from the start
        while len(to_clean) > 0:
            if unicodedata.category(to_clean[:1]).startswith(('P', 'S')):
                to_clean = to_clean[1:]
            else:
                break
        # Trim non-chars from the end
        while len(to_clean) > 0:
            end = len(to_clean)
            if unicodedata.category(to_clean[end-1:]).startswith(('P', 'S')):
                to_clean = to_clean[:end-1]
            else:
                break
            
        if len(to_clean) > 0:
            # FIXME Probably preferable/faster to just include "i\u2019m" etc in stopwords file.
            # There appears to be a lot of input using \u2019 instead of ASCII apostrophe.
            if to_clean.find(u'\u2019') > -1:
                to_clean = to_clean.replace(u'\u2019', "'")
        return to_clean
    
class TopWordsProcessor(PostsProcessor):
    def __init__(self, max_words, name, stopwords_file=None):
        PostsProcessor.__init__(self, max_words, name)
        # TODO How to handle different languages
        # Stopwords sourced from here: http://jmlr.csail.mit.edu/papers/volume5/lewis04a/a11-smart-stop-list/english.stop
        # Also the long-list from here: http://www.ranks.nl/resources/stopwords.html
        if stopwords_file == None:
            stopwords_file = "en_stopwords.txt"
        try:
            with codecs.open(stopwords_file, mode='r', encoding='utf-8') as f:
                self.stopwords = frozenset(line.strip() for line in f)
        except IOError:
            print "File " + stopwords_file + " does not exist."
            self.stopwords = ()
            
    def is_stopword(self, word):
        if word in self.stopwords:
            return True
        return False

    def is_valid(self, word, cleaned_word):
        if len(cleaned_word) == 0:
            return False
        if len(word) == 0:
            return False
        if self.is_stopword(cleaned_word):
            return False
        if self.is_hashtag(word):
            return False
        if self.is_mention(word):
            return False
        if self.is_link(word):
            return False
        return True
    
    def is_english(self, locale):
        if len(locale) > 2:
            locale = locale[:2]
        if locale.lower() == "en":
            return True
        return False

    def process_posts(self, posts):
        if len(posts) == 0:
                return;
        for post in posts:
            # It appears some posts don't have text.
            if not post.has_key("text"):
                continue;
            # FIXME Dirty, dirty hack.
            if not self.is_english(post["user"]["locale"]):
                continue
            for word in post["text"].lower().split():
                cleaned_word = self.clean_text(word)
                if not self.is_valid(word, cleaned_word):
                    continue
                else:
                    self.add_item(cleaned_word)
        self.latest_time = datetime.utcnow()
                
    
class TopMentionsProcessor(PostsProcessor):
    def process_posts(self, posts):
        if len(posts) == 0:
                return;
        for post in posts:
            for mention in post["entities"]["mentions"]:
                self.add_item(mention["name"].lower())
        self.latest_time = datetime.utcnow()

class TopHashtagsProcessor(PostsProcessor):
    def process_posts(self, posts):
        if len(posts) == 0:
                return;
        for post in posts:
            for tag in post["entities"]["hashtags"]:
                self.add_item(tag["name"].lower())
        self.latest_time = datetime.utcnow()

class TopLinksProcessor(PostsProcessor):
    # Standardise all links - so bit.ly/abcd/ matches bit.ly/abcd
    def standardise_link(self, link):
        length = len(link)
        if length > 0:
            if link[length-1:] == u'/':
                link = link[:length-1]
        return link
    
    def process_posts(self, posts):
        if len(posts) == 0:
                return;
        for post in posts:
            for link in post["entities"]["links"]:
                url = self.standardise_link(link["url"])
                self.add_item(url)
        self.latest_time = datetime.utcnow()
                

                

            
                
            
            
