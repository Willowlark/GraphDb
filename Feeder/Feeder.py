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
    def __init__(self, url):
        self.errMsg = "Invalid Url: Please try again!"
        self.url = url
        self.setUrl(self.url)

    # loadFeeds
    def load_feeds(self):
        return self.feeds

    # change Url
    def setUrl(self, newUrl):
        self.url = newUrl
        flag = validators.url(self.url)
        if flag:
            self.feeds = feedparser.parse(self.url)
        else:
            sys.exit(self.errMsg)

        list = self.feeds['entries']
        for i in range(len(list)):
            list[i] = Feed(list[i])
            self.feeds = list
