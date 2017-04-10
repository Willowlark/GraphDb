import feedparser
import validators
import sys

# * Created by Eliakah kakou
# Feed.py
# This class allows for more functionality in regards
# to the dictionary entered in the constructor


class Feed:
    # constructor
    def __init__(self, feed):
        self.feed = feed

    # This method returns a subset of the dictionary
    def extract(self):
        return {k: self.feed[k] for k in ('id', 'title', 'link', 'summary')}

    def record_content(self):
        return self.feed['link']

# * Created by Eliakah kakou
# RssFeeder.py
# This class gets an RSS feed and manipulates
# the data based on the url entered


class Feeder:

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