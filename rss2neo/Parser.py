"""
This file stores the static methods to interpret topic candidates from zero or more bodies of text.
The work that accomplishes this is in the methods parse_topics and parse_topics_not_nouns.
get_unstructured_topic returns the list of un-structured topics from the given body of text.
This uses the ne_chunker of the nltk_data package, to filter nouns of importance based on contextual observations.
get_structured_topic returns the structured topic instances form the body of the text in the rss feed summary.
is_structured returns a true if input data is structured, else false.
the subsequent methods are all used in the context of just this file and its aforementioned outward interface. They have each been tailored to usage in this predefined environment.
"""

from __future__ import division

import os
import sys
import inflect
import unicodedata
import nltk
import json
import pattern
from functools import wraps
from collections import defaultdict
from _markup_parser import markup_parser

"""
Set the 'infl' var to use a pre-built switch for singularization
Used to tell if a given noun is singular or not, then pattern.re is used to singularize it
"""
infl = inflect.engine()

class Topic_Candidate(object):
    """
    `Author`: Bill Clark
    A class created by the Parser to represent a Topic object in the graph, in relation
    to the given record. The metadata then, is strictly tied to the record used when
    creating the candidate. The candidate data does not all go onto the Topic object, the candidate carries
    properties that will be later copied to the relationship between this topic and the record. 
    """

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.title)

    def __init__(self, title, strength=0, label=None, after='', before='', suffix='', prefix='', depth=0):
        self.title = self.normalize_noun(title) if infl else title
        self.strength = strength
        self.label = label
        self.after = after
        self.before = ' '.join(before)
        self.depth = depth
        self.suffix = suffix.title if suffix is not '' else ''
        self.prefix = prefix.title if suffix is not '' else ''

    def keywordify(self):
        """
        `Author`: Bill Clark
        
        Returns a dictonary of the properties of the candidate. Used for compatibility in other methods.
        
        `return`: Dictonary of this candidate's properties. 
        """
        return self.__dict__

    def update_properties(self, node):
        """
        `Author`: Bill Clark
        
        Here we take a Topic node object and apply the properties in the candidate to it. We either update the 
        value or add it to the Topic node. This allows for running totals like strength as well as adding the 
        properties in the candidate that will be copied to the relationship later. 
        
        `node`: A topic node object
         
        `return`: The modified node. 
        """
        for key in self.__dict__:
            if self.__dict__[key] == self.title:
                pass
            elif node[key] is not None and type(node[key]) is not str:
                node[key] += self.__dict__[key]
            else: node[key] = self.__dict__[key]
        return node

    def normalize_noun(self, title):
        if infl.singular_noun(title) is False:
            return title
        else:
            import pattern.en
            return pattern.en.singularize(title)

    def __eq__(self, other):
        return self.title == other.title

    def __ne__(self, other):
        return self.title != other.title

    def __hash__(self):
        return hash(self.title)

    def append_after(self, word):
        self.after = self.after + ' ' + word

def get_structured_topic(extracted):
    """
    `Author` Bob S.

    used by external modules to gather the structured topics of the summary of the feed json
    make_set is used to specify whether a set of unique topic candidate instances is formed from the result of the call to _strucutred_topic

    `extracted` the json object of the feed being examined

    `return` the result of the structured topic investigation.
    """
    body_of_text = extracted['summary']
    return _structured_topic(body_of_text)

def get_unstructured_topic(extracted, keys=('id', 'title', 'summary'), make_set=True):
    """
     `Author` Bob S.

    used by external modules to gather the unstructured topics of the summary of the feed json

    `extracted` the json object of the feed being examined

    `keys` the optional list of args that are the keys of the associative dictionary extracted to have topics extracted

    `make_set` optional argument for creating set of unique instances on return

    `debug` optional argument for printing state of topic candidates before return

    `return` the set of the unique topic candidate instances to be inserted by RssGrapher
    """
    ret = []
    for key in keys:
            ret.extend(_parse_topics(extracted[key]))
    return set(ret)


def _structured_topic(body_of_text, try_markup=False):
    """
    `Author` Bob S.

    This method will render the list of structured topics form the predisposed format of data, a JSON string.

    `body_of_text` the string to be parsed from the rss feed

    `try_markup` the optional argument to attempt to markup the body of text as json for manipulation

    `return` ret, the list of structured topics from the body of text
    """
    if try_markup and not is_structured(body_of_text):
        mkup = markup_parser()
        return mkup.to_json(body_of_text)
    return json.loads(body_of_text)

def _parse_topics(body_of_text):
    """
    `Author` Bob S.

    Used for parsing topic candidates, form conjunctive crucial words, that are of the Noun persuasion.
    The instances of topic candidate that are returned will be used in the database as units for relation creation

    `body_of_text` - the raw body of text to be processed

    `debug` optional argument for printing state of topic candidates before return

    `return` topic candidates - the generated collection of Noun based topics that have been extracted and constructed
    """
    if isinstance(body_of_text, unicode):
        body_of_text = unicodedata.normalize('NFKD', body_of_text).encode('ascii', 'ignore')
    processed = _info_extract_preprocess(body_of_text)   # preprocessed body for tagged words in sentence form
    return _get_NP_topics(processed)

def _parse_topics_not_nouns(body_of_text):
    """
    `Author` Bob S.

    Method used for parsing topics that are not conjunctive noun words.
    Second to the NP form that is preferred use. Does not produce effective NNPs.
    However, only means to yield the non-nouns words of interest

    `kargs` - the params (in the form zero or more) raw bodies of text to be processed

    `yield` topic candidates - the generated collection of non-Noun topics that have been extracted and constructed
    """
    if isinstance(body_of_text, unicode):
        body_of_text = unicodedata.normalize('NFKD', body_of_text).encode('ascii', 'ignore')
    processed = _info_extract_preprocess(body_of_text)   # preprocessed body for tagged words in sentence form
    return _get_non_NP_topics(processed)

def is_structured(data):
    """
    `Author` Bob S.

    This method determines if the given python string, data, is structured data or not.
    Structured data is information in the format the development team has agreed on using as the format to be used when we not examining raw, unfiltered text.
    This format is JSON.

    `data` the literal string that is passed to be checked

    `return` True if the string can be leaded in JSON format, else False
    """
    try:
        json.loads(data)
    except:
        return False
    return True

def _info_extract_preprocess(document):
    """
    `Author` Bob S.

    This method is used to perform the reiterative process of preparing the given body of text to be parsed.
    First the sentences are tokenized using the default method of sent_tokenize(), next, the words are tokenized one by one.
    Finally those words are tagged by the default tagger of pos_tagger()

    `document` the string form body of text to be pre-processed

    `return` tagged - the tokenized, then tagged body of sentence delimited text.
    """
    sentences = nltk.sent_tokenize(document) #tokenize sentence into sentences
    tokenized = [nltk.word_tokenize(sent) for sent in sentences] # tokenize each sentences in sentences into tokenized
    tagged = [nltk.pos_tag(sent) for sent in tokenized] # tag the sentences in tokenized
    return tagged

def _get_NP_topics(tagged):
    """
    `Author` Bob S.

    this method creates and returns a list of topic candidate instances form the specified pre-processes body of text
    Each subdivided unit in the tagged param is processed only once, bounding the first half of this method to O(n).
    Then for each unique word form the tagged text, its number of appearances is counted and all associated topics have their count incremented to reflect this measure.
    Finally the list is returned in one state to be returned to the get_topics method

    `tagged` the pre-processed body of text returned form the ie_preprocess() method

    `debug` optional argument for printing state of topic candidates before return
    """
    listing = []
    counts = defaultdict(int)
    depth = 0
    topic = None
    prev_topic = None
    before = []
    for chunked in nltk.ne_chunk_sents(tagged, binary=False):
        for word_tag in chunked:
            depth += 1
            if type(word_tag) == nltk.Tree:
                title = " ".join([title for title, pos in word_tag.leaves()]) # the key word to be used as the likely topic
                topic = Topic_Candidate(title, depth=depth, prefix=prev_topic, before=before)
                before = []
                listing.append(topic)
                counts[title] += 1
                if prev_topic is not None:
                    prev_topic.suffix = topic.title
                prev_topic = topic
            else:
                word, pos = word_tag
                counts[word] += 1
                before.append(word)
                if topic is not None:
                    topic.append_after(word)

    # Build Counts Values for titles (and words) to be applied to fields of topic
    for title, count in counts.iteritems():
        for topic in listing:
            if title == topic.title:
                topic.strength = count

    return listing

def _get_non_NP_topics(tagged):
    """
    `Author` Bob S.

    This method is the only viable alternative to gathering stats on non-noun base words for topic making.
    Leverages the concept of grammar parsing (or using a commented out regex parser) to garner verb and adjective topics

    `tagged` - the pre-processed, sentence delimited, tokenized, tagged, body of text

    `return` labels, counts - the affiliated labels and count of appearances for likely topics
    """
    labels = defaultdict(set) # the dictionary of labels whose values are associated sets of topics
    counts =  defaultdict(int)  # the dictionary of topics whose value is the count of appearances in the entire body of text
    ret = []

    grammar = r"""
      NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
      PP: {<IN><NP>}               # Chunk prepositions followed by NP
      VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
      CLAUSE: {<NP><VP>}           # Chunk NP, PP, VP
      """
    cp = nltk.RegexpParser(grammar)

    """
    An alternative to pre-def grammar features chunking and chinking rules.
    This method failed to provide an increase in accuracy but has remained for posterity.
    >>> chunk_rule = ChunkRule("<.*>+", "Chunk everything")
    >>> chink_rule = ChinkRule("<VB\.>", "Chink on verbs/prepositions")
    >>> split_rule = SplitRule("<NN><VB>", "<DT><NN>",
    >>> "Split successive determiner/noun pairs")
    >>> chunk_parser = RegexpChunkParser([chunk_rule, chink_rule, split_rule], chunk_label = 'VB')
    """

    for sentence in tagged:
        """
        this line used in tandem with the alt chunker (chunk_parser) seen above

        >>> chunked = chunk_parser.parse(sentence)
        """
        chunked = cp.parse(sentence)
        for i in chunked:
            if type(i) != nltk.Tree and (i[1].startswith('V') or i[1].startswith('J')):
                labels[i[1]].add(i[0])
                counts[i[0]] += 1

    for label in labels.keys():
            for title in labels[label]:
                strength = counts[title]
                ret.append(Topic_Candidate(title=title, strength=strength, label=label))
    return ret

"""Code to assign working path of nltk_data resource to local copy, if one exists else tell user to download"""
try:
    # nltk.data.find(os.path.join('tokenizers', 'punkt.zip'))
    pass
except LookupError as e:
    print "\tPlease choose the location of the nltk_data resource (see file dialogue)"
    from  Tkinter import Tk
    import Tkinter, Tkconstants, tkFileDialog
    root = Tk()
    directory = tkFileDialog.askdirectory()
    nltk.data.path.append(directory)
