# * Created by Eliakah kakou
# Feeder.py
# This class gets an RSS feed and manipulates
# the data based on the url entered


from Feed import Feed
import feedparser
import validators
import sys


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
                print line,
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



