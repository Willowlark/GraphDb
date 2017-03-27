# -*- coding: utf-8 -*-

import nltk
import os
import validators
import unicodedata
import timeit
import operator
from functools import wraps
from collections import defaultdict
from colors import red, green, blue

def timer(function):

    @wraps(function)
    def func_timer(*args, **kwargs):
        t0 = timeit.default_timer()
        result = function(*args, **kwargs)
        t1 = timeit.default_timer()
        diff = t1 -t0
        phrase = " Total time running '%s': %s seconds " %(red(function.func_name), green(str(diff)))
        print '\n{:*^150}'.format(phrase)
        return result, diff
    return func_timer

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

class Topic_Candidate(object):
    """
    `Author`: Bill Clark
    A class created by the Parser to represent a Topic object in the graph, in relation
    to the given record. The metadata then, is strictly tied to the record used when
    creating the candidate.
    """

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.title)

    def __init__(self, topic, strength=None, label=None, after=None, before=None, suffix=None, prefix=None, depth=None):
        self.title = topic
        self.strength = strength
        self.label = label
        self.after = after
        self.before = before
        self.depth = depth
        self.suffix = suffix
        self.prefix = prefix

    def __eq__(self, other):
        return self.title == other.title

    def __ne__(self, other):
        return self.title != other.title

    def __hash__(self):
        return hash(self.title)

    def append_after(self, word):
        self.after.append(word)

# document = """Write a page that shows some data.
# I don't particularly care what it is, but there should be enough to be interesting.
# Choose at least 50 numbers.
# If you're only plotting one thing, such as US population over time, then get 50 years worth of data.
# If you're plotting returns of 10 stocks, do at least 5 days worth, or something like that.
# If you choose something that seems good but there aren't 50 numbers; maximum high jump at the Olympic Games would be stuck with only 29.
# Let me know and if I like it I'll okay it.
# Make a pretty graph of all your data. (Just one graph. Don't make 10 different pages to show 10 different stocks, draw them all on the same graph in 10 different colors.)
# If there's a lot of data make it respond to Mouseovers. (See the Sunrise/Sunset grapher for an example; it's at http://elvis.rowan.edu/~kilroy/sunrise/sunrise.html. That gives 3 numbers for each of 365 days, for 1095 values. Printing that many numbers on the canvas would make it unreadable, so they got moved to mouseovers.)
# Your data can be static files that you download, or information computed via some library, or fetched live from a website using an API, or any combination of those (or anything else reasonable). (The Sunrise/Sunset program uses the first two of these: a static file with all the states and zipcodes and their latitude/longitude, and a Perl package which computes sunrise/sunset given latitude/longitude.)
# You should put all the files for your project in the folder at this URL:
# http://elvis.rowan.edu/~Albus/awp/Canvas/
# where Albus is your Elvis username.
# ENJOY!"""

# document = """ASRC Federal Mission Solutions Rowan Collaboration Program – Fall, 2016
#
# Graph Database Evaluation and Reference Implementation
# Executive Summary
# A graph database is a database that uses graph structures for queries with nodes, relationships and properties to represent and store data.   Within graph databases, the relationship (and its subsequent properties), is just as important as the node itself.   This relationship allows data in each node to be directly coupled in a unique way, decreasing the time and complexity required to gather associated pieces of information that are related to the object in question.  The relationships contain their own metadata, which is used as part of the query process, providing another layer of filtering for the data queries and results.
# It is with these relationships that graph databases differ from conventional relational databases.  Relational databases store their relationship links in the data itself.  Queries searching for associated data need to traverse the data store and use the JOIN concept to collect the related data.  Depending on the size of the information and the number of associations one needs to manage, relational database implementations can lead to complex and time consuming queries.  Maintaining such a store as associations come and go can also be a tedious task within a relational database.  Graph databases, by design, allow simple and rapid retrieval of complex hierarchical structures that are difficult to model in relational systems.
# Background
# The increased power, capabilities and adoption rates of computers and communications systems are generating exponentially increasing amounts of data.  Within the C4 intelligence[a] pworld that data needs to analyzed for significant events, data or patterns to counter threats, stop the spread of disease and provide resource support to name a few.  In most cases information is collected and managed in stovepipes.  That information is then analyzed by experts within that stovepipe and decisions are made based on that data.  Unfortunately, by ponly using one stream of information, pieces of information may be missing from the overall decision process, especially if that missing information is from a totally different domain altogether.  For example, an analyst reviewing satellite data may be missing weather service and social media information that could better round out the decision process.  In many cases an analyst may have access to multiple feeds of information and will have to establish relationships between that information such as time and location to provide a more rounded out view of the item of interest.
# This leads us to why we want to explore Graph databases.  Imagine an analyst trying to manage information based on a multitude of people, places and things while also trying to establish and maintain information relationships to those objects at the same time within a relational database.[b]  The tables and queries would constantly be changing to accommodate new information (both existing and new formats) coming and going.  The timeliness [c]of retrieving the necessary information from such data store, that could be distributed, would
# become problematic over time.  Another issue would be completeness [d]of the data as knowing whether all the associations are accounted for would be difficult to determine.  Graph databases appear to solve these issues by decoupling the data from the relationship and in turn aligning properties with the relationships so the information and its metadata can be view and queried based on the objects of interest solely.
# Tasking
# As part of this effort we would like the team to focus on two areas:  An evaluation of prominent graph databases to determine a viable approach to meet the needs of the above scenarios and a reference implementation that demonstrates the strength of such a database in a domain with multiple disparate data feeds.[e]  A breakdown of the task is as follows:
# * Evaluate a few prominent  Graph DB implementations (Neo4j is a popular one) and identify/document pros/cons based on the following criteria:
#    * Performance - how the database under varying conditions
#    * Organization – how is the information retained, is this different between products
#    * Scaling – How do the products handle scaling up data content and complexity of queries
#    * Cost – What is the cost/licensing approach for each product.  Which are free…but do they have a license constraint.
#    *  Robustness of query language – How flexible is the language to perform simple to complex queries and is it easy to understand.
#    * Utilization – Who’s using it and on what products?
#    * Support – Is the product maintained, how often are updates produced?
#    * Product configurations - can the product support a web/cloud solution, standalone, networked, clusters?
#    * Services  - backup, clustering support, security, etc
#    * Visualization solutions – Can we easily visualize the data via a plugin or third party solution or do we have to implement our own solution? (e.g. Keyline looked like they had some solutions)
#    * Notification of changes – How does one get notified by changes to the data pfrom the database product.
#    * Batch updates – Does the product support a batch update model or is a single transaction at a time?
#    *  Data interoperability – What level of data conditioning needs to happen before it can be stored in the database?  For example, relational databases require the user to populate a defined schema layout; ORM is based on a predefined annotated class.  Is it name value pairs, etc?  How flexible is it to handling new data types/formats?
#    * Space utilization – Does the product use some kind of data compression?
#    * Transaction support – Does the product support this?
#    * “Time machine analysis” - The ability to look back in time at the data and potentially update it to see how actionable data has changed.
# * Pick one and define an approach to utilizing the database in both local and web/cloud based deployment environments.
# * Build reference implementations of a graph database supporting a C4 intelligence based problem.  Utilize disparate data points to build relationships that can be used to build actionable activity detection[f].  Possibly use data from resources such as data.gov as feeds.  Do we have any other data we can point them to?[g]
#    * Establish approaches for identifying/establishing relationships between the various disparate data feeds (e.g. time, location, name, etc).
#
#
# All developed artifacts are to be stored on Github.
# Goals
# * Evaluate a few Graph DB solutions and document in a white paper comparative details and how each DB performed against the above criteria.
# * A selected “best of breed” graph database to meet our C4 Intelligence needs (multiple disparate data feeds, some with significant volume).
# * A reference implementation of that database against a C4 Intelligence based scenario that showcases the value of graph databases within that community for the management of disparate data as well as the efficient deduction of action information, due to the relationships, of that data.
# * Recommendations for how to identify and build relationships from the data feeds.
#
#
# [a]Command Control Center and What?
# [b]What we will assume is an inevitable goal of someone in this work
# [c]point of interest 1
# [d]point of interest 2
# [e]Two strongest points of writings to be sought
# [f]good name, great objective
# [g]What does other data constitute? other software that can be used, or maybe other information on the work so far? What does the future hold?"""

document = body =_process_input(
        'http://www.foxnews.com/us/2017/02/10/marine-vet-speaks-out-about-viral-video-supporting-trump-travel-ban.html')


def preproc(document):
    sentences = nltk.sent_tokenize(document) #tokenize sentence into sentences
    tokenized = [nltk.word_tokenize(sent) for sent in sentences] # tokenize sentences in sentences
    tagged = [nltk.pos_tag(sent) for sent in tokenized] # tag the sentences in tokenized
    return tagged


def _new_get_continuous_chunks_NP(tagged):
    """
    This method return the dictionaries of critical words in the pre-processed text, tagged, that store info to be used by the graph database.
    The labels dictionary stores as a key the label to be given to the associated topic values. That is to say the key is the predisposed classification of the word when examined contextually by the nltk.ne_chunk(...)
    the counts dictionary stores as a key the title of the topic to be created and the value is the associated number of appearances throughout tagged.
    `tagged` - the pre-processed, sentence delimited, tokenized, tagged, body of text
    `return` labels, counts - the affiliated labels and count of appearances for likely topics
    """
    labels = defaultdict(set) # the dictionary of labels whose values are associated sets of topics
    counts =  defaultdict(int)  # the dictionary of topics whose value is the count of appearances in the entire body of text
    befores = defaultdict(list) # the dictionary of words that immediately precede the topic title
    afters = defaultdict(list) # the dictionary of words that immediately proceed the topic title
    depths = defaultdict(int)   # the dictionary of associated depths is number of words the topic title is within the body of text
    prefixes = defaultdict(str) # the dictionary of the one title that is the immediate suffix title of the key
    suffixes = defaultdict(str) # the dictionary of the  one title that is the immediate prefix title of the key
    commons = defaultdict(int) # the commonalities of unique tagged words throughout the document

    before_words = [] # list to reserve preceding words, recreated with each new topic
    suffix_title = None # the token that represents the title that came before the one being examined
    title = None # the current token being examined
    depth_index = 0 # the count of how many words deep the current title is
    for chunked in nltk.ne_chunk_sents(tagged, binary=False):
        current_chunk = []
        for i in chunked:
            depth_index = depth_index + 1
            if type(i) == nltk.Tree:
                title = " ".join([title for title, pos in i.leaves()]) # the key word to be used as the likely topic
                label = str(i).split(' ')[0][1:] # get the key that is the label of the named entity
                labels[label].add(title)
                counts[title] += 1
                if not title in depths.keys(): # NOTE depth maintains the first instance of the unique word encountered, subsequent encounters are not maintained by anything other than the count
                    depths[title] = depth_index
                current_chunk.append(title)
                befores[title].extend(before_words)
                if current_chunk:
                    current_chunk = []
                    before_words = []
                else:
                    pass
                before_words.extend(title.split(" "))
                if suffix_title is not None:
                    afters[suffix_title].extend(title.split(" "))
                    prefixes[title] = suffix_title
                else:
                    prefixes[title] = None
                suffixes[suffix_title] = title
                suffix_title = title
                commons[title] += 1
            else:
                before_words.append(i[0])
                if title is not None:
                    afters[title].append(i[0])
                commons[i[0]] += 1
        suffixes[title] = None # final title extracted has no suffix.

    return dict(labels), dict(counts), dict(befores), dict(afters), dict(suffixes), dict(prefixes), dict(depths), dict(commons)

@timer
def main2(n=None):
    listing = []
    tagged = preproc(document)
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
                topic = Topic_Candidate(title, depth=depth, prefix=prev_topic, before=before, after=[])
                before = []
                listing.append(topic)
                counts[title] += 1
                if prev_topic is not None:
                    prev_topic.suffix = topic
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
                topic.count = count

    for topic in sorted(listing, key = lambda k: k.depth): # sort by depth into the doc
        print green(repr(topic))
        for var in vars(topic):
            print '\t', var, ":", getattr(topic, var)
        print '\t', ' '.join(topic.before[-n:]), red(repr(topic)), ' '.join(topic.after[n:])

    # reconstruct the context of all topics from return listing alone
    first_topic = listing[0]
    topic = first_topic
    print blue(' '.join(topic.before)),
    while topic is not None:
        print red(str(topic)), blue(' '.join(topic.after)),
        topic = topic.suffix

@timer
def main(n = None):
    processed = preproc(document)
    listing = []
    labels, counts, befores, afters, suffixes, prefixes, depths, commons = _new_get_continuous_chunks_NP(processed)
    for label in labels.keys():
        for title in labels[label]:
            strength = counts[title]
            after = afters[title]
            before = befores[title]
            if n is not None:
                after = after[:n]
                before = before[-n:]
            suffix = suffixes[title]
            prefix = prefixes[title]
            depth = depths[title]   # NOTE depth maintains the first instance of the unique word encountered, subsequent encounters are not maintained by anything other than the count
            listing.append(Topic_Candidate(title, strength, label, after, before, suffix, prefix, depth))

    print
    for elem in sorted(set(listing), key = lambda k: k.depth): # sort by depth into the doc
        print green(repr(elem))
        for var in vars(elem):
            print '\t', var, ":", getattr(elem, var)
        print '\t', ' '.join(elem.before), red(repr(elem)), ' '.join(elem.after).strip()
        print

    # print words in context
    li = listing
    word = li[0]
    while word is not None:
        print blue(' '.join(word.before)), red(str(word)), blue(' '.join(word.after))
        next = word.suffix
        word = None
        for w in li:
            if next == w.title:
                word = w
                del w
                break

    print '\nOther common words', sorted(commons.items(), key=operator.itemgetter(1))[-20:]


if __name__ == '__main__':
    main2(10)