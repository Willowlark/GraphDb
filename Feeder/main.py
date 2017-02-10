# * Created by Eliakah kakou
# Main.py
# This class allows you call and test all classes

from RssFeedParser import RssFeedParser
def main():
    parser = RssFeedParser('http://popculturebrain.com/rss')
    parser.getFields()
    feeds = parser.getFeeds()
    print len( feeds['entries'])
    print [field for field in parser.getSummaries()[0]]
    print parser.getSummaries()[0]['summary']
    print parser.getSummaries()[0]['link']

main()