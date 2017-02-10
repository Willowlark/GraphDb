from time import sleep
import Feeder
import Parser
import Recorder
from py2neo import Graph
import sys

def _is_structured(data):
    pass

def execute(graphAddress):

    recorder = Recorder().initialize(graphAddress)

    while True:
        sleep(60)

        feeds = Feeder.load_feeds(file)
        for feed in feeds:
            extracted = Feeder.extract(feed)

            if _is_structured(extracted):
                topic, record_value = Parser.structured_topic(extracted)
            else:
                topic, record_value = Parser.parse_topics(extracted)

            if recorder.hasNode(topic):
                tnode = recorder.add_topic(topic) #this method is where location fixes would go.
            else:
                tnode = recorder.fetch_topic(topic)

            rnode = recorder.add_record(record_value)

            recorder.relate_then_push(tnode, rnode)

if __name__ == "__main__":
    execute(sys.argv[1])

"""
Data types:
feeds = list of feed objects
feed = singular rss feed
topic = list of 1 or more topic nodes.
record_value = the data in the record node (the url to the feed entry)
tnode = py2neo subgraph object for the topic node(s).
rnode = py2neo node object for record_value
"""