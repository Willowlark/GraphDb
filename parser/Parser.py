
from __future__ import division
import nltk, sys, validators, os
from pprint import pprint
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from Topic import Topic

class Parser():

    def structured_topic(self):
        pass

    @staticmethod
    def parse_topics(body):
        processed = ie_preprocess(body)
        return get_continuous_chunks(processed)

    def is_structured(self):
        return 0

def process_input(input):

    def process_string(string):
        text = string.decode('utf-8').strip()
        return text

    def process_url(url):
        import urllib
        from bs4 import BeautifulSoup
        html = urllib.urlopen(url).read().decode('utf8')
        text = BeautifulSoup(html, "lxml")
        text = text.find("div", {"class" : "article-text"})
        text = text.get_text()
        return text

    def process_file(file):
        text = get_text(file)
        text = text.decode('utf-8').strip()
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

def generate_frequency_by_pos(tagged, pos=('NN'), n=15):
    for _pos in pos:
        tagdict = findtags(_pos, tagged, n=n)
        for tag in sorted(tagdict):
            yield (tag, tagdict[tag])

def ie_preprocess(document):
   sentences = nltk.sent_tokenize(document)
   tokenized = [nltk.word_tokenize(sent) for sent in sentences]
   tagged = [nltk.pos_tag(sent) for sent in tokenized]
   return tagged

def get_continuous_chunks(tagged):
    ret_set = set()
    for sentence in tagged:
        # chunk_rule = ChunkRule("<.*>+", "Chunk everything")
        # chink_rule = ChinkRule("<VBD|IN|\.>", "Chink on verbs/prepositions")
        # split_rule = SplitRule("<DT><NN>", "<DT><NN>", "Split successive determiner/noun pairs")
        # chunk_parser = RegexpChunkParser([chunk_rule, chink_rule, split_rule],chunk_label='NP')
        # chunked = chunk_parser.parse(sentence)
        chunked = nltk.ne_chunk(sentence, binary=True)
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            if type(i) == nltk.Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_topic = Topic(" ".join(current_chunk))
                if named_topic not in continuous_chunk:
                    continuous_chunk.append(named_topic)
                    current_chunk = []
            else:
                continue
        ret_set |= set(continuous_chunk)
    return ret_set

def main():
    """
    General flow
        i.      process input as file, url or raw text into body
        ii.     get tokens of body into tokens
        iii.    get part of speech tags into tagged
        iv.     developed strongest accuracy for classifier of tags
        iv.     generate the top strongest words for topics
        /v.      yield the top hits of proper conjunctive nouns
    """

    # body = process_input('C:\Users\Bob S\PycharmProjects\my_nltk\work\GraphDatabaseEvaluationandImplementationCon-ops.docx.txt')
    body = process_input('http://www.foxnews.com/politics/2017/02/08/white-house-fires-back-at-immigration-order-critics-with-list-terror-arrests.html')

    tokenized = nltk.word_tokenize(body)

    # normalize text here
    text = nltk.Text(tokenized)
    # print text.similar('News')
    # print text.common_contexts(words=['News'])
    # print text.concordance('News')

    tagged = nltk.pos_tag(tokenized)
    """TODO Improve tagging methods for superior analyzation of hot words"""

    # print '-' * 100
    # tag_insight(tagged)
    # print '-' * 100

    gen = generate_frequency_by_pos(tagged=tagged, n=10, pos=('NN', 'JJ', 'VB'))

    dict = {}
    for elem in gen:
        dict[elem[0]] = elem[1]
    pprint(dict)

if __name__ == '__main__':
    debug = 0
    if debug:
        main()
    else:
        # demo usage in context
        body = process_input('http://www.foxnews.com/us/2017/02/10/marine-vet-speaks-out-about-viral-video-supporting-trump-travel-ban.html')
        topics = Parser.parse_topics(body)
        pprint(topics)
    sys.exit(0)




