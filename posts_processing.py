'''
Created on 2/03/2013

@author: Adam
'''
import operator
import json
import codecs
import unicodedata

class TopItems:
    def __init__(self, max_words):
        self.max_words = max_words
        self.lowest_count = -1
        self.lowest_word = ""
        self.words = {}
        self.sorted_vals = []
        
    def add_word(self, word, count):
        if count > self.lowest_count or not self.is_full():
            if self.is_full():
                self.words.pop(self.lowest_word, "");
            self.words[word] = count
            self.update_lowest_count();
            
    def is_full(self):
        return len(self.sorted_vals) == self.max_words;

    def update_lowest_count(self):
        self.sorted_vals = sorted(self.words.items(), key=operator.itemgetter(1), reverse=True)
        sorted_length = len(self.sorted_vals)
        self.lowest_word = self.sorted_vals[sorted_length - 1][0]
        self.lowest_count = self.sorted_vals[sorted_length - 1][1]

class PostsProcessor:
    def __init__(self, max_items): 
        self.MAX_ITEMS = max_items
        self.itemcount = {}
        self.top_items = TopItems(self.MAX_ITEMS)
        
    def process_posts(self, posts):
        # Do nothing in base class
        return
    
    def add_item(self, item):
        if self.itemcount.has_key(item):
            self.itemcount[item] += 1
        else:
            self.itemcount[item] = 1
        self.top_items.add_word(item, self.itemcount[item])
        
    def get_top_items_json(self):
        return json.dumps(self.top_items.sorted_vals)
    
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
    def __init__(self, max_words, stopwords_file=None):
        PostsProcessor.__init__(self, max_words)
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
                
    
class TopMentionsProcessor(PostsProcessor):
    pass

class TopHashtagsProcessor(PostsProcessor):
    pass

class TopLinksProcessor(PostsProcessor):
    pass
                

                

            
                
            
            
