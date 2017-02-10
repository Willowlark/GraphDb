# * Created by Eliakah kakou
# RssFeedParser.py
# This class allows you to parse a rss feed and access all of its fields

import feedparser

class RssFeedParser:

    #constructor
    def __init__(self, url):
        self.url = url
        self.setUrl(self.url)
        self.errMsg = "Invalid Url: Please reset it!"


    #change Url
    def setUrl(self, newUrl):
        self.url = newUrl
        try:
            self.feeds = feedparser.parse(self.url)
        except :
            print self.errMsg

    def getFields(self):
        try:
            print [field for field in self.feeds]
        except :
            print self.errMsg


    def getFeeds(self):
        if not self.url:
            print self.errMsg
        else:
            return self.feeds

    def getSummaries(self):
        size = len(self.feeds['entries'])
        list = []
        if size > 0:
            list = self.feeds['entries']
            return list
        else:
            print "There are no entries => no Summaries"



