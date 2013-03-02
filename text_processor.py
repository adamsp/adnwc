'''
Created on 2/03/2013

@author: Adam
'''
import operator
import json
import urllib

class TopWords:
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
        
def fetch_new_msgs(prev_max_msg, message_count):
    # TODO Need to take into account API failure, rate limiting, etc.
    url = "https://alpha-api.app.net/stream/0/posts/stream/global"
    url += "?" + str(prev_max_msg) + "&" + str(message_count)
    msgs = json.load(urllib.urlopen(url))
    return msgs["data"]

def is_stopword(word, language):
    # TODO
    return False

def is_valid(word, language):
    if is_stopword(word, language):
        return False
    if len(word) > 0 and word[0] == "@" or word[0] == "#":
        return False
    return True

class TextProcessor:
    def __init__(self, message_count):
        self.message_count = message_count 
        self.MAX_WORDS = 25
        self.wordcount = {}
        self.top_words = TopWords(self.MAX_WORDS)
        self.prev_max_msg = 0

    def get_top_words(self):
        count = 0

        while count < 3:
            count += 1
            new_msgs = fetch_new_msgs(self.prev_max_msg, self.message_count)
            for msg in new_msgs:
                for word in msg["text"].lower().split():
                    if not is_valid(word, msg["user"]["locale"]):
                        continue
                    if self.wordcount.has_key(word):
                        self.wordcount[word] += 1
                    else:
                        self.wordcount[word] = 1
                    self.top_words.add_word(word, self.wordcount[word])
        return json.dumps(self.top_words.sorted_vals)
                

                

            
                
            
            
