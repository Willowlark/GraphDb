
from __future__ import division
import nltk, sys, validators, os, operator
from pprint import pprint
from Topic import Topic
from collections import defaultdict

class Parser():

    def structured_topic(self):
        pass

    @staticmethod
    def parse_topics(body):
        processed = info_extract_preprocess(body)
        return get_continuous_chunks(processed)

    def is_structured(self):
        return 0

def process_input(input):

    def process_string(string):
        text = string.strip()
        return text

    def process_url(url):
        import urllib
        from bs4 import BeautifulSoup
        html = urllib.urlopen(url).read()
        text = BeautifulSoup(html, "lxml")
        text = text.find("div", {"class" : "article-text"})
        text = text.get_text()
        return text

    def process_file(file):
        text = get_text(file)
        text = text.strip()
        return text

    def get_text(file):
        import re

        """Read text from a file, normalizing whitespace and stripping HTML markup."""
        text = open(file).read()
        text = re.sub(r'<.*?>', ' ', text)
        text = re.sub('\s+', ' ', text)
        return text

    if validators.url(input):
        return process_url(input)
    elif os.path.exists(input):
        return process_file(input)
    else:
        return process_string(input)

def findtags(tag_prefix, tagged_text, n):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].most_common(n)) for tag in cfd.conditions())

def generate_frequency_by_pos(tagged, pos=('JJ', 'VB', 'NN'), n=5):
    for _pos in pos:
        tagdict = findtags(_pos, tagged, n=n)
        for tag in sorted(tagdict):
            yield (tag, tagdict[tag])

def info_extract_preprocess(document):
   sentences = nltk.sent_tokenize(document) #tokenize sentence into sentences
   tokenized = [nltk.word_tokenize(sent) for sent in sentences] # tokenize sentences in sentences
   tagged = [nltk.pos_tag(sent) for sent in tokenized] # tag the sentences in tokenized
   return tagged

def lemmatize_words(set):
    from nltk.stem import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    return [wordnet_lemmatizer.lemmatize(word) for word in set]

def get_continuous_chunks(tagged):
    labels = defaultdict(set) # the dictionary of labels whose values are associated sets of topics
    counts =  defaultdict(int)  # the dictionary of topics whose value is the count of appearances in the entire body of text
    for sentence in tagged:
        # used default named entity chunk grammar
        chunked = nltk.ne_chunk(sentence, binary=False)
        continuous_chunk, current_chunk = [], []
        for i in chunked:
            if type(i) == nltk.Tree:
                token = " ".join([token for token, pos in i.leaves()]) # the key word to be used as the likely topic
                label = str(i).split(' ')[0][1:] # get the key that is the label of the named entity
                labels[label].add(token)
                current_chunk.append(token)
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                counts[named_entity] += 1
                continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue
    return labels, counts

def debug():
    """
    General flow
        i.      process input as file, url or raw text into body
        ii.     get tokens of body into tokens
        iii.    get part of speech tags into tagged
        iv.     developed strongest accuracy for classifier of tags
        iv.     generate the top strongest words for topics
        /v.      yield the top hits of proper conjunctive nouns
    """
    body = process_input('http://www.foxnews.com/politics/2017/02/08/white-house-fires-back-at-immigration-order-critics-with-list-terror-arrests.html')
    tokenized = nltk.word_tokenize(body)
    tagged = nltk.pos_tag(tokenized)
    gen = generate_frequency_by_pos(tagged=tagged, pos=('JJ'))
    dict = {}
    for elem in gen:
        dict[elem[0]] = elem[1]
    pprint(dict)

if __name__ == '__main__':
    d_bug = 1
    if d_bug:
        debug()
    else:
        # demo usage in context
        body = process_input('http://www.foxnews.com/us/2017/02/10/marine-vet-speaks-out-about-viral-video-supporting-trump-travel-ban.html')
        labels, counts = Parser.parse_topics(body)
        for key in labels.keys():
            print key
            for ne in labels[key]:
                print "\t", ne, counts[ne]
    sys.exit(0)




