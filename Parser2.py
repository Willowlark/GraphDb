# -*- coding: utf-8 -*-

import nltk
from collections import defaultdict
from pprint import pprint
import timeit

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

    def __init__(self, topic, strength, label, after, before):
        self.title = topic
        self.strength = strength
        self.label = label
        self.after = after
        self.before = before


document = """ASRC Federal Mission Solutions Rowan Collaboration Program – Fall, 2016


Graph Database Evaluation and Reference Implementation
Executive Summary
A graph database is a database that uses graph structures for queries with nodes, relationships and properties to represent and store data.   Within graph databases, the relationship (and its subsequent properties), is just as important as the node itself.   This relationship allows data in each node to be directly coupled in a unique way, decreasing the time and complexity required to gather associated pieces of information that are related to the object in question.  The relationships contain their own metadata, which is used as part of the query process, providing another layer of filtering for the data queries and results.
It is with these relationships that graph databases differ from conventional relational databases.  Relational databases store their relationship links in the data itself.  Queries searching for associated data need to traverse the data store and use the JOIN concept to collect the related data.  Depending on the size of the information and the number of associations one needs to manage, relational database implementations can lead to complex and time consuming queries.  Maintaining such a store as associations come and go can also be a tedious task within a relational database.  Graph databases, by design, allow simple and rapid retrieval of complex hierarchical structures that are difficult to model in relational systems.
Background
The increased power, capabilities and adoption rates of computers and communications systems are generating exponentially increasing amounts of data.  Within the C4 intelligence[a] pworld that data needs to analyzed for significant events, data or patterns to counter threats, stop the spread of disease and provide resource support to name a few.  In most cases information is collected and managed in stovepipes.  That information is then analyzed by experts within that stovepipe and decisions are made based on that data.  Unfortunately, by ponly using one stream of information, pieces of information may be missing from the overall decision process, especially if that missing information is from a totally different domain altogether.  For example, an analyst reviewing satellite data may be missing weather service and social media information that could better round out the decision process.  In many cases an analyst may have access to multiple feeds of information and will have to establish relationships between that information such as time and location to provide a more rounded out view of the item of interest.
This leads us to why we want to explore Graph databases.  Imagine an analyst trying to manage information based on a multitude of people, places and things while also trying to establish and maintain information relationships to those objects at the same time within a relational database.[b]  The tables and queries would constantly be changing to accommodate new information (both existing and new formats) coming and going.  The timeliness [c]of retrieving the necessary information from such data store, that could be distributed, would
become problematic over time.  Another issue would be completeness [d]of the data as knowing whether all the associations are accounted for would be difficult to determine.  Graph databases appear to solve these issues by decoupling the data from the relationship and in turn aligning properties with the relationships so the information and its metadata can be view and queried based on the objects of interest solely.
Tasking
As part of this effort we would like the team to focus on two areas:  An evaluation of prominent graph databases to determine a viable approach to meet the needs of the above scenarios and a reference implementation that demonstrates the strength of such a database in a domain with multiple disparate data feeds.[e]  A breakdown of the task is as follows:
* Evaluate a few prominent  Graph DB implementations (Neo4j is a popular one) and identify/document pros/cons based on the following criteria:
   * Performance - how the database under varying conditions
   * Organization – how is the information retained, is this different between products
   * Scaling – How do the products handle scaling up data content and complexity of queries
   * Cost – What is the cost/licensing approach for each product.  Which are free…but do they have a license constraint.
   *  Robustness of query language – How flexible is the language to perform simple to complex queries and is it easy to understand.
   * Utilization – Who’s using it and on what products?
   * Support – Is the product maintained, how often are updates produced?
   * Product configurations - can the product support a web/cloud solution, standalone, networked, clusters?
   * Services  - backup, clustering support, security, etc
   * Visualization solutions – Can we easily visualize the data via a plugin or third party solution or do we have to implement our own solution? (e.g. Keyline looked like they had some solutions)
   * Notification of changes – How does one get notified by changes to the data pfrom the database product.
   * Batch updates – Does the product support a batch update model or is a single transaction at a time?
   *  Data interoperability – What level of data conditioning needs to happen before it can be stored in the database?  For example, relational databases require the user to populate a defined schema layout; ORM is based on a predefined annotated class.  Is it name value pairs, etc?  How flexible is it to handling new data types/formats?
   * Space utilization – Does the product use some kind of data compression?
   * Transaction support – Does the product support this?
   * “Time machine analysis” - The ability to look back in time at the data and potentially update it to see how actionable data has changed.
* Pick one and define an approach to utilizing the database in both local and web/cloud based deployment environments.
* Build reference implementations of a graph database supporting a C4 intelligence based problem.  Utilize disparate data points to build relationships that can be used to build actionable activity detection[f].  Possibly use data from resources such as data.gov as feeds.  Do we have any other data we can point them to?[g]
   * Establish approaches for identifying/establishing relationships between the various disparate data feeds (e.g. time, location, name, etc).


All developed artifacts are to be stored on Github.
Goals
* Evaluate a few Graph DB solutions and document in a white paper comparative details and how each DB performed against the above criteria.
* A selected “best of breed” graph database to meet our C4 Intelligence needs (multiple disparate data feeds, some with significant volume).
* A reference implementation of that database against a C4 Intelligence based scenario that showcases the value of graph databases within that community for the management of disparate data as well as the efficient deduction of action information, due to the relationships, of that data.
* Recommendations for how to identify and build relationships from the data feeds.


[a]Command Control Center and What?
[b]What we will assume is an inevitable goal of someone in this work
[c]point of interest 1
[d]point of interest 2
[e]Two strongest points of writings to be sought
[f]good name, great objective
[g]What does other data constitute? other software that can be used, or maybe other information on the work so far? What does the future hold?"""

def getNodes2(parent, nnp={}, key=None):
    ROOT = 'ROOT'
    new_key = None
    for node in parent:
        if type(node) is nltk.Tree:
            nnp[node.leaves()[0]] = []
            new_key = node.leaves()[0]
            getNodes(node, nnp, new_key)
        else:
            try:
                nnp[key].append(node)
            except Exception:
                pass

def preproc(document):
    sentences = nltk.sent_tokenize(document) #tokenize sentence into sentences
    tokenized = [nltk.word_tokenize(sent) for sent in sentences] # tokenize sentences in sentences
    tagged = [nltk.pos_tag(sent) for sent in tokenized] # tag the sentences in tokenized
    return tagged

# grammar = r"""
#     NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
#       {<NNP>+}                # chunk sequences of proper nouns
#     """
#
# cp = nltk.RegexpParser(grammar)
# for sentence in preproc(document):
#     result = cp.parse(sentence)
#     print '-' * 100
#
#     nnp = {}
#     getNodes(result, nnp)
#     pprint(nnp)
#     print
#     for key in nnp.keys():
#         lis = nnp[key]
#         if lis.index(key)-1 < 0:
#             pass
#         else:
#             print '\t', lis[lis.index(key)-1]
#         print lis[lis.index(key)]
#         try:
#             print '\t', lis[lis.index(key)+1]
#         except IndexError:
#             pass
#         print

def getNodes(parent):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'ROOT':
                print "======== Sentence ========="
                print "Sentence:", " ".join(node.leaves())
            else:
                print "Label:", node.label()
                print "Leaves:", node.leaves()

            getNodes(node)
        else:
            print "Word:", node

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
    before, after = defaultdict(list), defaultdict(list)
    for chunked in nltk.ne_chunk_sents(tagged, binary=False):
        a, b = [], []
        current_chunk = []
        for i in chunked:
            if type(i) == nltk.Tree:
                token = " ".join([token for token, pos in i.leaves()]) # the key word to be used as the likely topic
                label = str(i).split(' ')[0][1:] # get the key that is the label of the named entity
                labels[label].add(token)
                counts[token] += 1
                current_chunk.append(token)
                before[token].extend(b)
            elif current_chunk:
                current_chunk = []
            else:
                pass
            b.append("".join([token for token, _ in i.leaves()]) if type(i) == nltk.tree else i[0])
            after[token].append("".join([token for token, _ in i.leaves()]) if type(i) == nltk.tree else i[0])

    return dict(labels), dict(counts), dict(before), dict(after)

def main():
    processed = preproc(document)
    listing = []
    labels, counts, before, after = _get_continuous_chunks_NP(processed)
    print 'before'
    pprint(before)
    print
    print 'after'
    pprint(after)
    for k in after.keys():
        print k,
    print
    for k in before.keys():
        print k,
    print
    for label in labels.keys():
        for title in labels[label]:
            strength = counts[title]
            try:
                afts = after[title][:5]
            except Exception:
                pass
            befs = before[title][-5:]
            listing.append(Topic_Candidate(title, strength, label, afts, befs))
    for elem in set(listing):
        print elem
        print '\t', vars(elem)
if __name__ == '__main__':
    main()