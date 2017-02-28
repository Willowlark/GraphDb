from __future__ import division

import os
import unicodedata
import sys
from collections import defaultdict
import validators
import nltk
import json
from markup_parser import markup_parser

class Topic_Candidate(object):
    """
    `Author`: Bill Clark

    A class created by the Parser to represent a Topic object in the graph, in relation
    to the given record. The metadata then, is strictly tied to the record used when
    creating the candidate.
    """

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.__repr__()

    def __init__(self, topic, strength, label):
        self.title = topic
        self.strength = strength
        self.label = label


"""
This file stores the static methods to interpret topic candidates from zero or more bodies of text.
The work that accomplishes this is in the method parse_topics
Structured_topic returns the structured topic instances form the body of the text in the rss feed summary.
is_structured returns a true if input data is structured, else false.
"""

def get_structured_topic(extracted):
    """
    used by external modules to gather the structured topics of the summary of the feed json

    `extracted` the json object of the feed being examined
    `return` the result of the structured topic investigation.
    """
    body_of_text = extracted['summary']
    return _structured_topic(body_of_text)

def get_unstructured_topic(extracted, keys=('id', 'title', 'summary')):
    """
    used by external modules to gather the unstructured topics of the summary of the feed json


    `extracted` the json object of the feed being examined
    `keys` the optional list of args that are the keys of the associative dictionary extracted to have topics extracted
    `return` the set of the unique topic candidate instances to be inserted by RssGrapher 
    """
    ret = set()
    for key in keys:
        ret.update(_parse_topics(extracted[key]))
    return ret

def _structured_topic(body_of_text, try_markup=False):
    """
    This method will render the list of structured topics form the predisposed format of data, a JSON string.

    `kargs` the list of zero or more literal strings to be parsed from the rss feed
    `return` ret, the list of structured topics from the body of text
    """
    if try_markup and not is_structured(body_of_text):
        mkup = markup_parser()
        return mkup.to_json(body_of_text)
    return json.loads(body_of_text)

def _parse_topics(body_of_text):
    """
    Used for parsing topic candidates, form conjunctive crucial words, that are of the Noun persuasion.
    The instances of topic candidate that are returned will be used in the database as units for relation creation

    `kargs` - the params (in the form zero or more) of raw bodies of text to be processed
    `yield` topic candidates - the generated collection of Noun based topics that have been extracted and constructed
    """
    listing = []
    if isinstance(body_of_text, unicode):
        body_of_text = unicodedata.normalize('NFKD', body_of_text).encode('ascii', 'ignore')
    processed = _info_extract_preprocess(body_of_text)   # preprocessed body for tagged words in sentence form
    labels, counts = _get_continuous_chunks_NP(processed)
    for label in labels.keys():
        for title in labels[label]:
            strength = counts[title]
            listing.append(Topic_Candidate(title, strength, label))
    return listing

def _parse_topics_not_nouns(*kargs):
    """
    Method used for parsing topics that are not conjunctive noun words.
    Second to the NP form that is preferred use. Does not produce effective NNPs.
    However, only means to yield the non-nouns words of interest

    `kargs` - the params (in the form zero or more) raw bodies of text to be processed
    `yield` topic candidates - the generated collection of non-Noun topics that have been extracted and constructed
    """
    for body_of_text in kargs:
        processed = _info_extract_preprocess(body_of_text)   # preprocessed body for tagged words in sentence form
        labels, counts = _get_non_NP_chunks(processed)
        for label in labels.keys():
            for title in labels[label]:
                strength = counts[title]
                yield Topic_Candidate(title, strength, label)

def is_structured(data):
    """
    This method determines if the given python string, data, is structured data or not.
    Structured data is information in the format the development team has agreed on using as the format to be used when we not examining raw, unfiltered text.
    This format is JSON.

    `data` the literal string that is passed to be checked
    `return` True if the string can be leaded in JSON format, else False
    """
    try:
        json.loads(data)
    except ValueError:
        return False
    return True

def _info_extract_preprocess(document):
    """
    This method is used to perform the reiterative process of preparing the given body of text to be parsed.
    First the sentences are tokenized using the default method of sent_tokenize(), next, the words are tokenized one by one.
    Finally those words are tagged by the default tagger of pos_tagger()

    `document` the string form body of text to be pre-processed
    `return` tagged - the tokenized, then tagged body of sentence delimited text.
    """
    sentences = nltk.sent_tokenize(document) #tokenize sentence into sentences
    tokenized = [nltk.word_tokenize(sent) for sent in sentences] # tokenize sentences in sentences
    tagged = [nltk.pos_tag(sent) for sent in tokenized] # tag the sentences in tokenized
    return tagged

def _get_continuous_chunks_NP(tagged):
    """
    This method return the dictionaries of critical words in the pre-processed text, tagged, that store info to be used by the graph database.
    The labels dictionary stores as a key the label to be given to the associated topic values. That is to say the key is the predisposed classification of the word when examined contextually by the nltk.ne_chunk(...)
    the counts dictionary stores as a key the title of the topic to be created and the value is the associated number of appearances throughout tagged.

    `tagged` - the pre-processed, sentence delimited, tokenized, tagged, body of text
    `return` labels, counts - the affiliated labels and count of appearances for likely topics
    """
    labels = defaultdict(set) # the dictionary of labels whose values are associated sets of topics
    counts =  defaultdict(int)  # the dictionary of topics whose value is the count of appearances in the entire body of text
    for chunked in nltk.ne_chunk_sents(tagged, binary=False):
        continuous_chunk, current_chunk = [], []
        for i in chunked:
            if type(i) == nltk.Tree:
                token = " ".join([token for token, pos in i.leaves()]) # the key word to be used as the likely topic
                label = str(i).split(' ')[0][1:] # get the key that is the label of the named entity
                labels[label].add(token)
                counts[token] += 1
                current_chunk.append(token)
            elif current_chunk:
                current_chunk = []
            else:
                continue
    return labels, counts

def _get_non_NP_chunks(tagged):
    """
    This method is the only viable alternative to gathering stats on non-noun base words for topic making.
    Leverages the concept of grammar parsing (or using a commented out regex parser) to garner verb and adjective topics

    `tagged` - the pre-processed, sentence delimited, tokenized, tagged, body of text
    `return` labels, counts - the affiliated labels and count of appearances for likely topics
    """
    labels = defaultdict(set) # the dictionary of labels whose values are associated sets of topics
    counts =  defaultdict(int)  # the dictionary of topics whose value is the count of appearances in the entire body of text

    grammar = r"""
      NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
      PP: {<IN><NP>}               # Chunk prepositions followed by NP
      VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
      CLAUSE: {<NP><VP>}           # Chunk NP, PP, VP
      """
    cp = nltk.RegexpParser(grammar)

    """
    An alternative to pre-def grammar features chunking and chinking rules.
    This method failed to provide an increase in accuracy but will remain for posterity.

    >>> chunk_rule = ChunkRule("<.*>+", "Chunk everything")
    >>> chink_rule = ChinkRule("<VB\.>", "Chink on verbs/prepositions")
    >>> split_rule = SplitRule("<NN><VB>", "<DT><NN>",
    >>> "Split successive determiner/noun pairs")
    >>> chunk_parser = RegexpChunkParser([chunk_rule, chink_rule, split_rule], chunk_label = 'VB')
    """

    for sentence in tagged:
        """
        line used in tandem with the alt chunker seen above

        >>> chunked = chunk_parser.parse(sentence)
        """
        chunked = cp.parse(sentence)
        for i in chunked:
            if type(i) != nltk.Tree and (i[1].startswith('V') or i[1].startswith('J')):
                labels[i[1]].add(i[0])
                counts[i[0]] += 1
    return labels, counts

def _process_input(input):
    """
    used by main and debugger for testing purposes
    """

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

        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

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

def main():
    """demo usage in context"""

    body =_process_input(
        'http://www.foxnews.com/us/2017/02/10/marine-vet-speaks-out-about-viral-video-supporting-trump-travel-ban.html')

    # Use in practical development of NP parser (parser of choice)
    gen = _parse_topics(body)
    gen = sorted(gen, key=lambda x: x.strength)
    return gen

if __name__ == '__main__':
    print main()
    sys.exit(0)


"""
Used only for investigation of lemmatization.
Remnants kept in case it can be found useful.

def lemmatize_investigate():
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
"""