'''
Created on 2/03/2013

@author: Adam
'''
import operator
import json

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
    
    def is_stopword(self, word, language):
        # TODO
        return False
    
    def is_mention(self, item):
        if len(item) > 0 and item[0] == "@":
            return True
        return False
    
    def is_hashtag(self, item):
        if len(item) > 0 and item[0] == "#":
            return True
        return False
    
    def is_link(self, item):
        if len(item) > 0 and str(item).startswith(["http", "https"]):
            return True
        return False
    
class TopWordsProcessor(PostsProcessor):

    def is_valid(self, word, language):
        if self.is_stopword(word, language):
            return False
        if len(word) == 0:
            return False
        if self.is_hashtag(word):
            return False
        if self.is_mention(word):
            return False
        return True

    def process_posts(self, posts):
        if len(posts) == 0:
                return;
        for post in posts:
            for word in post["text"].lower().split():
                if not self.is_valid(word, post["user"]["locale"]):
                    continue
                else:
                    # TODO Clean word of punctuation etc before you add it.
                    self.add_item(word)
                
    
class TopMentionsProcessor(PostsProcessor):
    pass

class TopHashtagsProcessor(PostsProcessor):
    pass

class TopLinksProcessor(PostsProcessor):
    pass
                

                

            
                
            
            
