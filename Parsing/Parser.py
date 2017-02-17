
from __future__ import division
import nltk, sys, validators, os
from pprint import pprint
from collections import defaultdict
# from Topic_Candidate import Topic_Candidate
from Topic import Topic_Candidate

class Parser():
    """
    This class stores the static methods to interpret topic candidates from zero or more bodies of text.
    The work that accomplishes this is in the method parse_topics
    Structured_topic returns a structured topic instance.
    is_structured returns a true if input data is structured, else false.
    """

    @staticmethod
    def structured_topic(self):
        pass

    @staticmethod
    def parse_topics(*kargs):
        """
        Used for parsing topic candidates, form conjunctive crucial words, that are of the Noun persuasion.
        These instances of topic candidate that are returned will be used in the database as topics for relation creation

        `kargs` - the params (in the form zero or more) raw bodies of text to be processed
        `yield` topic candidates - the generated collection of topics that have been extracted and constructed
        """
        for body_of_text in kargs:
            processed = info_extract_preprocess(body_of_text)   # preprocessed body for tagged words in sentence form
            labels, counts = _get_continuous_chunks(processed)
            for label in labels.keys():
                for title in labels[label]:
                    strength = counts[title]
                    yield Topic_Candidate(title, strength, label)

    @staticmethod
    def parse_topics_not_nouns(n=5, pos=('JJ', 'VB'), *kargs):
        """
        Method used for parsing topics that are not conjunctive noun words

        `n` - the limiting value that represents the minimum requirement, that is the number of times the word appears in the text, to qualify it as a topic
        ``pos` - the un-mutable set that is the parts of speech desired as traits of sought after topics. NOTE supports nouns (NN) as well, but is not preferred algorithm to do so, see parse_topics.
        `kargs` - the params (in the form zero or more) raw bodies of text to be processed
        `yield` topic candidates - the generated collection of topics that have been extracted and constructed
        """
        for general_pos in pos:
            for body_of_text in kargs:
                tokenized = nltk.word_tokenize(body_of_text)
                tagged = nltk.pos_tag(tokenized)
                tagdict = findtags(general_pos, tagged, n)
                for specific_pos, list_topic_titles in tagdict.iteritems():
                    for title, strength in list_topic_titles:
                        yield Topic_Candidate(title, strength, specific_pos)

    @staticmethod
    def is_structured(data):
        """
        TODO

        :param data:
        :return:
        """
        return data is None

def _get_continuous_chunks(tagged):
    """
    This method return the dictionaries of critical words in the pre-processed text, tagged, that store info to be used by the graph database.
    The labels dictionary stores as a key the label to be given to the associated topic values. That is to say the key is the predisposed classification of the word when examined contextually by the nltk.ne_chunk(...)
    the counts dictionary stores as a key the title of the topic to be created and the value is the associated number of appearances throughout tagged.

    `tagged` - the pre-processed, sentence delimited, tokenized, tagged, body of text
    `return` labels, counts - the affiliated labels and count of appearances for likely topics
    """
    labels = defaultdict(set) # the dictionary of labels whose values are associated sets of topics
    counts =  defaultdict(int)  # the dictionary of topics whose value is the count of appearances in the entire body of text
    for sentence in tagged:
        # used default named entity chunk grammar, TODO research grammar as replacement
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

def _process_input(input):

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

def lemmatize_words(*set):
    from nltk.stem import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    return [wordnet_lemmatizer.lemmatize(word) for word in set]

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
    body = _process_input('http://www.foxnews.com/politics/2017/02/08/white-house-fires-back-at-immigration-order-critics-with-list-terror-arrests.html')
    tokenized = nltk.word_tokenize(body)
    tagged = nltk.pos_tag(tokenized)
    gen = generate_frequency_by_pos(tagged=tagged, pos=('JJ', 'VB'))
    from nltk.stem import WordNetLemmatizer
    wordnet_lemmatizer = WordNetLemmatizer()
    for elem in gen:
        print elem[0],
        for title, strength in elem[1]:
            print title, wordnet_lemmatizer.lemmatize(title), ',',
        print

def main():
    # demo usage in context
    body =_process_input(
        'http://www.foxnews.com/us/2017/02/10/marine-vet-speaks-out-about-viral-video-supporting-trump-travel-ban.html')

    gen = Parser.parse_topics(body)
    for topic in gen:
        print topic, ', ',
    print

    gen = Parser.parse_topics_not_nouns(5, ('JJ', 'VB'), body)
    for topic in gen:
        try:
            print topic, ', ',
        except UnicodeEncodeError as e:
            pass
    print

if __name__ == '__main__':
    d_bug = 0
    if d_bug:
        debug()
    else:
        main()
    sys.exit(0)




