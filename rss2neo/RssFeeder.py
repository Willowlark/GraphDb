import feedparser
import validators
import sys

class Feed:
    # * Created by Eliakah kakou
    # Feed.py
    # This class allows for more functionality in regards
    # to the dictionary entered in the constructor

    # constructor
    def __init__(self, feed):
        self.feed = feed

    # This method returns a subset of the dictionary
    def extract(self):
        return {k: self.feed[k] for k in ('id', 'title', 'link', 'summary')}

    def record_content(self):
        return self.feed['link']

class Feeder:
    """
    `Author`: Bill Clark
    
    An interface to fulfill a strategy pattern design in the Grapher with feeders.
    An implementation of this interface will be usable with the Grapher so long as
    it provides the appropriate returns. 
    
    Feeder instances should be created with a link to some sort of file. The result
    to come out of it's methods will be used by the Parser Module to generate topics
    about the information in the Feed. A Feed represents a single article of related
    data. The implementation should generate Feed objects as defined above in order
    to be encapsulated. 
    """
    def __init__(self, file):
        """
        A feeder should be initialized to read from it's source when commanded to
        via the load_feeds method. Feeds is a list of Feed objects specifically, 
        and is interacted with in the feeds generator call. 
        
        `file`: The file to process later. 
        """
        self.feeds = []
        self.path = file

    def feeds(self):
        """
        Returns the feeds the Feeder is holding on to via a generator structure.  
        """
        for feed in self.feeds:
            yield feed
        #feeds = []

    def fetch(self):
        """
        Calling this method should retrieve information using the file provided
        at initialization. Following that, that information will be standardized
        into a Feed object and stored in the feeds instance variable. This is going
        to be implemented in very different ways, depending on the file type used. 
        """
        pass


class RssFeeder(Feeder):
    # * Created by Eliakah kakou
    # RssFeeder.py
    # This class gets an RSS feed and manipulates
    # the data based on the url entered

    # constructor
    def __init__(self, file):
        self.feeds = []
        self.links = []
        self.getLinks(file)
        for i in range(len(self.links)):
            self.feeds.extend(self.getFeeds(self.links[i]))

    def getLinks(self, file):
        input_file = open(file)
        try:
            for i, line in enumerate(input_file):
                self.links.append(line)
                #print line,
        finally:
            input_file.close()

        # loadFeeds
    def load_feeds(self):
        return self.feeds

    # change Url
    def getFeeds(self, url):
        feeds = []
        flag = validators.url(url)
        if flag:
            feeds = feedparser.parse(url)
        else:
            sys.exit("Invalid Url: Please try again!")

        list = feeds['entries']
        for i in range(len(list)):
            list[i] = Feed(list[i])
            feeds = list

        return feeds

if __name__ == "__main__":
    feeder = Feeder('links.txt')
    feeds = feeder.load_feeds()

    for i in range(len(feeds)):
            print  feeds[i].extract()