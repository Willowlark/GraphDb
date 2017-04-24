"""This class contains the execution loop utilizing the Feeder, Parser and Recorder
classes to interact with a neo4j DB. Each sub module provides different functionality
and Grapher utilizes each of them to complete the task at hand."""

import sys
from time import sleep

import Parser
from Recorder import Recorder
import Feeder


def post_60(graphAddress, path):
    """
    `Author`: Bill Clark
    
    This method contains the object initializations and the control loop of
    a Grapher utility. It will declare a Recorder and Feeder using the parameters
    it is provided and setup a Parser. The loop will then scan every feed the Feeder
    provides. If the feed is NOT in the database, we parse it's topics and add/extract
    them to/from the DB. We then add that feed as a new record in the graph, linked
    to the topics we derived. If the feed already exists as a record, it's timestamp
    is checked. If there's no updated to the timestamp, the feed is skipped.
    This loop executes for all feeds provided, then sleeps 60 seconds before restarting.
    It is intended to run infinitely. 
    
    Executing the module rather than importing it will take the parameters from the
    command line and run this method. 
    
    `graphAddress`: The url of the graphDB the Grapher will work on.
    
    `path`: The path to the file to be used by the feeder. 
    """

    recorder = Recorder()
    recorder.initialize(graphAddress)
    feeder = Feeder.RssFeeder(path)
    while True:

        feeder.fetch()
        for feed in feeder.contents():
            extracted = feed.extract()
            record_value = feed.record_content()

            rnode = recorder.add_record(record_value)
            if not rnode:  # The node wasn't created because it already exists, move on.
                continue

            if Parser.is_structured(extracted):
                topics = Parser.get_structured_topic(extracted)
            else:
                topics = Parser.get_unstructured_topic(extracted)

            topics_graph = recorder.get_or_add_topics(topics)

            recorder.relate_then_push(topics_graph, rnode)

        print 'Finished; Sleeping for 60s'
        sleep(60)

if __name__ == "__main__":
    post_60(sys.argv[1], sys.argv[2])