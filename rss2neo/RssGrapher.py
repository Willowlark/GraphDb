import sys
from time import sleep

import Feeder
import Parser
from Recorder import Recorder


def execute(graphAddress, path):

    recorder = Recorder()
    recorder.initialize(graphAddress)
    feeder = Feeder.Feeder(path)

    while True:

        feeds = feeder.load_feeds()
        for feed in feeds:
            extracted = feed.extract()

            if Parser.is_structured(extracted):
                topics, record_value = Parser.get_structured_topic(extracted)
            else:
                topics, record_value = Parser.get_unstructured_topic(extracted)

            topics_graph = recorder.get_or_add_topics(topics)

            rnode = recorder.add_record(record_value) #confirm doesn't exist

            recorder.relate_then_push(topics_graph, rnode)

        print 'Sleeping for 60s'
        sleep(60)


if __name__ == "__main__":
    execute(sys.argv[1], 'links.txt')
    # more metadata
    # runtime with large feeds