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
        # TODO How to handle different languages
        # TODO Should stopwords be in base class?
        # Stopwords sourced from here: http://jmlr.csail.mit.edu/papers/volume5/lewis04a/a11-smart-stop-list/english.stop
        stopwords_file = "en_stopwords.txt"
        try:
            with open(stopwords_file, "r") as f:
                self.stopwords = frozenset(line.strip() for line in f)
        except IOError:
            print "File " + stopwords_file + " does not exist."
            
        
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
        if len(language) > 2: # If > 2, then probably a locale
            language = language[:2]
        # if word in self.stopwords[language]:
        if word in self.stopwords:
            return True
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
        if len(item) > 0 and str(item).startswith(("http", "https")):
            return True
        return False
    
    # TODO Is it more efficient to move the variables outside?
    # TODO Is translate efficient here?
    def clean_text(self, to_clean, clean_to=None):
        not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
        translate_table = dict((ord(char), clean_to) for char in not_letters_or_digits)
        # Trim non-chars from the start
        while len(to_clean) > 0:
            if len(to_clean[:1].translate(translate_table)) == 0:
                to_clean = to_clean[1:]
            else:
                break
        # Trim non-chars from the end
        while len(to_clean) > 0:
            end = len(to_clean)
            if len(to_clean[end-1:].translate(translate_table)) == 0:
                to_clean = to_clean[:end-1]
            else:
                break
        return to_clean
    
    def is_symbol(self, item):
        # This includes basic smiley faces
        if len(self.clean_text(item)) == 0:
            return True
        return False
    
class TopWordsProcessor(PostsProcessor):

    def is_valid(self, word, locale):
        if self.is_stopword(self.clean_text(word), locale):
            return False
        if len(word) == 0:
            return False
        if self.is_hashtag(word):
            return False
        if self.is_mention(word):
            return False
        if self.is_symbol(word):
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
                if not self.is_valid(word, post["user"]["locale"]):
                    continue
                else:
                    self.add_item(self.clean_text(word))
                
    
class TopMentionsProcessor(PostsProcessor):
    pass

class TopHashtagsProcessor(PostsProcessor):
    pass

class TopLinksProcessor(PostsProcessor):
    pass
                

                

            
                
            
            
