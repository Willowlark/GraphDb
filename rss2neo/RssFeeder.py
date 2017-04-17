import feedparser
import validators
import sys


class Feed:
    """
    `Author`: Eliakah kakou
    This class allows for more functionality in regards
    to the dictionary entered in the constructor
    """

    # constructor
    def __init__(self, feed):
        """
         constructor
        """
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
            # feeds = []

    def fetch(self):
        """
        Calling this method should retrieve information using the file provided
        at initialization. Following that, that information will be standardized
        into a Feed object and stored in the feeds instance variable. This is going
        to be implemented in very different ways, depending on the file type used. 
        """
        pass


class RssFeeder(Feeder):
    """ 
        `Author`: Eliakah kakou
        RssFeeder.py
        This class generates a list of feed instances containing relevant data about the file 
       """

    def __init__(self, file):
        """
        The constructor, initializes the RssFeeded instance 
        :param file: path to file containing list of links 
        """
        Feeder.__init__(self, file)
        self.feeds = []
        self.links = []
        self.path = file
        self.__getLinks(file)

    def load_feeds(self):
        """
            returns 'feeds' which contains all of the feed instances 
            :return: self.feeds
        """
        self.fetch()
        return self.feeds

    def __getLinks(self, file):
        """
        This method inserts each link from the file as an entry into the 'links' list 
        :param file:path to file containing list of links 
        """
        input_file = open(file)
        try:
            for i, line in enumerate(input_file):
                self.links.append(line)
                # print line,
        finally:
            input_file.close()

    def fetch(self):
        """
        This method appends all of the feed instances to 'feeds'
        :return: none
        """
        for i in range(len(self.links)):
            self.feeds.extend(self.__getFeeds(self.links[i]))

    def __getFeeds(self, url):
        """
                This method generates a Feed instance from the url given
               :param file: full file path
               :return: Feed generated from file
               """
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
