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

        print 'Sleeping for 60s'
        sleep(60)

def _timer(method, args):
    import time

    start = time.time()
    method(*args)
    print 'Time for single loop:', time.time() - start


if __name__ == "__main__":
    execute(sys.argv[1], 'links.txt')
    #_timer(execute, [sys.argv[1], 'links.txt'])